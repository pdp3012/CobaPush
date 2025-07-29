# 📋 INSTRUKSI PENGGUNAAN SHOPEE SCRAPER

## 🎯 Ringkasan
Scraper ini dapat mengambil data produk dari Shopee secara otomatis berdasarkan keyword yang dimasukkan user. Data yang di-scrape meliputi:
- Nama produk
- Harga
- Rating
- Jumlah terjual
- Nama toko
- Lokasi toko

## 🚀 Cara Penggunaan di Google Colab

### Langkah 1: Buka Google Colab
1. Kunjungi [colab.research.google.com](https://colab.research.google.com)
2. Klik "New Notebook" untuk membuat notebook baru

### Langkah 2: Setup Environment (Cell 1)
Copy-paste kode berikut ke cell pertama:

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

print("✅ Setup selesai! Semua dependencies terinstall.")
```

**Jalankan cell ini dan tunggu sampai selesai.**

### Langkah 3: Import Libraries dan Scraper Class (Cell 2)
Copy-paste kode dari file `shopee_colab_scraper.py` atau gunakan kode yang ada di file `colab_notebook.py` bagian CELL 2.

**Jalankan cell ini.**

### Langkah 4: Jalankan Scraper (Cell 3)
Copy-paste kode dari file `colab_notebook.py` bagian CELL 3.

**Jalankan cell ini dan ikuti instruksi yang muncul:**
- Masukkan keyword produk (contoh: "cabai rawit")
- Masukkan jumlah maksimal produk (1-100)

### Langkah 5: Lihat Hasil (Cell 4) - Opsional
Copy-paste kode dari file `colab_notebook.py` bagian CELL 4 untuk melihat hasil dalam format tabel.

### Langkah 6: Download File CSV (Cell 5) - Opsional
Copy-paste kode dari file `colab_notebook.py` bagian CELL 5 untuk mendownload file CSV.

## 📊 Contoh Output

```
============================================================
SHOPEE SCRAPER UNTUK GOOGLE COLAB
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
✓ Produk 1: Cabai Rawit Merah Segar 1kg - Fresh dari Kebun...
✓ Produk 2: Cabai Rawit Hijau Fresh 500gr - Premium Quality...
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
   Harga: Rp 25000 | Rating: 4.8 | Terjual: 1500
   Toko: Toko Sayur Segar | Lokasi: Jakarta Selatan

2. Cabai Rawit Hijau Fresh 500gr - Premium Quality...
   Harga: Rp 15000 | Rating: 4.5 | Terjual: 800
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

## 📁 File Output

Data akan tersimpan dalam file CSV dengan format:
```
shopee_[keyword]_[timestamp].csv
```

Contoh: `shopee_cabai_rawit_20231201_143022.csv`

## 💡 Tips Penggunaan

### Keyword yang Efektif:
- ✅ **Spesifik**: "cabai rawit merah" (lebih baik dari "cabai")
- ✅ **Bahasa Indonesia**: Gunakan bahasa Indonesia untuk hasil lebih baik
- ❌ **Terlalu Umum**: Hindari keyword seperti "makanan", "elektronik"

### Jumlah Produk:
- ✅ **Testing**: Mulai dengan 10-20 produk
- ✅ **Optimal**: 50-100 produk untuk data lengkap
- ⚠️ **Waktu**: Semakin banyak produk, semakin lama waktu eksekusi

### Troubleshooting:

#### Error: Chrome driver tidak ditemukan
```python
# Pastikan Chrome dan ChromeDriver sudah terinstall
!which google-chrome
!which chromedriver
```

#### Error: Tidak ada produk yang ditemukan
- Coba keyword yang berbeda
- Pastikan koneksi internet stabil
- Tunggu beberapa saat dan coba lagi

#### Error: Timeout
- Scraper akan otomatis mencoba selector alternatif
- Jika masih gagal, coba kurangi jumlah produk

#### Error: Memory/Runtime
- Restart runtime Colab
- Jalankan ulang dari awal

## 🔧 Fitur Anti-Bot

Scraper ini dilengkapi dengan fitur anti-bot detection:

1. **Random Delays**: Delay acak antara request
2. **User-Agent Rotation**: Menggunakan user-agent yang berbeda-beda
3. **Stealth Mode**: Chrome options untuk menghindari deteksi
4. **Natural Scrolling**: Scroll halaman secara natural
5. **Multiple Selectors**: Fallback selectors jika satu gagal

## 📈 Data yang Di-scrape

| Kolom | Deskripsi | Format |
|-------|-----------|--------|
| nama_produk | Nama lengkap produk | Text |
| harga | Harga dalam Rupiah | Number (tanpa format) |
| rating | Rating 1-5 bintang | Number (1.0-5.0) |
| jumlah_terjual | Jumlah unit terjual | Number |
| nama_toko | Nama seller/toko | Text |
| lokasi_toko | Lokasi seller/toko | Text |

## 🛡️ Keamanan dan Etika

- ✅ Menggunakan teknik yang menghormati rate limiting
- ✅ Tidak melakukan scraping berlebihan
- ✅ Data hanya untuk tujuan analisis dan penelitian
- ✅ Patuhi Terms of Service Shopee

## 📞 Support

Jika mengalami masalah:

1. **Pastikan semua dependencies terinstall**
2. **Chrome dan ChromeDriver terinstall dengan benar**
3. **Koneksi internet stabil**
4. **Google Drive ter-mount (untuk penyimpanan)**

## ⚠️ Disclaimer

Scraper ini dibuat untuk tujuan edukasi dan penelitian. Pengguna bertanggung jawab atas penggunaan yang sesuai dengan Terms of Service Shopee dan peraturan yang berlaku.

---

**🎉 Selamat menggunakan Shopee Scraper!**