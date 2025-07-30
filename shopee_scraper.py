import requests
import json
import time
import random
import pandas as pd
from urllib.parse import quote
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import undetected_chromedriver as uc
from fake_useragent import UserAgent
import re

class ShopeeScraper:
    def __init__(self):
        self.ua = UserAgent()
        self.session = requests.Session()
        self.setup_session()
        
    def setup_session(self):
        """Setup session dengan headers yang menyerupai browser asli"""
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
    
    def setup_driver(self):
        """Setup Chrome driver dengan anti-detection"""
        options = uc.ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument(f'--user-agent={self.ua.random}')
        
        # Tambahan untuk menghindari deteksi
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-plugins')
        options.add_argument('--disable-images')
        options.add_argument('--disable-javascript')
        options.add_argument('--disable-web-security')
        options.add_argument('--allow-running-insecure-content')
        
        driver = uc.Chrome(options=options)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        return driver
    
    def get_shopee_api_data(self, keyword, limit=50):
        """Menggunakan Shopee API untuk mendapatkan data produk"""
        try:
            # URL API Shopee
            search_url = f"https://shopee.co.id/api/v4/search/search_items"
            
            params = {
                'keyword': keyword,
                'limit': min(limit, 100),  # Shopee limit per request
                'newest': 0,
                'order': 'desc',
                'page_type': 'search',
                'scenario': 'PAGE_GLOBAL_SEARCH',
                'version': 2
            }
            
            headers = {
                'User-Agent': self.ua.random,
                'Accept': 'application/json',
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
                'Referer': f'https://shopee.co.id/search?keyword={quote(keyword)}',
                'X-Requested-With': 'XMLHttpRequest'
            }
            
            response = self.session.get(search_url, params=params, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                return self.parse_api_response(data, limit)
            else:
                print(f"API request failed with status code: {response.status_code}")
                return self.fallback_scraping(keyword, limit)
                
        except Exception as e:
            print(f"API method failed: {str(e)}")
            return self.fallback_scraping(keyword, limit)
    
    def parse_api_response(self, data, limit):
        """Parse response dari Shopee API"""
        products = []
        
        if 'items' in data:
            for item in data['items'][:limit]:
                try:
                    product_info = item.get('item_basic', {})
                    shop_info = item.get('shop_basic', {})
                    
                    # Extract product data
                    product_name = product_info.get('name', 'N/A')
                    price = product_info.get('price', 0) / 100000  # Convert from centavos
                    rating = product_info.get('item_rating', {}).get('rating_star', 0)
                    sold = product_info.get('historical_sold', 0)
                    shop_name = shop_info.get('name', 'N/A')
                    shop_location = shop_info.get('shop_location', 'N/A')
                    
                    products.append({
                        'nama_produk': product_name,
                        'harga': f"Rp {price:,.0f}",
                        'rating': f"{rating:.1f}",
                        'jumlah_terjual': sold,
                        'nama_toko': shop_name,
                        'lokasi_toko': shop_location
                    })
                    
                except Exception as e:
                    print(f"Error parsing product: {str(e)}")
                    continue
        
        return products
    
    def fallback_scraping(self, keyword, limit):
        """Fallback method menggunakan Selenium jika API gagal"""
        print("Using fallback Selenium method...")
        driver = None
        try:
            driver = self.setup_driver()
            
            # Navigate to search page
            search_url = f"https://shopee.co.id/search?keyword={quote(keyword)}"
            driver.get(search_url)
            
            # Wait for page to load
            time.sleep(random.uniform(3, 5))
            
            # Scroll to load more products
            self.scroll_page(driver, limit)
            
            # Extract product data
            products = self.extract_products_from_page(driver, limit)
            
            return products
            
        except Exception as e:
            print(f"Fallback scraping failed: {str(e)}")
            return []
        finally:
            if driver:
                driver.quit()
    
    def scroll_page(self, driver, limit):
        """Scroll halaman untuk memuat lebih banyak produk"""
        last_height = driver.execute_script("return document.body.scrollHeight")
        
        products_loaded = 0
        max_scrolls = 10
        
        for _ in range(max_scrolls):
            # Scroll down
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(random.uniform(2, 4))
            
            # Count loaded products
            try:
                products = driver.find_elements(By.CSS_SELECTOR, '[data-sqe="item"]')
                products_loaded = len(products)
                
                if products_loaded >= limit:
                    break
                    
            except:
                pass
            
            # Check if page height changed
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
    
    def extract_products_from_page(self, driver, limit):
        """Extract data produk dari halaman HTML"""
        products = []
        
        try:
            # Wait for products to load
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '[data-sqe="item"]'))
            )
            
            # Find all product elements
            product_elements = driver.find_elements(By.CSS_SELECTOR, '[data-sqe="item"]')[:limit]
            
            for element in product_elements:
                try:
                    # Extract product name
                    try:
                        name_element = element.find_element(By.CSS_SELECTOR, '[data-sqe="name"]')
                        product_name = name_element.text.strip()
                    except:
                        product_name = "N/A"
                    
                    # Extract price
                    try:
                        price_element = element.find_element(By.CSS_SELECTOR, '[data-sqe="price"]')
                        price_text = price_element.text.strip()
                        price = price_text.replace('Rp', '').replace('.', '').strip()
                    except:
                        price = "N/A"
                    
                    # Extract rating
                    try:
                        rating_element = element.find_element(By.CSS_SELECTOR, '[data-sqe="rating"]')
                        rating = rating_element.text.strip()
                    except:
                        rating = "N/A"
                    
                    # Extract sold count
                    try:
                        sold_element = element.find_element(By.CSS_SELECTOR, '[data-sqe="sold"]')
                        sold_text = sold_element.text.strip()
                        sold = re.findall(r'\d+', sold_text)
                        sold = sold[0] if sold else "0"
                    except:
                        sold = "0"
                    
                    # Extract shop name
                    try:
                        shop_element = element.find_element(By.CSS_SELECTOR, '[data-sqe="shop"]')
                        shop_name = shop_element.text.strip()
                    except:
                        shop_name = "N/A"
                    
                    # Extract shop location
                    try:
                        location_element = element.find_element(By.CSS_SELECTOR, '[data-sqe="location"]')
                        shop_location = location_element.text.strip()
                    except:
                        shop_location = "N/A"
                    
                    products.append({
                        'nama_produk': product_name,
                        'harga': f"Rp {price}" if price != "N/A" else "N/A",
                        'rating': rating,
                        'jumlah_terjual': sold,
                        'nama_toko': shop_name,
                        'lokasi_toko': shop_location
                    })
                    
                except Exception as e:
                    print(f"Error extracting product data: {str(e)}")
                    continue
                    
        except TimeoutException:
            print("Timeout waiting for products to load")
        except Exception as e:
            print(f"Error extracting products: {str(e)}")
        
        return products
    
    def scrape_products(self, keyword, limit=50):
        """Main method untuk scraping produk"""
        print(f"Starting to scrape products for keyword: '{keyword}'")
        print(f"Target: {limit} products")
        
        # Try API method first
        products = self.get_shopee_api_data(keyword, limit)
        
        if not products:
            print("API method failed, trying fallback method...")
            products = self.fallback_scraping(keyword, limit)
        
        print(f"Successfully scraped {len(products)} products")
        return products
    
    def save_to_csv(self, products, filename=None):
        """Save data ke CSV file"""
        if not filename:
            filename = f"shopee_products_{int(time.time())}.csv"
        
        df = pd.DataFrame(products)
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        print(f"Data saved to {filename}")
        return filename
    
    def display_results(self, products):
        """Display hasil scraping"""
        if not products:
            print("No products found!")
            return
        
        print(f"\n{'='*80}")
        print(f"SCRAPING RESULTS - {len(products)} PRODUCTS")
        print(f"{'='*80}")
        
        for i, product in enumerate(products, 1):
            print(f"\n{i}. {product['nama_produk']}")
            print(f"   Harga: {product['harga']}")
            print(f"   Rating: {product['rating']}")
            print(f"   Terjual: {product['jumlah_terjual']}")
            print(f"   Toko: {product['nama_toko']}")
            print(f"   Lokasi: {product['lokasi_toko']}")
            print("-" * 60)

def main():
    """Main function untuk menjalankan scraper"""
    print("="*80)
    print("SHOPEE PRODUCT SCRAPER")
    print("="*80)
    
    # Get user input
    keyword = input("Masukkan keyword produk yang ingin di-scrape: ").strip()
    
    while True:
        try:
            limit = int(input("Masukkan jumlah data yang ingin didapatkan (max 100): "))
            if 1 <= limit <= 100:
                break
            else:
                print("Jumlah data harus antara 1-100!")
        except ValueError:
            print("Masukkan angka yang valid!")
    
    # Initialize scraper
    scraper = ShopeeScraper()
    
    # Start scraping
    print(f"\nMemulai scraping untuk keyword: '{keyword}'")
    print("Mohon tunggu...")
    
    products = scraper.scrape_products(keyword, limit)
    
    if products:
        # Display results
        scraper.display_results(products)
        
        # Save to CSV
        filename = scraper.save_to_csv(products)
        
        print(f"\nScraping selesai! Data tersimpan di: {filename}")
    else:
        print("Tidak ada data yang berhasil di-scrape!")

if __name__ == "__main__":
    main()