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
from urllib.parse import quote
import warnings
warnings.filterwarnings('ignore')

class ShopeeScraper:
    def __init__(self):
        self.ua = UserAgent()
        self.session = requests.Session()
        self.setup_session()
        
    def setup_session(self):
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
        chrome_options.add_argument('--disable-images')
        chrome_options.add_argument('--disable-javascript')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-web-security')
        chrome_options.add_argument('--allow-running-insecure-content')
        
        # Window size
        chrome_options.add_argument('--window-size=1920,1080')
        
        driver = webdriver.Chrome(options=chrome_options)
        
        # Execute script to remove webdriver property
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        return driver
    
    def random_delay(self, min_delay=1, max_delay=3):
        """Random delay untuk menghindari deteksi"""
        delay = random.uniform(min_delay, max_delay)
        time.sleep(delay)
    
    def scroll_page(self, driver, scroll_pause_time=2):
        """Scroll halaman secara natural"""
        last_height = driver.execute_script("return document.body.scrollHeight")
        
        while True:
            # Scroll down
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            self.random_delay(scroll_pause_time, scroll_pause_time + 1)
            
            # Calculate new scroll height
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
    
    def extract_product_data(self, product_element):
        """Extract data dari element produk"""
        try:
            data = {}
            
            # Nama produk
            try:
                name_element = product_element.find_element(By.CSS_SELECTOR, '[data-sqe="link"]')
                data['nama_produk'] = name_element.get_attribute('title') or name_element.text
            except:
                try:
                    name_element = product_element.find_element(By.CSS_SELECTOR, '.ie3A\+n')
                    data['nama_produk'] = name_element.text
                except:
                    data['nama_produk'] = 'N/A'
            
            # Harga
            try:
                price_element = product_element.find_element(By.CSS_SELECTOR, '.vioxXd')
                price_text = price_element.text
                # Clean price text
                price_clean = re.sub(r'[^\d]', '', price_text)
                data['harga'] = price_clean if price_clean else 'N/A'
            except:
                data['harga'] = 'N/A'
            
            # Rating
            try:
                rating_element = product_element.find_element(By.CSS_SELECTOR, '.shopee-rating-stars__stars')
                rating_style = rating_element.get_attribute('style')
                # Extract rating from style attribute
                rating_match = re.search(r'width:\s*(\d+(?:\.\d+)?)%', rating_style)
                if rating_match:
                    rating_percent = float(rating_match.group(1))
                    data['rating'] = round(rating_percent / 20, 1)  # Convert to 5-star scale
                else:
                    data['rating'] = 'N/A'
            except:
                data['rating'] = 'N/A'
            
            # Jumlah terjual
            try:
                sold_element = product_element.find_element(By.CSS_SELECTOR, '.r6HknA')
                sold_text = sold_element.text
                # Extract number from text like "Terjual 1rb+"
                sold_match = re.search(r'(\d+(?:\.\d+)?)', sold_text)
                if sold_match:
                    data['jumlah_terjual'] = sold_match.group(1)
                else:
                    data['jumlah_terjual'] = 'N/A'
            except:
                data['jumlah_terjual'] = 'N/A'
            
            # Nama toko
            try:
                shop_element = product_element.find_element(By.CSS_SELECTOR, '.Cve6sh')
                data['nama_toko'] = shop_element.text
            except:
                data['nama_toko'] = 'N/A'
            
            # Lokasi toko
            try:
                location_element = product_element.find_element(By.CSS_SELECTOR, '.zGGwiV')
                data['lokasi_toko'] = location_element.text
            except:
                data['lokasi_toko'] = 'N/A'
            
            return data
            
        except Exception as e:
            print(f"Error extracting product data: {e}")
            return None
    
    def scrape_shopee(self, keyword, max_products=50):
        """Main scraping function"""
        print(f"Memulai scraping untuk keyword: {keyword}")
        print(f"Target jumlah produk: {max_products}")
        
        # Encode keyword untuk URL
        encoded_keyword = quote(keyword)
        url = f"https://shopee.co.id/search?keyword={encoded_keyword}"
        
        driver = None
        products_data = []
        
        try:
            driver = self.setup_driver()
            print("Browser berhasil dibuka")
            
            # Buka halaman
            driver.get(url)
            print(f"Membuka URL: {url}")
            
            # Tunggu halaman load
            self.random_delay(3, 5)
            
            # Scroll halaman untuk load lebih banyak produk
            print("Scrolling halaman...")
            self.scroll_page(driver)
            
            # Tunggu produk muncul
            wait = WebDriverWait(driver, 10)
            try:
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '[data-sqe="link"]')))
            except TimeoutException:
                print("Timeout menunggu produk muncul")
            
            # Extract produk
            print("Mengekstrak data produk...")
            product_elements = driver.find_elements(By.CSS_SELECTOR, '[data-sqe="link"]')
            
            if not product_elements:
                # Try alternative selector
                product_elements = driver.find_elements(By.CSS_SELECTOR, '.col-xs-2-4')
            
            print(f"Ditemukan {len(product_elements)} produk")
            
            for i, element in enumerate(product_elements):
                if len(products_data) >= max_products:
                    break
                
                try:
                    # Scroll ke element
                    driver.execute_script("arguments[0].scrollIntoView(true);", element)
                    self.random_delay(0.5, 1)
                    
                    # Extract data
                    product_data = self.extract_product_data(element)
                    if product_data:
                        products_data.append(product_data)
                        print(f"Berhasil extract produk {len(products_data)}: {product_data['nama_produk'][:50]}...")
                    
                except Exception as e:
                    print(f"Error pada produk {i}: {e}")
                    continue
            
            print(f"Berhasil mengekstrak {len(products_data)} produk")
            
        except Exception as e:
            print(f"Error dalam scraping: {e}")
        
        finally:
            if driver:
                driver.quit()
                print("Browser ditutup")
        
        return products_data
    
    def save_to_csv(self, data, filename="shopee_data.csv"):
        """Save data ke CSV"""
        if data:
            df = pd.DataFrame(data)
            df.to_csv(filename, index=False, encoding='utf-8-sig')
            print(f"Data berhasil disimpan ke {filename}")
            return df
        else:
            print("Tidak ada data untuk disimpan")
            return None
    
    def display_results(self, data):
        """Display hasil scraping"""
        if data:
            df = pd.DataFrame(data)
            print("\n=== HASIL SCRAPING ===")
            print(f"Total produk: {len(data)}")
            print("\nSample data:")
            print(df.head())
            return df
        else:
            print("Tidak ada data yang berhasil di-scrape")
            return None

def main():
    """Main function untuk menjalankan scraper"""
    print("=== SHOPEE SCRAPER ===")
    print("Scraper untuk mengambil data produk dari Shopee")
    print("=" * 50)
    
    # Input dari user
    keyword = input("Masukkan keyword produk yang ingin di-scrape: ")
    max_products = int(input("Masukkan jumlah maksimal produk yang ingin di-scrape: "))
    
    # Inisialisasi scraper
    scraper = ShopeeScraper()
    
    # Jalankan scraping
    print("\nMemulai proses scraping...")
    products_data = scraper.scrape_shopee(keyword, max_products)
    
    # Display dan save results
    if products_data:
        df = scraper.display_results(products_data)
        scraper.save_to_csv(products_data, f"shopee_{keyword.replace(' ', '_')}.csv")
        
        print(f"\nScraping selesai! Data tersimpan dalam file CSV.")
        print(f"Total produk berhasil di-scrape: {len(products_data)}")
    else:
        print("Gagal mendapatkan data produk")

if __name__ == "__main__":
    main()