# 🔧 TROUBLESHOOTING GUIDE - SHOPEE SCRAPER

## 🚨 Masalah yang Anda Hadapi

Berdasarkan error yang Anda alami, ada beberapa masalah utama:

1. **API Request Failed (403)** - Shopee memblokir request API
2. **Maximum Recursion Depth Exceeded** - Infinite loop dalam kode
3. **API Scraping Failed** - Method yang tidak stabil

## ✅ SOLUSI LENGKAP

### 🔥 SOLUSI CEPAT - Gunakan File yang Sudah Diperbaiki

**Gunakan file ini untuk menghindari masalah:**

1. **`shopee_scraper_fixed.py`** - Versi yang sudah diperbaiki (tanpa recursion)
2. **`colab_simple_scraper.py`** - Versi sederhana untuk Google Colab

### 📋 Langkah-langkah Perbaikan

#### **Option 1: Google Colab (Recommended)**

```python
# Copy dan paste kode ini ke Google Colab
# CELL 1: Install Dependencies
!pip install requests pandas selenium undetected-chromedriver fake-useragent beautifulsoup4 lxml webdriver-manager openpyxl
!apt-get update
!apt-get install -y chromium-chromedriver

# CELL 2: Import Libraries
import requests, json, time, random, pandas as pd
from urllib.parse import quote, urlencode
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import undetected_chromedriver as uc
from fake_useragent import UserAgent
import re
from datetime import datetime
from google.colab import files

# CELL 3: Simple Scraper Class
class SimpleShopeeScraper:
    def __init__(self):
        self.ua = UserAgent()
        self.base_url = "https://shopee.co.id"
        
    def setup_driver(self):
        options = uc.ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--remote-debugging-port=9222')
        options.add_argument('--disable-web-security')
        options.add_argument('--allow-running-insecure-content')
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-plugins')
        
        user_agent = self.ua.random
        options.add_argument(f'--user-agent={user_agent}')
        options.add_argument('--window-size=1920,1080')
        
        driver = uc.Chrome(options=options)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        return driver
    
    def scrape_products(self, keyword, limit=20):
        print(f"🚀 Scraping '{keyword}' sebanyak {limit} produk...")
        
        driver = None
        try:
            driver = self.setup_driver()
            if not driver:
                return []
            
            search_url = f"{self.base_url}/search?{urlencode({'keyword': keyword})}"
            driver.get(search_url)
            time.sleep(random.uniform(5, 8))
            
            # Handle popups
            try:
                cookie_buttons = driver.find_elements(By.XPATH, "//button[contains(text(), 'Accept') or contains(text(), 'Setuju')]")
                for button in cookie_buttons:
                    button.click()
                    time.sleep(1)
            except:
                pass
            
            # Scroll page
            for i in range(5):
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(random.uniform(2, 4))
            
            # Extract products
            products = []
            selectors = ['[data-sqe="item"]', '.col-xs-2-4', '[data-testid="product-card"]']
            
            for selector in selectors:
                try:
                    elements = driver.find_elements(By.CSS_SELECTOR, selector)[:limit]
                    if elements:
                        break
                except:
                    continue
            
            for element in elements:
                try:
                    # Extract data
                    name = "N/A"
                    price = "N/A"
                    rating = "N/A"
                    sold = "0"
                    shop = "N/A"
                    location = "N/A"
                    
                    # Try to get name
                    try:
                        name_elem = element.find_element(By.CSS_SELECTOR, '[data-sqe="name"]')
                        name = name_elem.text.strip()
                    except:
                        pass
                    
                    # Try to get price
                    try:
                        price_elem = element.find_element(By.CSS_SELECTOR, '[data-sqe="price"]')
                        price = price_elem.text.strip()
                    except:
                        pass
                    
                    products.append({
                        'nama_produk': name,
                        'harga': price,
                        'rating': rating,
                        'jumlah_terjual': sold,
                        'nama_toko': shop,
                        'lokasi_toko': location,
                        'diskon': 'N/A'
                    })
                except:
                    continue
            
            return products
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            return []
        finally:
            if driver:
                driver.quit()
    
    def save_to_csv(self, products, filename=None):
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"shopee_products_{timestamp}.csv"
        
        df = pd.DataFrame(products)
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        return filename

# CELL 4: Run Scraper
scraper = SimpleShopeeScraper()

keyword = input("🔍 Masukkan keyword: ").strip()
limit = int(input("📊 Jumlah data: "))

products = scraper.scrape_products(keyword, limit)

if products:
    print(f"✅ Berhasil scrape {len(products)} produk")
    
    # Display results
    for i, product in enumerate(products, 1):
        print(f"\n{i}. {product['nama_produk']}")
        print(f"   💰 {product['harga']}")
        print(f"   ⭐ {product['rating']}")
        print(f"   📦 {product['jumlah_terjual']}")
        print(f"   🏪 {product['nama_toko']}")
    
    # Save and download
    filename = scraper.save_to_csv(products)
    files.download(filename)
else:
    print("❌ Tidak ada data")
```

#### **Option 2: Local Environment**

```bash
# Install dependencies
pip install requests pandas selenium undetected-chromedriver fake-useragent beautifulsoup4 lxml webdriver-manager openpyxl

# Run fixed version
python shopee_scraper_fixed.py
```

### 🔍 ANALISIS MASALAH

#### **1. API 403 Error**
- **Penyebab**: Shopee memblokir request API
- **Solusi**: Gunakan Selenium method saja
- **File**: `colab_simple_scraper.py`

#### **2. Recursion Error**
- **Penyebab**: Infinite loop dalam kode
- **Solusi**: Gunakan versi yang sudah diperbaiki
- **File**: `shopee_scraper_fixed.py`

#### **3. API Scraping Failed**
- **Penyebab**: Method yang tidak stabil
- **Solusi**: Fokus pada Selenium method
- **File**: `colab_simple_scraper.py`

### 🛠️ TROUBLESHOOTING STEP BY STEP

#### **Step 1: Cek Environment**
```bash
# Cek Python version
python --version

# Cek dependencies
pip list | grep -E "(requests|pandas|selenium|undetected-chromedriver)"
```

#### **Step 2: Test Basic Setup**
```python
# Test basic imports
import requests
import pandas as pd
import selenium
import undetected_chromedriver as uc
from fake_useragent import UserAgent

print("✅ All imports successful")
```

#### **Step 3: Test Chrome Driver**
```python
# Test Chrome setup
import undetected_chromedriver as uc

options = uc.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

try:
    driver = uc.Chrome(options=options)
    driver.get("https://www.google.com")
    print("✅ Chrome driver working")
    driver.quit()
except Exception as e:
    print(f"❌ Chrome driver error: {e}")
```

#### **Step 4: Test Shopee Access**
```python
# Test basic Shopee access
import requests

try:
    response = requests.get("https://shopee.co.id")
    print(f"✅ Shopee accessible: {response.status_code}")
except Exception as e:
    print(f"❌ Shopee access error: {e}")
```

### 📊 COMPARISON OF SOLUTIONS

| Solution | Pros | Cons | Best For |
|----------|------|------|----------|
| `colab_simple_scraper.py` | ✅ Stable, No API issues | ⚠️ Slower | Google Colab |
| `shopee_scraper_fixed.py` | ✅ Fixed recursion, Dual method | ⚠️ Complex | Local Environment |
| Original scraper | ❌ API issues, Recursion | ❌ Unstable | Not recommended |

### 🎯 RECOMMENDED APPROACH

#### **Untuk Google Colab:**
1. Gunakan `colab_simple_scraper.py`
2. Copy-paste ke Colab
3. Run cell by cell
4. Input keyword dan jumlah data

#### **Untuk Local Environment:**
1. Install dependencies: `pip install -r requirements.txt`
2. Run: `python shopee_scraper_fixed.py`
3. Input keyword dan jumlah data

### 🚀 QUICK FIX COMMANDS

#### **Google Colab:**
```python
# Quick fix - langsung copy paste ini
!pip install requests pandas selenium undetected-chromedriver fake-useragent
!apt-get update && apt-get install -y chromium-chromedriver

import undetected_chromedriver as uc
from fake_useragent import UserAgent
import pandas as pd
from datetime import datetime
from google.colab import files

class QuickScraper:
    def __init__(self):
        self.ua = UserAgent()
    
    def scrape(self, keyword, limit=10):
        options = uc.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        
        driver = uc.Chrome(options=options)
        driver.get(f"https://shopee.co.id/search?keyword={keyword}")
        time.sleep(5)
        
        # Extract products (simplified)
        products = []
        elements = driver.find_elements_by_css_selector('[data-sqe="item"]')[:limit]
        
        for element in elements:
            try:
                name = element.find_element_by_css_selector('[data-sqe="name"]').text
                price = element.find_element_by_css_selector('[data-sqe="price"]').text
                products.append({'nama': name, 'harga': price})
            except:
                continue
        
        driver.quit()
        return products

# Usage
scraper = QuickScraper()
products = scraper.scrape("laptop", 5)
print(f"Found {len(products)} products")
```

#### **Local Environment:**
```bash
# Quick fix commands
pip install --upgrade selenium undetected-chromedriver
python shopee_scraper_fixed.py
```

### 📞 SUPPORT

Jika masih mengalami masalah:

1. **Cek error message** - Berikan detail error
2. **Cek environment** - Python version, OS
3. **Cek dependencies** - Pastikan semua terinstall
4. **Cek internet** - Koneksi stabil
5. **Cek keyword** - Coba keyword yang berbeda

### 🎉 SUCCESS INDICATORS

Scraper berhasil jika:
- ✅ Chrome driver berhasil dibuat
- ✅ Halaman Shopee berhasil dibuka
- ✅ Produk berhasil diextract
- ✅ Data tersimpan ke file
- ✅ File berhasil didownload

---

**💡 TIP**: Gunakan `colab_simple_scraper.py` untuk hasil yang paling stabil dan konsisten!