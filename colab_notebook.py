# ============================================================================
# SHOPEE SCRAPER UNTUK GOOGLE COLAB
# ============================================================================
# Copy-paste kode ini ke Google Colab untuk menjalankan scraper
# ============================================================================

# CELL 1: Setup Environment
"""
# Install dependencies
!pip install selenium pandas requests fake-useragent webdriver-manager beautifulsoup4 lxml

# Install Chrome dan ChromeDriver
!apt-get update
!apt-get install -y wget unzip
!wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add -
!echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list
!apt-get update
!apt-get install -y google-chrome-stable

!wget -N https://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_linux64.zip
!unzip -o chromedriver_linux64.zip
!chmod +x chromedriver
!mv chromedriver /usr/local/bin/

print("✅ Setup selesai! Semua dependencies terinstall.")
"""

# CELL 2: Import Libraries dan Scraper Class
"""
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
from datetime import datetime
warnings.filterwarnings('ignore')

class ShopeeColabScraper:
    def __init__(self):
        self.ua = UserAgent()
        self.base_url = "https://shopee.co.id"
        
    def setup_driver_colab(self):
        chrome_options = Options()
        
        # Settings untuk Colab
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--disable-plugins')
        chrome_options.add_argument('--disable-images')
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument(f'--user-agent={self.ua.random}')
        
        # Anti-detection
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        try:
            driver = webdriver.Chrome(options=chrome_options)
            driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            return driver
        except Exception as e:
            print(f"Error setting up driver: {e}")
            return None
    
    def random_delay(self, min_delay=1, max_delay=3):
        delay = random.uniform(min_delay, max_delay)
        time.sleep(delay)
    
    def scroll_page_colab(self, driver, max_scrolls=5):
        print("Scrolling halaman...")
        
        for i in range(max_scrolls):
            try:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                self.random_delay(2, 3)
                
                last_height = driver.execute_script("return document.body.scrollHeight")
                time.sleep(2)
                new_height = driver.execute_script("return document.body.scrollHeight")
                
                if new_height == last_height:
                    print(f"Reached end of page after {i+1} scrolls")
                    break
                    
            except Exception as e:
                print(f"Error during scroll {i+1}: {e}")
                break
    
    def extract_product_data_colab(self, element):
        try:
            data = {}
            
            # Nama produk - multiple selectors
            name_selectors = [
                '[data-sqe="link"]',
                '.ie3A\\+n',
                '.Cve6sh',
                'a[href*="/product/"]',
                '.col-xs-2-4 a'
            ]
            
            data['nama_produk'] = 'N/A'
            for selector in name_selectors:
                try:
                    name_element = element.find_element(By.CSS_SELECTOR, selector)
                    name_text = name_element.get_attribute('title') or name_element.text
                    if name_text and name_text.strip():
                        data['nama_produk'] = name_text.strip()
                        break
                except:
                    continue
            
            # Harga - multiple selectors
            price_selectors = [
                '.vioxXd',
                '.ZEgDH9',
                '.pmmxKx',
                '.shopee-item-card__text-price',
                '[data-sqe="name"] + div'
            ]
            
            data['harga'] = 'N/A'
            for selector in price_selectors:
                try:
                    price_element = element.find_element(By.CSS_SELECTOR, selector)
                    price_text = price_element.text
                    price_clean = re.sub(r'[^\\d]', '', price_text)
                    if price_clean:
                        data['harga'] = price_clean
                        break
                except:
                    continue
            
            # Rating
            try:
                rating_element = element.find_element(By.CSS_SELECTOR, '.shopee-rating-stars__stars')
                rating_style = rating_element.get_attribute('style')
                rating_match = re.search(r'width:\\s*(\\d+(?:\\.\\d+)?)%', rating_style)
                if rating_match:
                    rating_percent = float(rating_match.group(1))
                    data['rating'] = round(rating_percent / 20, 1)
                else:
                    data['rating'] = 'N/A'
            except:
                data['rating'] = 'N/A'
            
            # Jumlah terjual
            sold_selectors = [
                '.r6HknA',
                '.shopee-item-card__text-sold',
                '[data-sqe="name"] + div + div'
            ]
            
            data['jumlah_terjual'] = 'N/A'
            for selector in sold_selectors:
                try:
                    sold_element = element.find_element(By.CSS_SELECTOR, selector)
                    sold_text = sold_element.text
                    sold_match = re.search(r'(\\d+(?:\\.\\d+)?)', sold_text)
                    if sold_match:
                        data['jumlah_terjual'] = sold_match.group(1)
                        break
                except:
                    continue
            
            # Nama toko
            shop_selectors = [
                '.Cve6sh',
                '.shopee-item-card__shop-name',
                'a[href*="/shop/"]'
            ]
            
            data['nama_toko'] = 'N/A'
            for selector in shop_selectors:
                try:
                    shop_element = element.find_element(By.CSS_SELECTOR, selector)
                    shop_text = shop_element.text.strip()
                    if shop_text:
                        data['nama_toko'] = shop_text
                        break
                except:
                    continue
            
            # Lokasi toko
            location_selectors = [
                '.zGGwiV',
                '.shopee-item-card__shop-location',
                '.shopee-item-card__shop-name + div'
            ]
            
            data['lokasi_toko'] = 'N/A'
            for selector in location_selectors:
                try:
                    location_element = element.find_element(By.CSS_SELECTOR, selector)
                    location_text = location_element.text.strip()
                    if location_text:
                        data['lokasi_toko'] = location_text
                        break
                except:
                    continue
            
            return data
            
        except Exception as e:
            print(f"Error extracting product data: {e}")
            return None
    
    def scrape_shopee_colab(self, keyword, max_products=50):
        print(f"Memulai scraping untuk keyword: {keyword}")
        print(f"Target jumlah produk: {max_products}")
        
        encoded_keyword = quote(keyword)
        url = f"{self.base_url}/search?keyword={encoded_keyword}"
        
        driver = None
        products_data = []
        
        try:
            driver = self.setup_driver_colab()
            if not driver:
                print("Gagal setup Chrome driver")
                return []
            
            print("Browser berhasil dibuka")
            print(f"Membuka URL: {url}")
            driver.get(url)
            
            self.random_delay(5, 8)
            self.scroll_page_colab(driver)
            
            wait = WebDriverWait(driver, 15)
            try:
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '[data-sqe="link"]')))
            except TimeoutException:
                print("Timeout menunggu produk muncul, mencoba selector alternatif...")
            
            product_selectors = [
                '[data-sqe="link"]',
                '.col-xs-2-4',
                '.shopee-item-card',
                'a[href*="/product/"]'
            ]
            
            product_elements = []
            for selector in product_selectors:
                try:
                    elements = driver.find_elements(By.CSS_SELECTOR, selector)
                    if elements:
                        product_elements = elements
                        print(f"Ditemukan {len(elements)} produk dengan selector: {selector}")
                        break
                except:
                    continue
            
            if not product_elements:
                print("Tidak ada produk yang ditemukan")
                return []
            
            print("Mengekstrak data produk...")
            for i, element in enumerate(product_elements):
                if len(products_data) >= max_products:
                    break
                
                try:
                    driver.execute_script("arguments[0].scrollIntoView(true);", element)
                    self.random_delay(0.5, 1)
                    
                    product_data = self.extract_product_data_colab(element)
                    if product_data and product_data['nama_produk'] != 'N/A':
                        products_data.append(product_data)
                        print(f"✓ Produk {len(products_data)}: {product_data['nama_produk'][:50]}...")
                    
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
    
    def save_to_csv_colab(self, data, keyword):
        if data:
            df = pd.DataFrame(data)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"shopee_{keyword.replace(' ', '_')}_{timestamp}.csv"
            
            try:
                from google.colab import drive
                drive.mount('/content/drive')
                filepath = f"/content/drive/MyDrive/{filename}"
                df.to_csv(filepath, index=False, encoding='utf-8-sig')
                print(f"Data berhasil disimpan ke Google Drive: {filename}")
            except:
                df.to_csv(filename, index=False, encoding='utf-8-sig')
                print(f"Data berhasil disimpan ke local: {filename}")
            
            return df, filename
        else:
            print("Tidak ada data untuk disimpan")
            return None, None
    
    def display_results_colab(self, data, keyword):
        if data:
            df = pd.DataFrame(data)
            print("\\n" + "="*60)
            print("HASIL SCRAPING SHOPEE")
            print("="*60)
            print(f"Total produk: {len(data)}")
            print(f"Keyword: {keyword}")
            print("="*60)
            
            print("\\nSAMPLE DATA:")
            print("-" * 60)
            for i, row in df.head(5).iterrows():
                print(f"{i+1}. {row['nama_produk'][:60]}...")
                print(f"   Harga: Rp {row['harga']} | Rating: {row['rating']} | Terjual: {row['jumlah_terjual']}")
                print(f"   Toko: {row['nama_toko']} | Lokasi: {row['lokasi_toko']}")
                print()
            
            print("STATISTIK:")
            print("-" * 60)
            try:
                price_df = df[df['harga'] != 'N/A'].copy()
                if not price_df.empty:
                    price_df['harga'] = pd.to_numeric(price_df['harga'], errors='coerce')
                    price_df = price_df.dropna(subset=['harga'])
                    if not price_df.empty:
                        print(f"Rata-rata harga: Rp {price_df['harga'].mean():,.0f}")
                        print(f"Harga tertinggi: Rp {price_df['harga'].max():,.0f}")
                        print(f"Harga terendah: Rp {price_df['harga'].min():,.0f}")
            except:
                pass
            
            return df
        else:
            print("Tidak ada data yang berhasil di-scrape")
            return None

print("✅ Shopee Scraper class berhasil di-load!")
"""

# CELL 3: Jalankan Scraper
"""
def main_colab():
    print("="*60)
    print("SHOPEE SCRAPER UNTUK GOOGLE COLAB")
    print("="*60)
    print("Scraper yang dioptimalkan untuk environment Colab")
    print("="*60)
    
    keyword = input("Masukkan keyword produk yang ingin di-scrape: ")
    
    while True:
        try:
            max_products = int(input("Masukkan jumlah maksimal produk (1-100): "))
            if 1 <= max_products <= 100:
                break
            else:
                print("Jumlah produk harus antara 1-100")
        except ValueError:
            print("Masukkan angka yang valid")
    
    scraper = ShopeeColabScraper()
    
    print(f"\\nMemulai proses scraping untuk '{keyword}'...")
    start_time = time.time()
    
    products_data = scraper.scrape_shopee_colab(keyword, max_products)
    
    end_time = time.time()
    duration = end_time - start_time
    
    if products_data:
        df = scraper.display_results_colab(products_data, keyword)
        df, filename = scraper.save_to_csv_colab(products_data, keyword)
        
        print(f"\\n" + "="*60)
        print("SCRAPING SELESAI!")
        print("="*60)
        print(f"Waktu eksekusi: {duration:.2f} detik")
        print(f"Total produk berhasil di-scrape: {len(products_data)}")
        print(f"File tersimpan: {filename}")
        print("="*60)
        
        return df
    else:
        print("Gagal mendapatkan data produk")
        return None

# Jalankan scraper
result_df = main_colab()
"""

# CELL 4: Lihat Hasil
"""
# Display hasil dalam format tabel
if 'result_df' in locals() and result_df is not None:
    print("📊 HASIL SCRAPING DALAM FORMAT TABEL")
    print("="*80)
    display(result_df)
    
    print("\\n📈 STATISTIK TAMBAHAN")
    print("="*40)
    print(f"Total produk: {len(result_df)}")
    print(f"Kolom data: {list(result_df.columns)}")
    
    print("\\n✅ DATA YANG BERHASIL DI-SCRAPE:")
    for col in result_df.columns:
        non_na_count = result_df[col].ne('N/A').sum()
        print(f"- {col}: {non_na_count}/{len(result_df)} ({non_na_count/len(result_df)*100:.1f}%)")
        
else:
    print("❌ Tidak ada data untuk ditampilkan. Jalankan scraper terlebih dahulu.")
"""

# CELL 5: Download File CSV
"""
import os
from google.colab import files

# Cari file CSV terbaru
csv_files = [f for f in os.listdir('.') if f.endswith('.csv') and 'shopee' in f]

if csv_files:
    latest_file = max(csv_files, key=os.path.getctime)
    print(f"📁 File CSV ditemukan: {latest_file}")
    
    files.download(latest_file)
    print(f"✅ File {latest_file} berhasil didownload!")
    
else:
    print("❌ Tidak ada file CSV yang ditemukan. Jalankan scraper terlebih dahulu.")
"""

# ============================================================================
# INSTRUKSI PENGGUNAAN:
# ============================================================================
# 1. Buka Google Colab (colab.research.google.com)
# 2. Buat notebook baru
# 3. Copy-paste setiap CELL di atas ke cell terpisah
# 4. Jalankan cell secara berurutan
# 5. Ikuti instruksi yang muncul
# ============================================================================