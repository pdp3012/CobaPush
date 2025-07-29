# Shopee Scraper untuk Google Colab

Scraper canggih untuk mengambil data produk dari Shopee yang dioptimalkan untuk Google Colab. Scraper ini dapat mengatasi anti-bot measures dan melakukan scraping data secara otomatis berdasarkan keyword.

## Fitur Utama

- ✅ **Anti-Bot Detection**: Menggunakan teknik stealth untuk menghindari deteksi bot
- ✅ **Multiple Data Extraction**: Mengambil nama produk, harga, rating, jumlah terjual, nama toko, dan lokasi
- ✅ **Keyword-based Search**: User hanya perlu memasukkan keyword produk
- ✅ **Automatic URL Generation**: Otomatis mengarahkan ke halaman search Shopee
- ✅ **Google Colab Optimized**: Didesain khusus untuk environment Colab
- ✅ **CSV Export**: Data tersimpan dalam format CSV
- ✅ **Google Drive Integration**: Otomatis menyimpan ke Google Drive
- ✅ **Multiple Fallback Methods**: Menggunakan API dan web scraping sebagai backup

## Data yang Di-scrape

1. **Nama Produk** - Nama lengkap produk
2. **Harga** - Harga produk dalam Rupiah
3. **Rating** - Rating produk (1-5 bintang)
4. **Jumlah Terjual** - Jumlah unit yang telah terjual
5. **Nama Toko** - Nama toko/seller
6. **Lokasi Toko** - Lokasi toko/seller

## Cara Penggunaan di Google Colab

### 1. Setup Environment (Cell 1)
```python
# Install dependencies
!pip install selenium pandas requests fake-useragent webdriver-manager beautifulsoup4 lxml

# Install Chrome dan ChromeDriver
!apt-get update
!apt-get install -y wget unzip
!wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add -
!echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list
!apt-get update
!apt-get install -y google-chrome-stable

!wget -N https://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_linux64.zip
!unzip -o chromedriver_linux64.zip
!chmod +x chromedriver
!mv chromedriver /usr/local/bin/
```

### 2. Upload Scraper Code (Cell 2)
Upload file `shopee_colab_scraper.py` atau copy-paste kode scraper ke cell baru.

### 3. Jalankan Scraper (Cell 3)
```python
# Import dan jalankan scraper
from shopee_colab_scraper import main_colab
main_colab()
```

### 4. Input Data
- Masukkan keyword produk (contoh: "cabai rawit")
- Masukkan jumlah maksimal produk yang ingin di-scrape (1-100)

## Contoh Penggunaan

```
=== SHOPEE SCRAPER UNTUK GOOGLE COLAB ===
============================================================
Scraper yang dioptimalkan untuk environment Colab
============================================================

Masukkan keyword produk yang ingin di-scrape: cabai rawit
Masukkan jumlah maksimal produk (1-100): 20

Memulai proses scraping untuk 'cabai rawit'...
Memulai scraping untuk keyword: cabai rawit
Target jumlah produk: 20
Browser berhasil dibuka
Membuka URL: https://shopee.co.id/search?keyword=cabai%20rawit
Scrolling halaman...
Ditemukan 50 produk dengan selector: [data-sqe="link"]
Mengekstrak data produk...
✓ Produk 1: Cabai Rawit Merah Segar 1kg...
✓ Produk 2: Cabai Rawit Hijau Fresh 500gr...
...

============================================================
HASIL SCRAPING SHOPEE
============================================================
Total produk: 20
Keyword: cabai rawit
============================================================

SAMPLE DATA:
------------------------------------------------------------
1. Cabai Rawit Merah Segar 1kg - Fresh dari Kebun...
   Harga: 25000 | Rating: 4.8 | Terjual: 1500
   Toko: Toko Sayur Segar | Lokasi: Jakarta Selatan

2. Cabai Rawit Hijau Fresh 500gr - Premium Quality...
   Harga: 15000 | Rating: 4.5 | Terjual: 800
   Toko: Fresh Market | Lokasi: Bandung

...

STATISTIK:
------------------------------------------------------------
Rata-rata harga: Rp 18,500
Harga tertinggi: Rp 35,000
Harga terendah: Rp 8,000

============================================================
SCRAPING SELESAI!
============================================================
Waktu eksekusi: 45.23 detik
Total produk berhasil di-scrape: 20
File tersimpan: shopee_cabai_rawit_20231201_143022.csv
============================================================
```

## File Output

Data akan tersimpan dalam file CSV dengan format:
```
shopee_[keyword]_[timestamp].csv
```

Contoh: `shopee_cabai_rawit_20231201_143022.csv`

## Troubleshooting

### Error: Chrome driver tidak ditemukan
```python
# Pastikan Chrome dan ChromeDriver sudah terinstall dengan benar
!which google-chrome
!which chromedriver
```

### Error: Tidak ada produk yang ditemukan
- Coba keyword yang berbeda
- Pastikan koneksi internet stabil
- Tunggu beberapa saat dan coba lagi

### Error: Timeout
- Scraper akan otomatis mencoba selector alternatif
- Jika masih gagal, coba kurangi jumlah produk yang di-scrape

## Tips Penggunaan

1. **Keyword yang Spesifik**: Gunakan keyword yang spesifik untuk hasil yang lebih akurat
2. **Jumlah Produk**: Mulai dengan jumlah kecil (10-20) untuk testing
3. **Waktu Eksekusi**: Proses scraping membutuhkan waktu 30-60 detik tergantung jumlah produk
4. **Google Drive**: Pastikan Google Drive sudah ter-mount untuk penyimpanan otomatis

## Keamanan dan Etika

- Scraper ini menggunakan teknik yang menghormati rate limiting
- Tidak melakukan scraping berlebihan untuk menghindari beban server
- Data yang di-scrape hanya untuk tujuan analisis dan penelitian
- Patuhi Terms of Service Shopee

## Dependencies

- selenium==4.15.2
- pandas==2.1.3
- requests==2.31.0
- fake-useragent==1.4.0
- webdriver-manager==4.0.1
- beautifulsoup4==4.12.2
- lxml==4.9.3

## Support

Jika mengalami masalah, pastikan:
1. Semua dependencies terinstall dengan benar
2. Chrome dan ChromeDriver terinstall
3. Koneksi internet stabil
4. Google Drive ter-mount (untuk penyimpanan)

## Disclaimer

Scraper ini dibuat untuk tujuan edukasi dan penelitian. Pengguna bertanggung jawab atas penggunaan yang sesuai dengan Terms of Service Shopee dan peraturan yang berlaku.