# CELL 1: Install Dependencies
# ============================
!pip install requests pandas selenium undetected-chromedriver fake-useragent beautifulsoup4 lxml webdriver-manager openpyxl

# Install Chrome
!apt-get update
!apt-get install -y chromium-chromedriver

print("✅ Dependencies installed successfully!")

# CELL 2: Import Libraries
# ========================
import requests
import json
import time
import random
import pandas as pd
from urllib.parse import quote, urlencode
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import undetected_chromedriver as uc
from fake_useragent import UserAgent
import re
from datetime import datetime
from google.colab import files

print("✅ Libraries imported successfully!")

# CELL 3: Shopee Scraper Class
# ============================
class QuickShopeeScraper:
    def __init__(self):
        self.ua = UserAgent()
        self.session = requests.Session()
        self.base_url = "https://shopee.co.id"
        self.api_base = "https://shopee.co.id/api/v4"
        self.setup_session()
        
    def setup_session(self):
        headers = {
            'User-Agent': self.ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'id-ID,id;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Cache-Control': 'max-age=0',
            'DNT': '1'
        }
        self.session.headers.update(headers)
    
    def get_shopee_api_data(self, keyword, limit=50):
        try:
            # Get session cookies first
            session_response = self.session.get(self.base_url)
            if session_response.status_code != 200:
                print("Failed to get session cookies")
                return []
            
            # API endpoint untuk search
            search_url = f"{self.api_base}/search/search_items"
            
            # Parameters
            params = {
                'keyword': keyword,
                'limit': min(limit, 100),
                'newest': 0,
                'order': 'desc',
                'page_type': 'search',
                'scenario': 'PAGE_GLOBAL_SEARCH',
                'version': 2,
                't': int(time.time() * 1000)
            }
            
            # Headers untuk API request
            headers = {
                'User-Agent': self.ua.random,
                'Accept': 'application/json, text/plain, */*',
                'Accept-Language': 'id-ID,id;q=0.9,en;q=0.8',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
                'Referer': f'{self.base_url}/search?{urlencode({"keyword": keyword})}',
                'X-Requested-With': 'XMLHttpRequest',
                'X-Shopee-Language': 'id',
                'X-API-Source': 'pc',
                'X-Shopee-Client': 'web'
            }
            
            # Add random delay
            time.sleep(random.uniform(1, 3))
            
            response = self.session.get(search_url, params=params, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                return self.parse_api_response(data, limit)
            else:
                print(f"API request failed with status code: {response.status_code}")
                return []
                
        except Exception as e:
            print(f"API method failed: {str(e)}")
            return []
    
    def parse_api_response(self, data, limit):
        products = []
        
        try:
            if 'items' in data and data['items']:
                for item in data['items'][:limit]:
                    try:
                        product_info = item.get('item_basic', {})
                        shop_info = item.get('shop_basic', {})
                        
                        # Extract product data
                        product_name = product_info.get('name', 'N/A')
                        
                        # Handle price (convert from centavos)
                        price_min = product_info.get('price_min', 0)
                        price_max = product_info.get('price_max', 0)
                        if price_min == price_max:
                            price = f"Rp {price_min / 100000:,.0f}"
                        else:
                            price = f"Rp {price_min / 100000:,.0f} - Rp {price_max / 100000:,.0f}"
                        
                        # Handle rating
                        item_rating = product_info.get('item_rating', {})
                        rating = item_rating.get('rating_star', 0)
                        rating_count = item_rating.get('rating_count', [0])
                        total_rating = sum(rating_count) if rating_count else 0
                        
                        # Handle sold count
                        sold = product_info.get('historical_sold', 0)
                        
                        # Handle shop info
                        shop_name = shop_info.get('name', 'N/A')
                        shop_location = shop_info.get('shop_location', 'N/A')
                        
                        # Handle discount
                        discount = product_info.get('discount', 'N/A')
                        if discount != 'N/A':
                            discount = f"{discount}%"
                        
                        products.append({
                            'nama_produk': product_name,
                            'harga': price,
                            'rating': f"{rating:.1f} ({total_rating} ulasan)",
                            'jumlah_terjual': sold,
                            'nama_toko': shop_name,
                            'lokasi_toko': shop_location,
                            'diskon': discount
                        })
                        
                    except Exception as e:
                        print(f"Error parsing product: {str(e)}")
                        continue
                        
        except Exception as e:
            print(f"Error parsing API response: {str(e)}")
        
        return products
    
    def scrape_products(self, keyword, limit=50):
        print(f"Starting to scrape products for keyword: '{keyword}'")
        print(f"Target: {limit} products")
        
        # Try API method
        products = self.get_shopee_api_data(keyword, limit)
        
        print(f"Successfully scraped {len(products)} products")
        return products
    
    def save_to_csv(self, products, filename=None):
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"shopee_products_{timestamp}.csv"
        
        df = pd.DataFrame(products)
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        print(f"Data saved to {filename}")
        return filename
    
    def display_results(self, products):
        if not products:
            print("No products found!")
            return
        
        print(f"\n{'='*100}")
        print(f"SCRAPING RESULTS - {len(products)} PRODUCTS")
        print(f"{'='*100}")
        
        for i, product in enumerate(products, 1):
            print(f"\n{i}. {product['nama_produk']}")
            print(f"   💰 Harga: {product['harga']}")
            print(f"   ⭐ Rating: {product['rating']}")
            print(f"   📦 Terjual: {product['jumlah_terjual']}")
            print(f"   🏪 Toko: {product['nama_toko']}")
            print(f"   📍 Lokasi: {product['lokasi_toko']}")
            if product.get('diskon') and product['diskon'] != 'N/A':
                print(f"   🎯 Diskon: {product['diskon']}")
            print("-" * 80)

print("✅ Shopee Scraper class loaded successfully!")

# CELL 4: Quick Test
# ==================
# Test scraper dengan keyword sederhana
scraper = QuickShopeeScraper()

# Test dengan keyword "laptop"
keyword = "laptop"
limit = 5

print(f"🧪 Testing scraper dengan keyword: '{keyword}'")
products = scraper.scrape_products(keyword, limit)

if products:
    print(f"✅ Test berhasil! Dapat {len(products)} produk")
    scraper.display_results(products)
    
    # Save to CSV
    filename = scraper.save_to_csv(products)
    print(f"\n💾 File tersimpan: {filename}")
    
    # Download file
    files.download(filename)
else:
    print("❌ Test gagal - tidak ada data")

# CELL 5: User Input Scraping
# ===========================
# Masukkan keyword dan jumlah data yang diinginkan
keyword = input("🔍 Masukkan keyword produk: ").strip()
limit = int(input("📊 Jumlah data (max 100): "))

print(f"\n🚀 Memulai scraping untuk '{keyword}'...")
products = scraper.scrape_products(keyword, limit)

if products:
    scraper.display_results(products)
    
    # Save to CSV
    filename = scraper.save_to_csv(products)
    print(f"\n✅ Scraping selesai! File: {filename}")
    
    # Download file
    files.download(filename)
else:
    print("❌ Tidak ada data yang ditemukan")

# CELL 6: Multiple Keywords (Optional)
# ====================================
# Scrape multiple keywords sekaligus
keywords = ["laptop", "smartphone", "sepatu"]
all_products = []

for keyword in keywords:
    print(f"\n📦 Scraping '{keyword}'...")
    products = scraper.scrape_products(keyword, 10)
    
    if products:
        all_products.extend(products)
        print(f"✅ Dapat {len(products)} produk")
    else:
        print(f"❌ Tidak ada data untuk '{keyword}'")
    
    time.sleep(2)  # Delay between keywords

if all_products:
    print(f"\n🎉 Total semua produk: {len(all_products)}")
    
    # Save all products
    filename = scraper.save_to_csv(all_products, "shopee_all_products.csv")
    print(f"💾 Semua data tersimpan di: {filename}")
    
    # Download file
    files.download(filename)
else:
    print("❌ Tidak ada data yang berhasil di-scrape")