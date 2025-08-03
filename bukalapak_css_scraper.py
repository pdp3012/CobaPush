#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bukalapak CSS Selector Scraper - Advanced Implementation
Fokus pada CSS Selector dengan multiple fallback strategies
"""

import time
import re
import json
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from fake_useragent import UserAgent
from webdriver_manager.chrome import ChromeDriverManager
import logging
from datetime import datetime
import random

class BukalapakCSSScraper:
    """
    Advanced CSS Selector Scraper untuk Bukalapak
    Menggunakan multiple selector strategies untuk robustness
    """
    
    def __init__(self, headless=True):
        self.base_url = "https://www.bukalapak.com"
        self.driver = None
        self.ua = UserAgent()
        self.headless = headless
        self.products_data = []
        
        # Multiple CSS Selector strategies
        self.selectors = {
            # Primary selectors (most reliable)
            'primary': {
                'product_card': '[data-testid="product-card"], .product-card, .bl-product-card',
                'product_name': '[data-testid="product-name"], .product-name, .bl-product-name, h3 a, .product-title',
                'product_price': '[data-testid="product-price"], .product-price, .bl-product-price, .price, .amount',
                'store_name': '[data-testid="store-name"], .store-name, .bl-store-name, .seller-name',
                'store_location': '[data-testid="store-location"], .store-location, .bl-store-location, .location',
                'product_rating': '[data-testid="product-rating"], .product-rating, .bl-product-rating, .rating',
                'product_sold': '[data-testid="product-sold"], .product-sold, .bl-product-sold, .sold-count',
                'product_image': 'img[data-testid="product-image"], .product-image img, .bl-product-image img',
                'product_link': 'a[data-testid="product-link"], .product-link, .bl-product-link, a[href*="/p/"]'
            },
            # Alternative selectors (fallback)
            'alternative': {
                'product_card': '.product, .item, .card, [class*="product"], [class*="item"]',
                'product_name': 'h3, h4, .title, .name, [class*="title"], [class*="name"]',
                'product_price': '.price, .cost, .amount, [class*="price"], [class*="cost"]',
                'store_name': '.seller, .shop, .store, [class*="seller"], [class*="shop"]',
                'store_location': '.location, .city, .area, [class*="location"], [class*="city"]',
                'product_rating': '.rating, .star, .score, [class*="rating"], [class*="star"]',
                'product_sold': '.sold, .sales, .count, [class*="sold"], [class*="sales"]',
                'product_image': 'img',
                'product_link': 'a'
            }
        }
        
        self._setup_driver()
        
    def _setup_driver(self):
        """Setup Selenium WebDriver dengan anti-deteksi"""
        chrome_options = Options()
        
        if self.headless:
            chrome_options.add_argument("--headless")
            
        # Anti-deteksi settings
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument(f"--user-agent={self.ua.random}")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # Additional stealth settings
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-plugins")
        chrome_options.add_argument("--disable-images")  # Optional: untuk speed
        chrome_options.add_argument("--disable-javascript")  # Optional: untuk speed
        
        try:
            self.driver = webdriver.Chrome(
                service=webdriver.chrome.service.Service(ChromeDriverManager().install()),
                options=chrome_options
            )
            
            # Execute stealth scripts
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            self.driver.execute_script("Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]})")
            self.driver.execute_script("Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']})")
            
            print("WebDriver berhasil diinisialisasi dengan anti-deteksi")
            
        except Exception as e:
            print(f"Error setup WebDriver: {e}")
            raise
            
    def scrape_products(self, search_query="", max_pages=3):
        """
        Scrape produk dengan CSS Selector
        
        Args:
            search_query (str): Query pencarian
            max_pages (int): Maksimal halaman
        """
        print(f"Memulai scraping untuk query: {search_query}")
        
        try:
            for page in range(1, max_pages + 1):
                print(f"Scraping halaman {page}")
                
                # Construct URL
                if page == 1:
                    url = f"{self.base_url}/search?search%5Bkeywords%5D={search_query}"
                else:
                    url = f"{self.base_url}/search?search%5Bkeywords%5D={search_query}&page={page}"
                
                # Navigate to page
                self.driver.get(url)
                
                # Wait for page load
                self._wait_for_page_load()
                
                # Scroll to load all content
                self._scroll_page()
                
                # Extract products
                products = self._find_product_elements()
                
                if not products:
                    print(f"Tidak ada produk ditemukan di halaman {page}")
                    break
                    
                print(f"Menemukan {len(products)} produk di halaman {page}")
                
                # Extract data from each product
                for i, product in enumerate(products):
                    try:
                        product_data = self._extract_product_data(product)
                        if product_data:
                            self.products_data.append(product_data)
                            print(f"  Produk {i+1}: {product_data['nama_produk'][:50]}...")
                    except Exception as e:
                        print(f"Error ekstraksi produk {i+1}: {e}")
                        continue
                        
                # Random delay
                time.sleep(random.uniform(2, 5))
                
        except Exception as e:
            print(f"Error dalam scraping: {e}")
        finally:
            if self.driver:
                self.driver.quit()
                
        print(f"Scraping selesai. Total produk: {len(self.products_data)}")
        
    def _wait_for_page_load(self):
        """Wait untuk halaman load dengan multiple strategies"""
        try:
            # Wait for any product element to appear
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, self.selectors['primary']['product_card']))
            )
        except TimeoutException:
            try:
                # Fallback to alternative selector
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, self.selectors['alternative']['product_card']))
                )
            except TimeoutException:
                print("Timeout waiting for page load")
                
    def _scroll_page(self):
        """Scroll halaman untuk memuat semua konten"""
        try:
            last_height = self.driver.execute_script("return document.body.scrollHeight")
            
            for _ in range(3):  # Scroll 3 times
                # Scroll down
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
                
                # Calculate new height
                new_height = self.driver.execute_script("return document.body.scrollHeight")
                
                if new_height == last_height:
                    break
                    
                last_height = new_height
                
        except Exception as e:
            print(f"Error scrolling: {e}")
            
    def _find_product_elements(self):
        """Find product elements dengan multiple strategies"""
        products = []
        
        # Try primary selectors first
        for selector in self.selectors['primary']['product_card'].split(', '):
            try:
                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                if elements:
                    products = elements
                    print(f"Found products using selector: {selector}")
                    break
            except:
                continue
                
        # Fallback to alternative selectors
        if not products:
            for selector in self.selectors['alternative']['product_card'].split(', '):
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if elements:
                        products = elements
                        print(f"Found products using fallback selector: {selector}")
                        break
                except:
                    continue
                    
        return products
        
    def _extract_product_data(self, product_element):
        """
        Extract product data dengan multiple selector strategies
        
        Args:
            product_element: Selenium WebElement
            
        Returns:
            dict: Product data
        """
        try:
            product_data = {
                'nama_produk': self._extract_text_with_fallback(product_element, 'product_name'),
                'harga': self._extract_price_with_fallback(product_element),
                'jumlah_terjual': self._extract_sold_with_fallback(product_element),
                'nama_toko': self._extract_text_with_fallback(product_element, 'store_name'),
                'lokasi_toko': self._extract_text_with_fallback(product_element, 'store_location'),
                'rating_produk': self._extract_rating_with_fallback(product_element),
                'url_produk': self._extract_url_with_fallback(product_element),
                'gambar_produk': self._extract_image_with_fallback(product_element),
                'metode_scraping': 'CSS_Selector_Advanced',
                'timestamp_scraping': datetime.now().isoformat()
            }
            
            # Data validation
            if product_data['nama_produk'] and product_data['harga'] > 0:
                return product_data
            return None
            
        except Exception as e:
            print(f"Error extracting product data: {e}")
            return None
            
    def _extract_text_with_fallback(self, element, field_name):
        """Extract text dengan multiple selector fallback"""
        # Try primary selectors
        for selector in self.selectors['primary'][field_name].split(', '):
            try:
                found_element = element.find_element(By.CSS_SELECTOR, selector)
                text = found_element.text.strip()
                if text:
                    return text
            except:
                continue
                
        # Try alternative selectors
        for selector in self.selectors['alternative'][field_name].split(', '):
            try:
                found_element = element.find_element(By.CSS_SELECTOR, selector)
                text = found_element.text.strip()
                if text:
                    return text
            except:
                continue
                
        return ""
        
    def _extract_price_with_fallback(self, element):
        """Extract harga dengan multiple strategies"""
        price_text = self._extract_text_with_fallback(element, 'product_price')
        
        if price_text:
            # Remove currency symbols and convert to number
            price = re.sub(r'[^\d]', '', price_text)
            try:
                return int(price) if price else 0
            except:
                return 0
        return 0
        
    def _extract_sold_with_fallback(self, element):
        """Extract jumlah terjual dengan multiple strategies"""
        sold_text = self._extract_text_with_fallback(element, 'product_sold')
        
        if sold_text:
            # Extract number from text like "Terjual 123" or "123 terjual"
            sold_match = re.search(r'(\d+)', sold_text)
            try:
                return int(sold_match.group(1)) if sold_match else 0
            except:
                return 0
        return 0
        
    def _extract_rating_with_fallback(self, element):
        """Extract rating dengan multiple strategies"""
        rating_text = self._extract_text_with_fallback(element, 'product_rating')
        
        if rating_text:
            # Extract rating number
            rating_match = re.search(r'(\d+\.?\d*)', rating_text)
            try:
                return float(rating_match.group(1)) if rating_match else 0
            except:
                return 0
        return 0
        
    def _extract_url_with_fallback(self, element):
        """Extract URL dengan multiple strategies"""
        # Try primary selectors
        for selector in self.selectors['primary']['product_link'].split(', '):
            try:
                found_element = element.find_element(By.CSS_SELECTOR, selector)
                url = found_element.get_attribute('href')
                if url and '/p/' in url:
                    return url
            except:
                continue
                
        # Try alternative selectors
        for selector in self.selectors['alternative']['product_link'].split(', '):
            try:
                found_element = element.find_element(By.CSS_SELECTOR, selector)
                url = found_element.get_attribute('href')
                if url and '/p/' in url:
                    return url
            except:
                continue
                
        return ""
        
    def _extract_image_with_fallback(self, element):
        """Extract image URL dengan multiple strategies"""
        # Try primary selectors
        for selector in self.selectors['primary']['product_image'].split(', '):
            try:
                found_element = element.find_element(By.CSS_SELECTOR, selector)
                src = found_element.get_attribute('src')
                if src:
                    return src
            except:
                continue
                
        # Try alternative selectors
        for selector in self.selectors['alternative']['product_image'].split(', '):
            try:
                found_element = element.find_element(By.CSS_SELECTOR, selector)
                src = found_element.get_attribute('src')
                if src:
                    return src
            except:
                continue
                
        return ""
        
    def save_to_csv(self, filename="bukalapak_css_products.csv"):
        """Save data ke CSV"""
        try:
            df = pd.DataFrame(self.products_data)
            df.to_csv(filename, index=False, encoding='utf-8')
            print(f"Data berhasil disimpan ke {filename}")
            return filename
        except Exception as e:
            print(f"Error menyimpan CSV: {e}")
            return None
            
    def save_to_json(self, filename="bukalapak_css_products.json"):
        """Save data ke JSON"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.products_data, f, ensure_ascii=False, indent=2)
            print(f"Data berhasil disimpan ke {filename}")
            return filename
        except Exception as e:
            print(f"Error menyimpan JSON: {e}")
            return None
            
    def get_statistics(self):
        """Get statistics dari data yang di-scrape"""
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
            'unique_stores': df['nama_toko'].nunique()
        }
        
        return stats

def main():
    """Main function untuk demonstrasi CSS Selector scraper"""
    print("=" * 60)
    print("BUKALAPAK CSS SELECTOR SCRAPER")
    print("Advanced Implementation dengan Multiple Fallback Strategies")
    print("=" * 60)
    
    # Initialize scraper
    scraper = BukalapakCSSScraper(headless=True)
    
    # Test queries
    test_queries = ["laptop", "smartphone"]
    
    for query in test_queries:
        print(f"\n{'='*40}")
        print(f"SCRAPING: {query.upper()}")
        print(f"{'='*40}")
        
        # Scrape products
        scraper.scrape_products(search_query=query, max_pages=2)
        
        # Save data
        csv_file = scraper.save_to_csv(f"bukalapak_css_{query}.csv")
        json_file = scraper.save_to_json(f"bukalapak_css_{query}.json")
        
        # Show statistics
        stats = scraper.get_statistics()
        print(f"\nStatistik untuk {query}:")
        for key, value in stats.items():
            print(f"  {key}: {value}")
            
        # Clear data for next query
        scraper.products_data = []
        
    print("\nCSS Selector Scraping selesai!")

if __name__ == "__main__":
    main()