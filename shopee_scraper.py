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
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import re
from urllib.parse import quote
import warnings
warnings.filterwarnings('ignore')

class ShopeeScraper:
    def __init__(self):
        self.session = requests.Session()
        self.setup_session()
        self.driver = None
        
    def setup_session(self):
        """Setup session dengan headers yang realistic"""
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
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
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--disable-plugins')
        chrome_options.add_argument('--disable-images')
        chrome_options.add_argument('--disable-javascript')
        chrome_options.add_argument('--headless')
        
        # Random window size
        width = random.randint(1200, 1920)
        height = random.randint(800, 1080)
        chrome_options.add_argument(f'--window-size={width},{height}')
        
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
    def random_delay(self, min_delay=1, max_delay=3):
        """Random delay untuk menghindari detection"""
        delay = random.uniform(min_delay, max_delay)
        time.sleep(delay)
        
    def get_search_url(self, keyword):
        """Generate search URL dari keyword"""
        encoded_keyword = quote(keyword)
        return f"https://shopee.co.id/search?keyword={encoded_keyword}"
        
    def extract_product_data(self, product_element):
        """Extract data dari product element"""
        try:
            # Nama produk
            name_element = product_element.find('div', {'data-sqe': 'name'})
            product_name = name_element.get_text(strip=True) if name_element else "N/A"
            
            # Harga
            price_element = product_element.find('div', {'data-sqe': 'price'})
            if price_element:
                price_text = price_element.get_text(strip=True)
                # Clean price text
                price = re.sub(r'[^\d]', '', price_text)
            else:
                price = "N/A"
                
            # Rating
            rating_element = product_element.find('div', {'data-sqe': 'rating'})
            rating = rating_element.get_text(strip=True) if rating_element else "N/A"
            
            # Jumlah terjual
            sold_element = product_element.find('div', {'data-sqe': 'sold'})
            sold = sold_element.get_text(strip=True) if sold_element else "N/A"
            
            # Nama toko
            shop_element = product_element.find('div', {'data-sqe': 'shop'})
            shop_name = shop_element.get_text(strip=True) if shop_element else "N/A"
            
            # Lokasi toko
            location_element = product_element.find('div', {'data-sqe': 'location'})
            location = location_element.get_text(strip=True) if location_element else "N/A"
            
            return {
                'Nama Produk': product_name,
                'Harga': price,
                'Rating': rating,
                'Jumlah Terjual': sold,
                'Nama Toko': shop_name,
                'Lokasi Toko': location
            }
            
        except Exception as e:
            print(f"Error extracting product data: {e}")
            return None
            
    def scrape_shopee(self, keyword, max_products=50):
        """Main scraping function"""
        print(f"Memulai scraping untuk keyword: {keyword}")
        print(f"Target jumlah produk: {max_products}")
        
        try:
            self.setup_driver()
            search_url = self.get_search_url(keyword)
            
            print(f"Mengakses URL: {search_url}")
            self.driver.get(search_url)
            self.random_delay(2, 4)
            
            # Wait for page to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-sqe='link']"))
            )
            
            products_data = []
            page = 1
            
            while len(products_data) < max_products:
                print(f"Scraping halaman {page}...")
                
                # Scroll untuk load lebih banyak produk
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                self.random_delay(2, 3)
                
                # Get page source dan parse
                soup = BeautifulSoup(self.driver.page_source, 'html.parser')
                product_elements = soup.find_all('div', {'data-sqe': 'link'})
                
                if not product_elements:
                    print("Tidak ada produk ditemukan pada halaman ini")
                    break
                    
                for element in product_elements:
                    if len(products_data) >= max_products:
                        break
                        
                    product_data = self.extract_product_data(element)
                    if product_data:
                        products_data.append(product_data)
                        print(f"Berhasil scrape produk {len(products_data)}: {product_data['Nama Produk'][:50]}...")
                        
                # Check if there's next page
                try:
                    next_button = self.driver.find_element(By.CSS_SELECTOR, "button[aria-label='Next page']")
                    if not next_button.is_enabled():
                        print("Tidak ada halaman selanjutnya")
                        break
                    next_button.click()
                    self.random_delay(2, 4)
                    page += 1
                except NoSuchElementException:
                    print("Tidak ada tombol next page")
                    break
                    
            print(f"Scraping selesai! Total produk yang berhasil di-scrape: {len(products_data)}")
            return products_data
            
        except Exception as e:
            print(f"Error during scraping: {e}")
            return []
            
        finally:
            if self.driver:
                self.driver.quit()
                
    def save_to_csv(self, data, filename):
        """Save data ke CSV"""
        df = pd.DataFrame(data)
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        print(f"Data berhasil disimpan ke {filename}")
        
    def save_to_excel(self, data, filename):
        """Save data ke Excel"""
        df = pd.DataFrame(data)
        df.to_excel(filename, index=False)
        print(f"Data berhasil disimpan ke {filename}")

def main():
    """Main function untuk user interface"""
    print("=" * 60)
    print("SHOPEE PRODUCT SCRAPER")
    print("Dibuat oleh: Dosen Data Mining dengan 30 tahun pengalaman")
    print("=" * 60)
    
    # Input dari user
    keyword = input("Masukkan keyword produk yang ingin di-scrape: ").strip()
    
    while True:
        try:
            max_products = int(input("Masukkan jumlah data yang ingin didapatkan: "))
            if max_products > 0:
                break
            else:
                print("Jumlah data harus lebih dari 0!")
        except ValueError:
            print("Masukkan angka yang valid!")
    
    # Inisialisasi scraper
    scraper = ShopeeScraper()
    
    # Mulai scraping
    print("\nMemulai proses scraping...")
    print("Mohon tunggu, proses ini memakan waktu beberapa menit...")
    
    products_data = scraper.scrape_shopee(keyword, max_products)
    
    if products_data:
        # Save data
        filename_base = f"shopee_{keyword.replace(' ', '_')}_{len(products_data)}_products"
        
        # Save ke CSV
        csv_filename = f"{filename_base}.csv"
        scraper.save_to_csv(products_data, csv_filename)
        
        # Save ke Excel
        excel_filename = f"{filename_base}.xlsx"
        scraper.save_to_excel(products_data, excel_filename)
        
        # Display sample data
        print("\n" + "=" * 60)
        print("SAMPLE DATA YANG BERHASIL DI-SCRAPE:")
        print("=" * 60)
        
        df = pd.DataFrame(products_data)
        print(df.head(10).to_string(index=False))
        
        print(f"\nTotal data berhasil di-scrape: {len(products_data)}")
        print(f"File CSV: {csv_filename}")
        print(f"File Excel: {excel_filename}")
        
    else:
        print("Tidak ada data yang berhasil di-scrape. Silakan coba lagi.")

if __name__ == "__main__":
    main()