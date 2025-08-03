import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import re
from datetime import datetime
import urllib.parse

class CNNIndonesiaScraper:
    def __init__(self):
        self.base_url = "https://www.cnnindonesia.com"
        self.search_url = "https://www.cnnindonesia.com/search?query="
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
    def search_news(self, keyword, max_pages=5):
        """
        Mencari berita berdasarkan keyword
        """
        print(f"Mencari berita dengan keyword: {keyword}")
        
        all_news = []
        page = 1
        
        while page <= max_pages:
            try:
                # Encode keyword untuk URL
                encoded_keyword = urllib.parse.quote(keyword)
                url = f"{self.search_url}{encoded_keyword}"
                
                if page > 1:
                    url += f"&page={page}"
                
                print(f"Mengambil halaman {page}: {url}")
                
                response = requests.get(url, headers=self.headers, timeout=10)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Mencari artikel berita
                articles = soup.find_all('article', class_='box-list')
                
                if not articles:
                    print(f"Tidak ada artikel ditemukan di halaman {page}")
                    break
                
                page_news = []
                for article in articles:
                    try:
                        news_data = self._extract_article_data(article)
                        if news_data:
                            page_news.append(news_data)
                    except Exception as e:
                        print(f"Error extracting article: {e}")
                        continue
                
                if not page_news:
                    print(f"Tidak ada data berita yang berhasil diekstrak di halaman {page}")
                    break
                
                all_news.extend(page_news)
                print(f"Berhasil mengambil {len(page_news)} berita dari halaman {page}")
                
                # Delay untuk menghindari rate limiting
                time.sleep(2)
                page += 1
                
            except requests.RequestException as e:
                print(f"Error mengambil halaman {page}: {e}")
                break
            except Exception as e:
                print(f"Unexpected error di halaman {page}: {e}")
                break
        
        print(f"Total berita yang ditemukan: {len(all_news)}")
        return all_news
    
    def _extract_article_data(self, article):
        """
        Mengekstrak data dari satu artikel
        """
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
            
            # Thumbnail (opsional)
            img_element = article.find('img')
            thumbnail = img_element.get('src') if img_element else ""
            
            return {
                'judul': title,
                'tanggal': date,
                'link': link,
                'thumbnail': thumbnail
            }
            
        except Exception as e:
            print(f"Error extracting article data: {e}")
            return None
    
    def get_article_content(self, article_url):
        """
        Mengambil konten detail dari artikel
        """
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
            print(f"Error mengambil konten artikel {article_url}: {e}")
            return f"Error: {str(e)}"
    
    def scrape_with_content(self, keyword, max_pages=3, get_content=True):
        """
        Scraping berita dengan konten detail
        """
        print("=" * 50)
        print(f"Memulai scraping CNN Indonesia untuk keyword: '{keyword}'")
        print("=" * 50)
        
        # Mencari berita
        news_list = self.search_news(keyword, max_pages)
        
        if not news_list:
            print("Tidak ada berita yang ditemukan!")
            return pd.DataFrame()
        
        # Menambahkan konten detail jika diminta
        if get_content:
            print("\nMengambil konten detail artikel...")
            for i, news in enumerate(news_list):
                print(f"Progress: {i+1}/{len(news_list)} - {news['judul'][:50]}...")
                
                if news['link']:
                    content = self.get_article_content(news['link'])
                    news['konten'] = content
                else:
                    news['konten'] = "Link tidak tersedia"
                
                # Delay untuk menghindari rate limiting
                time.sleep(1)
        
        # Membuat DataFrame
        df = pd.DataFrame(news_list)
        
        # Menampilkan hasil
        print("\n" + "=" * 50)
        print("HASIL SCRAPING")
        print("=" * 50)
        print(f"Total berita: {len(df)}")
        print("\nKolom yang tersedia:")
        for col in df.columns:
            print(f"- {col}")
        
        return df
    
    def save_to_csv(self, df, filename=None):
        """
        Menyimpan hasil ke CSV
        """
        if df.empty:
            print("Tidak ada data untuk disimpan!")
            return
        
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"cnn_indonesia_berita_{timestamp}.csv"
        
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        print(f"\nData berhasil disimpan ke: {filename}")
        
        return filename

# Fungsi utama untuk menjalankan scraper
def main():
    # Inisialisasi scraper
    scraper = CNNIndonesiaScraper()
    
    # Input keyword dari user
    keyword = input("Masukkan keyword pencarian (contoh: cabai rawit): ").strip()
    
    if not keyword:
        print("Keyword tidak boleh kosong!")
        return
    
    # Konfirmasi pengambilan konten detail
    get_content = input("Apakah ingin mengambil konten detail artikel? (y/n): ").lower().strip() == 'y'
    
    # Jumlah halaman maksimal
    try:
        max_pages = int(input("Masukkan jumlah halaman maksimal (default: 3): ") or "3")
    except ValueError:
        max_pages = 3
    
    # Jalankan scraping
    df = scraper.scrape_with_content(keyword, max_pages, get_content)
    
    if not df.empty:
        # Tampilkan preview data
        print("\n" + "=" * 50)
        print("PREVIEW DATA")
        print("=" * 50)
        print(df.head())
        
        # Simpan ke CSV
        save_csv = input("\nApakah ingin menyimpan ke CSV? (y/n): ").lower().strip() == 'y'
        if save_csv:
            filename = scraper.save_to_csv(df)
            
        # Tampilkan statistik
        print("\n" + "=" * 50)
        print("STATISTIK")
        print("=" * 50)
        print(f"Total berita: {len(df)}")
        if 'tanggal' in df.columns:
            print(f"Rentang tanggal: {df['tanggal'].min()} - {df['tanggal'].max()}")
        
        # Tampilkan beberapa judul berita
        print("\nContoh judul berita:")
        for i, title in enumerate(df['judul'].head(5), 1):
            print(f"{i}. {title}")

# Contoh penggunaan langsung
if __name__ == "__main__":
    # Contoh penggunaan tanpa input manual
    scraper = CNNIndonesiaScraper()
    
    # Ganti keyword sesuai kebutuhan
    keyword = "cabai rawit"
    
    print("Contoh scraping untuk keyword:", keyword)
    df = scraper.scrape_with_content(keyword, max_pages=2, get_content=True)
    
    if not df.empty:
        # Simpan hasil
        filename = scraper.save_to_csv(df)
        print(f"\nData tersimpan di: {filename}")
        
        # Tampilkan hasil
        print("\nHasil scraping:")
        for idx, row in df.iterrows():
            print(f"\n{idx+1}. {row['judul']}")
            print(f"   Tanggal: {row['tanggal']}")
            print(f"   Link: {row['link']}")
            if 'konten' in row:
                print(f"   Konten: {row['konten'][:200]}...")
            print("-" * 50)

# Untuk menjalankan dengan input manual, uncomment baris berikut:
# main()