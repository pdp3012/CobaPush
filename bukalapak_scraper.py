#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bukalapak Scraper - Advanced Data Mining Tool
Dibuat oleh: Dosen Data Mining dengan 30 tahun pengalaman
Sertifikasi: International Data Mining Certification

Fitur:
- Scraping via API Bukalapak
- Scraping via CSS Selector (Selenium)
- Ekstraksi: nama produk, harga, jumlah terjual, nama toko, lokasi toko, rating
- Anti-deteksi dengan rotating user agents
- Error handling yang robust
- Data validation dan cleaning
"""

import requests
import json
import time
import re
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from fake_useragent import UserAgent
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import urljoin, urlparse
import logging
from datetime import datetime
import random

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bukalapak_scraper.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class BukalapakScraper:
    """
    Advanced Bukalapak Scraper dengan multiple approach
    """
    
    def __init__(self, headless=True, delay_range=(1, 3)):
        """
        Inisialisasi scraper
        
        Args:
            headless (bool): Mode headless untuk browser
            delay_range (tuple): Range delay antara request (min, max)
        """
        self.base_url = "https://www.bukalapak.com"
        self.api_base = "https://api.bukalapak.com"
        self.session = requests.Session()
        self.ua = UserAgent()
        self.delay_range = delay_range
        self.headless = headless
        self.driver = None
        
        # Setup session headers
        self._setup_session()
        
        # Data storage
        self.products_data = []
        
    def _setup_session(self):
        """Setup session dengan headers yang realistic"""
        headers = {
            'User-Agent': self.ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Cache-Control': 'max-age=0'
        }
        self.session.headers.update(headers)
        
    def _random_delay(self):
        """Delay random untuk menghindari deteksi"""
        delay = random.uniform(*self.delay_range)
        time.sleep(delay)
        
    def _setup_driver(self):
        """Setup Selenium WebDriver"""
        chrome_options = Options()
        
        if self.headless:
            chrome_options.add_argument("--headless")
            
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument(f"--user-agent={self.ua.random}")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        try:
            self.driver = webdriver.Chrome(
                service=webdriver.chrome.service.Service(ChromeDriverManager().install()),
                options=chrome_options
            )
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            logger.info("Selenium WebDriver berhasil diinisialisasi")
        except Exception as e:
            logger.error(f"Error setup WebDriver: {e}")
            raise
            
    def scrape_via_api(self, category="", search_query="", max_pages=5):
        """
        Scraping via Bukalapak API
        
        Args:
            category (str): Kategori produk
            search_query (str): Query pencarian
            max_pages (int): Maksimal halaman yang di-scrape
        """
        logger.info(f"Memulai scraping via API - Category: {category}, Query: {search_query}")
        
        try:
            for page in range(1, max_pages + 1):
                logger.info(f"Scraping halaman {page}")
                
                # Construct API URL
                if search_query:
                    api_url = f"{self.api_base}/products"
                    params = {
                        'keywords': search_query,
                        'page': page,
                        'limit': 50
                    }
                else:
                    api_url = f"{self.api_base}/categories/{category}/products"
                    params = {
                        'page': page,
                        'limit': 50
                    }
                
                # Make API request
                response = self.session.get(api_url, params=params)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    if 'data' in data and data['data']:
                        for product in data['data']:
                            product_info = self._extract_product_info_api(product)
                            if product_info:
                                self.products_data.append(product_info)
                    else:
                        logger.info(f"Tidak ada data di halaman {page}")
                        break
                else:
                    logger.warning(f"API request gagal dengan status code: {response.status_code}")
                    break
                    
                self._random_delay()
                
        except Exception as e:
            logger.error(f"Error dalam scraping API: {e}")
            
        logger.info(f"Scraping API selesai. Total produk: {len(self.products_data)}")
        
    def _extract_product_info_api(self, product_data):
        """
        Ekstrak informasi produk dari API response
        
        Args:
            product_data (dict): Data produk dari API
            
        Returns:
            dict: Informasi produk yang sudah dibersihkan
        """
        try:
            product_info = {
                'nama_produk': product_data.get('name', ''),
                'harga': self._extract_price_api(product_data),
                'jumlah_terjual': self._extract_sold_count_api(product_data),
                'nama_toko': product_data.get('store', {}).get('name', ''),
                'lokasi_toko': product_data.get('store', {}).get('location', ''),
                'rating_produk': self._extract_rating_api(product_data),
                'url_produk': product_data.get('url', ''),
                'kategori': product_data.get('category', {}).get('name', ''),
                'gambar_produk': product_data.get('images', [{}])[0].get('url', '') if product_data.get('images') else '',
                'metode_scraping': 'API',
                'timestamp_scraping': datetime.now().isoformat()
            }
            
            # Data validation
            if product_info['nama_produk'] and product_info['harga']:
                return product_info
            return None
            
        except Exception as e:
            logger.error(f"Error ekstraksi data API: {e}")
            return None
            
    def _extract_price_api(self, product_data):
        """Ekstrak harga dari API data"""
        try:
            price = product_data.get('price', 0)
            if isinstance(price, (int, float)):
                return price
            return 0
        except:
            return 0
            
    def _extract_sold_count_api(self, product_data):
        """Ekstrak jumlah terjual dari API data"""
        try:
            sold_count = product_data.get('sold_count', 0)
            if isinstance(sold_count, (int, float)):
                return sold_count
            return 0
        except:
            return 0
            
    def _extract_rating_api(self, product_data):
        """Ekstrak rating dari API data"""
        try:
            rating = product_data.get('rating', {}).get('average', 0)
            if isinstance(rating, (int, float)):
                return rating
            return 0
        except:
            return 0
    
    def scrape_via_css_selector(self, search_query="", max_pages=5):
        """
        Scraping via CSS Selector menggunakan Selenium
        
        Args:
            search_query (str): Query pencarian
            max_pages (int): Maksimal halaman yang di-scrape
        """
        logger.info(f"Memulai scraping via CSS Selector - Query: {search_query}")
        
        if not self.driver:
            self._setup_driver()
            
        try:
            for page in range(1, max_pages + 1):
                logger.info(f"Scraping halaman {page} via CSS Selector")
                
                # Construct search URL
                if page == 1:
                    search_url = f"{self.base_url}/search?search%5Bkeywords%5D={search_query}"
                else:
                    search_url = f"{self.base_url}/search?search%5Bkeywords%5D={search_query}&page={page}"
                
                # Navigate to page
                self.driver.get(search_url)
                
                # Wait for page to load
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='product-card']"))
                )
                
                # Scroll to load all products
                self._scroll_page()
                
                # Extract products
                products = self.driver.find_elements(By.CSS_SELECTOR, "[data-testid='product-card']")
                
                if not products:
                    logger.info(f"Tidak ada produk ditemukan di halaman {page}")
                    break
                    
                for product in products:
                    try:
                        product_info = self._extract_product_info_css(product)
                        if product_info:
                            self.products_data.append(product_info)
                    except Exception as e:
                        logger.error(f"Error ekstraksi produk CSS: {e}")
                        continue
                        
                self._random_delay()
                
        except Exception as e:
            logger.error(f"Error dalam scraping CSS: {e}")
        finally:
            if self.driver:
                self.driver.quit()
                
        logger.info(f"Scraping CSS Selector selesai. Total produk: {len(self.products_data)}")
        
    def _scroll_page(self):
        """Scroll halaman untuk memuat semua konten"""
        try:
            last_height = self.driver.execute_script("return document.body.scrollHeight")
            
            while True:
                # Scroll down
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                
                # Wait for new content
                time.sleep(2)
                
                # Calculate new scroll height
                new_height = self.driver.execute_script("return document.body.scrollHeight")
                
                if new_height == last_height:
                    break
                    
                last_height = new_height
                
        except Exception as e:
            logger.error(f"Error scrolling: {e}")
            
    def _extract_product_info_css(self, product_element):
        """
        Ekstrak informasi produk menggunakan CSS Selector
        
        Args:
            product_element: Selenium WebElement
            
        Returns:
            dict: Informasi produk yang sudah dibersihkan
        """
        try:
            # CSS Selectors untuk berbagai elemen
            selectors = {
                'nama_produk': '[data-testid="product-name"]',
                'harga': '[data-testid="product-price"]',
                'nama_toko': '[data-testid="store-name"]',
                'lokasi_toko': '[data-testid="store-location"]',
                'rating': '[data-testid="product-rating"]',
                'jumlah_terjual': '[data-testid="product-sold"]',
                'gambar': 'img[data-testid="product-image"]',
                'link': 'a[data-testid="product-link"]'
            }
            
            product_info = {
                'nama_produk': self._safe_extract_text(product_element, selectors['nama_produk']),
                'harga': self._extract_price_css(product_element, selectors['harga']),
                'jumlah_terjual': self._extract_sold_count_css(product_element, selectors['jumlah_terjual']),
                'nama_toko': self._safe_extract_text(product_element, selectors['nama_toko']),
                'lokasi_toko': self._safe_extract_text(product_element, selectors['lokasi_toko']),
                'rating_produk': self._extract_rating_css(product_element, selectors['rating']),
                'url_produk': self._safe_extract_attribute(product_element, selectors['link'], 'href'),
                'gambar_produk': self._safe_extract_attribute(product_element, selectors['gambar'], 'src'),
                'metode_scraping': 'CSS_Selector',
                'timestamp_scraping': datetime.now().isoformat()
            }
            
            # Data validation
            if product_info['nama_produk'] and product_info['harga']:
                return product_info
            return None
            
        except Exception as e:
            logger.error(f"Error ekstraksi CSS: {e}")
            return None
            
    def _safe_extract_text(self, element, selector):
        """Ekstrak text dengan error handling"""
        try:
            found_element = element.find_element(By.CSS_SELECTOR, selector)
            return found_element.text.strip()
        except NoSuchElementException:
            return ""
        except Exception as e:
            logger.error(f"Error ekstraksi text {selector}: {e}")
            return ""
            
    def _safe_extract_attribute(self, element, selector, attribute):
        """Ekstrak attribute dengan error handling"""
        try:
            found_element = element.find_element(By.CSS_SELECTOR, selector)
            return found_element.get_attribute(attribute)
        except NoSuchElementException:
            return ""
        except Exception as e:
            logger.error(f"Error ekstraksi attribute {selector}.{attribute}: {e}")
            return ""
            
    def _extract_price_css(self, element, selector):
        """Ekstrak harga dari CSS element"""
        try:
            price_text = self._safe_extract_text(element, selector)
            # Remove currency symbols and convert to number
            price = re.sub(r'[^\d]', '', price_text)
            return int(price) if price else 0
        except:
            return 0
            
    def _extract_sold_count_css(self, element, selector):
        """Ekstrak jumlah terjual dari CSS element"""
        try:
            sold_text = self._safe_extract_text(element, selector)
            # Extract number from text like "Terjual 123"
            sold_match = re.search(r'(\d+)', sold_text)
            return int(sold_match.group(1)) if sold_match else 0
        except:
            return 0
            
    def _extract_rating_css(self, element, selector):
        """Ekstrak rating dari CSS element"""
        try:
            rating_text = self._safe_extract_text(element, selector)
            # Extract rating number
            rating_match = re.search(r'(\d+\.?\d*)', rating_text)
            return float(rating_match.group(1)) if rating_match else 0
        except:
            return 0
            
    def save_to_csv(self, filename="bukalapak_products.csv"):
        """Simpan data ke CSV"""
        try:
            df = pd.DataFrame(self.products_data)
            df.to_csv(filename, index=False, encoding='utf-8')
            logger.info(f"Data berhasil disimpan ke {filename}")
            return filename
        except Exception as e:
            logger.error(f"Error menyimpan CSV: {e}")
            return None
            
    def save_to_json(self, filename="bukalapak_products.json"):
        """Simpan data ke JSON"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.products_data, f, ensure_ascii=False, indent=2)
            logger.info(f"Data berhasil disimpan ke {filename}")
            return filename
        except Exception as e:
            logger.error(f"Error menyimpan JSON: {e}")
            return None
            
    def get_statistics(self):
        """Dapatkan statistik data yang di-scrape"""
        if not self.products_data:
            return {}
            
        df = pd.DataFrame(self.products_data)
        
        stats = {
            'total_products': len(self.products_data),
            'avg_price': df['harga'].mean(),
            'max_price': df['harga'].max(),
            'min_price': df['harga'].min(),
            'avg_rating': df['rating_produk'].mean(),
            'total_sold': df['jumlah_terjual'].sum(),
            'unique_stores': df['nama_toko'].nunique(),
            'api_method_count': len(df[df['metode_scraping'] == 'API']),
            'css_method_count': len(df[df['metode_scraping'] == 'CSS_Selector'])
        }
        
        return stats
        
    def clear_data(self):
        """Bersihkan data yang tersimpan"""
        self.products_data = []
        logger.info("Data berhasil dibersihkan")

def main():
    """Main function untuk demonstrasi"""
    print("=" * 60)
    print("BUKALAPAK SCRAPER - Advanced Data Mining Tool")
    print("Dibuat oleh: Dosen Data Mining (30 tahun pengalaman)")
    print("=" * 60)
    
    # Inisialisasi scraper
    scraper = BukalapakScraper(headless=True, delay_range=(2, 5))
    
    # Contoh penggunaan
    search_queries = ["laptop", "smartphone", "headphone"]
    
    for query in search_queries:
        print(f"\nScraping untuk query: {query}")
        
        # Scraping via API
        print("1. Scraping via API...")
        scraper.scrape_via_api(search_query=query, max_pages=2)
        
        # Scraping via CSS Selector
        print("2. Scraping via CSS Selector...")
        scraper.scrape_via_css_selector(search_query=query, max_pages=2)
        
        # Simpan data
        csv_file = scraper.save_to_csv(f"bukalapak_{query}.csv")
        json_file = scraper.save_to_json(f"bukalapak_{query}.json")
        
        # Tampilkan statistik
        stats = scraper.get_statistics()
        print(f"\nStatistik untuk {query}:")
        for key, value in stats.items():
            print(f"  {key}: {value}")
            
        # Bersihkan data untuk query berikutnya
        scraper.clear_data()
        
    print("\nScraping selesai!")

if __name__ == "__main__":
    main()