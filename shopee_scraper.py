import time
import csv
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import messagebox, simpledialog
import re

class ShopeeScraper:
    def __init__(self):
        self.driver = None
        self.setup_driver()
        
    def setup_driver(self):
        """Setup Chrome driver dengan konfigurasi optimal untuk scraping"""
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
    def wait_for_element(self, by, value, timeout=10):
        """Menunggu elemen muncul dengan timeout"""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            return element
        except TimeoutException:
            return None
            
    def automated_login(self, phone, password):
        """Login otomatis ke Shopee"""
        try:
            print("🔄 Memulai proses login otomatis...")
            
            # Buka halaman login
            self.driver.get("https://shopee.co.id/buyer/login")
            time.sleep(3)
            
            # Tunggu dan klik tombol login dengan nomor telepon
            phone_login_btn = self.wait_for_element(By.XPATH, "//button[contains(text(), 'Log in with phone number')]")
            if phone_login_btn:
                phone_login_btn.click()
                time.sleep(2)
            
            # Input nomor telepon
            phone_input = self.wait_for_element(By.XPATH, "//input[@placeholder='Phone number']")
            if phone_input:
                phone_input.clear()
                phone_input.send_keys(phone)
                time.sleep(1)
                
                # Klik tombol "Send code" atau "Continue"
                send_code_btn = self.wait_for_element(By.XPATH, "//button[contains(text(), 'Send code') or contains(text(), 'Continue')]")
                if send_code_btn:
                    send_code_btn.click()
                    time.sleep(2)
                    
                    # Input password
                    password_input = self.wait_for_element(By.XPATH, "//input[@placeholder='Password']")
                    if password_input:
                        password_input.clear()
                        password_input.send_keys(password)
                        time.sleep(1)
                        
                        # Klik tombol login
                        login_btn = self.wait_for_element(By.XPATH, "//button[contains(text(), 'Log in') or contains(text(), 'Login')]")
                        if login_btn:
                            login_btn.click()
                            time.sleep(5)
                            
                            # Cek apakah login berhasil
                            if self.check_login_success():
                                print("✅ Login berhasil!")
                                return True
                            else:
                                print("❌ Login gagal, mencoba metode manual...")
                                return False
                                
        except Exception as e:
            print(f"❌ Error dalam login otomatis: {str(e)}")
            return False
            
    def check_login_success(self):
        """Cek apakah login berhasil"""
        try:
            # Cek apakah ada elemen yang menunjukkan user sudah login
            user_menu = self.driver.find_element(By.XPATH, "//div[contains(@class, 'navbar__username')]")
            return True
        except NoSuchElementException:
            return False
            
    def manual_login(self):
        """Login manual dengan interaksi user"""
        print("🔐 Silakan login manual ke Shopee.")
        messagebox.showinfo("Login", "Silakan login manual ke Shopee di browser.\nKlik OK jika sudah login.")
        
        # Tunggu sampai user login
        while not self.check_login_success():
            time.sleep(2)
            
        messagebox.showinfo("CAPTCHA", "Jika muncul CAPTCHA, silakan selesaikan dulu.\nKlik OK jika sudah selesai CAPTCHA.")
        time.sleep(3)
        
    def extract_product_data(self, card):
        """Ekstrak data produk dari card menggunakan CSS selector"""
        try:
            # Nama produk
            name_tag = card.select_one("div.line-clamp-2")
            price_tag = card.select_one("span.font-medium.text-base\\/5.truncate")
            
            if not name_tag or not price_tag:
                return None
                
            name = name_tag.text.strip()
            price = price_tag.text.strip()
            
            # Jumlah terjual
            sold_tag = card.select_one("div.truncate.text-shopee-black87.text-xs.min-h-4")
            sold = sold_tag.text.strip() if sold_tag else "Tidak ditemukan"
            
            # Lokasi toko
            location_tag = card.select_one("div.flex-shrink.min-w-0.truncate.text-shopee-black54")
            location = location_tag.text.strip() if location_tag else "Tidak ditemukan"
            
            # Rating produk
            rating_tag = card.select_one("div.text-shopee-black87.text-xs\\/sp14.flex-none")
            rating = rating_tag.text.strip() if rating_tag else "Tidak ditemukan"
            
            # Nama toko (mencoba beberapa selector)
            shop_name = "Tidak ditemukan"
            shop_selectors = [
                "div.text-shopee-black87.text-xs.min-h-4",
                "div.flex-shrink.min-w-0.truncate.text-shopee-black87",
                "div[data-sqe='link'] div.text-shopee-black87"
            ]
            
            for selector in shop_selectors:
                shop_tag = card.select_one(selector)
                if shop_tag and shop_tag.text.strip():
                    shop_name = shop_tag.text.strip()
                    break
                    
            return {
                'nama_produk': name,
                'harga': price,
                'jumlah_terjual': sold,
                'nama_toko': shop_name,
                'lokasi_toko': location,
                'rating_produk': rating
            }
            
        except Exception as e:
            print(f"❌ Error ekstraksi data: {str(e)}")
            return None
            
    def scroll_page(self, scroll_count=5):
        """Scroll halaman untuk memuat lebih banyak produk"""
        print("📜 Scrolling halaman untuk memuat produk...")
        for i in range(scroll_count):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            
    def scrape_products(self, keyword, max_products=50):
        """Scrape produk berdasarkan keyword"""
        try:
            # Coba login otomatis dulu
            login_success = self.automated_login("081316084860", "Pradipta301203")
            
            if not login_success:
                self.manual_login()
                
            # Navigasi ke halaman pencarian
            search_url = f"https://shopee.co.id/search?keyword={keyword.replace(' ', '%20')}"
            self.driver.get(search_url)
            time.sleep(5)
            
            # Scroll untuk memuat lebih banyak produk
            self.scroll_page()
            
            # Parse HTML
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            
            # Cari semua card produk
            product_cards = soup.find_all('div', {'data-sqe': 'link'})
            print(f"📦 Ditemukan {len(product_cards)} card produk")
            
            products = []
            for i, card in enumerate(product_cards[:max_products]):
                product_data = self.extract_product_data(card)
                if product_data:
                    products.append(product_data)
                    print(f"✅ Produk {i+1}: {product_data['nama_produk'][:50]}...")
                    
            print(f"🎉 Berhasil mengekstrak {len(products)} produk")
            return products
            
        except Exception as e:
            print(f"❌ Error dalam scraping: {str(e)}")
            return []
            
    def save_to_csv(self, products, filename="shopee_products.csv"):
        """Simpan data ke file CSV"""
        if not products:
            print("❌ Tidak ada data untuk disimpan")
            return
            
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=products[0].keys())
                writer.writeheader()
                writer.writerows(products)
                
            print(f"💾 Data berhasil disimpan ke {filename}")
            
        except Exception as e:
            print(f"❌ Error menyimpan file: {str(e)}")
            
    def save_to_json(self, products, filename="shopee_products.json"):
        """Simpan data ke file JSON"""
        if not products:
            print("❌ Tidak ada data untuk disimpan")
            return
            
        try:
            with open(filename, 'w', encoding='utf-8') as file:
                json.dump(products, file, ensure_ascii=False, indent=2)
                
            print(f"💾 Data berhasil disimpan ke {filename}")
            
        except Exception as e:
            print(f"❌ Error menyimpan file: {str(e)}")
            
    def close(self):
        """Tutup browser"""
        if self.driver:
            self.driver.quit()
            print("🔒 Browser ditutup")

def main():
    """Fungsi utama"""
    print("🚀 Shopee Product Scraper - Powered by Data Mining Expert")
    print("=" * 60)
    
    # Setup GUI untuk input
    root = tk.Tk()
    root.withdraw()  # Sembunyikan window utama
    
    # Input keyword
    keyword = simpledialog.askstring("Input", "Masukkan keyword produk yang ingin di-scrape:")
    if not keyword:
        print("❌ Keyword tidak boleh kosong")
        return
        
    # Input jumlah maksimal produk
    max_products = simpledialog.askinteger("Input", "Jumlah maksimal produk (default: 50):", initialvalue=50)
    if not max_products:
        max_products = 50
        
    root.destroy()
    
    # Inisialisasi scraper
    scraper = ShopeeScraper()
    
    try:
        # Mulai scraping
        print(f"🔍 Mencari produk dengan keyword: '{keyword}'")
        products = scraper.scrape_products(keyword, max_products)
        
        if products:
            # Simpan data
            scraper.save_to_csv(products, f"shopee_{keyword.replace(' ', '_')}.csv")
            scraper.save_to_json(products, f"shopee_{keyword.replace(' ', '_')}.json")
            
            # Tampilkan ringkasan
            print("\n📊 RINGKASAN HASIL SCRAPING:")
            print(f"Total produk: {len(products)}")
            print(f"Keyword: {keyword}")
            
            # Tampilkan beberapa contoh data
            print("\n📋 CONTOH DATA:")
            for i, product in enumerate(products[:3]):
                print(f"\nProduk {i+1}:")
                for key, value in product.items():
                    print(f"  {key}: {value}")
                    
        else:
            print("❌ Tidak ada produk yang ditemukan")
            
    except KeyboardInterrupt:
        print("\n⏹️ Scraping dihentikan oleh user")
    except Exception as e:
        print(f"❌ Error tidak terduga: {str(e)}")
    finally:
        scraper.close()

if __name__ == "__main__":
    main()