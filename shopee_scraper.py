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
import urllib.parse
import re
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

class ShopeeScraper:
    def __init__(self):
        self.ua = UserAgent()
        self.session = requests.Session()
        self.setup_session()
        self.setup_driver()
        
    def setup_session(self):
        """Setup session dengan headers yang menyerupai browser asli"""
        headers = {
            'User-Agent': self.ua.random,
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
        """Setup Chrome driver dengan opsi anti-deteksi"""
        chrome_options = Options()
        
        # Anti-deteksi options
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument(f'--user-agent={self.ua.random}')
        
        # Additional stealth options
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--disable-plugins')
        chrome_options.add_argument('--disable-images')
        chrome_options.add_argument('--disable-javascript')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-web-security')
        chrome_options.add_argument('--allow-running-insecure-content')
        
        # Window size
        chrome_options.add_argument('--window-size=1920,1080')
        
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        except Exception as e:
            print(f"Error setting up Chrome driver: {e}")
            print("Trying with different approach...")
            self.setup_driver_fallback()
    
    def setup_driver_fallback(self):
        """Fallback setup jika Chrome driver gagal"""
        try:
            from selenium.webdriver.chrome.service import Service
            from webdriver_manager.chrome import ChromeDriverManager
            
            service = Service(ChromeDriverManager().install())
            chrome_options = Options()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument(f'--user-agent={self.ua.random}')
            
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
        except Exception as e:
            print(f"Fallback setup failed: {e}")
            raise Exception("Tidak dapat menginisialisasi browser. Pastikan Chrome terinstall.")
    
    def random_delay(self, min_delay=1, max_delay=3):
        """Delay acak untuk menghindari deteksi bot"""
        delay = random.uniform(min_delay, max_delay)
        time.sleep(delay)
    
    def scroll_page(self, scroll_count=3):
        """Scroll halaman untuk memuat lebih banyak konten"""
        for i in range(scroll_count):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            self.random_delay(2, 4)
            self.driver.execute_script("window.scrollTo(0, 0);")
            self.random_delay(1, 2)
    
    def extract_product_data(self, product_element):
        """Ekstrak data produk dari elemen HTML"""
        try:
            data = {}
            
            # Nama produk
            try:
                name_element = product_element.find_element(By.CSS_SELECTOR, '[data-sqe="link"]')
                data['nama_produk'] = name_element.get_attribute('title') or name_element.text.strip()
            except:
                try:
                    name_element = product_element.find_element(By.CSS_SELECTOR, '.ie3A\+n')
                    data['nama_produk'] = name_element.text.strip()
                except:
                    data['nama_produk'] = "N/A"
            
            # Harga produk
            try:
                price_element = product_element.find_element(By.CSS_SELECTOR, '.vioxXd')
                price_text = price_element.text.strip()
                # Bersihkan format harga
                price_clean = re.sub(r'[^\d]', '', price_text)
                data['harga'] = int(price_clean) if price_clean else 0
            except:
                try:
                    price_element = product_element.find_element(By.CSS_SELECTOR, '.ZEgDH9')
                    price_text = price_element.text.strip()
                    price_clean = re.sub(r'[^\d]', '', price_text)
                    data['harga'] = int(price_clean) if price_clean else 0
                except:
                    data['harga'] = 0
            
            # Rating
            try:
                rating_element = product_element.find_element(By.CSS_SELECTOR, '.shopee-rating-stars__stars')
                rating_style = rating_element.get_attribute('style')
                if rating_style:
                    # Ekstrak rating dari style width
                    rating_match = re.search(r'width:\s*(\d+(?:\.\d+)?)%', rating_style)
                    if rating_match:
                        rating_percent = float(rating_match.group(1))
                        data['rating'] = round(rating_percent / 20, 1)  # Convert to 5-star scale
                    else:
                        data['rating'] = 0.0
                else:
                    data['rating'] = 0.0
            except:
                data['rating'] = 0.0
            
            # Jumlah terjual
            try:
                sold_element = product_element.find_element(By.CSS_SELECTOR, '.r6HknA')
                sold_text = sold_element.text.strip()
                # Ekstrak angka dari teks "Terjual X"
                sold_match = re.search(r'(\d+)', sold_text)
                data['jumlah_terjual'] = int(sold_match.group(1)) if sold_match else 0
            except:
                try:
                    sold_element = product_element.find_element(By.CSS_SELECTOR, '.ie3A\+n')
                    sold_text = sold_element.text.strip()
                    sold_match = re.search(r'(\d+)', sold_text)
                    data['jumlah_terjual'] = int(sold_match.group(1)) if sold_match else 0
                except:
                    data['jumlah_terjual'] = 0
            
            # Nama toko
            try:
                shop_element = product_element.find_element(By.CSS_SELECTOR, '.Cve6sh')
                data['nama_toko'] = shop_element.text.strip()
            except:
                try:
                    shop_element = product_element.find_element(By.CSS_SELECTOR, '.ie3A\+n')
                    data['nama_toko'] = shop_element.text.strip()
                except:
                    data['nama_toko'] = "N/A"
            
            # Lokasi toko
            try:
                location_element = product_element.find_element(By.CSS_SELECTOR, '.zGGwiV')
                data['lokasi_toko'] = location_element.text.strip()
            except:
                try:
                    location_element = product_element.find_element(By.CSS_SELECTOR, '.ie3A\+n')
                    data['lokasi_toko'] = location_element.text.strip()
                except:
                    data['lokasi_toko'] = "N/A"
            
            return data
            
        except Exception as e:
            print(f"Error extracting product data: {e}")
            return None
    
    def scrape_shopee(self, keyword, max_products=50):
        """Fungsi utama untuk scraping Shopee"""
        print(f"Memulai scraping untuk keyword: '{keyword}'")
        print(f"Target jumlah produk: {max_products}")
        
        # Encode keyword untuk URL
        encoded_keyword = urllib.parse.quote(keyword)
        search_url = f"https://shopee.co.id/search?keyword={encoded_keyword}"
        
        print(f"Mengakses URL: {search_url}")
        
        try:
            # Buka halaman
            self.driver.get(search_url)
            self.random_delay(3, 5)
            
            # Tunggu halaman dimuat
            wait = WebDriverWait(self.driver, 20)
            
            # Coba tunggu elemen produk muncul
            try:
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '[data-sqe="link"]')))
            except TimeoutException:
                print("Mencoba selector alternatif...")
                try:
                    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.col-xs-2-4')))
                except TimeoutException:
                    print("Halaman tidak dimuat dengan benar. Mencoba refresh...")
                    self.driver.refresh()
                    self.random_delay(5, 8)
            
            # Scroll untuk memuat lebih banyak produk
            print("Scrolling halaman untuk memuat lebih banyak produk...")
            self.scroll_page(scroll_count=5)
            
            # Cari semua elemen produk
            product_elements = []
            selectors = [
                '[data-sqe="link"]',
                '.col-xs-2-4',
                '.shopee-search-item-result__item',
                '.shopee-item-card'
            ]
            
            for selector in selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if elements:
                        product_elements = elements
                        print(f"Berhasil menemukan {len(elements)} produk dengan selector: {selector}")
                        break
                except:
                    continue
            
            if not product_elements:
                print("Tidak dapat menemukan elemen produk. Mencoba pendekatan alternatif...")
                # Coba ambil semua div yang mungkin berisi produk
                product_elements = self.driver.find_elements(By.TAG_NAME, "div")
                product_elements = [elem for elem in product_elements if elem.get_attribute("class") and "item" in elem.get_attribute("class").lower()]
            
            print(f"Total elemen yang ditemukan: {len(product_elements)}")
            
            # Ekstrak data produk
            products_data = []
            count = 0
            
            for element in product_elements:
                if count >= max_products:
                    break
                    
                try:
                    product_data = self.extract_product_data(element)
                    if product_data and product_data['nama_produk'] != "N/A":
                        products_data.append(product_data)
                        count += 1
                        print(f"Berhasil mengekstrak produk {count}: {product_data['nama_produk'][:50]}...")
                except Exception as e:
                    print(f"Error mengekstrak produk: {e}")
                    continue
                
                self.random_delay(0.5, 1)
            
            print(f"Berhasil mengekstrak {len(products_data)} produk")
            return products_data
            
        except Exception as e:
            print(f"Error saat scraping: {e}")
            return []
        
        finally:
            self.driver.quit()
    
    def save_to_excel(self, data, keyword):
        """Simpan data ke file Excel"""
        if not data:
            print("Tidak ada data untuk disimpan")
            return
        
        df = pd.DataFrame(data)
        
        # Bersihkan data
        df = df.dropna(subset=['nama_produk'])
        df = df[df['nama_produk'] != "N/A"]
        
        # Format harga
        df['harga'] = df['harga'].apply(lambda x: f"Rp {x:,}" if x > 0 else "N/A")
        
        # Format rating
        df['rating'] = df['rating'].apply(lambda x: f"{x}/5" if x > 0 else "N/A")
        
        # Format jumlah terjual
        df['jumlah_terjual'] = df['jumlah_terjual'].apply(lambda x: f"{x:,}" if x > 0 else "N/A")
        
        # Buat nama file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"shopee_{keyword.replace(' ', '_')}_{timestamp}.xlsx"
        
        # Simpan ke Excel
        df.to_excel(filename, index=False, engine='openpyxl')
        print(f"Data berhasil disimpan ke: {filename}")
        
        # Tampilkan preview
        print("\nPreview data:")
        print(df.head())
        print(f"\nTotal data: {len(df)} produk")
        
        return filename

def main():
    """Fungsi utama untuk menjalankan scraper"""
    print("=== SHOPEE SCRAPER ===")
    print("Scraper otomatis untuk data produk Shopee")
    print("=" * 50)
    
    # Input dari user
    keyword = input("Masukkan keyword produk yang ingin di-scrape: ").strip()
    if not keyword:
        print("Keyword tidak boleh kosong!")
        return
    
    try:
        max_products = int(input("Masukkan jumlah data yang ingin didapatkan (default: 50): ") or "50")
        if max_products <= 0:
            max_products = 50
    except ValueError:
        max_products = 50
        print("Input tidak valid, menggunakan default: 50")
    
    print(f"\nMemulai scraping untuk: '{keyword}'")
    print(f"Target jumlah data: {max_products}")
    print("Mohon tunggu...")
    
    # Inisialisasi scraper
    scraper = ShopeeScraper()
    
    try:
        # Lakukan scraping
        data = scraper.scrape_shopee(keyword, max_products)
        
        if data:
            # Simpan ke Excel
            filename = scraper.save_to_excel(data, keyword)
            print(f"\n✅ Scraping selesai! Data tersimpan di: {filename}")
        else:
            print("\n❌ Tidak ada data yang berhasil di-scrape")
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("Coba jalankan ulang atau periksa koneksi internet")
    
    finally:
        try:
            scraper.driver.quit()
        except:
            pass

if __name__ == "__main__":
    main()