import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
from urllib.parse import quote
import json
import csv
from datetime import datetime
import re

class BlibliScraper:
    def __init__(self):
        """
        Inisialisasi scraper dengan headers yang mirip browser
        """
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

    def build_search_url(self, keyword, page=1):
        """
        Membangun URL pencarian Blibli
        """
        encoded_keyword = quote(keyword)
        
        if page == 1:
            # URL untuk halaman pertama
            search_url = f"https://www.blibli.com/cari/{encoded_keyword}"
        else:
            # URL untuk halaman selanjutnya
            search_url = f"https://www.blibli.com/cari/{encoded_keyword}?page={page}"

        print(f"🔍 URL Pencarian: {search_url}")
        return search_url

    def get_page_content(self, url, max_retries=3):
        """
        Mendapatkan konten halaman dengan retry mechanism yang diperbaiki
        """
        for attempt in range(max_retries):
            try:
                print(f"🔄 Mengakses halaman (Percobaan {attempt + 1})...")

                # Tambahkan random delay sebelum request
                time.sleep(random.uniform(1, 3))

                response = self.session.get(url, timeout=15)
                response.raise_for_status()

                # Cek apakah halaman berhasil dimuat
                if response.status_code == 200 and len(response.content) > 1000:
                    print(f"✅ Berhasil mengakses halaman (Size: {len(response.content)} bytes)")
                    return response
                else:
                    print(f"⚠️  Response tidak normal: Status {response.status_code}, Size: {len(response.content)}")

            except requests.exceptions.RequestException as e:
                print(f"⚠️  Error pada percobaan {attempt + 1}: {e}")

            if attempt < max_retries - 1:
                wait_time = random.uniform(5, 10)
                print(f"⏳ Menunggu {wait_time:.1f} detik sebelum retry...")
                time.sleep(wait_time)

        print("❌ Gagal mengakses halaman setelah beberapa percobaan")
        return None

    def extract_product_data(self, soup):
        """
        Mengekstrak data produk dari halaman Blibli
        """
        products = []

        # Debug: Simpan HTML untuk analisis
        print("🔍 Menganalisis struktur halaman...")

        # Cari container produk dengan CSS selector yang spesifik untuk Blibli
        product_containers = self.find_product_containers(soup)

        if not product_containers:
            print("❌ Tidak ditemukan container produk")
            return products

        print(f"✅ Ditemukan {len(product_containers)} container produk")

        for idx, container in enumerate(product_containers):
            try:
                product_data = self.extract_single_product_robust(container, idx + 1)
                if product_data and self.validate_product_data(product_data):
                    products.append(product_data)
                    print(f"📦 Produk {len(products)}: {product_data['nama_produk'][:50]}... | {product_data['harga']}")
            except Exception as e:
                print(f"❌ Error ekstrak produk {idx + 1}: {e}")
                continue

        return products

    def find_product_containers(self, soup):
        """
        Mencari container produk dengan CSS selector yang spesifik untuk Blibli
        """
        containers = []

        # CSS selector untuk container produk Blibli
        container_selectors = [
            '[data-v-e343f6d0]',  # Selector umum untuk komponen Blibli
            'div[class*="els-product"]',  # Container produk
            'div[class*="product"]',  # Container produk alternatif
            'div[class*="card"]'  # Container card produk
        ]

        for selector in container_selectors:
            elements = soup.select(selector)
            if elements:
                print(f"🎯 Ditemukan {len(elements)} container dengan selector: {selector}")
                # Filter hanya yang mengandung data produk
                for element in elements:
                    # Cek apakah element ini mengandung data produk
                    if self.is_product_container(element):
                        containers.append(element)
                break

        # Jika tidak ditemukan dengan selector spesifik, gunakan strategi alternatif
        if not containers:
            print("🔄 Menggunakan strategi alternatif...")
            # Cari div yang mengandung elemen produk
            all_divs = soup.find_all('div')
            
            for div in all_divs:
                # Cek apakah div ini mengandung elemen produk
                if self.is_product_container(div):
                    containers.append(div)

        print(f"📊 Total container produk ditemukan: {len(containers)}")
        return containers[:50]  # Batasi maksimal 50 produk per halaman

    def is_product_container(self, element):
        """
        Mengecek apakah element adalah container produk
        """
        # Cek apakah element mengandung elemen produk Blibli
        has_title = element.find('div', class_='els-product__title-wrapper') is not None
        has_price = element.find('div', class_='els-product__fixed-price') is not None
        has_seller = element.find('span', class_='els-product__seller-name') is not None
        
        return has_title or has_price or has_seller

    def extract_single_product_robust(self, element, product_number):
        """
        Ekstrak data produk dengan CSS selector yang spesifik untuk Blibli
        """
        product_data = {
            'nama_produk': '',
            'harga': '',
            'rating': '',
            'jumlah_terjual': '',
            'nama_toko': '',
            'link_produk': '',
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

        try:
            # === EKSTRAK NAMA PRODUK ===
            product_data['nama_produk'] = self.extract_product_name(element)

            # === EKSTRAK HARGA ===
            product_data['harga'] = self.extract_price(element)

            # === EKSTRAK RATING ===
            product_data['rating'] = self.extract_rating(element)

            # === EKSTRAK JUMLAH TERJUAL ===
            product_data['jumlah_terjual'] = self.extract_sold_count(element)

            # === EKSTRAK NAMA TOKO ===
            product_data['nama_toko'] = self.extract_shop_name(element)

            # === EKSTRAK LINK PRODUK ===
            product_data['link_produk'] = self.extract_product_link(element)

            return product_data

        except Exception as e:
            print(f"❌ Error ekstrak produk {product_number}: {e}")
            return None

    def extract_product_name(self, element):
        """Ekstrak nama produk dengan CSS selector Blibli"""
        name = ""

        # CSS selector untuk nama produk
        title_selectors = [
            'div.els-product__title-wrapper span.els-product__title span',
            'div.els-product__title-wrapper .els-product__title',
            'span.els-product__title',
            'div[class*="title"] span'
        ]

        for selector in title_selectors:
            title_element = element.select_one(selector)
            if title_element:
                name = title_element.get_text(strip=True)
                if name and len(name) > 3:
                    break

        # Jika tidak ditemukan dengan selector, cari dengan strategi alternatif
        if not name:
            # Cari span yang mengandung teks panjang
            spans = element.find_all('span')
            for span in spans:
                text = span.get_text(strip=True)
                if len(text) > 10 and 'Rp' not in text and not re.match(r'^\d+[.,]\d*$', text):
                    name = text
                    break

        return name or "Nama tidak ditemukan"

    def extract_price(self, element):
        """Ekstrak harga dengan CSS selector Blibli"""
        price = ""

        # CSS selector untuk harga
        price_selectors = [
            'div.els-product__fixed-price',
            'div[title*="Rp"]',
            'div[class*="price"]'
        ]

        for selector in price_selectors:
            price_element = element.select_one(selector)
            if price_element:
                # Ambil teks dari element harga
                price_text = price_element.get_text(strip=True)
                if price_text and 'Rp' in price_text:
                    price = price_text
                    break

        # Jika tidak ditemukan dengan selector, cari dengan pattern
        if not price:
            price_pattern = re.compile(r'Rp[\s]*[\d,.\s]+')
            all_text = element.get_text()
            price_matches = price_pattern.findall(all_text)
            if price_matches:
                price = price_matches[0].strip()

        return price or "Harga tidak ditemukan"

    def extract_rating(self, element):
        """Ekstrak rating produk dengan CSS selector Blibli"""
        rating = ""

        # CSS selector untuk rating
        rating_selectors = [
            'div.els-product__rating-wrapper',
            'div[class*="rating"]'
        ]

        for selector in rating_selectors:
            rating_element = element.select_one(selector)
            if rating_element:
                # Cari angka rating dalam element
                rating_text = rating_element.get_text(strip=True)
                rating_match = re.search(r'([1-5]\.[0-9])', rating_text)
                if rating_match:
                    rating = rating_match.group(1)
                    break

        # Jika tidak ditemukan dengan selector, cari dengan pattern
        if not rating:
            rating_pattern = re.compile(r'\b([1-5]\.[0-9])\b')
            all_text = element.get_text()
            rating_matches = rating_pattern.findall(all_text)
            if rating_matches:
                rating = rating_matches[0]

        return rating

    def extract_sold_count(self, element):
        """Ekstrak jumlah terjual dengan CSS selector Blibli"""
        sold = ""

        # CSS selector untuk jumlah terjual
        sold_selectors = [
            'div.els-product__sold',
            'div[class*="sold"]'
        ]

        for selector in sold_selectors:
            sold_element = element.select_one(selector)
            if sold_element:
                sold_text = sold_element.get_text(strip=True)
                # Cari angka dalam teks terjual
                sold_match = re.search(r'(\d+)', sold_text)
                if sold_match:
                    sold = sold_match.group(1) + " terjual"
                    break

        # Jika tidak ditemukan dengan selector, cari dengan pattern
        if not sold:
            sold_patterns = [
                r'(\d+)\s*terjual',
                r'terjual\s*(\d+)',
                r'(\d+[kK]?)\s*terjual'
            ]
            
            all_text = element.get_text().lower()
            for pattern in sold_patterns:
                match = re.search(pattern, all_text)
                if match:
                    sold = match.group(1) + " terjual"
                    break

        return sold

    def extract_shop_name(self, element):
        """Ekstrak nama toko dengan CSS selector Blibli"""
        shop_name = ""

        # CSS selector untuk nama toko
        shop_selectors = [
            'span.els-product__seller-name',
            'span[class*="seller"]',
            'div[class*="seller"]'
        ]

        for selector in shop_selectors:
            shop_element = element.select_one(selector)
            if shop_element:
                shop_name = shop_element.get_text(strip=True)
                if shop_name and len(shop_name) > 3:
                    break

        # Jika tidak ditemukan dengan selector, cari dengan strategi alternatif
        if not shop_name:
            # Cari span yang mungkin nama toko
            spans = element.find_all('span')
            for span in spans:
                text = span.get_text(strip=True)
                if (len(text) > 3 and len(text) < 100 and
                    not re.search(r'Rp|terjual|\d+\.\d+|rating', text, re.IGNORECASE) and
                    not re.match(r'^[\d.,]+$', text) and
                    'store' in text.lower() or 'shop' in text.lower()):
                    shop_name = text
                    break

        return shop_name

    def extract_product_link(self, element):
        """Ekstrak link produk"""
        link = ""

        # Cari link yang mengarah ke halaman produk
        links = element.find_all('a', href=True)
        for a_tag in links:
            href = a_tag.get('href', '')
            # Blibli biasanya menggunakan path /p/ untuk produk
            if '/p/' in href or '/product/' in href:
                if href.startswith('/'):
                    link = 'https://www.blibli.com' + href
                else:
                    link = href
                break

        return link

    def validate_product_data(self, product_data):
        """Validasi data produk minimal"""
        if not product_data:
            return False

        # Minimal harus ada nama dan harga
        has_name = product_data.get('nama_produk') and product_data['nama_produk'] != "Nama tidak ditemukan"
        has_price = product_data.get('harga') and product_data['harga'] != "Harga tidak ditemukan"

        return has_name or has_price

    def scrape_products(self, keyword, max_pages=3, delay_range=(3, 7)):
        """
        Scraping produk dari multiple halaman dengan delay yang lebih aman
        """
        all_products = []

        print(f"\n🚀 Memulai scraping untuk keyword: '{keyword}'")
        print(f"📋 Target maksimal halaman: {max_pages}")
        print(f"⏱️  Delay antar halaman: {delay_range[0]}-{delay_range[1]} detik")

        for page in range(1, max_pages + 1):
            print(f"\n{'='*60}")
            print(f"📄 MEMPROSES HALAMAN {page}")
            print(f"{'='*60}")

            # Bangun URL untuk halaman
            current_url = self.build_search_url(keyword, page)

            # Dapatkan konten halaman
            response = self.get_page_content(current_url)
            if not response:
                print(f"❌ Gagal mengakses halaman {page}, melanjutkan ke halaman berikutnya...")
                continue

            # Parse konten dengan BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')

            # Debug: Cek apakah halaman berisi data produk
            page_text = soup.get_text().lower()
            if 'tidak ditemukan' in page_text or 'no result' in page_text:
                print(f"⚠️  Halaman {page}: Tidak ada hasil pencarian")
                break

            # Ekstrak data produk
            products = self.extract_product_data(soup)

            if products:
                all_products.extend(products)
                print(f"✅ Halaman {page}: {len(products)} produk berhasil diekstrak")
                print(f"📊 Total produk terkumpul: {len(all_products)}")
            else:
                print(f"❌ Halaman {page}: Tidak ditemukan produk yang valid")

                # Jika 2 halaman berturut-turut tidak ada produk, hentikan
                if page > 1:
                    print("🛑 Menghentikan scraping karena tidak ada produk di 2 halaman terakhir")
                    break

            # Delay antar halaman
            if page < max_pages:
                delay = random.uniform(delay_range[0], delay_range[1])
                print(f"⏳ Menunggu {delay:.1f} detik sebelum halaman berikutnya...")
                time.sleep(delay)

        print(f"\n🎯 SCRAPING SELESAI!")
        print(f"📊 Total produk ditemukan: {len(all_products)}")
        return all_products

    def save_to_csv(self, products, filename=None):
        """
        Menyimpan data ke file CSV dengan validasi
        """
        if not products:
            print("⚠️  Tidak ada data untuk disimpan")
            return False

        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'blibli_scraping_{timestamp}.csv'

        try:
            df = pd.DataFrame(products)

            # Bersihkan data sebelum menyimpan
            for col in df.columns:
                if col != 'timestamp':
                    df[col] = df[col].astype(str).str.strip()

            df.to_csv(filename, index=False, encoding='utf-8-sig')

            print(f"\n💾 Data berhasil disimpan ke: {filename}")
            print(f"📊 Jumlah baris: {len(df)}")
            print(f"📋 Kolom: {list(df.columns)}")

            # Tampilkan statistik kualitas data
            self.show_data_quality(df)

            return True

        except Exception as e:
            print(f"❌ Error menyimpan ke CSV: {e}")
            return False

    def show_data_quality(self, df):
        """Tampilkan statistik kualitas data"""
        print(f"\n📈 KUALITAS DATA:")
        for col in df.columns:
            if col != 'timestamp':
                valid_count = df[col].apply(lambda x: x != "" and "tidak ditemukan" not in str(x).lower()).sum()
                percentage = (valid_count / len(df)) * 100
                print(f"   • {col}: {valid_count}/{len(df)} ({percentage:.1f}%)")

    def display_summary(self, products):
        """
        Menampilkan ringkasan data yang di-scrape dengan format yang lebih baik
        """
        if not products:
            print("⚠️  Tidak ada data untuk ditampilkan")
            return

        print("\n" + "="*80)
        print("📊 RINGKASAN HASIL SCRAPING BLIBLI")
        print("="*80)

        df = pd.DataFrame(products)
        print(f"🎯 Total Produk: {len(products)}")

        # Tampilkan sample data dengan format yang rapi
        print(f"\n📋 SAMPLE DATA (3 produk pertama):")
        print("-" * 80)

        for i, product in enumerate(products[:3]):
            print(f"\nPRODUK {i+1}:")
            print(f"  📦 Nama: {product['nama_produk']}")
            print(f"  💰 Harga: {product['harga']}")
            print(f"  ⭐ Rating: {product['rating'] if product['rating'] else 'Tidak ada'}")
            print(f"  📈 Terjual: {product['jumlah_terjual'] if product['jumlah_terjual'] else 'Tidak ada'}")
            print(f"  🏪 Toko: {product['nama_toko'] if product['nama_toko'] else 'Tidak ada'}")
            print(f"  🔗 Link: {product['link_produk'][:60]}{'...' if len(product['link_produk']) > 60 else ''}")

        if len(products) > 3:
            print(f"\n... dan {len(products) - 3} produk lainnya")

# Fungsi main yang diperbaiki
def main():
    """
    Fungsi utama untuk menjalankan scraper dengan error handling yang lebih baik
    """
    print("="*80)
    print("🤖 BLIBLI SCRAPER - Versi Diperbaiki")
    print("👨‍💻 Dikembangkan berdasarkan: Tokopedia Scraper")
    print("🔧 Diadaptasi untuk: Website Blibli")
    print("="*80)
    print("⚠️  PERINGATAN:")
    print("   • Gunakan scraper ini dengan bijak dan bertanggung jawab")
    print("   • Patuhi ketentuan layanan Blibli")
    print("   • Jangan melakukan scraping berlebihan")
    print("="*80)

    # Inisialisasi scraper
    scraper = BlibliScraper()

    try:
        # Input dari user dengan validasi
        while True:
            keyword = input("\n🔍 Masukkan keyword pencarian: ").strip()
            if keyword and len(keyword) >= 2:
                break
            print("❌ Keyword harus minimal 2 karakter!")

        while True:
            try:
                max_pages_input = input("📄 Jumlah halaman (1-10, default=3): ").strip()
                if not max_pages_input:
                    max_pages = 3
                    break
                max_pages = int(max_pages_input)
                if 1 <= max_pages <= 10:
                    break
                else:
                    print("❌ Masukkan angka antara 1-10")
            except ValueError:
                print("❌ Masukkan angka yang valid!")

        # Konfirmasi sebelum scraping
        print(f"\n📋 KONFIGURASI SCRAPING:")
        print(f"   🔍 Keyword: '{keyword}'")
        print(f"   📄 Halaman: {max_pages}")
        print(f"   ⏱️  Estimasi waktu: {max_pages * 2}-{max_pages * 4} menit")

        confirm = input("\n🚀 Lanjutkan scraping? (y/n): ").lower()
        if confirm not in ['y', 'yes', 'ya']:
            print("❌ Scraping dibatalkan")
            return

        # Jalankan scraping
        print(f"\n🎬 MEMULAI SCRAPING...")
        start_time = datetime.now()

        products = scraper.scrape_products(keyword, max_pages)

        end_time = datetime.now()
        duration = end_time - start_time

        if products:
            print(f"\n🎉 SCRAPING BERHASIL DISELESAIKAN!")
            print(f"⏱️  Waktu eksekusi: {duration}")

            # Tampilkan ringkasan
            scraper.display_summary(products)

            # Simpan ke file
            save_option = input("\n💾 Simpan ke file CSV? (y/n): ").lower()
            if save_option in ['y', 'yes', 'ya']:
                custom_filename = input("📁 Nama file (kosongkan untuk auto): ").strip()
                filename = custom_filename if custom_filename else None

                if scraper.save_to_csv(products, filename):
                    print("✅ File berhasil disimpan!")
        else:
            print(f"\n❌ TIDAK ADA PRODUK YANG BERHASIL DI-SCRAPE")
            print(f"💡 KEMUNGKINAN PENYEBAB:")
            print(f"   • Keyword terlalu spesifik: '{keyword}'")
            print(f"   • Struktur website Blibli berubah")
            print(f"   • Koneksi internet bermasalah")
            print(f"   • Anti-bot detection aktif")

            print(f"\n🔧 SARAN PERBAIKAN:")
            print(f"   • Coba keyword yang lebih umum")
            print(f"   • Periksa koneksi internet")
            print(f"   • Tunggu beberapa saat sebelum mencoba lagi")

    except KeyboardInterrupt:
        print(f"\n\n⚠️  SCRAPING DIHENTIKAN OLEH USER")
        print(f"   Data yang sudah terkumpul mungkin hilang")

    except Exception as e:
        print(f"\n❌ ERROR TIDAK TERDUGA: {str(e)}")
        print(f"💡 Silakan coba lagi atau hubungi developer")

    finally:
        print(f"\n👋 Terima kasih telah menggunakan Blibli Scraper!")

# Jalankan program
if __name__ == "__main__":
    main()