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
import hashlib
import hmac
import base64
from datetime import datetime
import os

class AdvancedShopeeScraper:
    def __init__(self):
        self.ua = UserAgent()
        self.session = requests.Session()
        self.base_url = "https://shopee.co.id"
        self.api_base = "https://shopee.co.id/api/v4"
        self.setup_session()
        
    def setup_session(self):
        """Setup session dengan headers yang menyerupai browser asli"""
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
    
    def generate_signature(self, data, secret_key):
        """Generate signature untuk API request"""
        message = json.dumps(data, separators=(',', ':'))
        signature = hmac.new(
            secret_key.encode('utf-8'),
            message.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        return signature
    
    def get_shopee_api_data_v2(self, keyword, limit=50):
        """Menggunakan Shopee API v2 dengan signature"""
        try:
            # Get session cookies first
            session_response = self.session.get(self.base_url)
            if session_response.status_code != 200:
                print("Failed to get session cookies")
                return self.fallback_scraping(keyword, limit)
            
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
                't': int(time.time() * 1000)  # Timestamp
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
                return self.parse_api_response_v2(data, limit)
            else:
                print(f"API request failed with status code: {response.status_code}")
                print(f"Response: {response.text[:200]}")
                return self.fallback_scraping(keyword, limit)
                
        except Exception as e:
            print(f"API method failed: {str(e)}")
            return self.fallback_scraping(keyword, limit)
    
    def parse_api_response_v2(self, data, limit):
        """Parse response dari Shopee API v2"""
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
                        
                        # Handle image
                        image_url = product_info.get('image', 'N/A')
                        if image_url and image_url != 'N/A':
                            image_url = f"https://cf.shopee.co.id/file/{image_url}"
                        
                        products.append({
                            'nama_produk': product_name,
                            'harga': price,
                            'rating': f"{rating:.1f} ({total_rating} ulasan)",
                            'jumlah_terjual': sold,
                            'nama_toko': shop_name,
                            'lokasi_toko': shop_location,
                            'diskon': discount,
                            'gambar': image_url
                        })
                        
                    except Exception as e:
                        print(f"Error parsing product: {str(e)}")
                        continue
                        
        except Exception as e:
            print(f"Error parsing API response: {str(e)}")
        
        return products
    
    def setup_driver_advanced(self):
        """Setup Chrome driver dengan anti-detection yang lebih advanced"""
        options = uc.ChromeOptions()
        
        # Basic options
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        # Advanced anti-detection
        options.add_argument('--disable-web-security')
        options.add_argument('--allow-running-insecure-content')
        options.add_argument('--disable-features=VizDisplayCompositor')
        options.add_argument('--disable-ipc-flooding-protection')
        options.add_argument('--disable-renderer-backgrounding')
        options.add_argument('--disable-background-timer-throttling')
        options.add_argument('--disable-backgrounding-occluded-windows')
        options.add_argument('--disable-client-side-phishing-detection')
        options.add_argument('--disable-default-apps')
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-sync')
        options.add_argument('--disable-translate')
        options.add_argument('--hide-scrollbars')
        options.add_argument('--metrics-recording-only')
        options.add_argument('--mute-audio')
        options.add_argument('--no-first-run')
        options.add_argument('--safebrowsing-disable-auto-update')
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--ignore-ssl-errors')
        options.add_argument('--ignore-certificate-errors-spki-list')
        
        # Random user agent
        user_agent = self.ua.random
        options.add_argument(f'--user-agent={user_agent}')
        
        # Window size
        options.add_argument('--window-size=1920,1080')
        
        driver = uc.Chrome(options=options)
        
        # Execute scripts to hide automation
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        driver.execute_script("Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]})")
        driver.execute_script("Object.defineProperty(navigator, 'languages', {get: () => ['id-ID', 'id', 'en-US', 'en']})")
        
        return driver
    
    def fallback_scraping_advanced(self, keyword, limit):
        """Fallback method menggunakan Selenium dengan teknik yang lebih advanced"""
        print("Using advanced fallback Selenium method...")
        driver = None
        try:
            driver = self.setup_driver_advanced()
            
            # Navigate to search page
            search_url = f"{self.base_url}/search?{urlencode({'keyword': keyword})}"
            driver.get(search_url)
            
            # Random wait
            time.sleep(random.uniform(4, 7))
            
            # Handle potential popups
            self.handle_popups(driver)
            
            # Scroll to load more products
            self.scroll_page_advanced(driver, limit)
            
            # Extract product data
            products = self.extract_products_from_page_advanced(driver, limit)
            
            return products
            
        except Exception as e:
            print(f"Advanced fallback scraping failed: {str(e)}")
            return []
        finally:
            if driver:
                driver.quit()
    
    def handle_popups(self, driver):
        """Handle popup dan dialog yang mungkin muncul"""
        try:
            # Handle cookie consent
            cookie_buttons = driver.find_elements(By.XPATH, "//button[contains(text(), 'Accept') or contains(text(), 'Setuju') or contains(text(), 'OK')]")
            for button in cookie_buttons:
                try:
                    button.click()
                    time.sleep(1)
                except:
                    pass
            
            # Handle close buttons
            close_buttons = driver.find_elements(By.XPATH, "//button[@aria-label='Close'] | //button[contains(@class, 'close')]")
            for button in close_buttons:
                try:
                    button.click()
                    time.sleep(0.5)
                except:
                    pass
                    
        except Exception as e:
            print(f"Error handling popups: {str(e)}")
    
    def scroll_page_advanced(self, driver, limit):
        """Scroll halaman dengan teknik yang lebih advanced"""
        last_height = driver.execute_script("return document.body.scrollHeight")
        products_loaded = 0
        max_scrolls = 15
        scroll_pause_time = random.uniform(2, 4)
        
        for i in range(max_scrolls):
            # Scroll down dengan smooth scroll
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(scroll_pause_time)
            
            # Random pause
            if i % 3 == 0:
                time.sleep(random.uniform(1, 2))
            
            # Count loaded products
            try:
                # Try multiple selectors
                selectors = [
                    '[data-sqe="item"]',
                    '.col-xs-2-4',
                    '[data-testid="product-card"]',
                    '.shopee-search-item-result__item'
                ]
                
                for selector in selectors:
                    products = driver.find_elements(By.CSS_SELECTOR, selector)
                    if products:
                        products_loaded = len(products)
                        break
                
                if products_loaded >= limit:
                    break
                    
            except:
                pass
            
            # Check if page height changed
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                # Try one more time
                time.sleep(2)
                new_height = driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
            last_height = new_height
    
    def extract_products_from_page_advanced(self, driver, limit):
        """Extract data produk dengan teknik yang lebih advanced"""
        products = []
        
        try:
            # Wait for products to load
            selectors = [
                '[data-sqe="item"]',
                '.col-xs-2-4',
                '[data-testid="product-card"]',
                '.shopee-search-item-result__item'
            ]
            
            product_elements = []
            for selector in selectors:
                try:
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                    )
                    product_elements = driver.find_elements(By.CSS_SELECTOR, selector)[:limit]
                    if product_elements:
                        break
                except:
                    continue
            
            if not product_elements:
                print("No product elements found")
                return products
            
            for element in product_elements:
                try:
                    # Extract product name
                    name_selectors = [
                        '[data-sqe="name"]',
                        '.ie3A\+n',
                        '.Cve6sh',
                        'a[data-sqe="link"]',
                        '.shopee-item-card__text-name'
                    ]
                    
                    product_name = "N/A"
                    for selector in name_selectors:
                        try:
                            name_element = element.find_element(By.CSS_SELECTOR, selector)
                            product_name = name_element.text.strip()
                            if product_name:
                                break
                        except:
                            continue
                    
                    # Extract price
                    price_selectors = [
                        '[data-sqe="price"]',
                        '.vioxXd',
                        '.ZEgDH9',
                        '.shopee-item-card__text-price'
                    ]
                    
                    price = "N/A"
                    for selector in price_selectors:
                        try:
                            price_element = element.find_element(By.CSS_SELECTOR, selector)
                            price_text = price_element.text.strip()
                            if price_text:
                                price = price_text
                                break
                        except:
                            continue
                    
                    # Extract rating
                    rating_selectors = [
                        '[data-sqe="rating"]',
                        '.shopee-rating-stars__stars',
                        '.shopee-item-card__rating'
                    ]
                    
                    rating = "N/A"
                    for selector in rating_selectors:
                        try:
                            rating_element = element.find_element(By.CSS_SELECTOR, selector)
                            rating = rating_element.text.strip()
                            if rating:
                                break
                        except:
                            continue
                    
                    # Extract sold count
                    sold_selectors = [
                        '[data-sqe="sold"]',
                        '.r6HknA',
                        '.shopee-item-card__sold'
                    ]
                    
                    sold = "0"
                    for selector in sold_selectors:
                        try:
                            sold_element = element.find_element(By.CSS_SELECTOR, selector)
                            sold_text = sold_element.text.strip()
                            if sold_text:
                                sold_numbers = re.findall(r'\d+', sold_text)
                                sold = sold_numbers[0] if sold_numbers else "0"
                                break
                        except:
                            continue
                    
                    # Extract shop name
                    shop_selectors = [
                        '[data-sqe="shop"]',
                        '.shopee-item-card__shop-name'
                    ]
                    
                    shop_name = "N/A"
                    for selector in shop_selectors:
                        try:
                            shop_element = element.find_element(By.CSS_SELECTOR, selector)
                            shop_name = shop_element.text.strip()
                            if shop_name:
                                break
                        except:
                            continue
                    
                    # Extract shop location
                    location_selectors = [
                        '[data-sqe="location"]',
                        '.shopee-item-card__shop-location'
                    ]
                    
                    shop_location = "N/A"
                    for selector in location_selectors:
                        try:
                            location_element = element.find_element(By.CSS_SELECTOR, selector)
                            shop_location = location_element.text.strip()
                            if shop_location:
                                break
                        except:
                            continue
                    
                    products.append({
                        'nama_produk': product_name,
                        'harga': price,
                        'rating': rating,
                        'jumlah_terjual': sold,
                        'nama_toko': shop_name,
                        'lokasi_toko': shop_location,
                        'diskon': 'N/A',
                        'gambar': 'N/A'
                    })
                    
                except Exception as e:
                    print(f"Error extracting product data: {str(e)}")
                    continue
                    
        except Exception as e:
            print(f"Error extracting products: {str(e)}")
        
        return products
    
    def scrape_products(self, keyword, limit=50):
        """Main method untuk scraping produk"""
        print(f"Starting to scrape products for keyword: '{keyword}'")
        print(f"Target: {limit} products")
        
        # Try API method first
        products = self.get_shopee_api_data_v2(keyword, limit)
        
        if not products:
            print("API method failed, trying advanced fallback method...")
            products = self.fallback_scraping_advanced(keyword, limit)
        
        print(f"Successfully scraped {len(products)} products")
        return products
    
    def save_to_csv(self, products, filename=None):
        """Save data ke CSV file"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"shopee_products_{timestamp}.csv"
        
        df = pd.DataFrame(products)
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        print(f"Data saved to {filename}")
        return filename
    
    def save_to_excel(self, products, filename=None):
        """Save data ke Excel file"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"shopee_products_{timestamp}.xlsx"
        
        df = pd.DataFrame(products)
        df.to_excel(filename, index=False, engine='openpyxl')
        print(f"Data saved to {filename}")
        return filename
    
    def display_results(self, products):
        """Display hasil scraping"""
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

def main():
    """Main function untuk menjalankan scraper"""
    print("="*100)
    print("🛍️  ADVANCED SHOPEE PRODUCT SCRAPER 🛍️")
    print("="*100)
    
    # Get user input
    keyword = input("\n🔍 Masukkan keyword produk yang ingin di-scrape: ").strip()
    
    while True:
        try:
            limit = int(input("📊 Masukkan jumlah data yang ingin didapatkan (max 100): "))
            if 1 <= limit <= 100:
                break
            else:
                print("❌ Jumlah data harus antara 1-100!")
        except ValueError:
            print("❌ Masukkan angka yang valid!")
    
    # File format choice
    print("\n📁 Pilih format file output:")
    print("1. CSV")
    print("2. Excel")
    choice = input("Pilihan (1/2): ").strip()
    
    # Initialize scraper
    scraper = AdvancedShopeeScraper()
    
    # Start scraping
    print(f"\n🚀 Memulai scraping untuk keyword: '{keyword}'")
    print("⏳ Mohon tunggu...")
    
    products = scraper.scrape_products(keyword, limit)
    
    if products:
        # Display results
        scraper.display_results(products)
        
        # Save to file
        if choice == "2":
            filename = scraper.save_to_excel(products)
        else:
            filename = scraper.save_to_csv(products)
        
        print(f"\n✅ Scraping selesai! Data tersimpan di: {filename}")
        print(f"📈 Total produk yang berhasil di-scrape: {len(products)}")
    else:
        print("❌ Tidak ada data yang berhasil di-scrape!")

if __name__ == "__main__":
    main()