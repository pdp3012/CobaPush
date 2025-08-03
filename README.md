# Bukalapak Scraper - Advanced Data Mining Tool

## 🎓 Dibuat oleh: Dosen Data Mining dengan 30 tahun pengalaman
## 🌟 Sertifikasi: International Data Mining Certification

### 📋 Deskripsi
Advanced web scraping tool untuk website Bukalapak dengan dua pendekatan utama:
1. **API Scraping** - Menggunakan Bukalapak API endpoints
2. **CSS Selector Scraping** - Menggunakan Selenium dengan multiple fallback strategies

### 🎯 Data yang Di-Ekstrak
- ✅ Nama Produk
- ✅ Harga (termasuk diskon)
- ✅ Jumlah Terjual
- ✅ Nama Toko
- ✅ Lokasi Toko
- ✅ Rating Produk
- ✅ URL Produk
- ✅ Gambar Produk
- ✅ Kategori
- ✅ Informasi Toko (rating, verifikasi, dll)
- ✅ Spesifikasi Produk
- ✅ Metode Pengiriman
- ✅ Dan banyak lagi...

### 🚀 Fitur Utama

#### Anti-Deteksi
- Rotating User Agents
- Random delays
- Stealth browser settings
- Multiple fallback strategies

#### Robust Error Handling
- Retry mechanisms
- Multiple selector strategies
- Graceful error recovery
- Comprehensive logging

#### Data Quality
- Data validation
- Cleaning and normalization
- Statistics generation
- Multiple export formats

### 📁 Struktur Proyek
```
bukalapak-scraper/
├── bukalapak_scraper.py          # Main scraper (combined approach)
├── bukalapak_api_scraper.py      # API-only scraper
├── bukalapak_css_scraper.py      # CSS Selector-only scraper
├── requirements.txt              # Dependencies
├── README.md                     # Documentation
├── example_usage.py              # Contoh penggunaan
└── data/                         # Output directory
    ├── csv/
    ├── json/
    └── logs/
```

### 🛠️ Instalasi

1. **Clone repository**
```bash
git clone <repository-url>
cd bukalapak-scraper
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Install Chrome/Chromium** (untuk Selenium)
```bash
# Ubuntu/Debian
sudo apt-get install chromium-browser

# CentOS/RHEL
sudo yum install chromium

# macOS
brew install chromium
```

### 📖 Penggunaan

#### 1. Main Scraper (Kombinasi API + CSS)
```python
from bukalapak_scraper import BukalapakScraper

# Inisialisasi scraper
scraper = BukalapakScraper(headless=True, delay_range=(2, 5))

# Scraping via API
scraper.scrape_via_api(search_query="laptop", max_pages=3)

# Scraping via CSS Selector
scraper.scrape_via_css_selector(search_query="laptop", max_pages=3)

# Simpan data
scraper.save_to_csv("bukalapak_products.csv")
scraper.save_to_json("bukalapak_products.json")

# Tampilkan statistik
stats = scraper.get_statistics()
print(stats)
```

#### 2. API Scraper (Hanya API)
```python
from bukalapak_api_scraper import BukalapakAPIScraper

# Inisialisasi API scraper
api_scraper = BukalapakAPIScraper(delay_range=(2, 4))

# Search products
api_scraper.search_products(query="smartphone", max_pages=5)

# Get trending products
api_scraper.get_trending_products(max_pages=2)

# Get recommendations
api_scraper.get_recommendations(max_pages=2)

# Save data
api_scraper.save_to_csv("api_products.csv")
```

#### 3. CSS Selector Scraper (Hanya CSS)
```python
from bukalapak_css_scraper import BukalapakCSSScraper

# Inisialisasi CSS scraper
css_scraper = BukalapakCSSScraper(headless=True)

# Scrape products
css_scraper.scrape_products(search_query="headphone", max_pages=3)

# Save data
css_scraper.save_to_csv("css_products.csv")
```

### 🔧 Konfigurasi

#### Delay Settings
```python
# Slow scraping (lebih aman)
scraper = BukalapakScraper(delay_range=(3, 7))

# Fast scraping (risiko deteksi)
scraper = BukalapakScraper(delay_range=(1, 2))
```

#### Browser Settings
```python
# Headless mode (recommended)
scraper = BukalapakCSSScraper(headless=True)

# Visible browser (untuk debugging)
scraper = BukalapakCSSScraper(headless=False)
```

### 📊 Output Format

#### CSV Output
```csv
nama_produk,harga,jumlah_terjual,nama_toko,lokasi_toko,rating_produk,url_produk,metode_scraping,timestamp_scraping
Laptop Gaming Asus ROG,15000000,45,Toko Elektronik,Jakarta,4.5,https://...,API,2024-01-15T10:30:00
```

#### JSON Output
```json
{
  "nama_produk": "Laptop Gaming Asus ROG",
  "harga": 15000000,
  "jumlah_terjual": 45,
  "nama_toko": "Toko Elektronik",
  "lokasi_toko": "Jakarta",
  "rating_produk": 4.5,
  "url_produk": "https://...",
  "metode_scraping": "API",
  "timestamp_scraping": "2024-01-15T10:30:00"
}
```

### 📈 Statistik yang Tersedia
- Total produk
- Rata-rata harga
- Harga tertinggi/terendah
- Rata-rata rating
- Total terjual
- Jumlah toko unik
- Jumlah kategori unik
- Produk dengan diskon
- Toko terverifikasi
- Toko resmi

### 🛡️ Anti-Deteksi Features

#### User Agent Rotation
```python
# Automatic rotation setiap request
self.session.headers['User-Agent'] = self.ua.random
```

#### Stealth Browser
```python
# Anti-deteksi settings
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
```

#### Multiple Selector Strategies
```python
# Primary selectors
'product_card': '[data-testid="product-card"], .product-card, .bl-product-card'

# Fallback selectors
'product_card': '.product, .item, .card, [class*="product"]'
```

### ⚠️ Penting untuk Diperhatikan

#### Rate Limiting
- Gunakan delay yang cukup (2-5 detik)
- Monitor response status codes
- Implement retry mechanism

#### Legal Considerations
- Respect robots.txt
- Don't overload servers
- Use for educational/research purposes only
- Comply with website terms of service

#### Error Handling
- Network timeouts
- Element not found
- Page load failures
- API rate limiting

### 🔍 Troubleshooting

#### Common Issues

1. **ChromeDriver not found**
```bash
# Install webdriver-manager
pip install webdriver-manager
```

2. **Rate limiting**
```python
# Increase delay
scraper = BukalapakScraper(delay_range=(5, 10))
```

3. **Element not found**
```python
# Use alternative selectors
# Check if website structure changed
```

4. **API errors**
```python
# Check API endpoints
# Verify request headers
# Monitor rate limits
```

### 📝 Logging

Logs disimpan di `bukalapak_scraper.log` dengan format:
```
2024-01-15 10:30:00 - INFO - Scraping halaman 1
2024-01-15 10:30:05 - INFO - Found 50 products
2024-01-15 10:30:10 - ERROR - Rate limited, waiting 10 seconds
```

### 🎯 Best Practices

1. **Start Small**: Mulai dengan 1-2 halaman
2. **Monitor Logs**: Perhatikan error messages
3. **Respect Limits**: Jangan scrape terlalu agresif
4. **Data Validation**: Selalu validasi data yang di-scrape
5. **Backup Data**: Simpan data secara berkala

### 📞 Support

Untuk pertanyaan atau masalah:
- Check logs untuk error details
- Verify dependencies installation
- Test dengan query sederhana terlebih dahulu
- Monitor website changes

### 📄 License

Proyek ini dibuat untuk tujuan edukasi dan penelitian. Pastikan untuk mematuhi Terms of Service website yang di-scrape.

---

**Dibuat dengan ❤️ oleh Dosen Data Mining dengan 30 tahun pengalaman**