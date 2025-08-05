# -*- coding: utf-8 -*-
"""
Tokopedia Scraper Otomatis dengan Scrolling - FIXED FOR GOOGLE COLAB
Dosen Data Mining - 30 Tahun Pengalaman
"""

# Instal dependensi yang diperlukan
print("🚀 Menyiapkan environment...")
try:
    import subprocess
    import sys
    
    # Instal paket sistem untuk Chrome di Colab
    print("   ⏳ Menginstal Chrome dan ChromeDriver...")
    subprocess.run(['apt', 'update'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(['apt', 'install', '-y', 'wget', 'unzip'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # Download dan install Chrome
    subprocess.run(['wget', '-q', '-O', '-', 'https://dl.google.com/linux/linux_signing_key.pub', '|', 'apt-key', 'add', '-'], shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(['echo', '"deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main"', '>', '/etc/apt/sources.list.d/google-chrome.list'], shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(['apt', 'update'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(['apt', 'install', '-y', 'google-chrome-stable'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # Download ChromeDriver yang sesuai
    chrome_version = subprocess.check_output(['google-chrome', '--version'], text=True).strip().split()[-1].split('.')[0]
    chromedriver_version = chrome_version
    subprocess.run(['wget', '-q', f'https://chromedriver.storage.googleapis.com/LATEST_RELEASE_{chromedriver_version}'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # Download dan extract ChromeDriver
    subprocess.run(['wget', '-q', f'https://chromedriver.storage.googleapis.com/{chromedriver_version}/chromedriver_linux64.zip'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(['unzip', '-q', 'chromedriver_linux64.zip'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(['chmod', '+x', 'chromedriver'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(['mv', 'chromedriver', '/usr/local/bin/'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # Instal paket Python
    print("   ⏳ Menginstal paket Python...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", 
                          "selenium==4.15.2", "beautifulsoup4", "pandas", 
                          "webdriver-manager==4.0.1", "requests", "lxml"])
    print("✅ Environment siap!")
except Exception as e:
    print(f"⚠️ Peringatan setup awal: {e}")
    print("💡 Melanjutkan dengan dependensi yang tersedia...")

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
from urllib.parse import quote
from datetime import datetime
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import os

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
        """Setup Selenium WebDriver dengan penanganan error yang komprehensif"""
        print("🔧 Menginisialisasi Selenium WebDriver...")
        try:
            chrome_options = Options()
            if self.headless:
                chrome_options.add_argument('--headless=new')
            
            # Optimasi performa untuk Colab
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--disable-extensions')
            chrome_options.add_argument('--disable-plugins')
            chrome_options.add_argument('--disable-images')
            chrome_options.add_argument('--disable-blink-features=AutomationControlled')
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
            
            # METODE 1: Gunakan ChromeDriver sistem Colab
            print("   📥 Mencoba ChromeDriver sistem...")
            try:
                service = Service('/usr/local/bin/chromedriver')
                self.driver = webdriver.Chrome(service=service, options=chrome_options)
                self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
                print("   ✅ WebDriver berhasil diinisialisasi dengan ChromeDriver sistem.")
                return
            except Exception as e1:
                print(f"   ⚠️ ChromeDriver sistem gagal: {str(e1)[:100]}...")
                
            # METODE 2: Gunakan ChromeDriverManager
            print("   📥 Mencoba ChromeDriverManager...")
            try:
                service = Service(ChromeDriverManager().install())
                self.driver = webdriver.Chrome(service=service, options=chrome_options)
                self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
                print("   ✅ WebDriver berhasil diinisialisasi dengan ChromeDriverManager.")
                return
            except Exception as e2:
                print(f"   ⚠️ ChromeDriverManager gagal: {str(e2)[:100]}...")
                
            # METODE 3: Inisialisasi dasar
            print("   📥 Mencoba inisialisasi dasar...")
            try:
                self.driver = webdriver.Chrome(options=chrome_options)
                self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
                print("   ✅ WebDriver berhasil diinisialisasi dengan metode dasar.")
                return
            except Exception as e3:
                print(f"   ⚠️ Inisialisasi dasar gagal: {str(e3)[:100]}...")
                
            raise Exception("Semua metode inisialisasi gagal")
            
        except Exception as e:
            print(f"❌ Selenium setup gagal: {e}")
            print("💡 Solusi: Restart runtime Colab dan jalankan ulang.")
            print("🔄 Fallback ke mode requests...")
            self.use_selenium = False
            self.driver = None

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
        max_scroll_attempts = 50  # Batasi maksimal scroll
        no_new_content_count = 0
        max_no_new_content = 5
        
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
                        new_count = len(products)
                        if new_count > products_found:
                            products_found = new_count
                            no_new_content_count = 0  # Reset counter
                            break
                
                print(f"📊 Scroll {scroll_attempts + 1}: {products_found} produk ditemukan")
                
                # Cek apakah sudah mencapai target
                if products_found >= target_products:
                    print(f"🎯 Target {target_products} produk tercapai!")
                    break
                    
            except Exception as e:
                print(f"⚠️ Error menghitung produk: {e}")
            
            # Cek apakah ada perubahan tinggi halaman
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                no_new_content_count += 1
                print(f"   ⚠️ Tidak ada konten baru. Counter: {no_new_content_count}/{max_no_new_content}")
                
                # Jika sudah beberapa kali tidak ada konten baru, berhenti
                if no_new_content_count >= max_no_new_content:
                    print("🏁 Sudah mencapai akhir konten yang tersedia")
                    break
            else:
                no_new_content_count = 0  # Reset counter jika ada konten baru
                
            last_height = new_height
            scroll_attempts += 1
            
            # Random delay untuk menghindari deteksi
            time.sleep(random.uniform(1, 2))
            
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
                    # Tampilkan progress setiap 10 produk
                    if (i + 1) % 10 == 0 or (i + 1) == len(containers):
                        print(f"📦 Diproses: {i + 1}/{len(containers)} produk")
                        
        except Exception as e:
            print(f"❌ Error ekstraksi produk: {e}")
            import traceback
            traceback.print_exc()
            
        return products

    def find_product_containers(self, soup):
        """Mencari container produk dengan strategi yang lebih canggih"""
        containers = []
        
        # Strategi 1: Selector umum (prioritas tertinggi)
        container_selectors = [
            '[data-testid="master-product-card"]',
            '[data-testid*="product"]',
            'div[class*="ProductCard"]',
            'div[class*="product-card"]',
            'div[class*="product"]',
            'div[class*="card"]'
        ]
        
        for selector in container_selectors:
            elements = soup.select(selector)
            if elements:
                containers = elements
                break
                
        # Strategi 2: Berdasarkan pola link & harga (fallback)
        if not containers:
            print("🔄 Menggunakan strategi fallback berbasis pola...")
            all_divs = soup.find_all('div')
            for div in all_divs:
                links = div.find_all('a', href=True)
                price_texts = div.find_all(text=re.compile(r'Rp[\d,.\s]+'))
                if links and price_texts:
                    for link in links:
                        if '/p/' in link.get('href', ''):
                            containers.append(div)
                            break
                            
        # Strategi 3: Berdasarkan elemen harga (fallback terakhir)
        if not containers:
            print("🔄 Menggunakan strategi fallback berbasis harga...")
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
            
        return containers[:100]  # Batasi maksimal 100 container untuk mencegah overload

    def extract_product_name(self, element):
        """Ekstrak nama produk dengan strategi yang lebih robust"""
        # Strategi 1: Cari teks panjang yang masuk akal
        all_texts = [tag.get_text(strip=True) for tag in element.find_all(['span', 'p', 'h1', 'h2', 'h3', 'a', 'div'])]
        valid_texts = [
            t for t in all_texts 
            if 10 < len(t) < 200 
            and 'Rp' not in t 
            and not re.match(r'^[\d.,]+$', t)
            and not any(keyword in t.lower() for keyword in ['terjual', 'sold', 'rating', 'bintang'])
        ]
        
        if valid_texts:
            # Kembalikan teks terpanjang yang valid
            return max(valid_texts, key=len)
            
        # Strategi 2: Cari link produk
        links = element.find_all('a', href=True)
        for link in links:
            if '/p/' in link.get('href', ''):
                text = link.get_text(strip=True)
                if 10 < len(text) < 200:
                    return text
                    
        return "Nama tidak ditemukan"

    def extract_price(self, element):
        """Ekstrak harga dengan regex yang lebih akurat"""
        # Strategi 1: Regex yang lebih spesifik
        price_pattern = re.compile(r'Rp[\s]*[\d.,]+')
        all_text = element.get_text()
        price_matches = price_pattern.findall(all_text)
        if price_matches:
            return price_matches[0].strip()
            
        # Strategi 2: Tag langsung dengan pola harga
        for tag in element.find_all(['div', 'span']):
            text = tag.get_text(strip=True)
            if text.startswith('Rp') and len(text) < 50 and re.search(r'[\d]', text):
                return text
                
        return "Harga tidak ditemukan"

    def extract_rating(self, element):
        """Ekstrak rating"""
        # Strategi 1: Regex untuk angka desimal (1.0-5.0)
        rating_pattern = re.compile(r'\b([1-5][.,]\d)\b')
        all_text = element.get_text()
        rating_matches = rating_pattern.findall(all_text)
        if rating_matches:
            return rating_matches[0].replace(',', '.')
            
        # Strategi 2: Format angka sederhana
        for tag in element.find_all(['div', 'span']):
            text = tag.get_text(strip=True)
            if re.match(r'^[1-5][.,]\d$', text):
                return text.replace(',', '.')
                
        return ""

    def extract_sold_count(self, element):
        """Ekstrak jumlah terjual"""
        sold_patterns = [
            r'(\d+)\s*terjual', 
            r'(\d+)\s*sold',
            r'terjual\s*(\d+)', 
            r'sold\s*(\d+)',
            r'(\d+[kKmM]?)\s*terjual',
            r'Telah\s+Terjual\s+(\d+[kKmM]?)'
        ]
        
        all_text = element.get_text().lower()
        for pattern in sold_patterns:
            match = re.search(pattern, all_text)
            if match:
                return match.group(1) + " terjual"
                
        return ""

    def extract_shop_name(self, element):
        """Ekstrak nama toko"""
        # Cari semua teks dalam element
        all_texts = [tag.get_text(strip=True) for tag in element.find_all(['span', 'div'])]
        
        # Filter teks yang mungkin nama toko
        possible_shop_names = [
            text for text in all_texts
            if 3 < len(text) < 50 
            and not re.search(r'Rp|terjual|\d+\.\d+|rating|bintang|%|diskon', text, re.IGNORECASE)
            and not re.match(r'^[\d.,]+$', text)
            and len(text.split()) <= 5  # Nama toko biasanya tidak terlalu panjang
        ]
        
        # Return nama toko yang paling mungkin (biasanya di akhir)
        return possible_shop_names[-1] if possible_shop_names else ""

    def extract_product_link(self, element):
        """Ekstrak link produk"""
        links = element.find_all('a', href=True)
        for a_tag in links:
            href = a_tag.get('href', '')
            if '/p/' in href and 'tokopedia.com' in href:
                return href
            elif '/p/' in href and href.startswith('/'):
                return 'https://www.tokopedia.com' + href
            elif '/p/' in href:
                return 'https://www.tokopedia.com' + href if not href.startswith('http') else href
                
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
            print(f"🔗 Mengakses: {search_url}")
            self.driver.get(search_url)
            
            # Tunggu halaman load
            print("⏳ Menunggu halaman dimuat...")
            time.sleep(3)
            
            # Scroll otomatis hingga target tercapai
            self.scroll_page_automatically(target_products, scroll_pause_time=2)
            
            # Ekstrak semua produk
            print("🔍 Mengekstrak data produk...")
            products = self.extract_products_from_page()
            
            # Hapus duplikat
            unique_products = self.remove_duplicates(products)
            print(f"🎯 Scraping selesai! Total produk unik: {len(unique_products)}")
            
            return unique_products[:target_products]
            
        except Exception as e:
            print(f"❌ Error dalam scraping dengan scrolling: {e}")
            import traceback
            traceback.print_exc()
            print("🔄 Fallback ke mode requests...")
            return self.scrape_products_fallback(keyword, target_products)

    def scrape_products_fallback(self, keyword, target_products):
        """Fallback scraping menggunakan requests"""
        all_products = []
        page = 1
        max_pages = min(30, (target_products // 15) + 5)  # Estimasi halaman
        
        print(f"🔄 Menggunakan mode requests fallback...")
        print(f"📊 Target: {target_products} produk, Maksimal halaman: {max_pages}")
        
        while len(all_products) < target_products and page <= max_pages:
            print(f"📄 Memproses halaman {page}...")
            current_url = self.build_search_url(keyword, page)
            
            try:
                # Delay acak untuk menghindari rate limiting
                time.sleep(random.uniform(2, 4))
                response = self.session.get(current_url, timeout=15)
                response.raise_for_status()
                
                if response.status_code == 200 and len(response.content) > 1000:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    # Cek jika halaman tidak menemukan hasil
                    if 'tidak ditemukan' in soup.get_text().lower() or 'no result' in soup.get_text().lower():
                        print(f"🔍 Halaman {page}: Tidak ada hasil pencarian")
                        break
                    
                    # Cari container produk
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
                else:
                    print(f"⚠️ Halaman {page}: Response tidak normal")
                    
            except Exception as e:
                print(f"❌ Error halaman {page}: {e}")
                
            page += 1
            # Delay tambahan antar halaman
            if page <= max_pages and len(all_products) < target_products:
                time.sleep(random.uniform(3, 6))
                
        # Hapus duplikat sebelum return
        unique_products = self.remove_duplicates(all_products)
        print(f"🎯 Fallback selesai! Total produk unik: {len(unique_products)}")
        return unique_products[:target_products]

    def remove_duplicates(self, products):
        """Hapus produk duplikat berdasarkan nama dan harga"""
        if not products:
            return []
            
        seen = set()
        unique_products = []
        
        for product in products:
            # Buat key unik berdasarkan nama dan harga
            name = product.get('nama_produk', '').strip().lower()
            price = product.get('harga', '').strip().lower()
            key = (name, price)
            
            if key not in seen:
                seen.add(key)
                unique_products.append(product)
                
        return unique_products

    def save_to_csv(self, products, keyword):
        """Menyimpan data ke file CSV"""
        if not products:
            print("⚠️ Tidak ada data untuk disimpan")
            return False
            
        # Buat nama file otomatis dengan timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'tokopedia_{keyword.replace(" ", "_")}_{len(products)}produk_{timestamp}.csv'
        
        try:
            df = pd.DataFrame(products)
            
            # Bersihkan data
            for col in df.columns:
                if col != 'timestamp':
                    df[col] = df[col].astype(str).str.strip()
                    
            # Hapus duplikat berdasarkan nama & harga (langkah kedua)
            df = df.drop_duplicates(subset=['nama_produk', 'harga'], keep='first')
            
            # Simpan ke CSV
            df.to_csv(filename, index=False, encoding='utf-8-sig')
            print(f"💾 Data berhasil disimpan ke: {filename}")
            print(f"📊 Jumlah produk unik: {len(df)}")
            
            # Tampilkan statistik dasar
            self.show_basic_statistics(df)
            return True
            
        except Exception as e:
            print(f"❌ Error menyimpan CSV: {e}")
            return False

    def show_basic_statistics(self, df):
        """Tampilkan statistik data dasar"""
        print("\n📈 STATISTIK DATA:")
        print("=" * 40)
        print(f"Total produk: {len(df)}")
        
        # Statistik field yang terisi
        print("\n📊 Kualitas Data:")
        for col in ['nama_produk', 'harga', 'rating', 'jumlah_terjual', 'nama_toko']:
            if col in df.columns:
                filled_count = df[col].apply(lambda x: x and x != "Nama tidak ditemukan" and x != "Harga tidak ditemukan").sum()
                percentage = (filled_count / len(df)) * 100 if len(df) > 0 else 0
                print(f"  • {col}: {filled_count}/{len(df)} ({percentage:.1f}%)")

    def cleanup(self):
        """Bersihkan resources"""
        if self.driver:
            try:
                self.driver.quit()
                print("\n🧹 WebDriver ditutup.")
            except:
                print("\n🧹 WebDriver sudah ditutup.")
        else:
            print("\nℹ️ Tidak ada WebDriver yang perlu ditutup.")

def main():
    """Fungsi utama dengan optimasi"""
    print("="*70)
    print("🤖 TOKOPEDIA SCRAPER OTOMATIS - VERSION FIXED FOR COLAB")
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
    mode_choice = input("Pilihan (1/2, default=1): ").strip()
    
    use_selenium = mode_choice != "2"
    
    # Inisialisasi dan jalankan scraper
    print(f"\n🔧 Menginisialisasi scraper...")
    scraper = TokopediaScraperOptimized(use_selenium=use_selenium, headless=True)
    
    try:
        print(f"\n🚀 MEMULAI SCRAPING...")
        start_time = datetime.now()
        
        if use_selenium and scraper.driver:
            products = scraper.scrape_products_with_scrolling(keyword, target_products)
        else:
            products = scraper.scrape_products_fallback(keyword, target_products)
            
        end_time = datetime.now()
        duration = end_time - start_time
        
        if products:
            print(f"\n🎉 SCRAPING SELESAI!")
            print(f"⏱️ Waktu eksekusi: {duration}")
            print(f"📊 Produk ditemukan: {len(products)}")
            
            # Simpan otomatis ke CSV
            print(f"\n💾 Menyimpan hasil ke file CSV...")
            if scraper.save_to_csv(products, keyword):
                print("✅ File CSV berhasil dibuat!")
            else:
                print("❌ Gagal menyimpan file CSV.")
        else:
            print("\n❌ Tidak ada produk yang berhasil di-scrape.")
            print("💡 Saran:")
            print("   • Coba keyword yang berbeda")
            print("   • Periksa koneksi internet")
            print("   • Restart runtime dan coba lagi")
            
    except KeyboardInterrupt:
        print("\n⚠️ Scraping dihentikan oleh user.")
    except Exception as e:
        print(f"\n❌ Error tidak terduga: {e}")
        import traceback
        traceback.print_exc()
    finally:
        scraper.cleanup()

if __name__ == "__main__":
    main()