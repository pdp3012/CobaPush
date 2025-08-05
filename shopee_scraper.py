# Instal dependensi sistem (untuk Google Colab)
# !apt update > /dev/null 2>&1
# !apt install -y chromium-chromedriver google-chrome-stable xvfb > /dev/null 2>&1
# !pip install -q selenium==4.15.2 beautifulsoup4 pandas webdriver-manager > /dev/null 2>&1

import json, time, random
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def setup_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

def load_cookies(driver, path="cookies.json"):
    driver.get("https://shopee.co.id")
    with open(path, 'r') as f:
        cookies = json.load(f)
        for cookie in cookies:
            # Perbaikan handling sameSite
            if 'sameSite' in cookie and cookie['sameSite'] == 'unspecified':
                cookie['sameSite'] = 'Strict'
            if 'expirationDate' in cookie:
                cookie['expiry'] = int(cookie['expirationDate'])
                del cookie['expirationDate']
            if 'hostOnly' in cookie:
                del cookie['hostOnly']
            if 'storeId' in cookie:
                del cookie['storeId']
            if 'id' in cookie:
                del cookie['id']
            driver.add_cookie(cookie)
    driver.refresh()
    print("✅ Login otomatis via cookie berhasil!")

def slow_scroll(driver):
    height = driver.execute_script("return document.body.scrollHeight")
    for i in range(0, height, 400):
        driver.execute_script(f"window.scrollTo(0,{i});")
        time.sleep(random.uniform(0.2, 0.5))
    time.sleep(2)

def scrape_shopee(keyword, max_page, output_file):
    driver = setup_driver()
    load_cookies(driver)

    products = []
    for page in range(1, max_page + 1):
        print(f"Scraping halaman {page}...")
        url = f"https://shopee.co.id/search?keyword={keyword.replace(' ','%20')}&page={page-1}"
        driver.get(url)
        WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "shopee-search-item-result__item")))
        slow_scroll(driver)

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        items = soup.select(".shopee-search-item-result__item")
        
        for item in items:
            name = item.select_one("div.line-clamp-2").text.strip() if item.select_one("div.line-clamp-2") else "N/A"
            price = item.select_one("span.currency--GVKjl").text.strip() if item.select_one("span.currency--GVKjl") else "N/A"
            sold = item.select_one("div[data-sqe='sold']").text.strip() if item.select_one("div[data-sqe='sold']") else "Tidak ditemukan"
            location = item.select_one("div[data-sqe='location']").text.strip() if item.select_one("div[data-sqe='location']") else "Tidak ditemukan"
            rating = item.select_one("div.shopee-rating-stars__lit")
            rating = rating.get('style').split(":")[-1] if rating else "Tidak ditemukan"

            products.append({
                'product_name': name,
                'price': price,
                'sold': sold,
                'location': location,
                'rating': rating,
                'kategori': keyword
            })

        time.sleep(random.uniform(2, 4))

    if products:
        df = pd.DataFrame(products)
        df.to_csv(output_file, index=False)
        print(f"✅ Scraping selesai, data disimpan ke {output_file}")
        print(df.head())
    else:
        print("❌ Tidak ada produk ditemukan.")
    
    driver.quit()

if __name__ == "__main__":
    keyword = input("Masukkan kata kunci: ").strip()
    max_page = int(input("Jumlah halaman: "))
    output_file = input("Nama file CSV (misal: hasil.csv): ").strip()
    if not output_file.endswith(".csv"):
        output_file += ".csv"
    scrape_shopee(keyword, max_page, output_file)