# 🛍️ Advanced Shopee Product Scraper

**Dibuat oleh: Dosen Data Mining dengan 30 tahun pengalaman dalam web scraping**

## 📋 Deskripsi

Advanced Shopee Product Scraper adalah tool scraping yang powerful dan sophisticated untuk mengumpulkan data produk dari Shopee Indonesia. Tool ini dilengkapi dengan berbagai teknik anti-bot protection yang advanced untuk memastikan scraping berjalan lancar tanpa terdeteksi sebagai bot.

## ✨ Fitur Utama

- 🔍 **Keyword-based Search**: Cari produk berdasarkan keyword (contoh: "cabai rawit")
- 🛡️ **Advanced Anti-Bot Protection**: Multiple teknik untuk bypass anti-bot detection
- 📊 **Comprehensive Data Extraction**: 
  - Nama produk
  - Harga produk
  - Rating produk
  - Jumlah terjual
  - Nama toko
  - Lokasi toko
  - Timestamp scraping
- 💾 **Multiple Output Formats**: CSV dan Excel dengan formatting yang baik
- 🚀 **High Performance**: Optimized untuk Google Colab
- 🔄 **Automatic Pagination**: Otomatis scrape multiple halaman
- 🎯 **Duplicate Prevention**: Mencegah data duplikat
- 📈 **Real-time Statistics**: Monitoring progress dan performance

## 🛠️ Installation

### Untuk Google Colab

1. **Upload semua file ke Google Colab**
2. **Install dependencies**:
```python
# Jalankan cell ini terlebih dahulu
!pip install requests beautifulsoup4 selenium pandas openpyxl lxml urllib3
```

3. **Install Chrome dan ChromeDriver**:
```python
# Setup Chrome dan ChromeDriver
!apt-get update
!apt-get install -y wget unzip
!wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add -
!echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list
!apt-get update
!apt-get install -y google-chrome-stable
!wget -O /tmp/chromedriver.zip https://chromedriver.storage.googleapis.com/120.0.6099.109/chromedriver_linux64.zip
!unzip /tmp/chromedriver.zip -d /usr/local/bin/
!chmod +x /usr/local/bin/chromedriver
```

### Untuk Local Environment

1. **Clone repository**:
```bash
git clone <repository-url>
cd shopee-scraper
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Install Chrome dan ChromeDriver** (sesuaikan dengan OS Anda)

## 🚀 Cara Penggunaan

### 1. Basic Usage

```python
# Import scraper
from advanced_shopee_scraper import AdvancedShopeeScraper

# Inisialisasi scraper
scraper = AdvancedShopeeScraper()

# Mulai scraping
keyword = "cabai rawit"
max_products = 50
products_data = scraper.scrape_shopee(keyword, max_products)

# Save data
scraper.save_to_csv(products_data, "shopee_data.csv")
scraper.save_to_excel(products_data, "shopee_data.xlsx")
```

### 2. Interactive Mode

```python
# Jalankan file utama
python advanced_shopee_scraper.py
```

Kemudian ikuti instruksi yang muncul:
1. Masukkan keyword produk (contoh: "cabai rawit")
2. Masukkan jumlah data yang diinginkan
3. Tunggu proses scraping selesai

## 📊 Output Format

Data akan disimpan dalam format berikut:

| Kolom | Deskripsi |
|-------|-----------|
| Nama Produk | Nama lengkap produk |
| Harga | Harga produk (dalam angka) |
| Rating | Rating produk |
| Jumlah Terjual | Jumlah unit yang terjual |
| Nama Toko | Nama toko/seller |
| Lokasi Toko | Lokasi toko |
| Timestamp | Waktu scraping |

## 🔧 Advanced Anti-Bot Techniques

Tool ini menggunakan berbagai teknik anti-bot yang sophisticated:

1. **Rotating User Agents**: Menggunakan multiple user agents secara random
2. **Stealth JavaScript**: Menyembunyikan tanda-tanda automation
3. **Human-like Behavior**: 
   - Random delays
   - Human-like scrolling
   - Natural mouse movements
4. **Advanced Headers**: Headers yang realistic dan complete
5. **Multiple Selectors**: Fallback selectors untuk berbagai struktur HTML
6. **Session Management**: Proper session handling
7. **Error Recovery**: Automatic retry mechanism

## ⚠️ Troubleshooting

### Error: "Chrome driver not found"
```python
# Pastikan ChromeDriver sudah terinstall dengan benar
!which chromedriver
```

### Error: "No products found"
- Coba keyword yang berbeda
- Pastikan koneksi internet stabil
- Tunggu beberapa menit sebelum mencoba lagi

### Error: "Page not loading"
- Coba refresh halaman
- Periksa apakah Shopee sedang maintenance
- Gunakan VPN jika diperlukan

### Performance Issues
- Kurangi jumlah produk yang di-scrape
- Pastikan tidak ada aplikasi lain yang menggunakan banyak resources
- Gunakan headless mode (sudah default)

## 📈 Performance Tips

1. **Optimal Jumlah Produk**: 50-100 produk per session
2. **Interval Scraping**: Tunggu minimal 5 menit antara scraping sessions
3. **Keyword Specific**: Gunakan keyword yang spesifik untuk hasil yang lebih baik
4. **Network Stability**: Pastikan koneksi internet stabil

## 🔒 Legal Disclaimer

- Tool ini dibuat untuk tujuan edukasi dan research
- Pastikan compliance dengan Terms of Service Shopee
- Gunakan dengan bijak dan bertanggung jawab
- Penulis tidak bertanggung jawab atas penyalahgunaan tool

## 📞 Support

Jika mengalami masalah atau membutuhkan bantuan:

1. Periksa troubleshooting section
2. Pastikan semua dependencies terinstall dengan benar
3. Coba dengan keyword yang berbeda
4. Periksa log error untuk informasi detail

## 🎯 Contoh Penggunaan

```python
# Contoh scraping untuk berbagai produk
keywords = ["laptop gaming", "smartphone", "baju muslim", "sepatu nike"]
max_products = 30

for keyword in keywords:
    print(f"Scraping {keyword}...")
    scraper = AdvancedShopeeScraper()
    data = scraper.scrape_shopee(keyword, max_products)
    
    if data:
        filename = f"shopee_{keyword.replace(' ', '_')}.csv"
        scraper.save_to_csv(data, filename)
        print(f"✅ Berhasil scrape {len(data)} produk untuk {keyword}")
    else:
        print(f"❌ Gagal scrape {keyword}")
```

## 📝 Changelog

### Version 2.0 (Advanced)
- ✅ Advanced anti-bot protection
- ✅ Multiple selector fallbacks
- ✅ Human-like behavior simulation
- ✅ Better error handling
- ✅ Performance optimizations
- ✅ Enhanced data extraction

### Version 1.0 (Basic)
- ✅ Basic scraping functionality
- ✅ CSV/Excel export
- ✅ Simple anti-bot measures

---

**Dibuat dengan ❤️ oleh Dosen Data Mining dengan 30 tahun pengalaman**