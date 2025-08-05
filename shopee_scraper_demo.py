# ========================================
# SHOPEE SCRAPER - DEMO VERSION
# ========================================
# Quick demo untuk testing scraping Shopee

# Install dependencies
!apt update > /dev/null 2>&1
!apt install -y chromium-chromedriver google-chrome-stable xvfb > /dev/null 2>&1
!pip install -q selenium==4.15.2 beautifulsoup4 pandas webdriver-manager > /dev/null 2>&1

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
from selenium.common.exceptions import TimeoutException

def setup_driver():
    """Setup Chrome driver untuk Google Colab"""
    print("🚀 Setting up Chrome driver...")
    
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    
    print("✅ Chrome driver ready!")
    return driver

def load_cookies(driver):
    """Load cookies untuk login otomatis"""
    print("🍪 Loading cookies...")
    
    # Cookies data
    cookies_data = [
        {"domain": ".shopee.co.id", "name": "REC_T_ID", "value": "8bc721be-1c1c-11f0-ae34-12e5e49f7121", "path": "/"},
        {"domain": ".shopee.co.id", "name": "SPC_CDS_CHAT", "value": "f1163150-6b68-4f24-8b6d-3cd76e0d210e", "path": "/"},
        {"domain": ".shopee.co.id", "name": "SPC_CLIENTID", "value": "tShI1nMM4sC8L0nqtikqezkabjgnsexx", "path": "/"},
        {"domain": ".shopee.co.id", "name": "SPC_EC", "value": ".SjVpZFVBc0cybENMZks0aFxNDtw3BvSERjhCM90OrHdoM8fCswHSu7e2LEaEmHXk+g8ZngMR5SDktOM0OqCRJkeHs8hdM3BJonXuqJbaF4yeuhAAizI1SztLImpybKEWrcoaMXARpNFjuh75YJPFCOPu4qG3VYhhmbtzw5aoZXYorQVp4VW69roxzHj6rrIBp8raxGa0PZwLCo7L5iPj4MEQy4bUE27AmcLBcroWhAK0qkx7fY9FG5ZuSx21HdzY", "path": "/"},
        {"domain": ".shopee.co.id", "name": "SPC_F", "value": "yNV6DVNBrPCohZDT9b6hxEHwkYEt9gQX", "path": "/"},
        {"domain": ".shopee.co.id", "name": "SPC_R_T_ID", "value": "rm4TZCgZwiwoFwPe0QdyNFWyVlXFGPK99q1v3fhoJlRaOvFa0yokr89MpmBnZTmAz4/S26jgXcd1S3nQjGjkbcNbWLq7p8VLP3OqKBGXWA2QvY4EmO5EfBTf1VRgYp7cAG7IXkdtRuLLSO5QLR+z8rR3yuW7we48VQLvwBSwAPE=", "path": "/"},
        {"domain": ".shopee.co.id", "name": "SPC_R_T_IV", "value": "WnhxR25XY0tGNU1ydTFiUQ==", "path": "/"},
        {"domain": ".shopee.co.id", "name": "SPC_SI", "value": "BUB3aAAAAABDVWdFR3lmbCfiOQIAAAAAQWNBbXM3ak4=", "path": "/"},
        {"domain": ".shopee.co.id", "name": "SPC_ST", "value": ".Rkl0UTFHaTdPMk9sTTk2OCUeAul8Ul7ts13+AZKSCrZunlpkWzezFK+9VggWiKHopYqzfDH5vOTlKV6roTM6BbcJwT3yGNepFHq3fqoarWZETdPYPf2tk0+MTgZcyiewyTdyCAI+m/64kWoMjc1cDna/zHPhIOcgJ7OIMqN0hfMbDhiMC6WXff+cLx6ie6pnFeqs1fdWBsgwnHLjmYzVkQQjdfjeFM9dVjtELsnvBiArDXqhfFmEMvsh08xWcoCR", "path": "/"},
        {"domain": ".shopee.co.id", "name": "SPC_T_ID", "value": "rm4TZCgZwiwoFwPe0QdyNFWyVlXFGPK99q1v3fhoJlRaOvFa0yokr89MpmBnZTmAz4/S26jgXcd1S3nQjGjkbcNbWLq7p8VLP3OqKBGXWA2QvY4EmO5EfBTf1VRgYp7cAG7IXkdtRuLLSO5QLR+z8rR3yuW7we48VQLvwBSwAPE=", "path": "/"},
        {"domain": ".shopee.co.id", "name": "SPC_T_IV", "value": "WnhxR25XY0tGNU1ydTFiUQ==", "path": "/"},
        {"domain": ".shopee.co.id", "name": "SPC_U", "value": "213962152", "path": "/"},
        {"domain": "shopee.co.id", "name": "_QPWSDCXHZQA", "value": "84c53e6b-7a1b-48a9-f859-850fee955dac", "path": "/"},
        {"domain": "shopee.co.id", "name": "_sapid", "value": "3a0cb6642c76960c3f517a662e30795941bff9d2b36f905e35c6a0fe", "path": "/"},
        {"domain": "shopee.co.id", "name": "csrftoken", "value": "OxNwWhz6alhR7k9V7mIne33ZnyDCRUNv", "path": "/"},
        {"domain": "shopee.co.id", "name": "ds", "value": "e81daf46176c9652cedaa7733130a5f2", "path": "/"},
        {"domain": "shopee.co.id", "name": "REC7iLP4Q", "value": "d7f436da-822b-4a66-b7df-9656fbaf60cd", "path": "/"},
        {"domain": "shopee.co.id", "name": "shopee_webUnique_ccd", "value": "TQ9WNF9fdEDxLFW5rqcGpw%3D%3D%7CLzgno4zi476fAAcFQr%2B821%2BzHAZalZxe0%2FOSdSE0Hi4ZtBk%2B9EOJ%2BuS7UOVd43nXR2gMZ5UetlgFuL7FQLep%7CSSxr%2BH20QlVfm2f7%7C08%7C3", "path": "/"},
        {"domain": "shopee.co.id", "name": "SPC_SEC_SI", "value": "v1-Uk9LdlJJR3pNbk0yVVJoVKaCZbtdACfp4NsXwOP9keHDsQBkyzXX0we7kDEV9lmOhUkId1FmyycoCdfD43xC9hI4H8O2pPeVgIeI9DVgd9A=", "path": "/"}
    ]
    
    # Buka Shopee dan load cookies
    driver.get("https://shopee.co.id")
    time.sleep(3)
    
    for cookie in cookies_data:
        try:
            driver.add_cookie(cookie)
        except:
            continue
    
    driver.refresh()
    time.sleep(3)
    print("✅ Cookies loaded!")

def scrape_shopee_demo(keyword="laptop", max_page=1):
    """Demo scraping Shopee"""
    print(f"🔍 Demo scraping: '{keyword}' - {max_page} halaman")
    
    driver = setup_driver()
    load_cookies(driver)
    
    products = []
    
    for page in range(max_page):
        print(f"📄 Halaman {page+1}...")
        
        # Construct URL
        url = f"https://shopee.co.id/search?keyword={keyword.replace(' ','%20')}&page={page}"
        driver.get(url)
        
        # Wait for products to load
        try:
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".shopee-search-item-result__item"))
            )
        except:
            print("⚠️ Timeout waiting for products")
            continue
        
        # Scroll to load more content
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        
        # Parse HTML
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        items = soup.select(".shopee-search-item-result__item")
        
        print(f"📦 Found {len(items)} products")
        
        # Extract data
        for item in items:
            try:
                # Nama produk
                name_elem = item.select_one("div.line-clamp-2")
                name = name_elem.get_text(strip=True) if name_elem else "N/A"
                
                # Harga
                price_elem = item.select_one("span.currency--GVKjl")
                price = price_elem.get_text(strip=True) if price_elem else "N/A"
                
                # Terjual
                sold_elem = item.select_one("div[data-sqe='sold']")
                sold = sold_elem.get_text(strip=True) if sold_elem else "N/A"
                
                # Lokasi
                location_elem = item.select_one("div[data-sqe='location']")
                location = location_elem.get_text(strip=True) if location_elem else "N/A"
                
                products.append({
                    'product_name': name,
                    'price': price,
                    'sold': sold,
                    'location': location,
                    'keyword': keyword
                })
                
            except Exception as e:
                print(f"⚠️ Error extracting product: {e}")
                continue
        
        time.sleep(random.uniform(2, 4))
    
    driver.quit()
    
    # Save results
    if products:
        df = pd.DataFrame(products)
        filename = f"demo_shopee_{keyword.replace(' ','_')}.csv"
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        
        print(f"\n✅ Demo selesai!")
        print(f"📊 Total produk: {len(products)}")
        print(f"📁 File: {filename}")
        print("\n📋 Sample data:")
        print(df.head().to_string(index=False))
        
        return df
    else:
        print("❌ Tidak ada produk ditemukan")
        return None

# ========================================
# JALANKAN DEMO
# ========================================
print("🎯 SHOPEE SCRAPER DEMO")
print("=" * 40)

# Demo dengan keyword "laptop" - 1 halaman
result = scrape_shopee_demo("laptop", 1)

if result is not None:
    print(f"\n🎉 Demo berhasil! Total {len(result)} produk ditemukan.")
else:
    print("\n❌ Demo gagal!")