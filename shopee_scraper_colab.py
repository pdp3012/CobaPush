# Shopee Scraper untuk Google Colab
# Install dependencies terlebih dahulu
!pip install selenium pandas requests fake-useragent openpyxl webdriver-manager lxml beautifulsoup4

# Setup Chrome untuk Colab
!apt-get update
!apt install chromium-chromedriver

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
import os
warnings.filterwarnings('ignore')

class ShopeeScraperColab:
    def __init__(self):
        self.ua = UserAgent()
        self.session = requests.Session()
        self.setup_session()
        self.setup_driver_colab()
        
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
        
    def setup_driver_colab(self):
        """Setup Chrome driver khusus untuk Google Colab"""
        chrome_options = Options()
        
        # Anti-deteksi options untuk Colab
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument(f'--user-agent={self.ua.random}')
        
        # Colab-specific options
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--disable-plugins')
        chrome_options.add_argument('--disable-images')
        chrome_options.add_argument('--disable-javascript')
        chrome_options.add_argument('--disable-web-security')
        chrome_options.add_argument('--allow-running-insecure-content')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--remote-debugging-port=9222')
        
        # Additional stealth options
        chrome_options.add_argument('--disable-blink-features')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_argument('--disable-infobars')
        chrome_options.add_argument('--disable-notifications')
        chrome_options.add_argument('--disable-popup-blocking')
        chrome_options.add_argument('--disable-save-password-bubble')
        chrome_options.add_argument('--disable-translate')
        chrome_options.add_argument('--disable-web-security')
        chrome_options.add_argument('--disable-features=VizDisplayCompositor')
        
        try:
            # Set path untuk chromedriver di Colab
            os.environ['PATH'] += ':/usr/bin'
            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            print("✅ Chrome driver berhasil diinisialisasi")
        except Exception as e:
            print(f"Error setting up Chrome driver: {e}")
            print("Mencoba setup alternatif...")
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
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--disable-extensions')
            
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            print("✅ Chrome driver berhasil diinisialisasi (fallback)")
        except Exception as e:
            print(f"Fallback setup failed: {e}")
            raise Exception("Tidak dapat menginisialisasi browser. Pastikan Chrome terinstall.")
    
    def random_delay(self, min_delay=2, max_delay=5):
        """Delay acak untuk menghindari deteksi bot"""
        delay = random.uniform(min_delay, max_delay)
        time.sleep(delay)
    
    def scroll_page(self, scroll_count=5):
        """Scroll halaman untuk memuat lebih banyak konten"""
        print("Scrolling halaman untuk memuat lebih banyak produk...")
        for i in range(scroll_count):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            self.random_delay(3, 5)
            self.driver.execute_script("window.scrollTo(0, 0);")
            self.random_delay(2, 3)
            print(f"Scroll {i+1}/{scroll_count} selesai")
    
    def extract_product_data(self, product_element):
        """Ekstrak data produk dari elemen HTML dengan multiple selectors"""
        try:
            data = {}
            
            # Nama produk - multiple selectors
            name_selectors = [
                '[data-sqe="link"]',
                '.ie3A\+n',
                '.shopee-item-card__text-name',
                '.shopee-search-item-result__item-name',
                'a[data-sqe="link"]',
                '.col-xs-2-4 a'
            ]
            
            data['nama_produk'] = "N/A"
            for selector in name_selectors:
                try:
                    name_element = product_element.find_element(By.CSS_SELECTOR, selector)
                    name_text = name_element.get_attribute('title') or name_element.text.strip()
                    if name_text and len(name_text) > 3:
                        data['nama_produk'] = name_text
                        break
                except:
                    continue
            
            # Harga produk - multiple selectors
            price_selectors = [
                '.vioxXd',
                '.ZEgDH9',
                '.shopee-item-card__text-price',
                '.shopee-search-item-result__item-price',
                '[data-sqe="name"]'
            ]
            
            data['harga'] = 0
            for selector in price_selectors:
                try:
                    price_element = product_element.find_element(By.CSS_SELECTOR, selector)
                    price_text = price_element.text.strip()
                    # Bersihkan format harga
                    price_clean = re.sub(r'[^\d]', '', price_text)
                    if price_clean:
                        data['harga'] = int(price_clean)
                        break
                except:
                    continue
            
            # Rating - multiple selectors
            rating_selectors = [
                '.shopee-rating-stars__stars',
                '.shopee-item-card__rating',
                '.shopee-search-item-result__item-rating'
            ]
            
            data['rating'] = 0.0
            for selector in rating_selectors:
                try:
                    rating_element = product_element.find_element(By.CSS_SELECTOR, selector)
                    rating_style = rating_element.get_attribute('style')
                    if rating_style:
                        rating_match = re.search(r'width:\s*(\d+(?:\.\d+)?)%', rating_style)
                        if rating_match:
                            rating_percent = float(rating_match.group(1))
                            data['rating'] = round(rating_percent / 20, 1)
                            break
                except:
                    continue
            
            # Jumlah terjual - multiple selectors
            sold_selectors = [
                '.r6HknA',
                '.shopee-item-card__sold',
                '.shopee-search-item-result__item-sold'
            ]
            
            data['jumlah_terjual'] = 0
            for selector in sold_selectors:
                try:
                    sold_element = product_element.find_element(By.CSS_SELECTOR, selector)
                    sold_text = sold_element.text.strip()
                    sold_match = re.search(r'(\d+)', sold_text)
                    if sold_match:
                        data['jumlah_terjual'] = int(sold_match.group(1))
                        break
                except:
                    continue
            
            # Nama toko - multiple selectors
            shop_selectors = [
                '.Cve6sh',
                '.shopee-item-card__shop-name',
                '.shopee-search-item-result__item-shop'
            ]
            
            data['nama_toko'] = "N/A"
            for selector in shop_selectors:
                try:
                    shop_element = product_element.find_element(By.CSS_SELECTOR, selector)
                    shop_text = shop_element.text.strip()
                    if shop_text and len(shop_text) > 2:
                        data['nama_toko'] = shop_text
                        break
                except:
                    continue
            
            # Lokasi toko - multiple selectors
            location_selectors = [
                '.zGGwiV',
                '.shopee-item-card__shop-location',
                '.shopee-search-item-result__item-location'
            ]
            
            data['lokasi_toko'] = "N/A"
            for selector in location_selectors:
                try:
                    location_element = product_element.find_element(By.CSS_SELECTOR, selector)
                    location_text = location_element.text.strip()
                    if location_text and len(location_text) > 2:
                        data['lokasi_toko'] = location_text
                        break
                except:
                    continue
            
            return data
            
        except Exception as e:
            print(f"Error extracting product data: {e}")
            return None
    
    def scrape_shopee(self, keyword, max_products=50):
        """Fungsi utama untuk scraping Shopee"""
        print(f"🚀 Memulai scraping untuk keyword: '{keyword}'")
        print(f"📊 Target jumlah produk: {max_products}")
        
        # Encode keyword untuk URL
        encoded_keyword = urllib.parse.quote(keyword)
        search_url = f"https://shopee.co.id/search?keyword={encoded_keyword}"
        
        print(f"🌐 Mengakses URL: {search_url}")
        
        try:
            # Buka halaman
            self.driver.get(search_url)
            self.random_delay(5, 8)
            
            # Tunggu halaman dimuat
            wait = WebDriverWait(self.driver, 30)
            
            # Coba tunggu elemen produk muncul dengan multiple selectors
            product_selectors = [
                '[data-sqe="link"]',
                '.col-xs-2-4',
                '.shopee-search-item-result__item',
                '.shopee-item-card',
                'a[data-sqe="link"]'
            ]
            
            page_loaded = False
            for selector in product_selectors:
                try:
                    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
                    print(f"✅ Halaman berhasil dimuat dengan selector: {selector}")
                    page_loaded = True
                    break
                except TimeoutException:
                    continue
            
            if not page_loaded:
                print("⚠️ Halaman tidak dimuat dengan benar. Mencoba refresh...")
                self.driver.refresh()
                self.random_delay(8, 12)
            
            # Scroll untuk memuat lebih banyak produk
            self.scroll_page(scroll_count=8)
            
            # Cari semua elemen produk
            product_elements = []
            
            for selector in product_selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if elements and len(elements) > 0:
                        product_elements = elements
                        print(f"✅ Berhasil menemukan {len(elements)} produk dengan selector: {selector}")
                        break
                except:
                    continue
            
            if not product_elements:
                print("⚠️ Tidak dapat menemukan elemen produk. Mencoba pendekatan alternatif...")
                # Coba ambil semua div yang mungkin berisi produk
                all_divs = self.driver.find_elements(By.TAG_NAME, "div")
                product_elements = [elem for elem in all_divs if elem.get_attribute("class") and 
                                  any(keyword in elem.get_attribute("class").lower() for keyword in ["item", "card", "product"])]
                print(f"🔍 Ditemukan {len(product_elements)} elemen potensial")
            
            print(f"📦 Total elemen yang ditemukan: {len(product_elements)}")
            
            # Ekstrak data produk
            products_data = []
            count = 0
            
            for i, element in enumerate(product_elements):
                if count >= max_products:
                    break
                    
                try:
                    product_data = self.extract_product_data(element)
                    if product_data and product_data['nama_produk'] != "N/A" and len(product_data['nama_produk']) > 3:
                        products_data.append(product_data)
                        count += 1
                        print(f"✅ Produk {count}: {product_data['nama_produk'][:50]}...")
                        
                        # Progress indicator
                        if count % 10 == 0:
                            print(f"📈 Progress: {count}/{max_products} produk berhasil diekstrak")
                            
                except Exception as e:
                    print(f"❌ Error mengekstrak produk {i+1}: {e}")
                    continue
                
                self.random_delay(1, 2)
            
            print(f"🎉 Berhasil mengekstrak {len(products_data)} produk")
            return products_data
            
        except Exception as e:
            print(f"❌ Error saat scraping: {e}")
            return []
        
        finally:
            try:
                self.driver.quit()
                print("🔒 Browser ditutup")
            except:
                pass
    
    def save_to_excel(self, data, keyword):
        """Simpan data ke file Excel"""
        if not data:
            print("❌ Tidak ada data untuk disimpan")
            return None
        
        df = pd.DataFrame(data)
        
        # Bersihkan data
        df = df.dropna(subset=['nama_produk'])
        df = df[df['nama_produk'] != "N/A"]
        df = df[df['nama_produk'].str.len() > 3]
        
        if df.empty:
            print("❌ Tidak ada data valid untuk disimpan")
            return None
        
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
        print(f"💾 Data berhasil disimpan ke: {filename}")
        
        # Tampilkan preview
        print("\n📋 Preview data:")
        print(df.head(10))
        print(f"\n📊 Total data: {len(df)} produk")
        
        # Tampilkan statistik
        print("\n📈 Statistik data:")
        print(f"- Produk dengan harga: {len(df[df['harga'] != 'N/A'])}")
        print(f"- Produk dengan rating: {len(df[df['rating'] != 'N/A'])}")
        print(f"- Produk dengan info terjual: {len(df[df['jumlah_terjual'] != 'N/A'])}")
        
        return filename

def main_colab():
    """Fungsi utama untuk menjalankan scraper di Colab"""
    print("=" * 60)
    print("🛍️  SHOPEE SCRAPER - GOOGLE COLAB VERSION")
    print("🔧 Scraper otomatis untuk data produk Shopee")
    print("=" * 60)
    
    # Input dari user
    keyword = input("🔍 Masukkan keyword produk yang ingin di-scrape: ").strip()
    if not keyword:
        print("❌ Keyword tidak boleh kosong!")
        return
    
    try:
        max_products = int(input("📊 Masukkan jumlah data yang ingin didapatkan (default: 50): ") or "50")
        if max_products <= 0:
            max_products = 50
    except ValueError:
        max_products = 50
        print("⚠️ Input tidak valid, menggunakan default: 50")
    
    print(f"\n🚀 Memulai scraping untuk: '{keyword}'")
    print(f"📊 Target jumlah data: {max_products}")
    print("⏳ Mohon tunggu...")
    
    # Inisialisasi scraper
    scraper = ShopeeScraperColab()
    
    try:
        # Lakukan scraping
        data = scraper.scrape_shopee(keyword, max_products)
        
        if data:
            # Simpan ke Excel
            filename = scraper.save_to_excel(data, keyword)
            if filename:
                print(f"\n🎉 Scraping selesai! Data tersimpan di: {filename}")
                print(f"📁 File dapat diunduh dari panel file di sebelah kiri")
            else:
                print("\n❌ Gagal menyimpan data")
        else:
            print("\n❌ Tidak ada data yang berhasil di-scrape")
            print("💡 Tips: Coba keyword yang berbeda atau periksa koneksi internet")
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("💡 Tips: Coba jalankan ulang atau periksa koneksi internet")
    
    finally:
        try:
            scraper.driver.quit()
        except:
            pass

# Jalankan scraper
if __name__ == "__main__":
    main_colab()