# Blibli Scraper

Scraper untuk website Blibli yang dikembangkan berdasarkan referensi Tokopedia Scraper. Tool ini memungkinkan Anda untuk mengekstrak data produk dari hasil pencarian Blibli.

## 🚀 Fitur

- ✅ Scraping data produk dari hasil pencarian Blibli
- ✅ Ekstraksi data lengkap: nama produk, harga, rating, jumlah terjual, nama toko, dan link produk
- ✅ Support multiple halaman scraping
- ✅ Delay otomatis untuk menghindari deteksi bot
- ✅ Export data ke format CSV
- ✅ Error handling yang robust
- ✅ Validasi data kualitas
- ✅ Interface command line yang user-friendly

## 📋 Data yang Diekstrak

1. **Nama Produk** - Menggunakan CSS selector `els-product__title-wrapper`
2. **Harga** - Menggunakan CSS selector `els-product__fixed-price`
3. **Rating** - Menggunakan CSS selector `els-product__rating-wrapper`
4. **Jumlah Terjual** - Menggunakan CSS selector `els-product__sold`
5. **Nama Toko** - Menggunakan CSS selector `els-product__seller-name`
6. **Link Produk** - Link menuju halaman detail produk
7. **Timestamp** - Waktu scraping dilakukan

## 🛠️ Instalasi

1. Clone atau download repository ini
2. Install dependensi yang diperlukan:

```bash
pip install -r requirements.txt
```

## 📦 Dependensi

- `requests` - Untuk HTTP requests
- `beautifulsoup4` - Untuk parsing HTML
- `pandas` - Untuk manipulasi data dan export CSV
- `lxml` - Parser HTML yang lebih cepat

## 🚀 Cara Penggunaan

1. Jalankan script:

```bash
python blibli_scraper.py
```

2. Ikuti instruksi di terminal:
   - Masukkan keyword pencarian (minimal 2 karakter)
   - Tentukan jumlah halaman yang akan di-scrape (1-10)
   - Konfirmasi untuk memulai scraping

3. Tunggu proses scraping selesai

4. Pilih opsi untuk menyimpan data ke file CSV

## 📊 Output

Data akan disimpan dalam format CSV dengan kolom:
- `nama_produk`
- `harga`
- `rating`
- `jumlah_terjual`
- `nama_toko`
- `link_produk`
- `timestamp`

## ⚠️ Peringatan Penting

- **Gunakan dengan bijak**: Scraper ini hanya untuk tujuan edukasi dan penelitian
- **Patuhi ToS**: Pastikan Anda mematuhi Terms of Service Blibli
- **Rate Limiting**: Jangan melakukan scraping berlebihan untuk menghindari pemblokiran
- **Legal**: Pastikan penggunaan sesuai dengan hukum yang berlaku

## 🔧 Konfigurasi

### Cookies
Scraper menggunakan cookies yang telah dikonfigurasi untuk menghindari deteksi bot. Jika diperlukan, Anda dapat mengupdate cookies di method `__init__`:

```python
self.cookies = {
    'Blibli-Device-Id': 'your-device-id',
    'Blibli-Session-Id': 'your-session-id',
    'cf_clearance': 'your-cf-clearance',
    'forterToken': 'your-forter-token',
}
```

### Delay Settings
Anda dapat mengatur delay antar request di method `scrape_products`:

```python
products = scraper.scrape_products(keyword, max_pages=3, delay_range=(3, 7))
```

## 🐛 Troubleshooting

### Masalah Umum

1. **"Tidak ditemukan container produk"**
   - Struktur HTML Blibli mungkin berubah
   - Coba update CSS selectors

2. **"Gagal mengakses halaman"**
   - Periksa koneksi internet
   - Coba update cookies
   - Tunggu beberapa saat sebelum mencoba lagi

3. **"Anti-bot detection aktif"**
   - Kurangi jumlah halaman yang di-scrape
   - Tingkatkan delay antar request
   - Update User-Agent dan cookies

### Debug Mode

Untuk debugging, Anda dapat menambahkan print statements di method `extract_product_data`:

```python
# Debug: Simpan HTML untuk analisis
with open(f'debug_page_{page}.html', 'w', encoding='utf-8') as f:
    f.write(str(soup))
```

## 📝 Contoh Penggunaan

```python
from blibli_scraper import BlibliScraper

# Inisialisasi scraper
scraper = BlibliScraper()

# Scrape produk
products = scraper.scrape_products("laptop", max_pages=2)

# Simpan ke CSV
scraper.save_to_csv(products, "laptop_products.csv")

# Tampilkan ringkasan
scraper.display_summary(products)
```

## 🤝 Kontribusi

Kontribusi sangat diterima! Silakan buat pull request atau report issues jika menemukan bug atau ingin menambahkan fitur baru.

## 📄 Lisensi

Project ini dibuat untuk tujuan edukasi. Gunakan dengan bertanggung jawab.

## 👨‍💻 Developer

Dikembangkan berdasarkan referensi Tokopedia Scraper dan diadaptasi untuk website Blibli.

---

**Disclaimer**: Tool ini dibuat untuk tujuan edukasi. Pengguna bertanggung jawab penuh atas penggunaan tool ini sesuai dengan hukum yang berlaku dan Terms of Service website yang di-scrape.