import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import re
import json
from datetime import datetime

class ShopeeScraper:
    def __init__(self):
        self.driver = None
        self.setup_driver()
        
    def setup_driver(self):
        """Setup Chrome driver dengan konfigurasi optimal untuk scraping"""
        chrome_options = Options()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        
        # Untuk Google Colab, gunakan headless mode
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
    def login_shopee(self, phone="081316084860", password="Pradipta301203"):
        """Login otomatis ke Shopee"""
        try:
            print("🔐 Memulai proses login otomatis ke Shopee...")
            
            # Buka halaman login
            self.driver.get("https://shopee.co.id/buyer/login")
            time.sleep(3)
            
            # Tunggu sampai form login muncul
            wait = WebDriverWait(self.driver, 10)
            
            # Cari dan klik tombol login dengan nomor telepon
            try:
                phone_login_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Log in with phone number')]")))
                phone_login_btn.click()
                time.sleep(2)
            except:
                print("Tombol login dengan nomor telepon tidak ditemukan, mencoba alternatif...")
            
            # Input nomor telepon
            try:
                phone_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Phone number']")))
                phone_input.clear()
                phone_input.send_keys(phone)
                time.sleep(1)
                
                # Klik tombol next atau continue
                next_btn = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Next') or contains(text(), 'Continue')]")
                next_btn.click()
                time.sleep(3)
                
            except Exception as e:
                print(f"Error saat input nomor telepon: {e}")
                return False
            
            # Input password
            try:
                password_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='password']")))
                password_input.clear()
                password_input.send_keys(password)
                time.sleep(1)
                
                # Klik tombol login
                login_btn = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Log in') or contains(text(), 'Login')]")
                login_btn.click()
                time.sleep(5)
                
            except Exception as e:
                print(f"Error saat input password: {e}")
                return False
            
            # Cek apakah login berhasil
            try:
                # Tunggu sampai redirect ke homepage atau muncul elemen yang menandakan login berhasil
                wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'navbar') or contains(@class, 'header')]")))
                print("✅ Login berhasil!")
                return True
                
            except:
                print("⚠️ Login mungkin gagal atau memerlukan verifikasi tambahan")
                return False
                
        except Exception as e:
            print(f"❌ Error saat login: {e}")
            return False
    
    def handle_captcha(self):
        """Handle CAPTCHA jika muncul"""
        try:
            # Cek apakah ada CAPTCHA
            captcha_elements = self.driver.find_elements(By.XPATH, "//div[contains(text(), 'CAPTCHA') or contains(@class, 'captcha')]")
            if captcha_elements:
                print("🔄 CAPTCHA terdeteksi, menunggu penyelesaian manual...")
                time.sleep(10)  # Tunggu user menyelesaikan CAPTCHA
                return True
            return False
        except:
            return False
    
    def scroll_page(self, scroll_count=5):
        """Scroll halaman untuk memuat lebih banyak produk"""
        print("📜 Scrolling halaman untuk memuat lebih banyak produk...")
        for i in range(scroll_count):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            print(f"Scroll {i+1}/{scroll_count} selesai")
    
    def extract_product_data(self, card):
        """Ekstrak data produk dari card menggunakan CSS selector yang diberikan"""
        try:
            # Nama produk
            name_tag = card.select_one("div.line-clamp-2")
            name = name_tag.text.strip() if name_tag else "Tidak ditemukan"
            
            # Harga
            price_tag = card.select_one("span.font-medium.text-base\\/5.truncate")
            price = price_tag.text.strip() if price_tag else "Tidak ditemukan"
            
            # Jumlah terjual
            sold_tag = card.select_one("div.truncate.text-shopee-black87.text-xs.min-h-4")
            sold = sold_tag.text.strip() if sold_tag else "Tidak ditemukan"
            
            # Lokasi toko
            location_tag = card.select_one("div.flex-shrink.min-w-0.truncate.text-shopee-black54")
            location = location_tag.text.strip() if location_tag else "Tidak ditemukan"
            
            # Rating produk
            rating_tag = card.select_one("div.text-shopee-black87.text-xs\\/sp14.flex-none")
            rating = rating_tag.text.strip() if rating_tag else "Tidak ditemukan"
            
            # Nama toko (mencari alternatif selector)
            shop_tag = card.select_one("div.text-shopee-black87.text-xs.min-h-4")
            shop_name = shop_tag.text.strip() if shop_tag else "Tidak ditemukan"
            
            # Jika shop_name sama dengan sold, coba cari selector lain untuk nama toko
            if shop_name == sold:
                shop_tag = card.select_one("div.text-shopee-black87.text-xs")
                shop_name = shop_tag.text.strip() if shop_tag else "Tidak ditemukan"
            
            return {
                'nama_produk': name,
                'harga': price,
                'jumlah_terjual': sold,
                'nama_toko': shop_name,
                'lokasi_toko': location,
                'rating_produk': rating,
                'waktu_scraping': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
        except Exception as e:
            print(f"Error saat ekstrak data produk: {e}")
            return None
    
    def scrape_products(self, keyword, max_pages=3):
        """Scrape produk berdasarkan keyword"""
        all_products = []
        
        try:
            # Login terlebih dahulu
            if not self.login_shopee():
                print("❌ Gagal login, mencoba scraping tanpa login...")
            
            # Handle CAPTCHA jika ada
            self.handle_captcha()
            
            # Buka halaman pencarian
            search_url = f"https://shopee.co.id/search?keyword={keyword.replace(' ', '%20')}"
            print(f"🔍 Mencari produk: {keyword}")
            print(f"📄 URL: {search_url}")
            
            self.driver.get(search_url)
            time.sleep(5)
            
            # Handle CAPTCHA lagi jika muncul setelah search
            self.handle_captcha()
            
            for page in range(1, max_pages + 1):
                print(f"\n📄 Scraping halaman {page}/{max_pages}")
                
                # Scroll untuk memuat lebih banyak produk
                self.scroll_page(scroll_count=3)
                
                # Ambil HTML halaman
                page_source = self.driver.page_source
                soup = BeautifulSoup(page_source, 'html.parser')
                
                # Cari semua card produk
                product_cards = soup.find_all('div', {'data-sqe': 'link'})
                
                if not product_cards:
                    # Coba selector alternatif
                    product_cards = soup.find_all('div', class_=re.compile(r'.*product.*'))
                
                print(f"📦 Ditemukan {len(product_cards)} produk di halaman {page}")
                
                # Ekstrak data dari setiap card
                for i, card in enumerate(product_cards):
                    try:
                        product_data = self.extract_product_data(card)
                        if product_data and product_data['nama_produk'] != "Tidak ditemukan":
                            all_products.append(product_data)
                            print(f"✅ Produk {i+1}: {product_data['nama_produk'][:50]}...")
                    except Exception as e:
                        print(f"❌ Error pada produk {i+1}: {e}")
                        continue
                
                # Coba ke halaman berikutnya jika ada
                if page < max_pages:
                    try:
                        next_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Next') or contains(@class, 'next')]")
                        if next_button.is_enabled():
                            next_button.click()
                            time.sleep(3)
                        else:
                            print("Tidak ada halaman selanjutnya")
                            break
                    except:
                        print("Tidak dapat menemukan tombol next, berhenti di halaman ini")
                        break
            
            print(f"\n🎉 Scraping selesai! Total {len(all_products)} produk berhasil diambil")
            return all_products
            
        except Exception as e:
            print(f"❌ Error saat scraping: {e}")
            return all_products
    
    def save_to_csv(self, products, filename=None):
        """Simpan data ke CSV"""
        if not filename:
            filename = f"shopee_products_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        df = pd.DataFrame(products)
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        print(f"💾 Data berhasil disimpan ke {filename}")
        return filename
    
    def save_to_excel(self, products, filename=None):
        """Simpan data ke Excel"""
        if not filename:
            filename = f"shopee_products_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        
        df = pd.DataFrame(products)
        df.to_excel(filename, index=False, engine='openpyxl')
        print(f"💾 Data berhasil disimpan ke {filename}")
        return filename
    
    def display_results(self, products):
        """Tampilkan hasil scraping dalam format yang rapi"""
        if not products:
            print("❌ Tidak ada data produk yang ditemukan")
            return
        
        print(f"\n📊 HASIL SCRAPING SHOPEE")
        print("=" * 80)
        print(f"Total produk: {len(products)}")
        print("=" * 80)
        
        for i, product in enumerate(products[:10], 1):  # Tampilkan 10 produk pertama
            print(f"\n{i}. {product['nama_produk']}")
            print(f"   💰 Harga: {product['harga']}")
            print(f"   📦 Terjual: {product['jumlah_terjual']}")
            print(f"   🏪 Toko: {product['nama_toko']}")
            print(f"   📍 Lokasi: {product['lokasi_toko']}")
            print(f"   ⭐ Rating: {product['rating_produk']}")
            print("-" * 60)
        
        if len(products) > 10:
            print(f"... dan {len(products) - 10} produk lainnya")
    
    def close(self):
        """Tutup browser"""
        if self.driver:
            self.driver.quit()
            print("🔒 Browser ditutup")

# Fungsi utama untuk digunakan di Google Colab
def main():
    """Fungsi utama untuk scraping Shopee"""
    print("🚀 SHOPEE PRODUCT SCRAPER")
    print("=" * 50)
    
    # Inisialisasi scraper
    scraper = ShopeeScraper()
    
    try:
        # Input keyword dari user
        keyword = input("Masukkan keyword produk yang ingin dicari: ")
        if not keyword:
            keyword = "laptop"  # Default keyword
        
        max_pages = input("Masukkan jumlah halaman yang ingin di-scrape (default: 3): ")
        max_pages = int(max_pages) if max_pages.isdigit() else 3
        
        print(f"\n🔍 Memulai scraping untuk keyword: '{keyword}'")
        print(f"📄 Jumlah halaman: {max_pages}")
        
        # Mulai scraping
        products = scraper.scrape_products(keyword, max_pages)
        
        if products:
            # Tampilkan hasil
            scraper.display_results(products)
            
            # Simpan ke file
            csv_file = scraper.save_to_csv(products)
            excel_file = scraper.save_to_excel(products)
            
            print(f"\n✅ Scraping berhasil!")
            print(f"📁 File CSV: {csv_file}")
            print(f"📁 File Excel: {excel_file}")
            
            # Tampilkan statistik
            print(f"\n📈 STATISTIK:")
            print(f"   - Total produk: {len(products)}")
            print(f"   - Produk dengan harga: {len([p for p in products if p['harga'] != 'Tidak ditemukan'])}")
            print(f"   - Produk dengan rating: {len([p for p in products if p['rating_produk'] != 'Tidak ditemukan'])}")
            
        else:
            print("❌ Tidak ada produk yang berhasil di-scrape")
    
    except KeyboardInterrupt:
        print("\n⏹️ Scraping dihentikan oleh user")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        scraper.close()

# Jalankan jika file dijalankan langsung
if __name__ == "__main__":
    main()

# Untuk penggunaan di Google Colab, gunakan fungsi ini:
def scrape_shopee_colab(keyword="laptop", max_pages=3):
    """
    Fungsi untuk scraping Shopee di Google Colab
    
    Parameters:
    - keyword (str): Kata kunci produk yang ingin dicari
    - max_pages (int): Jumlah halaman yang ingin di-scrape
    
    Returns:
    - DataFrame: Data produk yang berhasil di-scrape
    """
    print(f"🚀 Memulai scraping Shopee untuk keyword: '{keyword}'")
    
    scraper = ShopeeScraper()
    
    try:
        products = scraper.scrape_products(keyword, max_pages)
        
        if products:
            df = pd.DataFrame(products)
            
            # Tampilkan preview
            print(f"\n📊 Preview data ({len(df)} produk):")
            print(df.head())
            
            # Simpan file
            csv_file = scraper.save_to_csv(products)
            excel_file = scraper.save_to_excel(products)
            
            print(f"\n✅ Scraping selesai!")
            print(f"📁 File tersimpan: {csv_file}, {excel_file}")
            
            return df
        else:
            print("❌ Tidak ada produk yang berhasil di-scrape")
            return pd.DataFrame()
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return pd.DataFrame()
    finally:
        scraper.close()

# Contoh penggunaan di Google Colab:
# df = scrape_shopee_colab("smartphone", 2)
# print(df)