# Simple Shopee Scraper untuk Google Colab
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
    chrome_options.add_argument('--disable-images')
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

def extract_product_info(element):
    """Ekstrak informasi produk dari elemen"""
    data = {
        'nama_produk': 'N/A',
        'harga': 0,
        'rating': 0.0,
        'jumlah_terjual': 0,
        'nama_toko': 'N/A',
        'lokasi_toko': 'N/A'
    }
    
    try:
        # Nama produk
        try:
            name_elem = element.find_element(By.CSS_SELECTOR, '[data-sqe="link"]')
            data['nama_produk'] = name_elem.get_attribute('title') or name_elem.text.strip()
        except:
            try:
                name_elem = element.find_element(By.CSS_SELECTOR, '.ie3A\+n')
                data['nama_produk'] = name_elem.text.strip()
            except:
                pass
        
        # Harga
        try:
            price_elem = element.find_element(By.CSS_SELECTOR, '.vioxXd')
            price_text = price_elem.text.strip()
            price_clean = re.sub(r'[^\d]', '', price_text)
            if price_clean:
                data['harga'] = int(price_clean)
        except:
            try:
                price_elem = element.find_element(By.CSS_SELECTOR, '.ZEgDH9')
                price_text = price_elem.text.strip()
                price_clean = re.sub(r'[^\d]', '', price_text)
                if price_clean:
                    data['harga'] = int(price_clean)
            except:
                pass
        
        # Rating
        try:
            rating_elem = element.find_element(By.CSS_SELECTOR, '.shopee-rating-stars__stars')
            rating_style = rating_elem.get_attribute('style')
            if rating_style:
                rating_match = re.search(r'width:\s*(\d+(?:\.\d+)?)%', rating_style)
                if rating_match:
                    rating_percent = float(rating_match.group(1))
                    data['rating'] = round(rating_percent / 20, 1)
        except:
            pass
        
        # Jumlah terjual
        try:
            sold_elem = element.find_element(By.CSS_SELECTOR, '.r6HknA')
            sold_text = sold_elem.text.strip()
            sold_match = re.search(r'(\d+)', sold_text)
            if sold_match:
                data['jumlah_terjual'] = int(sold_match.group(1))
        except:
            pass
        
        # Nama toko
        try:
            shop_elem = element.find_element(By.CSS_SELECTOR, '.Cve6sh')
            data['nama_toko'] = shop_elem.text.strip()
        except:
            pass
        
        # Lokasi toko
        try:
            loc_elem = element.find_element(By.CSS_SELECTOR, '.zGGwiV')
            data['lokasi_toko'] = loc_elem.text.strip()
        except:
            pass
            
    except Exception as e:
        print(f"Error extracting data: {e}")
    
    return data

def scrape_shopee(keyword, max_products=50):
    """Fungsi utama scraping Shopee"""
    print(f"🚀 Memulai scraping untuk: '{keyword}'")
    print(f"📊 Target: {max_products} produk")
    
    # Setup driver
    driver = setup_driver()
    
    try:
        # Encode keyword dan buat URL
        encoded_keyword = urllib.parse.quote(keyword)
        url = f"https://shopee.co.id/search?keyword={encoded_keyword}"
        
        print(f"🌐 Mengakses: {url}")
        
        # Buka halaman
        driver.get(url)
        time.sleep(5)
        
        # Tunggu halaman dimuat
        wait = WebDriverWait(driver, 20)
        
        # Coba berbagai selector
        selectors = [
            '[data-sqe="link"]',
            '.col-xs-2-4',
            '.shopee-search-item-result__item',
            '.shopee-item-card'
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
            print("⚠️ Tidak dapat menemukan produk. Mencoba selector alternatif...")
            # Coba ambil semua link yang mungkin produk
            products = driver.find_elements(By.TAG_NAME, "a")
            products = [p for p in products if p.get_attribute("data-sqe") == "link"]
        
        print(f"📦 Total elemen ditemukan: {len(products)}")
        
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
                product_data = extract_product_info(product)
                
                # Hanya ambil yang ada nama produk
                if product_data['nama_produk'] != 'N/A' and len(product_data['nama_produk']) > 3:
                    data.append(product_data)
                    count += 1
                    print(f"✅ {count}: {product_data['nama_produk'][:40]}...")
                    
                    if count % 10 == 0:
                        print(f"📈 Progress: {count}/{max_products}")
                        
            except Exception as e:
                print(f"❌ Error produk {i+1}: {e}")
                continue
            
            time.sleep(0.5)
        
        print(f"🎉 Berhasil mengekstrak {len(data)} produk")
        return data
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return []
        
    finally:
        driver.quit()
        print("🔒 Browser ditutup")

def save_to_excel(data, keyword):
    """Simpan data ke Excel"""
    if not data:
        print("❌ Tidak ada data untuk disimpan")
        return None
    
    df = pd.DataFrame(data)
    
    # Bersihkan data
    df = df.dropna(subset=['nama_produk'])
    df = df[df['nama_produk'] != 'N/A']
    df = df[df['nama_produk'].str.len() > 3]
    
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
print("🛍️  SIMPLE SHOPEE SCRAPER")
print("🔧 Scraper otomatis untuk Google Colab")
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
    
    # Jalankan scraping
    data = scrape_shopee(keyword, max_products)
    
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