# CNN Indonesia News Scraper

Scraper berita untuk CNN Indonesia yang dapat mengambil data judul, tanggal, link, dan konten detail artikel berdasarkan keyword pencarian.

## 📋 Fitur

- 🔍 Pencarian berita berdasarkan keyword
- 📰 Ekstraksi judul, tanggal, dan link berita
- 📝 Pengambilan konten detail artikel
- 📊 Export ke format CSV
- ⏱️ Rate limiting untuk menghindari blocking
- 🎯 Optimized untuk Google Colab

## 🚀 Cara Penggunaan di Google Colab

### 1. Install Dependencies
Jalankan cell pertama untuk menginstall library yang diperlukan:

```python
!pip install requests beautifulsoup4 pandas lxml
```

### 2. Copy-Paste Kode Scraper
Copy-paste seluruh kode dari file `cnn_scraper_colab_example.py` ke cell baru di Google Colab.

### 3. Ganti Keyword
Ubah variabel `keyword` sesuai kebutuhan:

```python
keyword = "cabai rawit"  # Ganti dengan keyword yang diinginkan
```

### 4. Jalankan Scraper
Jalankan cell untuk memulai scraping. Hasil akan otomatis tersimpan dalam format CSV dan siap didownload.

## 📁 File yang Tersedia

1. **`cnn_indonesia_scraper.py`** - Kode lengkap dengan fitur lengkap
2. **`cnn_scraper_colab_example.py`** - Versi sederhana untuk Google Colab
3. **`install_dependencies.py`** - Script instalasi dependencies
4. **`README.md`** - Panduan penggunaan

## 🎯 Contoh Penggunaan

### Pencarian Berita Sederhana
```python
scraper = CNNIndonesiaScraper()
keyword = "harga beras"
df = scraper.scrape_with_content(keyword, max_pages=2, get_content=False)
```

### Pencarian dengan Konten Detail
```python
scraper = CNNIndonesiaScraper()
keyword = "inflasi"
df = scraper.scrape_with_content(keyword, max_pages=3, get_content=True)
```

### Simpan ke CSV
```python
filename = scraper.save_to_csv(df)
from google.colab import files
files.download(filename)
```

## 📊 Data yang Diambil

Setiap berita akan berisi informasi berikut:

- **judul**: Judul artikel berita
- **tanggal**: Tanggal publikasi artikel
- **link**: URL lengkap artikel
- **konten**: Teks lengkap konten artikel (jika diminta)
- **thumbnail**: URL gambar thumbnail (jika tersedia)

## ⚙️ Parameter Konfigurasi

- `keyword`: Kata kunci pencarian
- `max_pages`: Jumlah halaman maksimal yang akan di-scrape (default: 3)
- `get_content`: Boolean untuk mengambil konten detail (default: True)

## 🔧 Troubleshooting

### Error "Connection timeout"
- Pastikan koneksi internet stabil
- Coba kurangi jumlah halaman (`max_pages`)

### Error "No articles found"
- Periksa keyword yang digunakan
- Coba keyword yang lebih umum

### Error "Rate limiting"
- Scraper sudah dilengkapi delay otomatis
- Jika masih error, tambahkan delay manual dengan `time.sleep(5)`

## 📝 Contoh Output

```
🚀 MEMULAI SCRAPING CNN INDONESIA
🔍 Keyword: 'cabai rawit'
📄 Max halaman: 2
📝 Ambil konten: Ya
============================================================
🔍 Mencari berita: 'cabai rawit'
📄 Halaman 1: https://www.cnnindonesia.com/search?query=cabai%20rawit
✅ 10 berita dari halaman 1
📄 Halaman 2: https://www.cnnindonesia.com/search?query=cabai%20rawit&page=2
✅ 8 berita dari halaman 2
📊 Total berita ditemukan: 18

📖 Mengambil konten detail artikel...
⏳ Progress: 1/18 - Harga Cabai Rawit Naik Lagi, Pedagang Keluhkan...
⏳ Progress: 2/18 - Pemerintah Siapkan Stok Cabai Rawit untuk...

============================================================
📊 HASIL SCRAPING
============================================================
📈 Total berita: 18
📋 Kolom: judul, tanggal, link, konten
```

## ⚠️ Disclaimer

- Scraper ini dibuat untuk tujuan edukasi dan penelitian
- Gunakan dengan bijak dan hormati Terms of Service website
- Jangan melakukan scraping berlebihan yang dapat membebani server
- Pastikan penggunaan sesuai dengan kebijakan website target

## 🤝 Kontribusi

Jika menemukan bug atau ingin menambahkan fitur, silakan buat issue atau pull request.

## 📞 Support

Untuk pertanyaan atau bantuan, silakan buat issue di repository ini.