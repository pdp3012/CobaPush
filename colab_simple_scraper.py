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

# CELL 3: Simple Shopee Scraper Class
# ===================================
class SimpleShopeeScraper:
    def __init__(self):
        self.ua = UserAgent()
        self.base_url = "https://shopee.co.id"
        
    def setup_driver(self):
        """Setup Chrome driver untuk Google Colab"""
        try:
            options = uc.ChromeOptions()
            
            # Basic options
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-blink-features=AutomationControlled')
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            
            # Colab specific options
            options.add_argument('--headless')
            options.add_argument('--disable-gpu')
            options.add_argument('--remote-debugging-port=9222')
            
            # Anti-detection
            options.add_argument('--disable-web-security')
            options.add_argument('--allow-running-insecure-content')
            options.add_argument('--disable-extensions')
            options.add_argument('--disable-plugins')
            
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
            
        except Exception as e:
            print(f"❌ Failed to setup driver: {str(e)}")
            return None
    
    def scrape_products(self, keyword, limit=20):
        """Main scraping method menggunakan Selenium"""
        print(f"🚀 Memulai scraping untuk keyword: '{keyword}'")
        print(f"📊 Target: {limit} produk")
        print("-" * 50)
        
        driver = None
        try:
            # Setup driver
            print("🔧 Setting up Chrome driver...")
            driver = self.setup_driver()
            if not driver:
                print("❌ Failed to setup Chrome driver")
                return []
            
            # Navigate to search page
            search_url = f"{self.base_url}/search?{urlencode({'keyword': keyword})}"
            print(f"🔗 Navigating to: {search_url}")
            driver.get(search_url)
            
            # Wait for page to load
            wait_time = random.uniform(5, 8)
            print(f"⏳ Waiting {wait_time:.1f} seconds for page to load...")
            time.sleep(wait_time)
            
            # Handle popups
            self.handle_popups(driver)
            
            # Scroll to load more products
            self.scroll_page(driver, limit)
            
            # Extract product data
            products = self.extract_products(driver, limit)
            
            print(f"✅ Scraping selesai! Dapat {len(products)} produk")
            return products
            
        except Exception as e:
            print(f"❌ Scraping failed: {str(e)}")
            return []
        finally:
            if driver:
                try:
                    driver.quit()
                    print("🔒 Driver closed")
                except:
                    pass
    
    def handle_popups(self, driver):
        """Handle popup dan dialog"""
        try:
            print("🔍 Handling popups...")
            
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
            print(f"⚠️ Error handling popups: {str(e)}")
    
    def scroll_page(self, driver, limit):
        """Scroll halaman untuk memuat lebih banyak produk"""
        print("📜 Scrolling page to load more products...")
        last_height = driver.execute_script("return document.body.scrollHeight")
        products_loaded = 0
        max_scrolls = 8
        scroll_pause_time = random.uniform(2, 4)
        
        for i in range(max_scrolls):
            # Scroll down
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(scroll_pause_time)
            
            # Random pause
            if i % 2 == 0:
                time.sleep(random.uniform(1, 2))
            
            # Count loaded products
            try:
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
                    print(f"✅ Found {products_loaded} products, stopping scroll")
                    break
                    
            except:
                pass
            
            # Check if page height changed
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                time.sleep(2)
                new_height = driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    print("📄 Reached end of page")
                    break
            last_height = new_height
    
    def extract_products(self, driver, limit):
        """Extract data produk dari halaman"""
        products = []
        
        try:
            print("🔍 Extracting product data...")
            
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
                    WebDriverWait(driver, 15).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                    )
                    product_elements = driver.find_elements(By.CSS_SELECTOR, selector)[:limit]
                    if product_elements:
                        print(f"✅ Found {len(product_elements)} product elements with selector: {selector}")
                        break
                except:
                    continue
            
            if not product_elements:
                print("❌ No product elements found")
                return products
            
            for i, element in enumerate(product_elements):
                try:
                    # Extract product name
                    name_selectors = [
                        '[data-sqe="name"]',
                        '.ie3A\\+n',
                        '.Cve6sh',
                        'a[data-sqe="link"]',
                        '.shopee-item-card__text-name',
                        'a[href*="/product/"]'
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
                        '.shopee-item-card__text-price',
                        '.shopee-item-card__text-price-current'
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
                        '.shopee-item-card__rating',
                        '.shopee-rating-stars'
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
                        '.shopee-item-card__sold',
                        '.shopee-item-card__text-sold'
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
                        '.shopee-item-card__shop-name',
                        '.shopee-item-card__shop'
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
                        '.shopee-item-card__shop-location',
                        '.shopee-item-card__location'
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
                        'diskon': 'N/A'
                    })
                    
                    print(f"✅ Extracted product {i+1}: {product_name[:50]}...")
                    
                except Exception as e:
                    print(f"⚠️ Error extracting product {i+1}: {str(e)}")
                    continue
                    
        except Exception as e:
            print(f"❌ Error extracting products: {str(e)}")
        
        return products
    
    def save_to_csv(self, products, filename=None):
        """Save data ke CSV file"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"shopee_products_{timestamp}.csv"
        
        df = pd.DataFrame(products)
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        print(f"💾 Data saved to {filename}")
        return filename
    
    def display_results(self, products):
        """Display hasil scraping"""
        if not products:
            print("❌ No products found!")
            return
        
        print(f"\n{'='*100}")
        print(f"📋 SCRAPING RESULTS - {len(products)} PRODUCTS")
        print(f"{'='*100}")
        
        for i, product in enumerate(products, 1):
            print(f"\n{i}. {product['nama_produk']}")
            print(f"   💰 Harga: {product['harga']}")
            print(f"   ⭐ Rating: {product['rating']}")
            print(f"   📦 Terjual: {product['jumlah_terjual']}")
            print(f"   🏪 Toko: {product['nama_toko']}")
            print(f"   📍 Lokasi: {product['lokasi_toko']}")
            print("-" * 80)

print("✅ Simple Shopee Scraper class loaded successfully!")

# CELL 4: Test Scraper
# ====================
# Test scraper dengan keyword sederhana
scraper = SimpleShopeeScraper()

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
limit = int(input("📊 Jumlah data (max 50): "))

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
    
    time.sleep(3)  # Delay between keywords

if all_products:
    print(f"\n🎉 Total semua produk: {len(all_products)}")
    
    # Save all products
    filename = scraper.save_to_csv(all_products, "shopee_all_products.csv")
    print(f"💾 Semua data tersimpan di: {filename}")
    
    # Download file
    files.download(filename)
else:
    print("❌ Tidak ada data yang berhasil di-scrape")