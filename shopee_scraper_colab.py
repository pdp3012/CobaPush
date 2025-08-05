# ========================================
# SHOPEE SCRAPER - GOOGLE COLAB VERSION
# ========================================
# Dosen Data Mining dengan 30 tahun pengalaman
# Sertifikasi Internasional Web Scraping

# Install dependencies untuk Google Colab
import subprocess
import sys

def install_dependencies():
    """Install semua dependencies yang diperlukan"""
    print("🔧 Installing dependencies...")
    
    # Update package manager
    subprocess.run(["apt", "update"], capture_output=True, text=True)
    
    # Install Chrome dan ChromeDriver
    subprocess.run(["apt", "install", "-y", "chromium-chromedriver", "google-chrome-stable", "xvfb"], 
                   capture_output=True, text=True)
    
    # Install Python packages
    subprocess.run([sys.executable, "-m", "pip", "install", "-q", 
                   "selenium==4.15.2", "beautifulsoup4", "pandas", "webdriver-manager"], 
                   capture_output=True, text=True)
    
    print("✅ Dependencies installed successfully!")

# Jalankan instalasi
install_dependencies()

import json
import time
import random
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class ShopeeScraperColab:
    def __init__(self):
        """Inisialisasi scraper dengan konfigurasi optimal"""
        self.driver = None
        # Cookies data sudah di-embed dalam class
        self.cookies_data = [
            {
                "domain": ".shopee.co.id",
                "expirationDate": 1760508938.540668,
                "hostOnly": False,
                "httpOnly": True,
                "name": "REC_T_ID",
                "path": "/",
                "sameSite": "unspecified",
                "secure": True,
                "session": False,
                "storeId": "0",
                "value": "8bc721be-1c1c-11f0-ae34-12e5e49f7121",
                "id": 1
            },
            {
                "domain": ".shopee.co.id",
                "hostOnly": False,
                "httpOnly": False,
                "name": "SPC_CDS_CHAT",
                "path": "/",
                "sameSite": "unspecified",
                "secure": False,
                "session": True,
                "storeId": "0",
                "value": "f1163150-6b68-4f24-8b6d-3cd76e0d210e",
                "id": 2
            },
            {
                "domain": ".shopee.co.id",
                "expirationDate": 1754911883.554243,
                "hostOnly": False,
                "httpOnly": False,
                "name": "SPC_CLIENTID",
                "path": "/",
                "sameSite": "unspecified",
                "secure": True,
                "session": False,
                "storeId": "0",
                "value": "tShI1nMM4sC8L0nqtikqezkabjgnsexx",
                "id": 3
            },
            {
                "domain": ".shopee.co.id",
                "expirationDate": 1769916526.700498,
                "hostOnly": False,
                "httpOnly": True,
                "name": "SPC_EC",
                "path": "/",
                "sameSite": "unspecified",
                "secure": True,
                "session": False,
                "storeId": "0",
                "value": ".SjVpZFVBc0cybENMZks0aFxNDtw3BvSERjhCM90OrHdoM8fCswHSu7e2LEaEmHXk+g8ZngMR5SDktOM0OqCRJkeHs8hdM3BJonXuqJbaF4yeuhAAizI1SztLImpybKEWrcoaMXARpNFjuh75YJPFCOPu4qG3VYhhmbtzw5aoZXYorQVp4VW69roxzHj6rrIBp8raxGa0PZwLCo7L5iPj4MEQy4bUE27AmcLBcroWhAK0qkx7fY9FG5ZuSx21HdzY",
                "id": 4
            },
            {
                "domain": ".shopee.co.id",
                "expirationDate": 1760508938.540625,
                "hostOnly": False,
                "httpOnly": False,
                "name": "SPC_F",
                "path": "/",
                "sameSite": "unspecified",
                "secure": True,
                "session": False,
                "storeId": "0",
                "value": "yNV6DVNBrPCohZDT9b6hxEHwkYEt9gQX",
                "id": 5
            },
            {
                "domain": ".shopee.co.id",
                "expirationDate": 1769916526.700532,
                "hostOnly": False,
                "httpOnly": False,
                "name": "SPC_R_T_ID",
                "path": "/",
                "sameSite": "unspecified",
                "secure": True,
                "session": False,
                "storeId": "0",
                "value": "rm4TZCgZwiwoFwPe0QdyNFWyVlXFGPK99q1v3fhoJlRaOvFa0yokr89MpmBnZTmAz4/S26jgXcd1S3nQjGjkbcNbWLq7p8VLP3OqKBGXWA2QvY4EmO5EfBTf1VRgYp7cAG7IXkdtRuLLSO5QLR+z8rR3yuW7we48VQLvwBSwAPE=",
                "id": 6
            },
            {
                "domain": ".shopee.co.id",
                "expirationDate": 1769916526.700144,
                "hostOnly": False,
                "httpOnly": False,
                "name": "SPC_R_T_IV",
                "path": "/",
                "sameSite": "unspecified",
                "secure": True,
                "session": False,
                "storeId": "0",
                "value": "WnhxR25XY0tGNU1ydTFiUQ==",
                "id": 7
            },
            {
                "domain": ".shopee.co.id",
                "expirationDate": 1754450926.700391,
                "hostOnly": False,
                "httpOnly": True,
                "name": "SPC_SI",
                "path": "/",
                "sameSite": "unspecified",
                "secure": True,
                "session": False,
                "storeId": "0",
                "value": "BUB3aAAAAABDVWdFR3lmbCfiOQIAAAAAQWNBbXM3ak4=",
                "id": 8
            },
            {
                "domain": ".shopee.co.id",
                "expirationDate": 1769916526.700427,
                "hostOnly": False,
                "httpOnly": True,
                "name": "SPC_ST",
                "path": "/",
                "sameSite": "unspecified",
                "secure": True,
                "session": False,
                "storeId": "0",
                "value": ".Rkl0UTFHaTdPMk9sTTk2OCUeAul8Ul7ts13+AZKSCrZunlpkWzezFK+9VggWiKHopYqzfDH5vOTlKV6roTM6BbcJwT3yGNepFHq3fqoarWZETdPYPf2tk0+MTgZcyiewyTdyCAI+m/64kWoMjc1cDna/zHPhIOcgJ7OIMqN0hfMbDhiMC6WXff+cLx6ie6pnFeqs1fdWBsgwnHLjmYzVkQQjdfjeFM9dVjtELsnvBiArDXqhfFmEMvsh08xWcoCR",
                "id": 9
            },
            {
                "domain": ".shopee.co.id",
                "expirationDate": 1769916526.700264,
                "hostOnly": False,
                "httpOnly": True,
                "name": "SPC_T_ID",
                "path": "/",
                "sameSite": "unspecified",
                "secure": True,
                "session": False,
                "storeId": "0",
                "value": "rm4TZCgZwiwoFwPe0QdyNFWyVlXFGPK99q1v3fhoJlRaOvFa0yokr89MpmBnZTmAz4/S26jgXcd1S3nQjGjkbcNbWLq7p8VLP3OqKBGXWA2QvY4EmO5EfBTf1VRgYp7cAG7IXkdtRuLLSO5QLR+z8rR3yuW7we48VQLvwBSwAPE=",
                "id": 10
            },
            {
                "domain": ".shopee.co.id",
                "expirationDate": 1769916526.700335,
                "hostOnly": False,
                "httpOnly": True,
                "name": "SPC_T_IV",
                "path": "/",
                "sameSite": "unspecified",
                "secure": True,
                "session": False,
                "storeId": "0",
                "value": "WnhxR25XY0tGNU1ydTFiUQ==",
                "id": 11
            },
            {
                "domain": ".shopee.co.id",
                "expirationDate": 1769916526.700467,
                "hostOnly": False,
                "httpOnly": False,
                "name": "SPC_U",
                "path": "/",
                "sameSite": "unspecified",
                "secure": True,
                "session": False,
                "storeId": "0",
                "value": "213962152",
                "id": 12
            },
            {
                "domain": "shopee.co.id",
                "expirationDate": 1754408210.615685,
                "hostOnly": True,
                "httpOnly": False,
                "name": "_QPWSDCXHZQA",
                "path": "/",
                "sameSite": "unspecified",
                "secure": False,
                "session": False,
                "storeId": "0",
                "value": "84c53e6b-7a1b-48a9-f859-850fee955dac",
                "id": 13
            },
            {
                "domain": "shopee.co.id",
                "hostOnly": True,
                "httpOnly": False,
                "name": "_sapid",
                "path": "/",
                "sameSite": "unspecified",
                "secure": False,
                "session": True,
                "storeId": "0",
                "value": "3a0cb6642c76960c3f517a662e30795941bff9d2b36f905e35c6a0fe",
                "id": 14
            },
            {
                "domain": "shopee.co.id",
                "hostOnly": True,
                "httpOnly": False,
                "name": "csrftoken",
                "path": "/",
                "sameSite": "unspecified",
                "secure": False,
                "session": True,
                "storeId": "0",
                "value": "OxNwWhz6alhR7k9V7mIne33ZnyDCRUNv",
                "id": 15
            },
            {
                "domain": "shopee.co.id",
                "expirationDate": 1754964700.165573,
                "hostOnly": True,
                "httpOnly": False,
                "name": "ds",
                "path": "/",
                "sameSite": "unspecified",
                "secure": False,
                "session": False,
                "storeId": "0",
                "value": "e81daf46176c9652cedaa7733130a5f2",
                "id": 16
            },
            {
                "domain": "shopee.co.id",
                "expirationDate": 1754964699.321718,
                "hostOnly": True,
                "httpOnly": False,
                "name": "REC7iLP4Q",
                "path": "/",
                "sameSite": "unspecified",
                "secure": False,
                "session": False,
                "storeId": "0",
                "value": "d7f436da-822b-4a66-b7df-9656fbaf60cd",
                "id": 17
            },
            {
                "domain": "shopee.co.id",
                "expirationDate": 1754964700.165107,
                "hostOnly": True,
                "httpOnly": False,
                "name": "shopee_webUnique_ccd",
                "path": "/",
                "sameSite": "unspecified",
                "secure": False,
                "session": False,
                "storeId": "0",
                "value": "TQ9WNF9fdEDxLFW5rqcGpw%3D%3D%7CLzgno4zi476fAAcFQr%2B821%2BzHAZalZxe0%2FOSdSE0Hi4ZtBk%2B9EOJ%2BuS7UOVd43nXR2gMZ5UetlgFuL7FQLep%7CSSxr%2BH20QlVfm2f7%7C08%7C3",
                "id": 18
            },
            {
                "domain": "shopee.co.id",
                "expirationDate": 1754446568.820477,
                "hostOnly": True,
                "httpOnly": True,
                "name": "SPC_SEC_SI",
                "path": "/",
                "sameSite": "unspecified",
                "secure": True,
                "session": False,
                "storeId": "0",
                "value": "v1-Uk9LdlJJR3pNbk0yVVJoVKaCZbtdACfp4NsXwOP9keHDsQBkyzXX0we7kDEV9lmOhUkId1FmyycoCdfD43xC9hI4H8O2pPeVgIeI9DVgd9A=",
                "id": 19
            }
        ]

    def setup_driver(self):
        """Setup Chrome driver dengan konfigurasi optimal untuk Google Colab"""
        print("🚀 Setting up Chrome driver...")
        
        options = Options()
        
        # Konfigurasi untuk Google Colab
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-plugins")
        options.add_argument("--disable-images")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        
        # Tambahan untuk menghindari deteksi bot
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        try:
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=options)
            
            # Execute script untuk menghindari deteksi
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            print("✅ Chrome driver setup berhasil!")
            return True
        except Exception as e:
            print(f"❌ Error setting up driver: {e}")
            return False

    def load_cookies(self):
        """Load cookies untuk login otomatis"""
        print("🍪 Loading cookies untuk login otomatis...")
        
        try:
            # Buka halaman Shopee terlebih dahulu
            self.driver.get("https://shopee.co.id")
            time.sleep(3)
            
            # Load cookies dari data yang sudah disediakan
            for cookie in self.cookies_data:
                try:
                    # Clean up cookie data
                    clean_cookie = {}
                    for key, value in cookie.items():
                        if key in ['name', 'value', 'domain', 'path']:
                            clean_cookie[key] = value
                        elif key == 'expirationDate':
                            clean_cookie['expiry'] = int(value)
                        elif key == 'httpOnly':
                            clean_cookie['httpOnly'] = value
                        elif key == 'secure':
                            clean_cookie['secure'] = value
                        elif key == 'sameSite' and value != 'unspecified':
                            clean_cookie['sameSite'] = value
                    
                    self.driver.add_cookie(clean_cookie)
                except Exception as e:
                    print(f"⚠️ Warning: Gagal menambahkan cookie {cookie.get('name', 'unknown')}: {e}")
                    continue
            
            # Refresh halaman setelah menambahkan cookies
            self.driver.refresh()
            time.sleep(5)
            
            print("✅ Cookies loaded successfully!")
            return True
                
        except Exception as e:
            print(f"❌ Error loading cookies: {e}")
            return False

    def slow_scroll(self, duration=3):
        """Scroll halaman secara perlahan untuk memuat konten"""
        print("📜 Scrolling halaman...")
        
        try:
            # Get scroll height
            last_height = self.driver.execute_script("return document.body.scrollHeight")
            
            # Scroll step by step
            for i in range(0, last_height, 300):
                self.driver.execute_script(f"window.scrollTo(0, {i});")
                time.sleep(random.uniform(0.1, 0.3))
            
            # Scroll to bottom
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(duration)
            
            # Scroll back to top
            self.driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(1)
            
        except Exception as e:
            print(f"⚠️ Warning: Error during scrolling: {e}")

    def extract_product_data(self, item):
        """Extract data produk dari elemen HTML"""
        try:
            # Nama produk - multiple selectors untuk kompatibilitas
            name_selectors = [
                "div.line-clamp-2", 
                ".ie3A\+n", 
                "[data-sqe='name']",
                ".shopee-item-card__text-name",
                ".shopee-search-item-result__item-name"
            ]
            name = "N/A"
            for selector in name_selectors:
                name_elem = item.select_one(selector)
                if name_elem:
                    name = name_elem.get_text(strip=True)
                    break
            
            # Harga - multiple selectors
            price_selectors = [
                "span.currency--GVKjl", 
                ".ZEgDH9", 
                "[data-sqe='price']",
                ".shopee-item-card__text-price",
                ".shopee-search-item-result__item-price"
            ]
            price = "N/A"
            for selector in price_selectors:
                price_elem = item.select_one(selector)
                if price_elem:
                    price = price_elem.get_text(strip=True)
                    break
            
            # Terjual - multiple selectors
            sold_selectors = [
                "div[data-sqe='sold']", 
                ".r6HknA", 
                ".ie3A\+n + div",
                ".shopee-item-card__text-sold",
                ".shopee-search-item-result__item-sold"
            ]
            sold = "Tidak ditemukan"
            for selector in sold_selectors:
                sold_elem = item.select_one(selector)
                if sold_elem:
                    sold = sold_elem.get_text(strip=True)
                    break
            
            # Lokasi - multiple selectors
            location_selectors = [
                "div[data-sqe='location']", 
                ".zGGwiV", 
                ".ie3A\+n + div + div",
                ".shopee-item-card__text-location",
                ".shopee-search-item-result__item-location"
            ]
            location = "Tidak ditemukan"
            for selector in location_selectors:
                location_elem = item.select_one(selector)
                if location_elem:
                    location = location_elem.get_text(strip=True)
                    break
            
            # Rating
            rating_elem = item.select_one("div.shopee-rating-stars__lit, .shopee-rating-stars")
            if rating_elem:
                style = rating_elem.get('style', '')
                if 'width:' in style:
                    rating = style.split('width:')[-1].split(';')[0].strip()
                else:
                    rating = "Tidak ditemukan"
            else:
                rating = "Tidak ditemukan"
            
            # Link produk
            link_elem = item.select_one("a[href*='/product/']")
            product_link = "https://shopee.co.id" + link_elem.get('href', '') if link_elem else "N/A"
            
            return {
                'product_name': name,
                'price': price,
                'sold': sold,
                'location': location,
                'rating': rating,
                'product_link': product_link
            }
            
        except Exception as e:
            print(f"⚠️ Warning: Error extracting product data: {e}")
            return {
                'product_name': "Error",
                'price': "Error",
                'sold': "Error",
                'location': "Error",
                'rating': "Error",
                'product_link': "Error"
            }

    def scrape_products(self, keyword, max_page=1):
        """Scrape produk dari Shopee berdasarkan keyword"""
        print(f"🔍 Memulai scraping untuk keyword: '{keyword}'")
        print(f"📄 Jumlah halaman: {max_page}")
        
        all_products = []
        
        for page in range(max_page):
            current_page = page + 1
            print(f"\n📄 Scraping halaman {current_page}/{max_page}...")
            
            try:
                # Construct URL
                encoded_keyword = keyword.replace(' ', '%20')
                url = f"https://shopee.co.id/search?keyword={encoded_keyword}&page={page}"
                
                print(f"🌐 Mengakses: {url}")
                self.driver.get(url)
                
                # Wait for page to load - multiple selectors
                selectors = [
                    ".shopee-search-item-result__item", 
                    "[data-sqe='item']",
                    ".shopee-item-card",
                    ".shopee-search-item-result__item-card"
                ]
                
                items_found = False
                for selector in selectors:
                    try:
                        WebDriverWait(self.driver, 15).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                        )
                        items_found = True
                        break
                    except TimeoutException:
                        continue
                
                if not items_found:
                    print("⚠️ Tidak ada elemen produk ditemukan pada halaman ini")
                    continue
                
                # Scroll untuk memuat semua konten
                self.slow_scroll()
                
                # Parse HTML
                soup = BeautifulSoup(self.driver.page_source, 'html.parser')
                
                # Find product items - multiple selectors
                items = []
                for selector in selectors:
                    items = soup.select(selector)
                    if items:
                        break
                
                if not items:
                    print("⚠️ Tidak ada produk ditemukan pada halaman ini")
                    continue
                
                print(f"📦 Ditemukan {len(items)} produk pada halaman {current_page}")
                
                # Extract data dari setiap produk
                page_products = []
                for i, item in enumerate(items, 1):
                    product_data = self.extract_product_data(item)
                    product_data['kategori'] = keyword
                    product_data['halaman'] = current_page
                    page_products.append(product_data)
                    
                    if i % 10 == 0:
                        print(f"   ✅ Proses {i}/{len(items)} produk")
                
                all_products.extend(page_products)
                print(f"✅ Halaman {current_page} selesai: {len(page_products)} produk")
                
                # Delay antara halaman
                if current_page < max_page:
                    delay = random.uniform(3, 6)
                    print(f"⏳ Menunggu {delay:.1f} detik sebelum halaman berikutnya...")
                    time.sleep(delay)
                
            except TimeoutException:
                print(f"❌ Timeout pada halaman {current_page}")
                continue
            except Exception as e:
                print(f"❌ Error pada halaman {current_page}: {e}")
                continue
        
        return all_products

    def save_to_csv(self, products, filename):
        """Simpan data ke file CSV"""
        if not products:
            print("❌ Tidak ada data untuk disimpan")
            return False
        
        try:
            df = pd.DataFrame(products)
            
            # Clean filename
            if not filename.endswith('.csv'):
                filename += '.csv'
            
            # Save to CSV
            df.to_csv(filename, index=False, encoding='utf-8-sig')
            
            print(f"✅ Data berhasil disimpan ke: {filename}")
            print(f"📊 Total produk: {len(products)}")
            print(f"📋 Kolom: {', '.join(df.columns)}")
            
            # Show sample data
            print("\n📋 Sample data:")
            print(df.head().to_string(index=False))
            
            return True
            
        except Exception as e:
            print(f"❌ Error saving to CSV: {e}")
            return False

    def run_scraper(self, keyword, max_page=1, output_file="hasil_scraping.csv"):
        """Jalankan scraper lengkap"""
        print("=" * 60)
        print("🛒 SHOPEE SCRAPER - GOOGLE COLAB VERSION")
        print("=" * 60)
        
        try:
            # Setup driver
            if not self.setup_driver():
                return False
            
            # Load cookies untuk login
            if not self.load_cookies():
                print("⚠️ Warning: Gagal load cookies, melanjutkan tanpa login...")
            
            # Scrape products
            products = self.scrape_products(keyword, max_page)
            
            if not products:
                print("❌ Tidak ada produk ditemukan")
                return False
            
            # Save to CSV
            success = self.save_to_csv(products, output_file)
            
            return success
            
        except Exception as e:
            print(f"❌ Error dalam scraping: {e}")
            return False
        
        finally:
            # Cleanup
            if self.driver:
                print("🧹 Cleaning up...")
                self.driver.quit()

# ========================================
# KONFIGURASI SCRAPING
# ========================================
# Ubah parameter di bawah ini sesuai kebutuhan

# Kata kunci produk yang ingin di-scrape
KEYWORD = "laptop gaming"  # Ganti dengan kata kunci yang diinginkan

# Jumlah halaman yang ingin di-scrape
MAX_PAGE = 2  # Ganti dengan jumlah halaman yang diinginkan

# Nama file output
OUTPUT_FILE = "hasil_scraping_shopee.csv"  # Ganti dengan nama file yang diinginkan

# ========================================
# JALANKAN SCRAPER
# ========================================
if __name__ == "__main__":
    print(f"🎯 Konfigurasi Scraping:")
    print(f"   🔍 Keyword: {KEYWORD}")
    print(f"   📄 Jumlah halaman: {MAX_PAGE}")
    print(f"   💾 File output: {OUTPUT_FILE}")
    print()
    
    # Run scraper
    scraper = ShopeeScraperColab()
    success = scraper.run_scraper(KEYWORD, MAX_PAGE, OUTPUT_FILE)
    
    if success:
        print("\n🎉 Scraping selesai dengan sukses!")
        print(f"📁 File hasil: {OUTPUT_FILE}")
    else:
        print("\n❌ Scraping gagal!")