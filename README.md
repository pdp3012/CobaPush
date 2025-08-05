# 🛍️ Enhanced Shopee Scraper

**Dikembangkan oleh: Dosen Data Mining dengan 30 tahun pengalaman profesional**

## 📋 Deskripsi

Enhanced Shopee Scraper adalah tool scraping canggih yang dirancang untuk mengekstrak data produk dari platform Shopee Indonesia secara otomatis. Tool ini dilengkapi dengan fitur auto-login via cookies, error handling yang robust, dan optimasi performa untuk scraping skala besar.

## ✨ Fitur Utama

- 🔐 **Auto-Login via Cookies**: Login otomatis menggunakan file cookies.json
- 🛡️ **Anti-Deteksi Bot**: Konfigurasi khusus untuk menghindari deteksi sebagai bot
- 🔄 **Retry Mechanism**: Sistem retry otomatis jika scraping gagal
- 📊 **Data Validation**: Validasi dan cleaning data hasil scraping
- 📝 **Comprehensive Logging**: Log detail untuk monitoring dan debugging
- 🎯 **Multiple Selector Fallback**: Fallback selector untuk handling perubahan struktur HTML
- ⚡ **Performance Optimization**: Optimasi untuk scraping cepat dan efisien

## 🚀 Instalasi

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Install Chrome Browser
Pastikan Chrome browser sudah terinstall di sistem Anda.

### 3. Setup Cookies (Opsional)
Untuk scraping dengan login, buat file `cookies.json` dengan format:

```json
[
  {
    "name": "session_id",
    "value": "your_session_value",
    "domain": ".shopee.co.id",
    "path": "/",
    "expirationDate": 1735689600,
    "sameSite": "Strict",
    "secure": true,
    "httpOnly": false
  }
]
```

## 📖 Cara Penggunaan

### 1. Basic Usage

```bash
python enhanced_shopee_scraper.py
```

### 2. Programmatic Usage

```python
from enhanced_shopee_scraper import ShopeeScraper

# Initialize scraper
scraper = ShopeeScraper(headless=True, cookies_file="cookies.json")

# Start scraping
success = scraper.scrape_shopee(
    keyword="laptop gaming",
    max_page=5,
    output_file="hasil_scraping.csv"
)
```

## 📊 Data yang Di-scrape

Setiap produk akan menghasilkan data dengan format:

| Field | Deskripsi |
|-------|-----------|
| `product_name` | Nama produk |
| `price` | Harga produk |
| `sold` | Jumlah terjual |
| `location` | Lokasi penjual |
| `rating` | Rating produk |
| `product_link` | Link produk |
| `kategori` | Kata kunci pencarian |
| `halaman` | Halaman sumber data |
| `scraped_at` | Timestamp scraping |

## 🔧 Konfigurasi

### Parameter Scraper

```python
scraper = ShopeeScraper(
    headless=True,        # Mode headless browser
    cookies_file="cookies.json"  # Path ke file cookies
)
```

### Timeout dan Retry

```python
# Dalam class ShopeeScraper
self.wait_timeout = 20      # Timeout untuk loading halaman (detik)
self.retry_attempts = 3     # Jumlah retry jika gagal
```

## 📁 Struktur File

```
project/
├── enhanced_shopee_scraper.py  # Main scraper (RECOMMENDED)
├── shopee_scraper.py          # Original scraper
├── requirements.txt           # Dependencies
├── cookies.json              # Login cookies (opsional)
├── scraping.log              # Log file (auto-generated)
└── README.md                 # Dokumentasi
```

## 🛠️ Troubleshooting

### 1. ChromeDriver Error
```
Error: ChromeDriver not found
```
**Solusi**: Install Chrome browser dan pastikan webdriver-manager dapat mengunduh driver yang sesuai.

### 2. Timeout Error
```
TimeoutException: Message: timeout
```
**Solusi**: 
- Periksa koneksi internet
- Tingkatkan `wait_timeout` value
- Coba scraping dengan jumlah halaman lebih sedikit

### 3. No Products Found
```
Tidak ada produk ditemukan
```
**Solusi**:
- Periksa selector CSS apakah masih valid
- Coba dengan kata kunci yang berbeda
- Periksa apakah Shopee memblokir IP

### 4. Cookie Login Failed
```
Gagal load cookies
```
**Solusi**:
- Periksa format file cookies.json
- Pastikan cookies masih valid (tidak expired)
- Coba scraping tanpa login

## 🔍 Tips Penggunaan

### 1. Optimasi Performa
- Gunakan mode headless untuk scraping cepat
- Batasi jumlah halaman untuk testing
- Gunakan delay yang cukup antara request

### 2. Data Quality
- Selalu validasi hasil scraping
- Periksa file log untuk error
- Backup data sebelum scraping skala besar

### 3. Anti-Ban Strategy
- Gunakan delay random antara request
- Rotasi User-Agent (jika diperlukan)
- Gunakan proxy rotation (untuk skala besar)

## 📈 Monitoring dan Logging

Scraper menghasilkan log detail di file `scraping.log`:

```
2024-01-15 10:30:15 - INFO - ✅ WebDriver berhasil diinisialisasi
2024-01-15 10:30:18 - INFO - ✅ Login otomatis via cookies berhasil!
2024-01-15 10:30:25 - INFO - 🔍 Mengakses: https://shopee.co.id/search?keyword=laptop&page=0
2024-01-15 10:30:35 - INFO - 📦 Ditemukan 50 produk di halaman 1
```

## ⚠️ Disclaimer

- Tool ini dibuat untuk tujuan edukasi dan penelitian
- Gunakan dengan bijak dan hormati Terms of Service Shopee
- Penulis tidak bertanggung jawab atas penyalahgunaan tool
- Pastikan compliance dengan regulasi data protection

## 🤝 Kontribusi

Untuk berkontribusi pada pengembangan tool ini:

1. Fork repository
2. Buat feature branch
3. Commit perubahan
4. Push ke branch
5. Buat Pull Request

## 📞 Support

Untuk pertanyaan dan support:
- Cek file `scraping.log` untuk error detail
- Periksa dokumentasi ini
- Buat issue di repository

---

**Dikembangkan dengan ❤️ oleh Dosen Data Mining dengan 30 tahun pengalaman profesional**