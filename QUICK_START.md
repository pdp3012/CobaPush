# 🚀 Quick Start Guide - Enhanced Shopee Scraper

## 📋 Langkah Cepat untuk Memulai

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Setup Cookies (Opsional)
```bash
python extract_cookies.py
```
Atau buat manual file `cookies.json` dengan cookies Shopee Anda.

### 3. Test Scraper
```bash
python test_scraper.py
```

### 4. Jalankan Scraper

#### Single Keyword:
```bash
python enhanced_shopee_scraper.py
```

#### Multiple Keywords (Batch):
```bash
python batch_scraper.py
```

## 🎯 Contoh Penggunaan

### Basic Scraping
```python
from enhanced_shopee_scraper import ShopeeScraper

scraper = ShopeeScraper(headless=True)
scraper.scrape_shopee("laptop", 3, "hasil.csv")
```

### Batch Scraping
Edit `config.json`:
```json
{
  "keywords": ["laptop", "smartphone", "headphone"],
  "max_pages_per_keyword": 2,
  "delay_between_keywords": 10
}
```

Lalu jalankan:
```bash
python batch_scraper.py
```

## 📊 Output Format

Data akan disimpan dalam format CSV dengan kolom:
- `product_name`: Nama produk
- `price`: Harga
- `sold`: Jumlah terjual
- `location`: Lokasi penjual
- `rating`: Rating produk
- `product_link`: Link produk
- `kategori`: Kata kunci pencarian
- `halaman`: Halaman sumber
- `scraped_at`: Timestamp

## ⚠️ Troubleshooting

### ChromeDriver Error
```bash
# Install Chrome browser
# Pastikan webdriver-manager terinstall
pip install webdriver-manager
```

### Cookies Error
```bash
# Extract cookies dari Chrome
python extract_cookies.py
```

### Timeout Error
- Periksa koneksi internet
- Kurangi jumlah halaman
- Tingkatkan delay

## 📁 File Penting

- `enhanced_shopee_scraper.py` - Main scraper
- `batch_scraper.py` - Batch scraping
- `extract_cookies.py` - Cookie extractor
- `test_scraper.py` - Testing script
- `config.json` - Konfigurasi batch
- `cookies.json` - Login cookies
- `requirements.txt` - Dependencies

## 🎉 Selamat Mencoba!

Untuk informasi lengkap, baca `README.md`