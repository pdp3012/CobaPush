# Simple Shopee Scraper untuk Google Colab - FIXED VERSION
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
    """Setup Chrome driver untuk Colab dengan opsi yang lebih robust"""
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
    chrome_options.add_argument('--disable-web-security')
    chrome_options.add_argument('--allow-running-insecure-content')
    
    # Additional stealth options
    chrome_options.add_argument('--disable-blink-features')
    chrome_options.add_argument('--disable-infobars')
    chrome_options.add_argument('--disable-notifications')
    chrome_options.add_argument('--disable-popup-blocking')
    chrome_options.add_argument('--disable-save-password-bubble')
    chrome_options.add_argument('--disable-translate')
    chrome_options.add_argument('--disable-features=VizDisplayCompositor')
    
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

def wait_for_page_load(driver, timeout=30):
    """Tunggu halaman dimuat dengan berbagai indikator"""
    wait = WebDriverWait(driver, timeout)
    
    # Coba berbagai indikator bahwa halaman sudah dimuat
    indicators = [
        'body',
        '.shopee-search-item-result',
        '.shopee-search-item-result__item',
        '[data-sqe="link"]',
        '.col-xs-2-4',
        '.shopee-item-card',
        '.shopee-search-item-result__item-name',
        '.shopee-item-card__text-name'
    ]
    
    for indicator in indicators:
        try:
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, indicator)))
            print(f"✅ Halaman dimuat dengan indikator: {indicator}")
            return True
        except TimeoutException:
            continue
    
    print("⚠️ Halaman tidak dimuat dengan indikator standar, mencoba refresh...")
    return False

def find_product_elements(driver):
    """Cari elemen produk dengan berbagai selector"""
    selectors = [
        # Selector utama Shopee
        '[data-sqe="link"]',
        '.shopee-search-item-result__item',
        '.shopee-item-card',
        '.col-xs-2-4',
        
        # Selector alternatif
        '.shopee-search-item-result__item-name',
        '.shopee-item-card__text-name',
        'a[href*="/product/"]',
        'a[href*="/i."]',
        
        # Selector umum
        '.shopee-search-item-result a',
        '.shopee-item-card a',
        '[data-sqe="name"]',
        
        # Selector fallback
        'a[title]',
        'a[data-sqe]',
        '.shopee-search-item-result *',
        '.shopee-item-card *'
    ]
    
    products = []
    used_selector = None
    
    for selector in selectors:
        try:
            elements = driver.find_elements(By.CSS_SELECTOR, selector)
            if elements and len(elements) > 0:
                # Filter elemen yang mungkin produk
                filtered_elements = []
                for elem in elements:
                    try:
                        # Cek apakah elemen memiliki atribut yang menandakan produk
                        href = elem.get_attribute('href')
                        title = elem.get_attribute('title')
                        text = elem.text.strip()
                        
                        if (href and ('/product/' in href or '/i.' in href)) or \
                           (title and len(title) > 5) or \
                           (text and len(text) > 5):
                            filtered_elements.append(elem)
                    except:
                        continue
                
                if filtered_elements:
                    products = filtered_elements
                    used_selector = selector
                    print(f"✅ Ditemukan {len(products)} produk dengan selector: {selector}")
                    break
        except Exception as e:
            print(f"Error dengan selector {selector}: {e}")
            continue
    
    if not products:
        print("⚠️ Tidak dapat menemukan produk dengan selector standar, mencoba pendekatan alternatif...")
        
        # Coba ambil semua link yang mungkin produk
        try:
            all_links = driver.find_elements(By.TAG_NAME, "a")
            products = []
            for link in all_links:
                try:
                    href = link.get_attribute('href')
                    title = link.get_attribute('title')
                    text = link.text.strip()
                    
                    # Filter berdasarkan URL atau teks
                    if (href and ('/product/' in href or '/i.' in href)) or \
                       (title and len(title) > 10 and not title.startswith('http')) or \
                       (text and len(text) > 10 and not text.startswith('http')):
                        products.append(link)
                except:
                    continue
            
            if products:
                used_selector = "all_links_filtered"
                print(f"✅ Ditemukan {len(products)} produk dengan pendekatan alternatif")
        except Exception as e:
            print(f"Error dengan pendekatan alternatif: {e}")
    
    return products, used_selector

def extract_product_info(element, selector_type):
    """Ekstrak informasi produk dari elemen dengan multiple approaches"""
    data = {
        'nama_produk': 'N/A',
        'harga': 0,
        'rating': 0.0,
        'jumlah_terjual': 0,
        'nama_toko': 'N/A',
        'lokasi_toko': 'N/A'
    }
    
    try:
        # Nama produk - multiple approaches
        name_selectors = [
            '[data-sqe="link"]',
            '.ie3A\+n',
            '.shopee-item-card__text-name',
            '.shopee-search-item-result__item-name',
            'a[data-sqe="link"]',
            '.col-xs-2-4 a',
            'a[title]',
            'a'
        ]
        
        for name_sel in name_selectors:
            try:
                name_elem = element.find_element(By.CSS_SELECTOR, name_sel)
                name_text = name_elem.get_attribute('title') or name_elem.text.strip()
                if name_text and len(name_text) > 5:
                    data['nama_produk'] = name_text
                    break
            except:
                continue
        
        # Jika masih N/A, coba ambil dari parent element
        if data['nama_produk'] == 'N/A':
            try:
                parent = element.find_element(By.XPATH, "..")
                name_text = parent.text.strip()
                if name_text and len(name_text) > 5:
                    data['nama_produk'] = name_text
            except:
                pass
        
        # Harga - multiple selectors
        price_selectors = [
            '.vioxXd',
            '.ZEgDH9',
            '.shopee-item-card__text-price',
            '.shopee-search-item-result__item-price',
            '[data-sqe="name"]',
            '.price',
            '.item-price',
            '.product-price'
        ]
        
        for price_sel in price_selectors:
            try:
                price_elem = element.find_element(By.CSS_SELECTOR, price_sel)
                price_text = price_elem.text.strip()
                price_clean = re.sub(r'[^\d]', '', price_text)
                if price_clean and len(price_clean) > 3:
                    data['harga'] = int(price_clean)
                    break
            except:
                continue
        
        # Rating - multiple selectors
        rating_selectors = [
            '.shopee-rating-stars__stars',
            '.shopee-item-card__rating',
            '.shopee-search-item-result__item-rating',
            '.rating',
            '.stars'
        ]
        
        for rating_sel in rating_selectors:
            try:
                rating_elem = element.find_element(By.CSS_SELECTOR, rating_sel)
                rating_style = rating_elem.get_attribute('style')
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
            '.shopee-search-item-result__item-sold',
            '.sold',
            '.sales'
        ]
        
        for sold_sel in sold_selectors:
            try:
                sold_elem = element.find_element(By.CSS_SELECTOR, sold_sel)
                sold_text = sold_elem.text.strip()
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
            '.shopee-search-item-result__item-shop',
            '.shop-name',
            '.seller-name'
        ]
        
        for shop_sel in shop_selectors:
            try:
                shop_elem = element.find_element(By.CSS_SELECTOR, shop_sel)
                shop_text = shop_elem.text.strip()
                if shop_text and len(shop_text) > 2:
                    data['nama_toko'] = shop_text
                    break
            except:
                continue
        
        # Lokasi toko - multiple selectors
        location_selectors = [
            '.zGGwiV',
            '.shopee-item-card__shop-location',
            '.shopee-search-item-result__item-location',
            '.location',
            '.shop-location'
        ]
        
        for loc_sel in location_selectors:
            try:
                loc_elem = element.find_element(By.CSS_SELECTOR, loc_sel)
                loc_text = loc_elem.text.strip()
                if loc_text and len(loc_text) > 2:
                    data['lokasi_toko'] = loc_text
                    break
            except:
                continue
                
    except Exception as e:
        print(f"Error extracting data: {e}")
    
    return data

def scrape_shopee(keyword, max_products=50):
    """Fungsi utama scraping Shopee dengan error handling yang lebih baik"""
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
        time.sleep(8)  # Tunggu lebih lama untuk loading
        
        # Tunggu halaman dimuat
        page_loaded = wait_for_page_load(driver, 30)
        
        if not page_loaded:
            print("⚠️ Halaman tidak dimuat dengan benar, mencoba refresh...")
            driver.refresh()
            time.sleep(10)
            page_loaded = wait_for_page_load(driver, 30)
        
        # Scroll untuk memuat lebih banyak konten
        print("📜 Scrolling halaman untuk memuat lebih banyak produk...")
        for i in range(5):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)
            driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(2)
            print(f"Scroll {i+1}/5 selesai")
        
        # Cari elemen produk
        products, used_selector = find_product_elements(driver)
        
        if not products:
            print("❌ Tidak dapat menemukan produk sama sekali")
            print("💡 Mungkin Shopee telah mengubah struktur website mereka")
            return []
        
        print(f"📦 Total elemen ditemukan: {len(products)}")
        
        # Ekstrak data
        data = []
        count = 0
        
        for i, product in enumerate(products):
            if count >= max_products:
                break
                
            try:
                product_data = extract_product_info(product, used_selector)
                
                # Hanya ambil yang ada nama produk
                if product_data['nama_produk'] != 'N/A' and len(product_data['nama_produk']) > 5:
                    data.append(product_data)
                    count += 1
                    print(f"✅ {count}: {product_data['nama_produk'][:50]}...")
                    
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
print("🛍️  SIMPLE SHOPEE SCRAPER - FIXED VERSION")
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
        print("💡 Tips: Coba keyword yang lebih spesifik seperti 'cabai rawit' atau 'smartphone samsung'")