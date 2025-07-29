import requests
import time
import random
import json
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from fake_useragent import UserAgent
import re
from urllib.parse import quote, urlencode
import warnings
from datetime import datetime
warnings.filterwarnings('ignore')

class AdvancedShopeeScraper:
    def __init__(self):
        self.ua = UserAgent()
        self.session = requests.Session()
        self.base_url = "https://shopee.co.id"
        self.api_url = "https://shopee.co.id/api/v4/search/search_items"
        self.setup_session()
        
    def setup_session(self):
        """Setup session dengan headers yang realistic"""
        headers = {
            'User-Agent': self.ua.random,
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9,id;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Referer': 'https://shopee.co.id/',
            'Origin': 'https://shopee.co.id',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'X-Requested-With': 'XMLHttpRequest'
        }
        self.session.headers.update(headers)
    
    def get_shopee_cookies(self):
        """Get cookies dari Shopee"""
        try:
            response = self.session.get(self.base_url)
            return self.session.cookies
        except Exception as e:
            print(f"Error getting cookies: {e}")
            return None
    
    def search_products_api(self, keyword, limit=50, offset=0):
        """Search produk menggunakan API Shopee"""
        try:
            cookies = self.get_shopee_cookies()
            if not cookies:
                return []
            
            # Parameters untuk API
            params = {
                'keyword': keyword,
                'limit': limit,
                'offset': offset,
                'page_type': 'search',
                'scenario': 'PAGE_GLOBAL_SEARCH',
                'version': '2'
            }
            
            # Headers untuk API request
            api_headers = {
                'User-Agent': self.ua.random,
                'Accept': 'application/json, text/plain, */*',
                'Accept-Language': 'en-US,en;q=0.9,id;q=0.8',
                'Referer': f'{self.base_url}/search?keyword={quote(keyword)}',
                'X-Requested-With': 'XMLHttpRequest'
            }
            
            response = self.session.get(
                self.api_url,
                params=params,
                headers=api_headers,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                if 'items' in data:
                    return data['items']
            
            return []
            
        except Exception as e:
            print(f"Error in API search: {e}")
            return []
    
    def extract_product_data_api(self, item):
        """Extract data dari API response"""
        try:
            data = {}
            
            # Basic product info
            data['nama_produk'] = item.get('item_basic', {}).get('name', 'N/A')
            data['harga'] = item.get('item_basic', {}).get('price', 0) // 100000  # Convert from centavos
            data['rating'] = item.get('item_basic', {}).get('item_rating', {}).get('rating_star', 'N/A')
            data['jumlah_terjual'] = item.get('item_basic', {}).get('historical_sold', 'N/A')
            
            # Shop info
            shop_info = item.get('shop_basic', {})
            data['nama_toko'] = shop_info.get('name', 'N/A')
            data['lokasi_toko'] = shop_info.get('location', 'N/A')
            
            # Additional info
            data['kategori'] = item.get('item_basic', {}).get('categories', [{}])[0].get('display_name', 'N/A')
            data['brand'] = item.get('item_basic', {}).get('brand', 'N/A')
            data['discount'] = item.get('item_basic', {}).get('discount', 'N/A')
            
            return data
            
        except Exception as e:
            print(f"Error extracting API data: {e}")
            return None
    
    def setup_driver(self):
        """Setup Chrome driver dengan anti-detection"""
        chrome_options = Options()
        
        # Anti-detection settings
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument(f'--user-agent={self.ua.random}')
        
        # Additional stealth settings
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--disable-plugins')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-web-security')
        chrome_options.add_argument('--allow-running-insecure-content')
        
        # Window size
        chrome_options.add_argument('--window-size=1920,1080')
        
        # Headless mode (optional)
        # chrome_options.add_argument('--headless')
        
        driver = webdriver.Chrome(options=chrome_options)
        
        # Execute script to remove webdriver property
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        return driver
    
    def scrape_web_fallback(self, keyword, max_products=50):
        """Fallback scraping menggunakan web browser"""
        print("Menggunakan fallback web scraping...")
        
        driver = None
        products_data = []
        
        try:
            driver = self.setup_driver()
            
            # Buka halaman search
            encoded_keyword = quote(keyword)
            url = f"{self.base_url}/search?keyword={encoded_keyword}"
            driver.get(url)
            
            # Tunggu halaman load
            time.sleep(5)
            
            # Scroll untuk load lebih banyak produk
            self.scroll_page(driver)
            
            # Extract produk elements
            product_elements = driver.find_elements(By.CSS_SELECTOR, '[data-sqe="link"]')
            
            if not product_elements:
                product_elements = driver.find_elements(By.CSS_SELECTOR, '.col-xs-2-4')
            
            for i, element in enumerate(product_elements[:max_products]):
                try:
                    product_data = self.extract_product_data_web(element)
                    if product_data:
                        products_data.append(product_data)
                except Exception as e:
                    print(f"Error extracting web data: {e}")
                    continue
            
        except Exception as e:
            print(f"Error in web scraping: {e}")
        
        finally:
            if driver:
                driver.quit()
        
        return products_data
    
    def extract_product_data_web(self, element):
        """Extract data dari web element"""
        try:
            data = {}
            
            # Nama produk
            try:
                name_element = element.find_element(By.CSS_SELECTOR, '[data-sqe="link"]')
                data['nama_produk'] = name_element.get_attribute('title') or name_element.text
            except:
                data['nama_produk'] = 'N/A'
            
            # Harga
            try:
                price_element = element.find_element(By.CSS_SELECTOR, '.vioxXd')
                price_text = price_element.text
                price_clean = re.sub(r'[^\d]', '', price_text)
                data['harga'] = price_clean if price_clean else 'N/A'
            except:
                data['harga'] = 'N/A'
            
            # Rating
            try:
                rating_element = element.find_element(By.CSS_SELECTOR, '.shopee-rating-stars__stars')
                rating_style = rating_element.get_attribute('style')
                rating_match = re.search(r'width:\s*(\d+(?:\.\d+)?)%', rating_style)
                if rating_match:
                    rating_percent = float(rating_match.group(1))
                    data['rating'] = round(rating_percent / 20, 1)
                else:
                    data['rating'] = 'N/A'
            except:
                data['rating'] = 'N/A'
            
            # Jumlah terjual
            try:
                sold_element = element.find_element(By.CSS_SELECTOR, '.r6HknA')
                sold_text = sold_element.text
                sold_match = re.search(r'(\d+(?:\.\d+)?)', sold_text)
                if sold_match:
                    data['jumlah_terjual'] = sold_match.group(1)
                else:
                    data['jumlah_terjual'] = 'N/A'
            except:
                data['jumlah_terjual'] = 'N/A'
            
            # Nama toko
            try:
                shop_element = element.find_element(By.CSS_SELECTOR, '.Cve6sh')
                data['nama_toko'] = shop_element.text
            except:
                data['nama_toko'] = 'N/A'
            
            # Lokasi toko
            try:
                location_element = element.find_element(By.CSS_SELECTOR, '.zGGwiV')
                data['lokasi_toko'] = location_element.text
            except:
                data['lokasi_toko'] = 'N/A'
            
            return data
            
        except Exception as e:
            print(f"Error extracting web data: {e}")
            return None
    
    def scroll_page(self, driver, scroll_pause_time=2):
        """Scroll halaman secara natural"""
        last_height = driver.execute_script("return document.body.scrollHeight")
        
        for _ in range(3):  # Scroll 3 times
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(scroll_pause_time)
            
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
    
    def scrape_shopee(self, keyword, max_products=50):
        """Main scraping function dengan API dan fallback"""
        print(f"Memulai scraping untuk keyword: {keyword}")
        print(f"Target jumlah produk: {max_products}")
        
        products_data = []
        
        # Try API first
        print("Mencoba menggunakan API Shopee...")
        api_items = self.search_products_api(keyword, max_products)
        
        if api_items:
            print(f"Berhasil mendapatkan {len(api_items)} produk dari API")
            for item in api_items:
                product_data = self.extract_product_data_api(item)
                if product_data:
                    products_data.append(product_data)
        
        # If API fails or insufficient data, use web scraping
        if len(products_data) < max_products:
            print(f"API hanya memberikan {len(products_data)} produk, menggunakan web scraping...")
            web_products = self.scrape_web_fallback(keyword, max_products - len(products_data))
            products_data.extend(web_products)
        
        print(f"Total produk berhasil di-scrape: {len(products_data)}")
        return products_data
    
    def save_to_csv(self, data, keyword):
        """Save data ke CSV"""
        if data:
            df = pd.DataFrame(data)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"shopee_{keyword.replace(' ', '_')}_{timestamp}.csv"
            df.to_csv(filename, index=False, encoding='utf-8-sig')
            print(f"Data berhasil disimpan ke {filename}")
            return df, filename
        else:
            print("Tidak ada data untuk disimpan")
            return None, None
    
    def display_results(self, data):
        """Display hasil scraping"""
        if data:
            df = pd.DataFrame(data)
            print("\n=== HASIL SCRAPING ===")
            print(f"Total produk: {len(data)}")
            print("\nSample data:")
            print(df.head(10))
            
            # Summary statistics
            print("\n=== STATISTIK ===")
            if 'harga' in df.columns:
                try:
                    price_df = df[df['harga'] != 'N/A'].copy()
                    if not price_df.empty:
                        price_df['harga'] = pd.to_numeric(price_df['harga'], errors='coerce')
                        print(f"Rata-rata harga: Rp {price_df['harga'].mean():,.0f}")
                        print(f"Harga tertinggi: Rp {price_df['harga'].max():,.0f}")
                        print(f"Harga terendah: Rp {price_df['harga'].min():,.0f}")
                except:
                    pass
            
            return df
        else:
            print("Tidak ada data yang berhasil di-scrape")
            return None

def main():
    """Main function untuk menjalankan scraper"""
    print("=== ADVANCED SHOPEE SCRAPER ===")
    print("Scraper canggih untuk mengambil data produk dari Shopee")
    print("Menggunakan kombinasi API dan web scraping")
    print("=" * 60)
    
    # Input dari user
    keyword = input("Masukkan keyword produk yang ingin di-scrape: ")
    
    while True:
        try:
            max_products = int(input("Masukkan jumlah maksimal produk yang ingin di-scrape (1-100): "))
            if 1 <= max_products <= 100:
                break
            else:
                print("Jumlah produk harus antara 1-100")
        except ValueError:
            print("Masukkan angka yang valid")
    
    # Inisialisasi scraper
    scraper = AdvancedShopeeScraper()
    
    # Jalankan scraping
    print(f"\nMemulai proses scraping untuk '{keyword}'...")
    start_time = time.time()
    
    products_data = scraper.scrape_shopee(keyword, max_products)
    
    end_time = time.time()
    duration = end_time - start_time
    
    # Display dan save results
    if products_data:
        df = scraper.display_results(products_data)
        df, filename = scraper.save_to_csv(products_data, keyword)
        
        print(f"\n=== SCRAPING SELESAI ===")
        print(f"Waktu eksekusi: {duration:.2f} detik")
        print(f"Total produk berhasil di-scrape: {len(products_data)}")
        print(f"Data tersimpan dalam file: {filename}")
        
        # Show file location
        import os
        print(f"Lokasi file: {os.path.abspath(filename)}")
        
    else:
        print("Gagal mendapatkan data produk")

if __name__ == "__main__":
    main()