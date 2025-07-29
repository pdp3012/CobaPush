# Shopee API Scraper - Alternative Approach
# Copy-paste kode ini ke Google Colab dan jalankan

# Install dependencies
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

def setup_driver():
    """Setup Chrome driver untuk Colab"""
    chrome_options = Options()
    
    # Anti-deteksi options
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    # Colab-specific options
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--window-size=1920,1080')
    
    # User agent
    ua = UserAgent()
    chrome_options.add_argument(f'--user-agent={ua.random}')
    
    try:
        os.environ['PATH'] += ':/usr/bin'
        driver = webdriver.Chrome(options=chrome_options)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        print("✅ Chrome driver berhasil diinisialisasi")
        return driver
    except Exception as e:
        print(f"Error: {e}")
        print("Mencoba setup alternatif...")
        
        try:
            from selenium.webdriver.chrome.service import Service
            from webdriver_manager.chrome import ChromeDriverManager
            
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=chrome_options)
            print("✅ Chrome driver berhasil diinisialisasi (fallback)")
            return driver
        except Exception as e2:
            print(f"Fallback failed: {e2}")
            raise Exception("Tidak dapat menginisialisasi browser")

def get_shopee_api_data(keyword, max_products=50):
    """Menggunakan pendekatan API Shopee"""
    print("🔄 Mencoba pendekatan API Shopee...")
    
    # Setup session
    session = requests.Session()
    ua = UserAgent()
    
    headers = {
        'User-Agent': ua.random,
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Referer': 'https://shopee.co.id/',
        'Origin': 'https://shopee.co.id',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
    }
    
    session.headers.update(headers)
    
    try:
        # Pertama, dapatkan cookies dan session
        print("🌐 Mengakses halaman utama Shopee...")
        main_response = session.get('https://shopee.co.id/')
        time.sleep(2)
        
        # Coba berbagai endpoint API
        api_endpoints = [
            f'https://shopee.co.id/api/v4/search/search_items?keyword={urllib.parse.quote(keyword)}&limit={max_products}&offset=0&page_type=search&scenario=PAGE_GLOBAL_SEARCH&version=2',
            f'https://shopee.co.id/api/v4/search/search_items?keyword={urllib.parse.quote(keyword)}&limit={max_products}&offset=0&page_type=search&scenario=PAGE_GLOBAL_SEARCH&version=1',
            f'https://shopee.co.id/api/v4/search/search_items?keyword={urllib.parse.quote(keyword)}&limit={max_products}&offset=0&page_type=search&scenario=PAGE_GLOBAL_SEARCH',
        ]
        
        for endpoint in api_endpoints:
            try:
                print(f"🔗 Mencoba endpoint: {endpoint}")
                response = session.get(endpoint, timeout=30)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    if 'items' in data and data['items']:
                        print(f"✅ Berhasil mendapatkan {len(data['items'])} produk dari API")
                        return parse_api_data(data['items'], max_products)
                    elif 'data' in data and 'items' in data['data']:
                        print(f"✅ Berhasil mendapatkan {len(data['data']['items'])} produk dari API")
                        return parse_api_data(data['data']['items'], max_products)
                        
            except Exception as e:
                print(f"❌ Error dengan endpoint {endpoint}: {e}")
                continue
        
        print("❌ Tidak dapat mengakses API Shopee")
        return []
        
    except Exception as e:
        print(f"❌ Error dalam pendekatan API: {e}")
        return []

def parse_api_data(items, max_products):
    """Parse data dari API response"""
    data = []
    
    for i, item in enumerate(items[:max_products]):
        try:
            product_data = {
                'nama_produk': item.get('item_basic', {}).get('name', 'N/A'),
                'harga': item.get('item_basic', {}).get('price', 0) // 100000,  # Convert from centavos
                'rating': round(item.get('item_basic', {}).get('item_rating', {}).get('rating_star', 0), 1),
                'jumlah_terjual': item.get('item_basic', {}).get('historical_sold', 0),
                'nama_toko': item.get('shop_basic', {}).get('name', 'N/A'),
                'lokasi_toko': item.get('shop_basic', {}).get('location', 'N/A')
            }
            
            if product_data['nama_produk'] != 'N/A' and len(product_data['nama_produk']) > 5:
                data.append(product_data)
                print(f"✅ {len(data)}: {product_data['nama_produk'][:50]}...")
                
        except Exception as e:
            print(f"❌ Error parsing item {i}: {e}")
            continue
    
    return data

def scrape_with_selenium_fallback(keyword, max_products=50):
    """Scraping dengan Selenium sebagai fallback"""
    print("🔄 Mencoba pendekatan Selenium...")
    
    driver = setup_driver()
    
    try:
        # Encode keyword dan buat URL
        encoded_keyword = urllib.parse.quote(keyword)
        url = f"https://shopee.co.id/search?keyword={encoded_keyword}"
        
        print(f"🌐 Mengakses: {url}")
        
        # Buka halaman
        driver.get(url)
        time.sleep(10)
        
        # Tunggu halaman dimuat
        wait = WebDriverWait(driver, 30)
        
        # Coba berbagai selector
        selectors = [
            '[data-sqe="link"]',
            '.shopee-search-item-result__item',
            '.shopee-item-card',
            '.col-xs-2-4',
            'a[href*="/product/"]',
            'a[href*="/i."]',
            'a[title]'
        ]
        
        products = []
        for selector in selectors:
            try:
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
                products = driver.find_elements(By.CSS_SELECTOR, selector)
                if products:
                    print(f"✅ Ditemukan {len(products)} produk dengan selector: {selector}")
                    break
            except:
                continue
        
        if not products:
            print("⚠️ Tidak dapat menemukan produk dengan selector standar")
            # Coba ambil semua link
            products = driver.find_elements(By.TAG_NAME, "a")
            products = [p for p in products if p.get_attribute("href") and ('/product/' in p.get_attribute("href") or '/i.' in p.get_attribute("href"))]
            print(f"✅ Ditemukan {len(products)} produk dengan pendekatan link")
        
        # Scroll untuk memuat lebih banyak
        print("📜 Scrolling halaman...")
        for i in range(3):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)
            driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(2)
        
        # Ambil ulang produk setelah scroll
        products = driver.find_elements(By.CSS_SELECTOR, '[data-sqe="link"]')
        if not products:
            products = driver.find_elements(By.CSS_SELECTOR, '.col-xs-2-4')
        
        # Ekstrak data
        data = []
        count = 0
        
        for i, product in enumerate(products):
            if count >= max_products:
                break
                
            try:
                # Coba ekstrak nama produk
                name = product.get_attribute('title') or product.text.strip()
                
                if name and len(name) > 5:
                    product_data = {
                        'nama_produk': name,
                        'harga': 0,
                        'rating': 0.0,
                        'jumlah_terjual': 0,
                        'nama_toko': 'N/A',
                        'lokasi_toko': 'N/A'
                    }
                    
                    # Coba ekstrak harga
                    try:
                        price_elem = product.find_element(By.CSS_SELECTOR, '.vioxXd, .ZEgDH9, .price')
                        price_text = price_elem.text.strip()
                        price_clean = re.sub(r'[^\d]', '', price_text)
                        if price_clean:
                            product_data['harga'] = int(price_clean)
                    except:
                        pass
                    
                    data.append(product_data)
                    count += 1
                    print(f"✅ {count}: {name[:50]}...")
                    
            except Exception as e:
                print(f"❌ Error produk {i+1}: {e}")
                continue
            
            time.sleep(0.5)
        
        print(f"🎉 Berhasil mengekstrak {len(data)} produk dengan Selenium")
        return data
        
    except Exception as e:
        print(f"❌ Error dengan Selenium: {e}")
        return []
        
    finally:
        driver.quit()
        print("🔒 Browser ditutup")

def scrape_shopee_hybrid(keyword, max_products=50):
    """Hybrid approach: API first, then Selenium fallback"""
    print(f"🚀 Memulai scraping untuk: '{keyword}'")
    print(f"📊 Target: {max_products} produk")
    
    # Coba API approach first
    data = get_shopee_api_data(keyword, max_products)
    
    if data and len(data) > 0:
        print(f"✅ Berhasil mendapatkan {len(data)} produk dengan API")
        return data
    
    print("⚠️ API approach gagal, mencoba Selenium...")
    
    # Fallback ke Selenium
    data = scrape_with_selenium_fallback(keyword, max_products)
    
    if data and len(data) > 0:
        print(f"✅ Berhasil mendapatkan {len(data)} produk dengan Selenium")
        return data
    
    print("❌ Kedua pendekatan gagal")
    return []

def save_to_excel(data, keyword):
    """Simpan data ke Excel"""
    if not data:
        print("❌ Tidak ada data untuk disimpan")
        return None
    
    df = pd.DataFrame(data)
    
    # Bersihkan data
    df = df.dropna(subset=['nama_produk'])
    df = df[df['nama_produk'] != 'N/A']
    df = df[df['nama_produk'].str.len() > 5]
    
    if df.empty:
        print("❌ Tidak ada data valid")
        return None
    
    # Format data
    df['harga'] = df['harga'].apply(lambda x: f"Rp {x:,}" if x > 0 else "N/A")
    df['rating'] = df['rating'].apply(lambda x: f"{x}/5" if x > 0 else "N/A")
    df['jumlah_terjual'] = df['jumlah_terjual'].apply(lambda x: f"{x:,}" if x > 0 else "N/A")
    
    # Buat nama file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"shopee_{keyword.replace(' ', '_')}_{timestamp}.xlsx"
    
    # Simpan
    df.to_excel(filename, index=False, engine='openpyxl')
    print(f"💾 Data tersimpan: {filename}")
    
    # Preview
    print("\n📋 Preview data:")
    print(df.head())
    print(f"\n📊 Total: {len(df)} produk")
    
    return filename

# ===== MAIN PROGRAM =====
print("=" * 60)
print("🛍️  SHOPEE HYBRID SCRAPER")
print("🔧 API + Selenium approach untuk Google Colab")
print("=" * 60)

# Input dari user
keyword = input("🔍 Masukkan keyword produk: ").strip()
if not keyword:
    print("❌ Keyword tidak boleh kosong!")
else:
    try:
        max_products = int(input("📊 Jumlah data (default 50): ") or "50")
        if max_products <= 0:
            max_products = 50
    except:
        max_products = 50
        print("⚠️ Menggunakan default: 50")
    
    print(f"\n🚀 Memulai scraping: '{keyword}'")
    print(f"📊 Target: {max_products} produk")
    print("⏳ Mohon tunggu...")
    
    # Jalankan hybrid scraping
    data = scrape_shopee_hybrid(keyword, max_products)
    
    if data:
        filename = save_to_excel(data, keyword)
        if filename:
            print(f"\n🎉 Selesai! File: {filename}")
            print("📁 Download dari panel file di sebelah kiri")
        else:
            print("\n❌ Gagal menyimpan data")
    else:
        print("\n❌ Tidak ada data yang berhasil di-scrape")
        print("💡 Coba keyword lain atau periksa koneksi internet")
        print("💡 Tips: Coba keyword yang lebih spesifik seperti 'cabai rawit' atau 'smartphone samsung'")