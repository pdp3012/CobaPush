#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Advanced Shopee Product Scraper
Dibuat oleh: Dosen Data Mining dengan 30 tahun pengalaman

Fitur:
- Advanced anti-bot protection
- Multiple selector fallbacks
- Human-like behavior simulation
- Comprehensive data extraction
- Google Colab optimized
- Multiple output formats
"""

import requests
import time
import random
import json
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
import re
from urllib.parse import quote
import warnings
import os
from datetime import datetime
import logging
warnings.filterwarnings('ignore')

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('shopee_scraper.log'),
        logging.StreamHandler()
    ]
)

class FinalShopeeScraper:
    def __init__(self, headless=True, verbose=True):
        """
        Initialize Advanced Shopee Scraper
        
        Args:
            headless (bool): Run browser in headless mode
            verbose (bool): Enable verbose logging
        """
        self.session = requests.Session()
        self.driver = None
        self.verbose = verbose
        self.headless = headless
        
        # Advanced user agents
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/121.0'
        ]
        
        # Multiple selectors for different HTML structures
        self.selectors = {
            'product': [
                "div[data-sqe='link']",
                ".shopee-search-item-result__item",
                "[data-testid='product-card']",
                ".col-xs-2-4",
                ".shopee-item-card",
                ".shopee-search-item-result__item-name"
            ],
            'name': [
                'div[data-sqe="name"]',
                '.ie3A\+n',
                '.Cve6sh',
                '[data-testid="product-card"] .ie3A\+n',
                '.shopee-search-item-result__item-name',
                '.shopee-item-card__text-name',
                '.shopee-search-item-result__item-name'
            ],
            'price': [
                'div[data-sqe="price"]',
                '.vioxXd',
                '.ZEgDH9',
                '[data-testid="product-card"] .vioxXd',
                '.shopee-search-item-result__item-price',
                '.shopee-item-card__text-price',
                '.shopee-search-item-result__item-price'
            ],
            'rating': [
                'div[data-sqe="rating"]',
                '.shopee-rating-stars__stars',
                '.shopee-rating-stars__stars--active',
                '[data-testid="product-card"] .shopee-rating-stars',
                '.shopee-item-card__rating'
            ],
            'sold': [
                'div[data-sqe="sold"]',
                '.r6HknA',
                '.shopee-search-item-result__item-sold',
                '[data-testid="product-card"] .r6HknA',
                '.shopee-item-card__sold'
            ],
            'shop': [
                'div[data-sqe="shop"]',
                '.shopee-search-item-result__shop-name',
                '.shopee-search-item-result__item-shop',
                '[data-testid="product-card"] .shopee-search-item-result__shop-name',
                '.shopee-item-card__shop-name'
            ],
            'location': [
                'div[data-sqe="location"]',
                '.shopee-search-item-result__shop-location',
                '.shopee-search-item-result__item-location',
                '[data-testid="product-card"] .shopee-search-item-result__shop-location',
                '.shopee-item-card__shop-location'
            ]
        }
        
        self.setup_session()
        
    def setup_session(self):
        """Setup session dengan headers yang realistic"""
        headers = {
            'User-Agent': random.choice(self.user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9,id;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Cache-Control': 'max-age=0',
            'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"'
        }
        self.session.headers.update(headers)
        
    def setup_driver(self):
        """Setup Chrome driver dengan advanced anti-detection"""
        chrome_options = Options()
        
        # Basic anti-detection
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # Advanced anti-detection
        chrome_options.add_argument('--disable-web-security')
        chrome_options.add_argument('--allow-running-insecure-content')
        chrome_options.add_argument('--disable-features=VizDisplayCompositor')
        chrome_options.add_argument('--disable-ipc-flooding-protection')
        
        # Performance optimizations
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--disable-plugins')
        chrome_options.add_argument('--disable-images')
        chrome_options.add_argument('--disable-javascript')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-software-rasterizer')
        
        # Additional arguments
        chrome_options.add_argument('--disable-background-timer-throttling')
        chrome_options.add_argument('--disable-backgrounding-occluded-windows')
        chrome_options.add_argument('--disable-renderer-backgrounding')
        chrome_options.add_argument('--disable-features=TranslateUI')
        
        # Random window size
        width = random.randint(1200, 1920)
        height = random.randint(800, 1080)
        chrome_options.add_argument(f'--window-size={width},{height}')
        
        # Set user agent
        user_agent = random.choice(self.user_agents)
        chrome_options.add_argument(f'--user-agent={user_agent}')
        
        # Headless mode
        if self.headless:
            chrome_options.add_argument('--headless')
        
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            
            # Execute stealth scripts
            stealth_js = """
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined,
            });
            
            Object.defineProperty(navigator, 'plugins', {
                get: () => [1, 2, 3, 4, 5],
            });
            
            Object.defineProperty(navigator, 'languages', {
                get: () => ['en-US', 'en'],
            });
            
            window.chrome = {
                runtime: {},
            };
            
            Object.defineProperty(navigator, 'permissions', {
                get: () => ({
                    query: async () => ({ state: 'granted' }),
                }),
            });
            """
            
            self.driver.execute_script(stealth_js)
            
            if self.verbose:
                logging.info("✅ Chrome driver berhasil diinisialisasi")
                
        except Exception as e:
            logging.error(f"❌ Error setting up Chrome driver: {e}")
            raise
            
    def random_delay(self, min_delay=2, max_delay=5):
        """Random delay dengan human-like behavior"""
        delay = random.uniform(min_delay, max_delay)
        time.sleep(delay)
        
    def human_like_scroll(self):
        """Scroll seperti manusia"""
        try:
            scroll_height = self.driver.execute_script("return document.body.scrollHeight")
            current_position = 0
            scroll_step = random.randint(300, 700)
            
            while current_position < scroll_height:
                current_position += scroll_step
                self.driver.execute_script(f"window.scrollTo(0, {current_position});")
                time.sleep(random.uniform(0.5, 1.5))
                
        except Exception as e:
            logging.warning(f"Warning during scrolling: {e}")
            
    def get_search_url(self, keyword):
        """Generate search URL dari keyword"""
        encoded_keyword = quote(keyword)
        return f"https://shopee.co.id/search?keyword={encoded_keyword}"
        
    def extract_element_text(self, element, selectors, default="N/A"):
        """Extract text dari element menggunakan multiple selectors"""
        for selector in selectors:
            try:
                found_element = element.select_one(selector)
                if found_element:
                    text = found_element.get_text(strip=True)
                    if text and text != "":
                        return text
            except Exception as e:
                continue
        return default
        
    def extract_product_data(self, product_element):
        """Extract data dari product element dengan multiple selectors"""
        try:
            # Extract semua data menggunakan multiple selectors
            product_name = self.extract_element_text(product_element, self.selectors['name'])
            price_text = self.extract_element_text(product_element, self.selectors['price'])
            rating = self.extract_element_text(product_element, self.selectors['rating'])
            sold = self.extract_element_text(product_element, self.selectors['sold'])
            shop_name = self.extract_element_text(product_element, self.selectors['shop'])
            location = self.extract_element_text(product_element, self.selectors['location'])
            
            # Clean price text
            if price_text != "N/A":
                price = re.sub(r'[^\d]', '', price_text)
            else:
                price = "N/A"
                
            return {
                'Nama Produk': product_name,
                'Harga': price,
                'Rating': rating,
                'Jumlah Terjual': sold,
                'Nama Toko': shop_name,
                'Lokasi Toko': location,
                'Timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
        except Exception as e:
            logging.error(f"Error extracting product data: {e}")
            return None
            
    def scrape_shopee(self, keyword, max_products=50):
        """Main scraping function dengan advanced techniques"""
        logging.info(f"🚀 Memulai scraping untuk keyword: {keyword}")
        logging.info(f"📊 Target jumlah produk: {max_products}")
        
        try:
            self.setup_driver()
            search_url = self.get_search_url(keyword)
            
            logging.info(f"🌐 Mengakses URL: {search_url}")
            self.driver.get(search_url)
            self.random_delay(3, 6)
            
            # Wait for page to load dengan multiple selectors
            page_loaded = False
            for selector in self.selectors['product']:
                try:
                    WebDriverWait(self.driver, 15).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                    )
                    page_loaded = True
                    logging.info(f"✅ Halaman berhasil dimuat dengan selector: {selector}")
                    break
                except TimeoutException:
                    continue
                    
            if not page_loaded:
                logging.error("❌ Gagal memuat halaman produk")
                return []
                
            products_data = []
            page = 1
            retry_count = 0
            max_retries = 3
            
            while len(products_data) < max_products and retry_count < max_retries:
                logging.info(f"📄 Scraping halaman {page}...")
                
                # Human-like scroll
                self.human_like_scroll()
                self.random_delay(2, 4)
                
                # Get page source dan parse
                soup = BeautifulSoup(self.driver.page_source, 'html.parser')
                
                # Find product elements dengan multiple selectors
                product_elements = []
                for selector in self.selectors['product']:
                    elements = soup.select(selector)
                    if elements:
                        product_elements = elements
                        logging.info(f"✅ Ditemukan {len(elements)} produk dengan selector: {selector}")
                        break
                        
                if not product_elements:
                    logging.warning("⚠️ Tidak ada produk ditemukan pada halaman ini")
                    retry_count += 1
                    continue
                    
                new_products = 0
                for element in product_elements:
                    if len(products_data) >= max_products:
                        break
                        
                    product_data = self.extract_product_data(element)
                    if product_data and product_data['Nama Produk'] != "N/A":
                        # Check duplicate
                        if not any(p['Nama Produk'] == product_data['Nama Produk'] for p in products_data):
                            products_data.append(product_data)
                            new_products += 1
                            if self.verbose:
                                logging.info(f"✅ Produk {len(products_data)}: {product_data['Nama Produk'][:50]}...")
                            
                if new_products == 0:
                    retry_count += 1
                else:
                    retry_count = 0
                    
                # Try to go to next page
                try:
                    next_button = self.driver.find_element(By.CSS_SELECTOR, "button[aria-label='Next page']")
                    if not next_button.is_enabled():
                        logging.info("📄 Tidak ada halaman selanjutnya")
                        break
                    next_button.click()
                    self.random_delay(3, 5)
                    page += 1
                except NoSuchElementException:
                    logging.info("📄 Tidak ada tombol next page")
                    break
                    
            logging.info(f"🎉 Scraping selesai! Total produk yang berhasil di-scrape: {len(products_data)}")
            return products_data
            
        except Exception as e:
            logging.error(f"❌ Error during scraping: {e}")
            return []
            
        finally:
            if self.driver:
                self.driver.quit()
                
    def save_to_csv(self, data, filename):
        """Save data ke CSV dengan encoding yang proper"""
        try:
            df = pd.DataFrame(data)
            df.to_csv(filename, index=False, encoding='utf-8-sig')
            logging.info(f"💾 Data berhasil disimpan ke {filename}")
        except Exception as e:
            logging.error(f"❌ Error saving CSV: {e}")
        
    def save_to_excel(self, data, filename):
        """Save data ke Excel dengan formatting"""
        try:
            df = pd.DataFrame(data)
            
            # Create Excel writer
            with pd.ExcelWriter(filename, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name='Shopee Data', index=False)
                
                # Get workbook and worksheet
                workbook = writer.book
                worksheet = writer.sheets['Shopee Data']
                
                # Auto-adjust column widths
                for column in worksheet.columns:
                    max_length = 0
                    column_letter = column[0].column_letter
                    for cell in column:
                        try:
                            if len(str(cell.value)) > max_length:
                                max_length = len(str(cell.value))
                        except:
                            pass
                    adjusted_width = min(max_length + 2, 50)
                    worksheet.column_dimensions[column_letter].width = adjusted_width
                    
            logging.info(f"💾 Data berhasil disimpan ke {filename}")
        except Exception as e:
            logging.error(f"❌ Error saving Excel: {e}")

def main():
    """Main function untuk user interface yang lebih user-friendly"""
    print("=" * 70)
    print("🛍️  FINAL ADVANCED SHOPEE PRODUCT SCRAPER")
    print("👨‍🏫 Dibuat oleh: Dosen Data Mining dengan 30 tahun pengalaman")
    print("🔧 Dilengkapi dengan Advanced Anti-Bot Protection")
    print("🚀 Optimized untuk Google Colab")
    print("=" * 70)
    
    # Input dari user
    keyword = input("🔍 Masukkan keyword produk yang ingin di-scrape: ").strip()
    
    while True:
        try:
            max_products = int(input("📊 Masukkan jumlah data yang ingin didapatkan: "))
            if max_products > 0:
                break
            else:
                print("❌ Jumlah data harus lebih dari 0!")
        except ValueError:
            print("❌ Masukkan angka yang valid!")
    
    # Inisialisasi scraper
    scraper = FinalShopeeScraper(headless=True, verbose=True)
    
    # Mulai scraping
    print("\n🚀 Memulai proses scraping...")
    print("⏳ Mohon tunggu, proses ini memakan waktu beberapa menit...")
    print("🛡️ Anti-bot protection sedang aktif...")
    
    start_time = time.time()
    products_data = scraper.scrape_shopee(keyword, max_products)
    end_time = time.time()
    
    if products_data:
        # Calculate execution time
        execution_time = end_time - start_time
        print(f"\n⏱️ Waktu eksekusi: {execution_time:.2f} detik")
        
        # Save data
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename_base = f"shopee_{keyword.replace(' ', '_')}_{len(products_data)}_products_{timestamp}"
        
        # Save ke CSV
        csv_filename = f"{filename_base}.csv"
        scraper.save_to_csv(products_data, csv_filename)
        
        # Save ke Excel
        excel_filename = f"{filename_base}.xlsx"
        scraper.save_to_excel(products_data, excel_filename)
        
        # Display sample data
        print("\n" + "=" * 70)
        print("📋 SAMPLE DATA YANG BERHASIL DI-SCRAPE:")
        print("=" * 70)
        
        df = pd.DataFrame(products_data)
        print(df.head(10).to_string(index=False))
        
        # Display statistics
        print(f"\n📈 STATISTIK SCRAPING:")
        print(f"✅ Total data berhasil di-scrape: {len(products_data)}")
        print(f"📁 File CSV: {csv_filename}")
        print(f"📁 File Excel: {excel_filename}")
        print(f"⏱️ Waktu eksekusi: {execution_time:.2f} detik")
        print(f"🚀 Rata-rata: {len(products_data)/execution_time:.2f} produk/detik")
        
    else:
        print("❌ Tidak ada data yang berhasil di-scrape. Silakan coba lagi.")

if __name__ == "__main__":
    main()