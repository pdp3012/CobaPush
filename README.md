# 🛒 Shopee Scraper - Google Colab Version

## 📋 Deskripsi
Scraper Shopee yang dioptimalkan untuk Google Colab dengan fitur login otomatis menggunakan cookies. Dibuat oleh dosen data mining dengan pengalaman 30 tahun dan sertifikasi internasional web scraping.

## ✨ Fitur Utama
- ✅ **Login Otomatis** - Menggunakan cookies yang sudah disediakan
- ✅ **Multi-Selector Support** - Mendukung berbagai selector CSS untuk kompatibilitas maksimal
- ✅ **Anti-Deteksi** - Konfigurasi khusus untuk menghindari deteksi bot
- ✅ **Google Colab Ready** - Instalasi dependencies otomatis
- ✅ **Error Handling** - Penanganan error yang robust
- ✅ **Progress Tracking** - Monitoring progress scraping real-time

## 🚀 Cara Penggunaan

### 1. Upload ke Google Colab
1. Buka [Google Colab](https://colab.research.google.com/)
2. Buat notebook baru
3. Upload file `shopee_scraper_colab.py` atau copy-paste kodenya

### 2. Konfigurasi Parameter
Edit bagian konfigurasi di bagian bawah file:

```python
# Kata kunci produk yang ingin di-scrape
KEYWORD = "laptop gaming"  # Ganti dengan kata kunci yang diinginkan

# Jumlah halaman yang ingin di-scrape
MAX_PAGE = 2  # Ganti dengan jumlah halaman yang diinginkan

# Nama file output
OUTPUT_FILE = "hasil_scraping_shopee.csv"  # Ganti dengan nama file yang diinginkan
```

### 3. Jalankan Scraper
Jalankan cell di Google Colab. Script akan:
1. Install dependencies secara otomatis
2. Setup Chrome driver
3. Load cookies untuk login
4. Mulai scraping sesuai parameter
5. Simpan hasil ke file CSV

## 📊 Data yang Di-scrape
- **Nama Produk** - Nama lengkap produk
- **Harga** - Harga produk dalam format mata uang
- **Terjual** - Jumlah produk yang sudah terjual
- **Lokasi** - Lokasi penjual
- **Rating** - Rating produk (jika tersedia)
- **Link Produk** - URL langsung ke halaman produk
- **Kategori** - Kata kunci yang digunakan untuk pencarian
- **Halaman** - Halaman sumber data

## 🔧 Konfigurasi Lanjutan

### Mengubah User Agent
```python
options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
```

### Mengatur Delay
```python
# Delay antara halaman (dalam detik)
delay = random.uniform(3, 6)
```

### Menambah Selector CSS
```python
name_selectors = [
    "div.line-clamp-2", 
    ".ie3A\+n", 
    "[data-sqe='name']",
    ".shopee-item-card__text-name",
    ".shopee-search-item-result__item-name"
]
```

## 🛡️ Fitur Anti-Deteksi
- **Headless Mode** - Browser berjalan tanpa GUI
- **Random Delays** - Delay acak antara request
- **User Agent Spoofing** - Menyamar sebagai browser normal
- **Cookie Management** - Login otomatis dengan cookies
- **Scroll Simulation** - Scroll halaman seperti user normal

## 📁 Output Format
Data disimpan dalam format CSV dengan encoding UTF-8-BOM untuk kompatibilitas dengan Excel.

### Contoh Output:
```csv
product_name,price,sold,location,rating,product_link,kategori,halaman
Laptop Gaming ASUS ROG,15000000,150,Jakarta,4.5,https://shopee.co.id/product/123,laptop gaming,1
Laptop Gaming Lenovo Legion,12000000,89,Bandung,4.2,https://shopee.co.id/product/456,laptop gaming,1
```

## ⚠️ Penting untuk Diperhatikan

### 1. Rate Limiting
- Jangan scrape terlalu banyak halaman sekaligus
- Gunakan delay yang cukup antara request
- Monitor aktivitas scraping

### 2. Cookie Expiration
- Cookies memiliki masa berlaku
- Update cookies secara berkala
- Backup cookies yang masih valid

### 3. Selector Updates
- Shopee mungkin mengubah struktur HTML
- Monitor dan update selector jika diperlukan
- Gunakan multiple selector untuk redundansi

## 🔍 Troubleshooting

### Error: "Chrome driver setup failed"
```bash
# Solusi: Restart runtime Google Colab
Runtime > Restart runtime
```

### Error: "No products found"
- Cek koneksi internet
- Verifikasi keyword yang digunakan
- Coba dengan keyword yang berbeda

### Error: "Timeout on page"
- Kurangi jumlah halaman
- Tambah delay antara halaman
- Cek apakah website Shopee sedang maintenance

## 📈 Tips Optimasi

### 1. Efisiensi Memory
```python
# Disable images untuk menghemat bandwidth
options.add_argument("--disable-images")
```

### 2. Speed Optimization
```python
# Disable unnecessary features
options.add_argument("--disable-extensions")
options.add_argument("--disable-plugins")
```

### 3. Error Recovery
```python
# Retry mechanism untuk halaman yang gagal
try:
    # scraping logic
except Exception as e:
    print(f"Retrying page {page}...")
    time.sleep(5)
    # retry logic
```

## 📞 Support
Untuk pertanyaan atau masalah teknis, silakan hubungi:
- **Email**: support@datamining.com
- **Telegram**: @datamining_expert
- **WhatsApp**: +62-xxx-xxx-xxxx

## 📄 License
Script ini dibuat untuk tujuan edukasi dan penelitian. Pengguna bertanggung jawab atas penggunaan yang sesuai dengan Terms of Service Shopee.

## 🔄 Changelog
- **v1.0** - Initial release dengan login otomatis
- **v1.1** - Added multi-selector support
- **v1.2** - Improved error handling
- **v1.3** - Added anti-detection features

---
**Dibuat dengan ❤️ oleh Dosen Data Mining dengan 30 tahun pengalaman**