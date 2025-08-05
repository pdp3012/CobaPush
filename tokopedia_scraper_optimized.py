# -*- coding: utf-8 -*-
"""
Tokopedia Scraper Otomatis dengan Scrolling - Optimized Version
Dosen Data Mining - 30 Tahun Pengalaman
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
from urllib.parse import quote, urljoin
from datetime import datetime
import re
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

class TokopediaScraperOptimized:
    def __init__(self, use_selenium=True, headless=True):
        """
        Inisialisasi scraper dengan opsi Selenium untuk scrolling otomatis
        """
        self.use_selenium = use_selenium
        self.headless = headless
        self.driver = None
        
        # Headers untuk requests
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Cache-Control': 'max-age=0'
        }
        
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        
        # Inisialisasi Selenium jika diperlukan
        if self.use_selenium:
            self._setup_selenium()

    def _setup_selenium(self):
        """Setup Selenium WebDriver dengan optimasi"""
        try:
            chrome_options = Options()
            
            if self.headless:
                chrome_options.add_argument('--headless')
            
            # Optimasi performa
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--disable-extensions')
            chrome_options.add_argument('--disable-plugins')
            chrome_options.add_argument('--disable-images')  # Tidak load gambar untuk kecepatan
            chrome_options.add_argument('--disable-javascript')  # Opsional, bisa di-comment jika perlu JS
            chrome_options.add_argument('--disable-blink-features=AutomationControlled')
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            # User agent yang lebih realistis
            chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
            
            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
        except Exception as e:
            print(f"⚠️ Selenium setup gagal: {e}")
            print("🔄 Fallback ke requests mode...")
            self.use_selenium = False

    def build_search_url(self, keyword, page=1):
        """Membangun URL pencarian Tokopedia"""
        encoded_keyword = quote(keyword)
        if page == 1:
            return f"https://www.tokopedia.com/search?st=&q={encoded_keyword}&srp_component_id=02.01.00.00&srp_page_id=&srp_page_title=&navsource="
        else:
            return f"https://www.tokopedia.com/search?st=&q={encoded_keyword}&srp_component_id=02.01.00.00&srp_page_id=&srp_page_title=&navsource=&page={page}"

    def scroll_page_automatically(self, target_products, scroll_pause_time=2):
        """
        Scroll otomatis hingga target produk tercapai
        """
        print("🔄 Memulai scrolling otomatis...")
        
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        products_found = 0
        scroll_attempts = 0
        max_scroll_attempts = 50  # Maksimal scroll attempts
        
        while products_found < target_products and scroll_attempts < max_scroll_attempts:
            # Scroll ke bawah
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            
            # Tunggu loading
            time.sleep(scroll_pause_time)
            
            # Hitung produk yang ditemukan
            try:
                # Coba berbagai selector untuk produk
                product_selectors = [
                    '[data-testid="master-product-card"]',
                    '[data-testid*="product"]',
                    'div[class*="product"]',
                    'div[class*="card"]',
                    'div[class*="item"]'
                ]
                
                for selector in product_selectors:
                    products = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if products:
                        products_found = len(products)
                        break
                
                print(f"📊 Scroll {scroll_attempts + 1}: {products_found} produk ditemukan")
                
            except Exception as e:
                print(f"⚠️ Error menghitung produk: {e}")
            
            # Cek apakah ada perubahan tinggi halaman
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                # Coba scroll lagi atau cek apakah sudah di akhir
                time.sleep(scroll_pause_time * 2)
                new_height = self.driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    print("🏁 Sudah mencapai akhir halaman")
                    break
            
            last_height = new_height
            scroll_attempts += 1
            
            # Random delay untuk menghindari deteksi
            time.sleep(random.uniform(1, 3))
        
        print(f"✅ Scrolling selesai. Total produk ditemukan: {products_found}")
        return products_found

    def extract_products_from_page(self):
        """Ekstrak semua produk dari halaman yang sudah di-scroll"""
        products = []
        
        try:
            # Dapatkan HTML setelah scrolling
            page_source = self.driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')
            
            # Cari container produk
            containers = self.find_product_containers(soup)
            
            print(f"🔍 Menemukan {len(containers)} container produk")
            
            # Ekstrak data dari setiap container
            for i, container in enumerate(containers):
                product_data = self.extract_single_product_robust(container)
                if product_data and self.validate_product_data(product_data):
                    products.append(product_data)
                    
                    if (i + 1) % 10 == 0:
                        print(f"📦 Diproses: {i + 1}/{len(containers)} produk")
            
        except Exception as e:
            print(f"❌ Error ekstraksi produk: {e}")
        
        return products

    def find_product_containers(self, soup):
        """Mencari container produk dengan strategi yang lebih canggih"""
        containers = []
        
        # Strategi 1: Selector umum
        container_selectors = [
            '[data-testid="master-product-card"]',
            '[data-testid*="product"]',
            'div[class*="product"]',
            'div[class*="card"]',
            'div[class*="item"]',
            'div[class*="ProductCard"]',
            'div[class*="product-card"]'
        ]
        
        for selector in container_selectors:
            elements = soup.select(selector)
            if elements:
                containers = elements
                print(f"✅ Menggunakan selector: {selector}")
                break
        
        # Strategi 2: Berdasarkan pola link & harga
        if not containers:
            all_divs = soup.find_all('div')
            for div in all_divs:
                links = div.find_all('a', href=True)
                price_texts = div.find_all(text=re.compile(r'Rp[\d,.\s]+'))
                if links and price_texts:
                    for link in links:
                        if '/p/' in link.get('href', ''):
                            containers.append(div)
                            break
        
        # Strategi 3: Berdasarkan elemen harga
        if not containers:
            price_elements = soup.find_all(text=re.compile(r'Rp[\d,.\s]+'))
            parent_containers = set()
            for price_element in price_elements:
                parent = price_element.parent
                for _ in range(5):
                    if parent and parent.name == 'div':
                        text_content = parent.get_text()
                        if len(text_content) > 50 and 'Rp' in text_content:
                            parent_containers.add(parent)
                            break
                    parent = parent.parent if parent else None
            containers = list(parent_containers)
        
        return containers

    def extract_product_name(self, element):
        """Ekstrak nama produk dengan strategi yang lebih robust"""
        # Strategi 1: Panjang teks
        spans = element.find_all('span')
        for span in spans:
            text = span.get_text(strip=True)
            if 10 < len(text) < 200 and 'Rp' not in text and not re.match(r'^[\d.,]+$', text):
                return text
        
        # Strategi 2: Link produk
        links = element.find_all('a', href=True)
        for link in links:
            if '/p/' in link.get('href', ''):
                text = link.get_text(strip=True)
                if 10 < len(text) < 200:
                    return text
        
        # Strategi 3: Teks terpanjang
        all_texts = [tag.get_text(strip=True) for tag in element.find_all(['span', 'p', 'h1', 'h2', 'h3', 'a'])]
        valid_texts = [t for t in all_texts if 10 < len(t) < 200 and 'Rp' not in t and not re.match(r'^[\d.,]+$', t)]
        return max(valid_texts, key=len) if valid_texts else "Nama tidak ditemukan"

    def extract_price(self, element):
        """Ekstrak harga dengan regex yang lebih akurat"""
        # Strategi 1: Regex yang lebih spesifik
        price_pattern = re.compile(r'Rp[\s]*[\d,.\s]+')
        all_text = element.get_text()
        price_matches = price_pattern.findall(all_text)
        if price_matches:
            return price_matches[0].strip()
        
        # Strategi 2: Tag langsung
        for tag in element.find_all(['div', 'span']):
            text = tag.get_text(strip=True)
            if text.startswith('Rp') and len(text) < 50:
                return text
        
        return "Harga tidak ditemukan"

    def extract_rating(self, element):
        """Ekstrak rating"""
        # Strategi 1: Regex
        rating_pattern = re.compile(r'\b([1-5]\.[0-9])\b')
        all_text = element.get_text()
        rating_matches = rating_pattern.findall(all_text)
        if rating_matches:
            return rating_matches[0]
        
        # Strategi 2: Format angka
        for tag in element.find_all(['div', 'span']):
            text = tag.get_text(strip=True)
            if re.match(r'^[1-5]\.[0-9]$', text):
                return text
        
        return ""

    def extract_sold_count(self, element):
        """Ekstrak jumlah terjual"""
        sold_patterns = [
            r'(\d+)\s*terjual', r'(\d+)\s*sold',
            r'terjual\s*(\d+)', r'sold\s*(\d+)',
            r'(\d+[kKmM]?)\s*terjual'
        ]
        all_text = element.get_text().lower()
        for pattern in sold_patterns:
            match = re.search(pattern, all_text)
            if match:
                return match.group(1) + " terjual"
        return ""

    def extract_shop_name(self, element):
        """Ekstrak nama toko"""
        spans = element.find_all('span')
        texts = [span.get_text(strip=True) for span in spans]
        possible_shop_names = [
            text for text in texts
            if 3 < len(text) < 100 and
            not re.search(r'Rp|terjual|\d+\.\d+|rating', text, re.IGNORECASE) and
            not re.match(r'^[\d.,]+$', text)
        ]
        return possible_shop_names[-1] if possible_shop_names else ""

    def extract_product_link(self, element):
        """Ekstrak link produk"""
        links = element.find_all('a', href=True)
        for a_tag in links:
            href = a_tag.get('href', '')
            if '/p/' in href:
                return 'https://www.tokopedia.com' + href if href.startswith('/') else href
        return ""

    def extract_single_product_robust(self, element):
        """Ekstrak data produk secara robust"""
        try:
            return {
                'nama_produk': self.extract_product_name(element),
                'harga': self.extract_price(element),
                'rating': self.extract_rating(element),
                'jumlah_terjual': self.extract_sold_count(element),
                'nama_toko': self.extract_shop_name(element),
                'link_produk': self.extract_product_link(element),
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
        except Exception as e:
            print(f"⚠️ Error ekstraksi produk: {e}")
            return None

    def validate_product_data(self, product_data):
        """Validasi data produk minimal"""
        if not product_data:
            return False
        has_name = product_data.get('nama_produk') and product_data['nama_produk'] != "Nama tidak ditemukan"
        has_price = product_data.get('harga') and product_data['harga'] != "Harga tidak ditemukan"
        return has_name or has_price

    def scrape_products_with_scrolling(self, keyword, target_products):
        """
        Scraping produk dengan scrolling otomatis
        """
        if not self.use_selenium or not self.driver:
            print("❌ Selenium tidak tersedia, menggunakan mode requests...")
            return self.scrape_products_fallback(keyword, target_products)
        
        try:
            print(f"🚀 Memulai scraping dengan scrolling untuk '{keyword}' (Target: {target_products} produk)")
            
            # Buka halaman pencarian
            search_url = self.build_search_url(keyword)
            self.driver.get(search_url)
            
            # Tunggu halaman load
            time.sleep(3)
            
            # Scroll otomatis hingga target tercapai
            self.scroll_page_automatically(target_products)
            
            # Ekstrak semua produk
            products = self.extract_products_from_page()
            
            # Hapus duplikat
            unique_products = self.remove_duplicates(products)
            
            print(f"🎯 Scraping selesai! Total produk unik: {len(unique_products)}")
            return unique_products[:target_products]
            
        except Exception as e:
            print(f"❌ Error dalam scraping dengan scrolling: {e}")
            print("🔄 Fallback ke mode requests...")
            return self.scrape_products_fallback(keyword, target_products)

    def scrape_products_fallback(self, keyword, target_products):
        """Fallback scraping menggunakan requests"""
        all_products = []
        page = 1
        max_pages = min(50, (target_products // 20) + 5)
        
        print(f"🔄 Menggunakan mode requests fallback...")
        
        while len(all_products) < target_products and page <= max_pages:
            print(f"📄 Memproses halaman {page}...")
            current_url = self.build_search_url(keyword, page)
            
            try:
                time.sleep(random.uniform(1, 3))
                response = self.session.get(current_url, timeout=15)
                response.raise_for_status()
                
                if response.status_code == 200 and len(response.content) > 1000:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    if 'tidak ditemukan' in soup.get_text().lower():
                        print(f"🔍 Halaman {page}: Tidak ada hasil pencarian")
                        break
                    
                    containers = self.find_product_containers(soup)
                    if containers:
                        page_products = []
                        for container in containers:
                            product_data = self.extract_single_product_robust(container)
                            if product_data and self.validate_product_data(product_data):
                                page_products.append(product_data)
                        
                        if page_products:
                            all_products.extend(page_products)
                            print(f"✅ Halaman {page}: {len(page_products)} produk ditemukan (Total: {len(all_products)})")
                        else:
                            print(f"⚠️ Halaman {page}: Tidak ada produk valid")
                    else:
                        print(f"❌ Halaman {page}: Tidak ditemukan container produk")
                
            except Exception as e:
                print(f"❌ Error halaman {page}: {e}")
            
            page += 1
            if page <= max_pages:
                time.sleep(random.uniform(2, 5))
        
        unique_products = self.remove_duplicates(all_products)
        return unique_products[:target_products]

    def remove_duplicates(self, products):
        """Hapus produk duplikat"""
        seen = set()
        unique_products = []
        
        for product in products:
            # Buat key unik berdasarkan nama dan harga
            key = (product.get('nama_produk', ''), product.get('harga', ''))
            if key not in seen:
                seen.add(key)
                unique_products.append(product)
        
        return unique_products

    def save_to_csv(self, products, keyword):
        """Menyimpan data ke file CSV"""
        if not products:
            print("⚠️ Tidak ada data untuk disimpan")
            return False
        
        # Buat nama file otomatis
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'tokopedia_{keyword.replace(" ", "_")}_{len(products)}produk_{timestamp}.csv'
        
        try:
            df = pd.DataFrame(products)
            
            # Bersihkan data
            for col in df.columns:
                if col != 'timestamp':
                    df[col] = df[col].astype(str).str.strip()
            
            # Hapus duplikat berdasarkan nama & harga
            df = df.drop_duplicates(subset=['nama_produk', 'harga'], keep='first')
            
            df.to_csv(filename, index=False, encoding='utf-8-sig')
            print(f"💾 Data berhasil disimpan ke: {filename}")
            print(f"📊 Jumlah produk unik: {len(df)}")
            
            # Tampilkan statistik
            self.show_statistics(df)
            
            return True
            
        except Exception as e:
            print(f"❌ Error menyimpan CSV: {e}")
            return False

    def show_statistics(self, df):
        """Tampilkan statistik data"""
        print("\n📈 STATISTIK DATA:")
        print("=" * 40)
        print(f"Total produk: {len(df)}")
        
        # Statistik harga
        price_col = df['harga'].str.extract(r'Rp\s*([\d,]+)')[0]
        if not price_col.empty:
            price_col = price_col.str.replace(',', '').astype(float)
            print(f"Harga rata-rata: Rp {price_col.mean():,.0f}")
            print(f"Harga minimum: Rp {price_col.min():,.0f}")
            print(f"Harga maksimum: Rp {price_col.max():,.0f}")
        
        # Statistik rating
        rating_col = df['rating'].str.extract(r'([\d.]+)')[0]
        if not rating_col.empty:
            rating_col = rating_col.astype(float)
            print(f"Rating rata-rata: {rating_col.mean():.1f}")
        
        # Top toko
        top_shops = df['nama_toko'].value_counts().head(5)
        print(f"\n🏪 Top 5 Toko:")
        for shop, count in top_shops.items():
            print(f"  {shop}: {count} produk")

    def cleanup(self):
        """Bersihkan resources"""
        if self.driver:
            try:
                self.driver.quit()
            except:
                pass

def main():
    """Fungsi utama dengan optimasi"""
    print("="*70)
    print("🤖 TOKOPEDIA SCRAPER OTOMATIS - VERSION OPTIMIZED")
    print("📚 Dosen Data Mining - 30 Tahun Pengalaman")
    print("="*70)
    
    # Input otomatis dari user
    keyword = input("🔍 Masukkan keyword pencarian: ").strip()
    if not keyword:
        print("❌ Keyword tidak boleh kosong!")
        return

    while True:
        try:
            target_products = int(input("🔢 Jumlah produk yang diinginkan: "))
            if target_products > 0:
                break
            else:
                print("❌ Jumlah harus positif!")
        except ValueError:
            print("❌ Masukkan angka yang valid!")

    # Opsi scraping
    print("\n⚙️ Pilih mode scraping:")
    print("1. Scrolling Otomatis (Recommended)")
    print("2. Requests Fallback")
    
    mode_choice = input("Pilihan (1/2): ").strip()
    use_selenium = mode_choice != "2"

    # Inisialisasi dan jalankan scraper
    scraper = TokopediaScraperOptimized(use_selenium=use_selenium, headless=True)
    
    try:
        if use_selenium:
            products = scraper.scrape_products_with_scrolling(keyword, target_products)
        else:
            products = scraper.scrape_products_fallback(keyword, target_products)
        
        if products:
            scraper.save_to_csv(products, keyword)
        else:
            print("\n❌ Tidak ada produk yang berhasil di-scrape.")
    
    finally:
        scraper.cleanup()

if __name__ == "__main__":
    # Instal dependensi jika belum ada
    try:
        import subprocess
        import sys
        
        required_packages = ['requests', 'beautifulsoup4', 'pandas', 'selenium']
        for package in required_packages:
            try:
                __import__(package.replace('-', '_'))
            except ImportError:
                print(f"📦 Installing {package}...")
                subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", package])
        
        print("✅ Semua dependensi siap!")
        
    except Exception as e:
        print(f"⚠️ Error instalasi dependensi: {e}")
        print("🔄 Lanjutkan dengan dependensi yang tersedia...")
    
    main()