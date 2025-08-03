# 🛒 Shopee Product Scraper

**Scraper produk Shopee dengan fitur login otomatis dan ekstraksi data lengkap**

## 📋 Deskripsi

Scraper ini dirancang untuk mengambil data produk dari website Shopee Indonesia dengan fitur-fitur berikut:

- ✅ **Login otomatis** dengan nomor telepon dan password
- ✅ **Ekstraksi data lengkap**: nama produk, harga, jumlah terjual, nama toko, lokasi toko, rating
- ✅ **CSS Selector yang tepat** sesuai dengan struktur HTML Shopee
- ✅ **Anti-deteksi** dengan konfigurasi Chrome driver yang optimal
- ✅ **Handle CAPTCHA** secara otomatis
- ✅ **Export ke CSV dan Excel**
- ✅ **Kompatibel dengan Google Colab**

## 🚀 Cara Penggunaan di Google Colab

### Langkah 1: Setup Dependencies
Jalankan cell pertama untuk menginstall semua dependencies yang diperlukan:

```python
# Install packages
!pip install selenium beautifulsoup4 pandas openpyxl requests lxml

# Install Chrome dan ChromeDriver
!apt-get update
!apt-get install -y wget unzip
!wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add -
!echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list
!apt-get update
!apt-get install -y google-chrome-stable

# Download ChromeDriver
!wget -O /tmp/chromedriver.zip https://chromedriver.storage.googleapis.com/$(curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE)/chromedriver_linux64.zip
!unzip /tmp/chromedriver.zip -d /usr/local/bin/
!chmod +x /usr/local/bin/chromedriver
```

### Langkah 2: Load Scraper
Copy-paste seluruh kode dari file `shopee_scraper.py` ke cell kedua.

### Langkah 3: Jalankan Scraping
Gunakan fungsi `scrape_shopee_colab()` untuk melakukan scraping:

```python
# Contoh penggunaan
df = scrape_shopee_colab("laptop", 2)
print(df)
```

## 📊 Data yang Diambil

Scraper ini mengambil data berikut dari setiap produk:

| Field | Deskripsi | CSS Selector |
|-------|-----------|--------------|
| `nama_produk` | Nama produk | `div.line-clamp-2` |
| `harga` | Harga produk | `span.font-medium.text-base\/5.truncate` |
| `jumlah_terjual` | Jumlah terjual | `div.truncate.text-shopee-black87.text-xs.min-h-4` |
| `nama_toko` | Nama toko | `div.text-shopee-black87.text-xs.min-h-4` |
| `lokasi_toko` | Lokasi toko | `div.flex-shrink.min-w-0.truncate.text-shopee-black54` |
| `rating_produk` | Rating produk | `div.text-shopee-black87.text-xs\/sp14.flex-none` |
| `waktu_scraping` | Waktu scraping | Auto-generated |

## 🔧 Konfigurasi Login

Scraper menggunakan kredensial default:
- **Nomor Telepon**: `081316084860`
- **Password**: `Pradipta301203`

Untuk mengubah kredensial, edit parameter di fungsi `login_shopee()`:

```python
def login_shopee(self, phone="YOUR_PHONE", password="YOUR_PASSWORD"):
```

## 📁 Output Files

Scraper akan menghasilkan file:
- **CSV**: `shopee_products_YYYYMMDD_HHMMSS.csv`
- **Excel**: `shopee_products_YYYYMMDD_HHMMSS.xlsx`

## 🎯 Contoh Penggunaan

### Scraping Produk Laptop
```python
df_laptop = scrape_shopee_colab("laptop", 3)
```

### Scraping Produk Smartphone
```python
df_smartphone = scrape_shopee_colab("smartphone", 2)
```

### Scraping dengan Keyword Kustom
```python
df_custom = scrape_shopee_colab("headphone wireless", 1)
```

## 📈 Analisis Data

Setelah scraping, Anda dapat melakukan analisis data:

```python
# Statistik dasar
print(f"Total produk: {len(df)}")
print(f"Produk dengan harga: {len(df[df['harga'] != 'Tidak ditemukan'])}")
print(f"Produk dengan rating: {len(df[df['rating_produk'] != 'Tidak ditemukan'])}")

# Preview data
print(df.head())
```

## 🔍 Troubleshooting

### Masalah Login
- Pastikan nomor telepon dan password benar
- Jika login gagal, scraper akan mencoba scraping tanpa login
- Periksa apakah ada verifikasi 2FA yang diperlukan

### Masalah CAPTCHA
- Scraper akan mendeteksi CAPTCHA secara otomatis
- Jika CAPTCHA muncul, tunggu beberapa saat atau refresh halaman

### Masalah CSS Selector
- Jika data tidak terambil, kemungkinan struktur HTML Shopee berubah
- Periksa dan update CSS selector sesuai kebutuhan

### Masalah Chrome Driver
- Pastikan Chrome dan ChromeDriver terinstall dengan benar
- Restart runtime Google Colab jika diperlukan

## ⚠️ Disclaimer

- Scraper ini dibuat untuk tujuan edukasi dan penelitian
- Gunakan dengan bijak dan hormati Terms of Service Shopee
- Jangan melakukan scraping berlebihan yang dapat membebani server
- Penulis tidak bertanggung jawab atas penggunaan yang melanggar hukum

## 🛠️ Dependencies

- `selenium`: Web automation
- `beautifulsoup4`: HTML parsing
- `pandas`: Data manipulation
- `openpyxl`: Excel file handling
- `requests`: HTTP requests
- `lxml`: XML/HTML parser

## 📞 Support

Jika mengalami masalah atau memerlukan bantuan:
1. Periksa error message dengan teliti
2. Pastikan semua dependencies terinstall
3. Coba restart runtime Google Colab
4. Periksa koneksi internet

## 🔄 Update Log

- **v1.0**: Initial release dengan fitur login otomatis
- **v1.1**: Penambahan handle CAPTCHA
- **v1.2**: Optimasi CSS selector
- **v1.3**: Penambahan export Excel dan visualisasi

---

**Dibuat dengan ❤️ untuk keperluan edukasi data mining**