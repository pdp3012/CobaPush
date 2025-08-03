# CNN Indonesia Scraper untuk Google Colab
# Copy-paste kode ini ke cell baru di Google Colab

# Install dependencies (jalankan sekali saja)
!pip install requests beautifulsoup4 pandas lxml

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import urllib.parse
from datetime import datetime

class CNNIndonesiaScraper:
    def __init__(self):
        self.base_url = "https://www.cnnindonesia.com"
        self.search_url = "https://www.cnnindonesia.com/search?query="
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
    def search_news(self, keyword, max_pages=3):
        """Mencari berita berdasarkan keyword"""
        print(f"🔍 Mencari berita: '{keyword}'")
        
        all_news = []
        page = 1
        
        while page <= max_pages:
            try:
                # Encode keyword untuk URL
                encoded_keyword = urllib.parse.quote(keyword)
                url = f"{self.search_url}{encoded_keyword}"
                
                if page > 1:
                    url += f"&page={page}"
                
                print(f"📄 Halaman {page}: {url}")
                
                response = requests.get(url, headers=self.headers, timeout=10)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Mencari artikel berita
                articles = soup.find_all('article', class_='box-list')
                
                if not articles:
                    print(f"❌ Tidak ada artikel di halaman {page}")
                    break
                
                page_news = []
                for article in articles:
                    try:
                        news_data = self._extract_article_data(article)
                        if news_data:
                            page_news.append(news_data)
                    except Exception as e:
                        continue
                
                if not page_news:
                    print(f"❌ Tidak ada data berita di halaman {page}")
                    break
                
                all_news.extend(page_news)
                print(f"✅ {len(page_news)} berita dari halaman {page}")
                
                time.sleep(2)  # Delay untuk menghindari rate limiting
                page += 1
                
            except Exception as e:
                print(f"❌ Error halaman {page}: {e}")
                break
        
        print(f"📊 Total berita ditemukan: {len(all_news)}")
        return all_news
    
    def _extract_article_data(self, article):
        """Mengekstrak data dari satu artikel"""
        try:
            # Judul dan link
            title_element = article.find('h2', class_='title')
            if not title_element:
                title_element = article.find('h3', class_='title')
            
            if not title_element:
                return None
            
            title = title_element.get_text(strip=True)
            
            # Link artikel
            link_element = title_element.find('a')
            if not link_element:
                return None
            
            link = link_element.get('href')
            if link and not link.startswith('http'):
                link = self.base_url + link
            
            # Tanggal
            date_element = article.find('span', class_='date')
            if not date_element:
                date_element = article.find('div', class_='date')
            
            date = date_element.get_text(strip=True) if date_element else ""
            
            return {
                'judul': title,
                'tanggal': date,
                'link': link
            }
            
        except Exception as e:
            return None
    
    def get_article_content(self, article_url):
        """Mengambil konten detail dari artikel"""
        try:
            response = requests.get(article_url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Mencari konten artikel
            content_element = soup.find('div', class_='detail-text')
            if not content_element:
                content_element = soup.find('div', class_='content-text')
            if not content_element:
                content_element = soup.find('div', class_='article-content')
            
            if content_element:
                # Menghapus elemen yang tidak diinginkan
                for unwanted in content_element.find_all(['script', 'style', 'iframe']):
                    unwanted.decompose()
                
                # Mengambil semua paragraf
                paragraphs = content_element.find_all('p')
                content = '\n\n'.join([p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)])
                
                return content
            else:
                return "Konten tidak ditemukan"
                
        except Exception as e:
            return f"Error: {str(e)}"
    
    def scrape_with_content(self, keyword, max_pages=3, get_content=True):
        """Scraping berita dengan konten detail"""
        print("=" * 60)
        print(f"🚀 MEMULAI SCRAPING CNN INDONESIA")
        print(f"🔍 Keyword: '{keyword}'")
        print(f"📄 Max halaman: {max_pages}")
        print(f"📝 Ambil konten: {'Ya' if get_content else 'Tidak'}")
        print("=" * 60)
        
        # Mencari berita
        news_list = self.search_news(keyword, max_pages)
        
        if not news_list:
            print("❌ Tidak ada berita yang ditemukan!")
            return pd.DataFrame()
        
        # Menambahkan konten detail jika diminta
        if get_content:
            print("\n📖 Mengambil konten detail artikel...")
            for i, news in enumerate(news_list):
                print(f"⏳ Progress: {i+1}/{len(news_list)} - {news['judul'][:50]}...")
                
                if news['link']:
                    content = self.get_article_content(news['link'])
                    news['konten'] = content
                else:
                    news['konten'] = "Link tidak tersedia"
                
                time.sleep(1)  # Delay untuk menghindari rate limiting
        
        # Membuat DataFrame
        df = pd.DataFrame(news_list)
        
        # Menampilkan hasil
        print("\n" + "=" * 60)
        print("📊 HASIL SCRAPING")
        print("=" * 60)
        print(f"📈 Total berita: {len(df)}")
        print(f"📋 Kolom: {', '.join(df.columns)}")
        
        return df
    
    def save_to_csv(self, df, filename=None):
        """Menyimpan hasil ke CSV"""
        if df.empty:
            print("❌ Tidak ada data untuk disimpan!")
            return
        
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"cnn_indonesia_{timestamp}.csv"
        
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        print(f"💾 Data tersimpan: {filename}")
        
        return filename

# ========================================
# CONTOH PENGGUNAAN
# ========================================

# Inisialisasi scraper
scraper = CNNIndonesiaScraper()

# Ganti keyword sesuai kebutuhan
keyword = "cabai rawit"  # Bisa diganti dengan keyword lain

print("🎯 CONTOH SCRAPING CNN INDONESIA")
print("=" * 50)

# Jalankan scraping
df = scraper.scrape_with_content(keyword, max_pages=2, get_content=True)

if not df.empty:
    # Tampilkan preview
    print("\n📋 PREVIEW DATA:")
    print(df.head())
    
    # Simpan ke CSV
    filename = scraper.save_to_csv(df)
    
    # Tampilkan beberapa hasil
    print("\n📰 CONTOH BERITA:")
    for idx, row in df.head(3).iterrows():
        print(f"\n{idx+1}. {row['judul']}")
        print(f"   📅 {row['tanggal']}")
        print(f"   🔗 {row['link']}")
        if 'konten' in row:
            print(f"   📝 {row['konten'][:150]}...")
        print("-" * 50)
    
    # Download file CSV (untuk Google Colab)
    from google.colab import files
    files.download(filename)
    print(f"\n📥 File {filename} siap didownload!")
else:
    print("❌ Tidak ada data yang berhasil di-scrape")

# ========================================
# CARA PENGGUNAAN LAIN
# ========================================

# Untuk keyword lain, ganti saja variabel keyword:
# keyword = "harga beras"
# keyword = "inflasi"
# keyword = "pemilu 2024"
# dll

# Untuk tidak mengambil konten detail (lebih cepat):
# df = scraper.scrape_with_content(keyword, max_pages=3, get_content=False)

# Untuk lebih banyak halaman:
# df = scraper.scrape_with_content(keyword, max_pages=5, get_content=True)