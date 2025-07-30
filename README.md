# 🛍️ Advanced Shopee Product Scraper

Scraper canggih untuk mengambil data produk dari Shopee dengan kemampuan anti-bot detection dan parsing data yang lengkap.

## ✨ Fitur Utama

- ✅ **Anti-Bot Detection**: Menggunakan teknik advanced untuk menghindari deteksi bot
- ✅ **Dual Method**: API + Selenium fallback untuk hasil maksimal
- ✅ **Data Lengkap**: Nama produk, harga, rating, terjual, toko, lokasi
- ✅ **Export Options**: CSV dan Excel format
- ✅ **User-Friendly**: Interface yang mudah digunakan
- ✅ **Google Colab Ready**: Siap digunakan di Google Colab

## 📊 Data yang Di-scrape

- 📦 **Nama Produk**: Nama lengkap produk
- 💰 **Harga**: Harga dalam format Rupiah
- ⭐ **Rating**: Rating produk dan jumlah ulasan
- 📊 **Jumlah Terjual**: Total penjualan produk
- 🏪 **Nama Toko**: Nama seller/toko
- 📍 **Lokasi Toko**: Lokasi seller
- 🎯 **Diskon**: Persentase diskon (jika ada)
- 🖼️ **Gambar**: URL gambar produk (jika ada)

## 🚀 Cara Penggunaan

### 1. Google Colab (Recommended)

1. Buka [Google Colab](https://colab.research.google.com/)
2. Upload file `shopee_scraper_colab.ipynb`
3. Jalankan semua cell secara berurutan
4. Masukkan keyword dan jumlah data yang diinginkan
5. Download hasil scraping

### 2. Local Environment

#### Install Dependencies

```bash
pip install -r requirements.txt
```

#### Run Scraper

```bash
python shopee_scraper_advanced.py
```

#### Atau gunakan versi basic:

```bash
python shopee_scraper.py
```

## 📝 Contoh Penggunaan

### Input User
```
🔍 Masukkan keyword produk yang ingin di-scrape: cabai rawit
📊 Masukkan jumlah data yang ingin didapatkan (max 100): 20
```

### Output
```
🚀 Memulai scraping untuk keyword: 'cabai rawit'
⏳ Mohon tunggu...

Starting to scrape products for keyword: 'cabai rawit'
Target: 20 products
Successfully scraped 20 products

====================================================================================================
SCRAPING RESULTS - 20 PRODUCTS
====================================================================================================

1. Cabai Rawit Merah Segar 1kg
   💰 Harga: Rp 25,000
   ⭐ Rating: 4.8 (156 ulasan)
   📦 Terjual: 1,234
   🏪 Toko: Toko Sayur Segar
   📍 Lokasi: Jakarta Selatan
   🎯 Diskon: 10%
   --------------------------------------------------------------------------------

2. Cabai Rawit Hijau Fresh 500gr
   💰 Harga: Rp 15,000
   ⭐ Rating: 4.6 (89 ulasan)
   📦 Terjual: 567
   🏪 Toko: Fresh Market
   📍 Lokasi: Bandung
   --------------------------------------------------------------------------------
```

## 🔧 Teknik Anti-Bot

### 1. API Method
- Menggunakan Shopee API v4
- Headers yang menyerupai browser asli
- Random delays dan user agents
- Session management

### 2. Selenium Fallback
- Undetected ChromeDriver
- Advanced Chrome options
- JavaScript injection untuk hide automation
- Multiple selectors untuk robustness

### 3. Anti-Detection Features
- Random user agents
- Realistic browser headers
- Session cookies management
- Rate limiting dengan delays
- Popup handling

## 📁 File Structure

```
shopee-scraper/
├── shopee_scraper.py              # Basic version
├── shopee_scraper_advanced.py     # Advanced version
├── shopee_scraper_colab.ipynb     # Google Colab notebook
├── requirements.txt               # Dependencies
└── README.md                     # Documentation
```

## 🛠️ Dependencies

- `requests`: HTTP requests
- `pandas`: Data manipulation
- `selenium`: Web automation
- `undetected-chromedriver`: Anti-detection Chrome
- `fake-useragent`: Random user agents
- `beautifulsoup4`: HTML parsing
- `openpyxl`: Excel export

## ⚠️ Disclaimer

**PENTING**: Scraper ini dibuat untuk tujuan edukasi dan penelitian. Pengguna bertanggung jawab untuk:

- Mematuhi Terms of Service Shopee
- Tidak melakukan scraping berlebihan
- Menggunakan data dengan bijak
- Menghormati privasi dan hak cipta
- Tidak menggunakan untuk tujuan komersial tanpa izin

## 🆘 Troubleshooting

### Common Issues

1. **Chrome Driver Error**
   ```bash
   # Install Chrome
   sudo apt-get install chromium-chromedriver
   ```

2. **API Rate Limited**
   - Kurangi jumlah data yang di-scrape
   - Tambah delay antara requests
   - Gunakan proxy (jika diperlukan)

3. **No Data Found**
   - Coba keyword yang berbeda
   - Periksa koneksi internet
   - Restart runtime (Google Colab)

4. **Permission Error**
   ```bash
   # Fix permissions
   chmod +x shopee_scraper.py
   ```

### Performance Tips

1. **Google Colab**: Gunakan GPU runtime untuk performa lebih baik
2. **Local**: Pastikan Chrome terinstall dan up-to-date
3. **Network**: Gunakan koneksi internet yang stabil
4. **Memory**: Tutup aplikasi lain jika menggunakan local environment

## 📈 Advanced Features

### Custom Headers
```python
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'id-ID,id;q=0.9,en;q=0.8',
    'X-Shopee-Language': 'id'
}
```

### Custom Selectors
```python
selectors = [
    '[data-sqe="item"]',
    '.col-xs-2-4',
    '[data-testid="product-card"]',
    '.shopee-search-item-result__item'
]
```

### Export Options
```python
# CSV Export
scraper.save_to_csv(products, 'my_products.csv')

# Excel Export
scraper.save_to_excel(products, 'my_products.xlsx')
```

## 🤝 Contributing

Kontribusi sangat diterima! Silakan:

1. Fork repository
2. Buat feature branch
3. Commit changes
4. Push ke branch
5. Buat Pull Request

## 📄 License

Project ini dilisensikan di bawah MIT License - lihat file [LICENSE](LICENSE) untuk detail.

## 📞 Support

Jika ada pertanyaan atau masalah:

1. Buka issue di GitHub
2. Cek troubleshooting section
3. Pastikan menggunakan versi terbaru
4. Berikan detail error yang lengkap

---

**Happy Scraping! 🚀**