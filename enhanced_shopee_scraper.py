"""
Enhanced Shopee Scraper
Dikembangkan oleh: Dosen Data Mining dengan 30 tahun pengalaman
Fitur: Auto-login via cookies, robust scraping, error handling, dan data validation
"""

import json
import time
import random
import logging
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
import os

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scraping.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class ShopeeScraper:
    def __init__(self, headless=True, cookies_file="cookies.json"):
        """
        Inisialisasi Shopee Scraper
        
        Args:
            headless (bool): Mode headless untuk browser
            cookies_file (str): Path ke file cookies
        """
        self.cookies_file = cookies_file
        self.driver = None
        self.headless = headless
        self.wait_timeout = 20
        self.retry_attempts = 3
        
    def setup_driver(self):
        """Setup Chrome WebDriver dengan konfigurasi optimal"""
        try:
            options = webdriver.ChromeOptions()
            
            if self.headless:
                options.add_argument("--headless=new")
            
            # Konfigurasi untuk stabilitas dan performa
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")
            options.add_argument("--disable-extensions")
            options.add_argument("--disable-plugins")
            options.add_argument("--disable-images")  # Mempercepat loading
            options.add_argument("--window-size=1920,1080")
            options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36")
            
            # Tambahan untuk menghindari deteksi bot
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=options)
            
            # Execute script untuk menghilangkan webdriver property
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            logger.info("✅ WebDriver berhasil diinisialisasi")
            return True
            
        except Exception as e:
            logger.error(f"❌ Gagal setup WebDriver: {str(e)}")
            return False
    
    def load_cookies(self):
        """Load cookies dari file untuk auto-login"""
        try:
            if not os.path.exists(self.cookies_file):
                logger.warning(f"⚠️ File cookies {self.cookies_file} tidak ditemukan. Scraping akan dilakukan tanpa login.")
                return False
            
            # Buka halaman Shopee terlebih dahulu
            self.driver.get("https://shopee.co.id")
            time.sleep(3)
            
            with open(self.cookies_file, 'r', encoding='utf-8') as f:
                cookies = json.load(f)
                
            for cookie in cookies:
                try:
                    # Normalisasi cookie data
                    cookie_data = cookie.copy()
                    
                    # Handle sameSite attribute
                    if 'sameSite' in cookie_data:
                        if cookie_data['sameSite'] == 'unspecified':
                            cookie_data['sameSite'] = 'Strict'
                    
                    # Convert expirationDate to expiry
                    if 'expirationDate' in cookie_data:
                        cookie_data['expiry'] = int(cookie_data['expirationDate'])
                        del cookie_data['expirationDate']
                    
                    # Remove problematic fields
                    for field in ['hostOnly', 'storeId', 'id']:
                        if field in cookie_data:
                            del cookie_data[field]
                    
                    self.driver.add_cookie(cookie_data)
                    
                except Exception as e:
                    logger.warning(f"⚠️ Gagal menambahkan cookie {cookie.get('name', 'unknown')}: {str(e)}")
                    continue
            
            # Refresh halaman untuk menerapkan cookies
            self.driver.refresh()
            time.sleep(3)
            
            logger.info("✅ Login otomatis via cookies berhasil!")
            return True
            
        except Exception as e:
            logger.error(f"❌ Gagal load cookies: {str(e)}")
            return False
    
    def slow_scroll(self, scroll_pause_time=0.5):
        """Scroll halaman secara perlahan untuk memuat konten"""
        try:
            # Get scroll height
            last_height = self.driver.execute_script("return document.body.scrollHeight")
            
            while True:
                # Scroll down dengan interval
                for i in range(0, last_height, 400):
                    self.driver.execute_script(f"window.scrollTo(0, {i});")
                    time.sleep(random.uniform(0.2, 0.5))
                
                # Wait to load page
                time.sleep(scroll_pause_time)
                
                # Calculate new scroll height and compare with last scroll height
                new_height = self.driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height
                
            logger.info("✅ Scroll halaman selesai")
            
        except Exception as e:
            logger.warning(f"⚠️ Gagal melakukan scroll: {str(e)}")
    
    def extract_product_data(self, item):
        """Extract data produk dari elemen HTML"""
        try:
            # Nama produk dengan multiple selector fallback
            name_selectors = [
                "div.line-clamp-2",
                "div[data-sqe='name']",
                ".ie3A\+n",
                "div[data-sqe='link']"
            ]
            name = "N/A"
            for selector in name_selectors:
                name_elem = item.select_one(selector)
                if name_elem:
                    name = name_elem.get_text(strip=True)
                    break
            
            # Harga dengan multiple selector fallback
            price_selectors = [
                "span.currency--GVKjl",
                "div[data-sqe='price']",
                ".ZEgDH9",
                "span[data-sqe='price']"
            ]
            price = "N/A"
            for selector in price_selectors:
                price_elem = item.select_one(selector)
                if price_elem:
                    price = price_elem.get_text(strip=True)
                    break
            
            # Jumlah terjual
            sold_selectors = [
                "div[data-sqe='sold']",
                ".r6HknA",
                "div[data-sqe='sales']"
            ]
            sold = "Tidak ditemukan"
            for selector in sold_selectors:
                sold_elem = item.select_one(selector)
                if sold_elem:
                    sold = sold_elem.get_text(strip=True)
                    break
            
            # Lokasi
            location_selectors = [
                "div[data-sqe='location']",
                ".zGGwiV",
                "div[data-sqe='shop_location']"
            ]
            location = "Tidak ditemukan"
            for selector in location_selectors:
                location_elem = item.select_one(selector)
                if location_elem:
                    location = location_elem.get_text(strip=True)
                    break
            
            # Rating
            rating_selectors = [
                "div.shopee-rating-stars__lit",
                ".shopee-rating-stars__stars",
                "div[data-sqe='rating']"
            ]
            rating = "Tidak ditemukan"
            for selector in rating_selectors:
                rating_elem = item.select_one(selector)
                if rating_elem:
                    style_attr = rating_elem.get('style', '')
                    if 'width:' in style_attr:
                        rating = style_attr.split('width:')[-1].split(';')[0].strip()
                    break
            
            # Link produk
            link = "N/A"
            link_elem = item.select_one("a[data-sqe='link']")
            if link_elem:
                link = link_elem.get('href', 'N/A')
                if link.startswith('/'):
                    link = f"https://shopee.co.id{link}"
            
            return {
                'product_name': name,
                'price': price,
                'sold': sold,
                'location': location,
                'rating': rating,
                'product_link': link,
                'scraped_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
        except Exception as e:
            logger.warning(f"⚠️ Gagal extract data produk: {str(e)}")
            return {
                'product_name': 'N/A',
                'price': 'N/A',
                'sold': 'N/A',
                'location': 'N/A',
                'rating': 'N/A',
                'product_link': 'N/A',
                'scraped_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
    
    def scrape_page(self, keyword, page_num):
        """Scrape satu halaman hasil pencarian"""
        try:
            # Construct URL
            url = f"https://shopee.co.id/search?keyword={keyword.replace(' ', '%20')}&page={page_num-1}"
            logger.info(f"🔍 Mengakses: {url}")
            
            self.driver.get(url)
            
            # Wait for page to load
            try:
                WebDriverWait(self.driver, self.wait_timeout).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "shopee-search-item-result__item"))
                )
            except TimeoutException:
                logger.warning(f"⚠️ Timeout menunggu halaman {page_num} load")
                return []
            
            # Scroll untuk memuat semua konten
            self.slow_scroll()
            
            # Parse HTML
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            
            # Find product items
            items = soup.select(".shopee-search-item-result__item")
            logger.info(f"📦 Ditemukan {len(items)} produk di halaman {page_num}")
            
            products = []
            for item in items:
                product_data = self.extract_product_data(item)
                product_data['kategori'] = keyword
                product_data['halaman'] = page_num
                products.append(product_data)
            
            return products
            
        except Exception as e:
            logger.error(f"❌ Gagal scrape halaman {page_num}: {str(e)}")
            return []
    
    def scrape_shopee(self, keyword, max_page, output_file):
        """Main scraping function"""
        try:
            # Setup driver
            if not self.setup_driver():
                return False
            
            # Load cookies untuk login
            self.load_cookies()
            
            all_products = []
            
            for page in range(1, max_page + 1):
                logger.info(f"🔄 Scraping halaman {page}/{max_page}...")
                
                # Retry mechanism
                for attempt in range(self.retry_attempts):
                    products = self.scrape_page(keyword, page)
                    if products:
                        all_products.extend(products)
                        break
                    else:
                        logger.warning(f"⚠️ Attempt {attempt + 1} gagal untuk halaman {page}")
                        if attempt < self.retry_attempts - 1:
                            time.sleep(random.uniform(5, 10))
                
                # Random delay antara halaman
                if page < max_page:
                    delay = random.uniform(3, 6)
                    logger.info(f"⏳ Menunggu {delay:.1f} detik...")
                    time.sleep(delay)
            
            # Save results
            if all_products:
                df = pd.DataFrame(all_products)
                
                # Data cleaning
                df = df.drop_duplicates(subset=['product_name', 'price'])
                df = df[df['product_name'] != 'N/A']
                
                # Save to CSV
                df.to_csv(output_file, index=False, encoding='utf-8-sig')
                
                logger.info(f"✅ Scraping selesai! Total {len(df)} produk disimpan ke {output_file}")
                logger.info(f"📊 Statistik: {len(df)} produk unik dari {max_page} halaman")
                
                # Show sample data
                print("\n" + "="*50)
                print("SAMPLE DATA HASIL SCRAPING:")
                print("="*50)
                print(df.head().to_string(index=False))
                print("="*50)
                
                return True
            else:
                logger.error("❌ Tidak ada produk ditemukan")
                return False
                
        except Exception as e:
            logger.error(f"❌ Error dalam scraping: {str(e)}")
            return False
        
        finally:
            if self.driver:
                self.driver.quit()
                logger.info("🔚 WebDriver ditutup")

def main():
    """Main function untuk menjalankan scraper"""
    print("🛍️  ENHANCED SHOPEE SCRAPER")
    print("="*50)
    print("Dikembangkan oleh: Dosen Data Mining (30 tahun pengalaman)")
    print("="*50)
    
    # Input parameters
    keyword = input("🔍 Masukkan kata kunci pencarian: ").strip()
    if not keyword:
        print("❌ Kata kunci tidak boleh kosong!")
        return
    
    try:
        max_page = int(input("📄 Jumlah halaman yang akan di-scrape: "))
        if max_page <= 0:
            print("❌ Jumlah halaman harus lebih dari 0!")
            return
    except ValueError:
        print("❌ Jumlah halaman harus berupa angka!")
        return
    
    output_file = input("💾 Nama file output (misal: hasil.csv): ").strip()
    if not output_file:
        output_file = f"shopee_{keyword}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    elif not output_file.endswith('.csv'):
        output_file += '.csv'
    
    # Headless mode option
    headless_input = input("🖥️  Mode headless? (y/n, default: y): ").strip().lower()
    headless = headless_input != 'n'
    
    print("\n🚀 Memulai scraping...")
    print("="*50)
    
    # Initialize and run scraper
    scraper = ShopeeScraper(headless=headless)
    success = scraper.scrape_shopee(keyword, max_page, output_file)
    
    if success:
        print(f"\n🎉 SCRAPING BERHASIL!")
        print(f"📁 File tersimpan: {output_file}")
        print(f"📊 Cek file log: scraping.log")
    else:
        print(f"\n💥 SCRAPING GAGAL!")
        print(f"📊 Cek file log: scraping.log untuk detail error")

if __name__ == "__main__":
    main()