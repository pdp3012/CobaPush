# -*- coding: utf-8 -*-
"""
Web Scraping Berita dari Liputan6.com
Dibuat untuk: Keperluan riset dan akademis
"""
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
from urllib.parse import quote, urljoin
import re
from datetime import datetime
import json
# Untuk menghindari error SSL
import ssl
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class Liputan6Scraper:
    """Scraper untuk mengambil data berita dari Liputan6.com"""

    def __init__(self):
        """Inisialisasi session dan headers"""
        self.session = requests.Session()
        self.session.headers.update({
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
        })

    def get_search_url(self, keyword, page=1):
        """
        Membangun URL pencarian Liputan6 berdasarkan keyword dan halaman
        """
        encoded_keyword = quote(keyword)
        # Liputan6 menggunakan endpoint search dengan parameter q
        search_url = f"https://www.liputan6.com/search?q={encoded_keyword}&page={page}"
        print(f"🔍 URL Pencarian yang Dibuat: {search_url}")
        return search_url

    def get_page_content(self, url, max_retries=3):
        """
        Mendapatkan konten halaman dengan retry mechanism dan delay acak
        """
        for attempt in range(max_retries):
            try:
                print(f"🔄 Mengakses halaman (Percobaan {attempt + 1})...")
                # Delay acak sebelum request untuk menghindari deteksi bot
                time.sleep(random.uniform(2, 5))

                response = self.session.get(url, timeout=15, verify=False)
                response.raise_for_status()

                if response.status_code == 200 and len(response.content) > 5000:
                    print(f"✅ Berhasil mengakses halaman (Size: {len(response.content):,} bytes)")
                    return response
                else:
                    print(f"⚠️ Response tidak normal: Status {response.status_code}, Size: {len(response.content):,} bytes")

            except requests.exceptions.RequestException as e:
                print(f"❌ Request error: {e} (Percobaan {attempt + 1})")

            if attempt < max_retries - 1:
                time.sleep(random.uniform(10, 20))

        print("❌ Gagal mengakses halaman setelah beberapa percobaan")
        return None

    def extract_article_links_from_page(self, search_html):
        """
        Mengekstrak link dan judul artikel dari halaman hasil pencarian Liputan6.
        Liputan6 menggunakan struktur HTML yang berbeda dari Detik
        """
        if not search_html:
            return []

        soup = BeautifulSoup(search_html, 'html.parser')
        articles_data = []

        # --- METODE UTAMA: Cari container artikel Liputan6 ---
        # Liputan6 menggunakan struktur yang berbeda
        article_containers = []
        container_selectors = [
            'article', # Tag article
            '.article-list-item', # Class khusus Liputan6
            '.article-item', # Class artikel item
            '.news-item', # Class berita item
            '.content-item', # Class konten item
            'div[class*="article"]', # Div dengan class mengandung 'article'
            'div[class*="news"]', # Div dengan class mengandung 'news'
            'div[class*="content"]' # Div dengan class mengandung 'content'
        ]

        for selector in container_selectors:
            containers = soup.select(selector)
            if containers:
                article_containers.extend(containers)
                print(f"📦 Ditemukan {len(containers)} container dengan selector: {selector}")
        
        # Jika tidak ditemukan container dengan selector umum, gunakan fallback
        if not article_containers:
            print("🔍 Tidak menemukan container dengan selector umum, menggunakan fallback...")
            # Fallback: cari semua link yang mengarah ke artikel liputan6
            # Pola umum: https://www.liputan6.com/.../read/...
            all_links = soup.find_all('a', href=re.compile(r'https?://.*\.liputan6\.com/.*/read/\d+'))
            for link in all_links:
                parent = link.find_parent()
                if parent and parent not in article_containers:
                     article_containers.append(parent)
                elif link not in article_containers:
                     article_containers.append(link)

        print(f"📦 Total container/artikel potensial ditemukan: {len(article_containers)}")

        # --- EKSTRAKSI DATA DARI SETIAP CONTAINER ---
        for container in article_containers:
            try:
                # Cari link artikel dalam container
                # Liputan6 menggunakan struktur yang berbeda
                link_element = None
                
                # Coba berbagai selector untuk link artikel Liputan6
                link_selectors = [
                    'a[href*="/read/"]', # Link dengan pola /read/
                    'a[href*="liputan6.com"]', # Link ke liputan6.com
                    '.article-title a', # Link dalam judul artikel
                    '.news-title a', # Link dalam judul berita
                    'h2 a', # Link dalam h2
                    'h3 a', # Link dalam h3
                    'a[class*="title"]' # Link dengan class mengandung 'title'
                ]
                
                for selector in link_selectors:
                    link_element = container.select_one(selector)
                    if link_element:
                        break

                if not link_element:
                    continue

                # --- EKSTRAK URL ---
                url = link_element.get('href')
                if not url or 'liputan6.com' not in url:
                    continue

                # Pastikan URL lengkap
                if url.startswith('/'):
                    url = urljoin('https://www.liputan6.com', url)

                # --- EKSTRAK JUDUL ---
                title = None
                # 1. Ambil dari teks link
                title = link_element.get_text(strip=True)
                # 2. Jika tidak ada atau terlalu pendek, coba cari elemen judul lain
                if not title or len(title) < 5:
                    title_selectors = ['h2', 'h3', '.article-title', '.news-title', '.title', '[class*="title"]']
                    for sel in title_selectors:
                        title_elem = container.select_one(sel)
                        if title_elem:
                            tmp_title = title_elem.get_text(strip=True)
                            if tmp_title and len(tmp_title) > 5:
                                title = tmp_title
                                break
                
                # Jika judul masih tidak ditemukan, lewati artikel ini
                if not title or len(title.strip()) == 0:
                    print(f"   ⚠️ Artikel ditemukan tapi judul kosong/tidak valid. URL: {url[:80]}...")
                    continue

                # Tambahkan ke list jika data valid
                articles_data.append({
                    'title': title.strip(),
                    'url': url
                })

            except Exception as e:
                print(f"   ⚠️ Error saat memproses container: {e}")
                continue

        print(f"✅ Berhasil mengekstrak {len(articles_data)} link artikel dari halaman ini")
        return articles_data

    def clean_text(self, text):
        """Membersihkan teks dari karakter tidak diinginkan"""
        if not text:
            return ""
        # Hapus karakter khusus dan whitespace berlebih
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        return text

    def extract_article_details(self, article_url):
        """
        Mengekstrak detail artikel: tanggal rilis dan isi konten
        """
        html_content = self.get_page_content(article_url)
        if not html_content:
            return None, None

        soup = BeautifulSoup(html_content.text, 'html.parser')

        # Ekstrak tanggal rilis
        date_published = None
        # Coba berbagai selector untuk tanggal Liputan6
        date_selectors = [
            'time[datetime]',  # Tag time dengan atribut datetime
            '.article-date time',
            '.article-date',
            '.publish-date',
            '.date-published',
            '.read__time',
            'time',
            '[datetime]',
            '.article-meta time',
            '.news-date'
        ]

        for selector in date_selectors:
            date_element = soup.select_one(selector)
            if date_element:
                # Coba ambil dari atribut datetime dulu
                if date_element.has_attr('datetime'):
                    date_published = date_element['datetime']
                    break
                else:
                    # Coba ambil teks
                    date_text = date_element.get_text(strip=True)
                    if date_text and len(date_text) > 5:
                        # Bersihkan tanggal
                        date_text = re.sub(r'[^\d/\-\s:]', '', date_text).strip()
                        if date_text:
                            date_published = date_text
                            break

        # Jika masih tidak ketemu, cari dengan regex di seluruh teks
        if not date_published:
            body_text = soup.get_text()
            # Prioritaskan format yang umum di Indonesia
            date_patterns = [
                r'(\d{1,2}\s+(Januari|Februari|Maret|April|Mei|Juni|Juli|Agustus|September|Oktober|November|Desember)\s+\d{4}\s*\d{1,2}:\d{2})',
                r'(\d{1,2}\s+(Januari|Februari|Maret|April|Mei|Juni|Juli|Agustus|September|Oktober|November|Desember)\s+\d{4})',
                r'(\d{1,2}[/-]\d{1,2}[/-]\d{4}\s*\d{1,2}:\d{2})',
                r'(\d{1,2}[/-]\d{1,2}[/-]\d{4})',
                r'(\d{4}[/-]\d{2}[/-]\d{2})'
            ]
            for pattern in date_patterns:
                match = re.search(pattern, body_text)
                if match:
                    date_published = match.group(1)
                    break

        # Ekstrak konten artikel
        content_text = ""
        # Coba berbagai selector untuk konten Liputan6
        content_selectors = [
            '.article-content-body', # Selector utama Liputan6
            '.read__content',
            '.article-content',
            '.news-content',
            'article .content',
            'article',
            '.post-content',
            '.article-body',
            '.content-body'
        ]

        content_element = None
        for selector in content_selectors:
            content_element = soup.select_one(selector)
            if content_element:
                print(f"   📝 Konten ditemukan dengan selector: {selector}")
                break

        if content_element:
            # Bersihkan konten
            for unwanted in content_element(["script", "style", "nav", "aside", "header", "footer", "advertisement", "ads", "noscript"]):
                unwanted.decompose()

            for unwanted in content_element.find_all(class_=re.compile(r'.*(ads|advertisement|promo|related|widget|sidebar|footer).*', re.I)):
                unwanted.decompose()
            for unwanted in content_element.find_all(id=re.compile(r'.*(ads|advertisement|promo|related|widget).*', re.I)):
                unwanted.decompose()

            content_text = content_element.get_text(separator=' ', strip=True)
        else:
            # Fallback: ambil teks dari body
            print("   ⚠️ Tidak menemukan container konten utama, menggunakan fallback...")
            body = soup.find('body')
            if body:
                for unwanted in body(["script", "style", "nav", "aside", "header", "footer", "noscript"]):
                    unwanted.decompose()
                content_text = body.get_text(separator=' ', strip=True)

        content_text = self.clean_text(content_text)

        # Potong jika terlalu panjang
        if len(content_text) > 20000:
            content_text = content_text[:20000] + "... (konten dipotong)"

        return date_published, content_text

    def scrape_liputan6_news(self, keyword, max_articles=500, max_pages=50):
        """
        Scraping berita dari Liputan6 berdasarkan keyword
        """
        print(f"🚀 MEMULAI SCRAPING BERITA LIPUTAN6 UNTUK KEYWORD: '{keyword}'")
        print(f"📊 Target: {max_articles} artikel maksimal dari {max_pages} halaman")
        start_time = datetime.now()

        all_article_links = []
        processed_urls = set()
        current_page = 1
        consecutive_empty_pages = 0
        max_consecutive_empty = 3

        # --- TAHAP 1: Kumpulkan link artikel ---
        print("\n🔍 TAHAP 1: Mengumpulkan link artikel...")
        while len(all_article_links) < max_articles and current_page <= max_pages and consecutive_empty_pages < max_consecutive_empty:
            print(f"\n📄 Memproses halaman hasil pencarian {current_page}...")
            search_url = self.get_search_url(keyword, current_page)
            response = self.get_page_content(search_url)

            if not response:
                print(f"❌ Gagal mengambil halaman {current_page}")
                current_page += 1
                continue

            page_links = self.extract_article_links_from_page(response.text)

            if not page_links:
                print(f"ℹ️ Tidak menemukan artikel baru di halaman {current_page}")
                consecutive_empty_pages += 1
            else:
                print(f"✅ Menemukan {len(page_links)} artikel di halaman {current_page}")
                consecutive_empty_pages = 0

                initial_count = len(all_article_links)
                for link_data in page_links:
                    if len(all_article_links) >= max_articles:
                        break
                    url = link_data['url']
                    if url not in processed_urls:
                        processed_urls.add(url)
                        all_article_links.append(link_data)

                added_count = len(all_article_links) - initial_count
                print(f"📈 Menambahkan {added_count} artikel baru (total link unik: {len(all_article_links)})")

            if len(all_article_links) >= max_articles:
                print(f"🎯 Telah mencapai target {max_articles} link artikel.")
                break

            current_page += 1
            # Delay antar halaman
            if current_page <= max_pages:
                delay = random.uniform(3, 6)
                print(f"⏳ Delay {delay:.1f} detik sebelum halaman berikutnya...")
                time.sleep(delay)

        if not all_article_links:
            print("❌ Tidak menemukan link artikel")
            return pd.DataFrame()

        print(f"\n✅ Berhasil mengumpulkan {len(all_article_links)} link artikel unik")

        # --- TAHAP 2: Ekstrak detail dari setiap artikel ---
        results = []
        target_count = min(max_articles, len(all_article_links))
        print(f"\n📄 TAHAP 2: Mengekstrak detail dari {target_count} artikel...")

        for i, article_data in enumerate(all_article_links[:target_count], 1):
            url = article_data['url']
            title = article_data['title']
            print(f"\n[{i}/{target_count}] Memproses: {title[:60]}...")

            try:
                date_published, content_text = self.extract_article_details(url)

                results.append({
                    'judul_berita': self.clean_text(title),
                    'link_berita': url,
                    'tanggal_rilis': date_published if date_published else "Tanggal tidak ditemukan",
                    'detail_konten': content_text if content_text else "Konten tidak dapat diambil"
                })
                print(f"   ✅ Detail artikel berhasil diekstrak")

            except Exception as e:
                print(f"   ❌ Error memproses artikel: {e}")
                results.append({
                    'judul_berita': self.clean_text(title),
                    'link_berita': url,
                    'tanggal_rilis': "Error saat mengambil data",
                    'detail_konten': f"Error: {str(e)}"
                })

            # Delay antar artikel untuk menghindari rate limiting
            if i < target_count:
                time.sleep(random.uniform(2, 4))

        end_time = datetime.now()
        duration = end_time - start_time

        if results:
            df = pd.DataFrame(results)
            print(f"\n✅ SCRAPING SELESAI!")
            print(f"⏱️ Waktu eksekusi: {duration}")
            print(f"📊 Artikel berhasil diekstrak: {len(results)}")
            return df
        else:
            print("❌ Tidak ada data yang berhasil diekstrak")
            return pd.DataFrame()

    def display_statistics(self, df):
        """Menampilkan statistik hasil scraping"""
        if df.empty:
            print("📊 Tidak ada data untuk ditampilkan")
            return

        print("\n📈 STATISTIK HASIL SCRAPING:")
        print(f"   • Total Artikel: {len(df)}")

        # Statistik Tanggal
        valid_dates = df['tanggal_rilis'].apply(
            lambda x: x != "Tanggal tidak ditemukan" and not str(x).startswith("Error")
        ).sum()
        print(f"   • Tanggal Valid: {valid_dates} ({(valid_dates/len(df)*100):.1f}%)")

        # Statistik Konten
        valid_content = df['detail_konten'].apply(
            lambda x: isinstance(x, str) and len(x) > 100 and not str(x).startswith("Error")
        ).sum()
        print(f"   • Konten Valid: {valid_content} ({(valid_content/len(df)*100):.1f}%)")

        # Rata-rata panjang konten
        if valid_content > 0:
            avg_content_len = df[df['detail_konten'].apply(lambda x: isinstance(x, str) and len(x) > 100)]['detail_konten'].str.len().mean()
            print(f"   • Rata-rata Panjang Konten: {avg_content_len:.0f} karakter")

    def save_results(self, df_results, keyword):
        """Menyimpan hasil ke file CSV dan JSON secara otomatis"""
        if df_results.empty:
            print("❌ Tidak ada data untuk disimpan.")
            return

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Nama file
        csv_filename = f"berita_liputan6_{keyword.replace(' ', '_')}_{timestamp}.csv"
        json_filename = f"berita_liputan6_{keyword.replace(' ', '_')}_{timestamp}.json"

        # Simpan ke CSV
        try:
            df_results.to_csv(csv_filename, index=False, encoding='utf-8-sig')
            print(f"💾 Hasil disimpan ke CSV: {csv_filename}")
        except Exception as e:
            print(f"❌ Gagal menyimpan ke CSV: {e}")

        # Simpan ke JSON
        try:
            df_results.to_json(json_filename, orient='records', indent=4, force_ascii=False)
            print(f"💾 Hasil disimpan ke JSON: {json_filename}")
        except Exception as e:
            print(f"❌ Gagal menyimpan ke JSON: {e}")

def main():
    """Fungsi utama program"""
    print("=" * 90)
    print("🎓 PROGRAM SCRAPING BERITA LIPUTAN6.COM")
    print("👨‍💻 Dikembangkan untuk: Keperluan Riset dan Akademis")
    print("=" * 90)
    print("⚠️ PENTING:")
    print(" • Gunakan scraper ini dengan bijak dan etis")
    print(" • Patuhi ketentuan layanan Liputan6.com")
    print(" • Data hasil scraping hanya untuk keperluan penelitian/analisis")
    print("=" * 90)

    # Inisialisasi scraper
    scraper = Liputan6Scraper()

    try:
        # === INPUT LANGSUNG TANPA KONFIRMASI ===
        # Input keyword
        keyword = input("\n🔍 Masukkan keyword pencarian berita: ").strip()
        if not keyword:
            print("❌ Keyword tidak boleh kosong!")
            return

        # Input jumlah artikel
        while True:
            try:
                max_articles_input = input("📊 Jumlah maksimal artikel (default 10, maks 2000): ").strip()
                if not max_articles_input:
                    max_articles = 10
                    break
                max_articles = int(max_articles_input)
                if 1 <= max_articles <= 2000:
                    break
                else:
                    print("❌ Masukkan angka antara 1-2000")
            except ValueError:
                print("❌ Masukkan angka yang valid!")

        # Parameter default untuk halaman
        max_pages = min(100, max_articles // 5 + 5)
        max_pages = max(10, max_pages)
        max_pages = min(100, max_pages)

        print(f"\n📝 Konfigurasi scraping:")
        print(f"   • Keyword: '{keyword}'")
        print(f"   • Maksimal artikel: {max_articles}")
        print(f"   • Maksimal halaman (auto): {max_pages}")

        # === LANGSUNG MULAI SCRAPING TANPA KONFIRMASI ===
        print(f"\n🚀 Memulai proses scraping...")
        df_results = scraper.scrape_liputan6_news(keyword, max_articles, max_pages)

        if not df_results.empty:
            # Tampilkan statistik
            scraper.display_statistics(df_results)

            # Tampilkan preview hasil
            print("\n" + "=" * 90)
            print("📊 HASIL SCRAPING (Preview 5 baris pertama):")
            print("=" * 90)
            print(df_results.head().to_string(index=False, max_colwidth=30))

            # === LANGSUNG SIMPAN KE CSV DAN JSON TANPA KONFIRMASI ===
            print(f"\n💾 Menyimpan hasil ke file...")
            scraper.save_results(df_results, keyword)

            # Tampilkan preview data akhir
            print("\n📄 PREVIEW DETAIL KONTEN (3 Artikel Pertama):")
            print("=" * 90)
            for idx, row in df_results.head(3).iterrows():
                print(f"\n📋 Judul: {row['judul_berita']}")
                print(f"📅 Tanggal: {row['tanggal_rilis']}")
                print(f"🔗 URL: {row['link_berita']}")
                konten_preview = str(row['detail_konten'])[:500] + ("..." if len(str(row['detail_konten'])) > 500 else "")
                print(f"📝 Konten (preview 500 karakter):")
                print(f"   {konten_preview}")
                print("-" * 50)

        else:
            print("\n❌ Maaf, tidak ada data yang berhasil diambil.")
            print("💡 Tips:")
            print("   • Pastikan keyword yang dimasukkan spesifik")
            print("   • Periksa koneksi internet")
            print("   • Coba keyword lain")

    except KeyboardInterrupt:
        print("\n⚠️ Program dihentikan oleh user")
    except Exception as e:
        print(f"\n❌ Terjadi error: {e}")
        print("💡 Silakan coba lagi atau hubungi developer")

    print("\n👋 Terima kasih telah menggunakan program ini!")
    print("📚 Gunakan data dengan bijak dan sesuai etika riset")

# Jalankan program
if __name__ == "__main__":
    main()