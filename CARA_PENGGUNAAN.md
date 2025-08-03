# 📖 Cara Penggunaan Shopee Scraper

**Dibuat oleh: Dosen Data Mining dengan 30 tahun pengalaman scraping**

## 🚀 Cara Cepat Mulai

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Jalankan dengan GUI (Paling Mudah)
```bash
python gui_scraper.py
```

### 3. Jalankan dengan Command Line
```bash
python run_scraper.py "laptop gaming" -n 20
```

### 4. Jalankan Script Utama
```bash
python shopee_scraper.py
```

## 📋 Detail Penggunaan

### 🖥️ GUI Application (gui_scraper.py)

**Fitur:**
- Interface grafis yang user-friendly
- Real-time log output
- Progress bar
- Auto/manual login options
- One-click file opening

**Cara Pakai:**
1. Jalankan: `python gui_scraper.py`
2. Masukkan keyword produk
3. Set jumlah maksimal produk
4. Pilih metode login (otomatis/manual)
5. Klik "🚀 Mulai Scraping"
6. Tunggu proses selesai
7. Klik file output untuk membuka folder

### 💻 Command Line (run_scraper.py)

**Syntax:**
```bash
python run_scraper.py [keyword] [options]
```

**Options:**
- `-n, --num_products`: Jumlah maksimal produk (default: 50)
- `--no-login`: Skip login otomatis, langsung manual

**Contoh:**
```bash
# Scrape 20 produk laptop
python run_scraper.py "laptop" -n 20

# Scrape 100 produk smartphone dengan login manual
python run_scraper.py "smartphone" -n 100 --no-login

# Scrape produk gaming
python run_scraper.py "gaming"
```

### 🔧 Script Utama (shopee_scraper.py)

**Fitur:**
- Interactive input dengan GUI dialog
- Full control atas semua parameter
- Detailed output dan analisis

**Cara Pakai:**
1. Jalankan: `python shopee_scraper.py`
2. Masukkan keyword saat diminta
3. Set jumlah produk maksimal
4. Ikuti instruksi login
5. Tunggu proses selesai

### 🧪 Testing (test_scraper.py)

**Fitur:**
- Test semua komponen scraper
- Validasi CSS selector
- Test export data
- Performance testing

**Cara Pakai:**
```bash
python test_scraper.py
```

### 📚 Contoh Penggunaan (example_usage.py)

**Fitur:**
- 5 contoh penggunaan berbeda
- Batch processing
- Data analysis
- Custom extraction

**Cara Pakai:**
```bash
python example_usage.py
```

## 🔐 Proses Login

### Login Otomatis (Default)
- Script akan mencoba login dengan kredensial yang sudah diset
- Nomor: `081316084860`
- Password: `Pradipta301203`

### Login Manual (Jika otomatis gagal)
1. Browser akan terbuka ke halaman login Shopee
2. Login manual dengan akun Anda
3. Klik OK jika sudah selesai
4. Jika ada CAPTCHA, selesaikan dan klik OK

## 📊 Data yang Diekstrak

Setiap produk akan memiliki data berikut:

| Field | Deskripsi | Contoh |
|-------|-----------|---------|
| `nama_produk` | Nama lengkap produk | "Laptop Gaming Asus ROG Strix G15" |
| `harga` | Harga dalam format mata uang | "Rp 15.000.000" |
| `jumlah_terjual` | Statistik penjualan | "Terjual 1rb+" |
| `nama_toko` | Nama seller/toko | "TechStore Official" |
| `lokasi_toko` | Lokasi geografis | "Jakarta" |
| `rating_produk` | Rating dan ulasan | "4.8 (2.5rb ulasan)" |

## 📁 Output Files

### Format CSV
```csv
nama_produk,harga,jumlah_terjual,nama_toko,lokasi_toko,rating_produk
"Laptop Gaming Asus ROG","Rp 15.000.000","Terjual 1rb+","TechStore","Jakarta","4.8 (2.5rb ulasan)"
```

### Format JSON
```json
[
  {
    "nama_produk": "Laptop Gaming Asus ROG",
    "harga": "Rp 15.000.000",
    "jumlah_terjual": "Terjual 1rb+",
    "nama_toko": "TechStore",
    "lokasi_toko": "Jakarta",
    "rating_produk": "4.8 (2.5rb ulasan)"
  }
]
```

## ⚙️ Konfigurasi Lanjutan

### Mengubah Kredensial
Edit file `config.py`:
```python
LOGIN_CONFIG = {
    'phone': '081316084860',  # Ganti dengan nomor Anda
    'password': 'Pradipta301203',  # Ganti dengan password Anda
    'login_url': 'https://shopee.co.id/buyer/login'
}
```

### Mengubah CSS Selector
Edit file `config.py` bagian `CSS_SELECTORS`:
```python
CSS_SELECTORS = {
    'product_name': 'div.line-clamp-2',
    'product_price': 'span.font-medium.text-base\\/5.truncate',
    # ... lainnya
}
```

### Mengubah Delay dan Timeout
Edit file `config.py`:
```python
SCRAPING_CONFIG = {
    'default_max_products': 50,
    'scroll_count': 5,
    'scroll_delay': 2,  # Delay scroll dalam detik
    'page_load_delay': 5,  # Delay load halaman
}
```

## 🐛 Troubleshooting

### Error: ChromeDriver not found
```bash
pip install webdriver-manager
```

### Error: Login gagal
1. Cek koneksi internet
2. Pastikan kredensial benar
3. Coba login manual
4. Pastikan akun tidak terblokir

### Error: Tidak ada data ditemukan
1. Cek keyword yang dimasukkan
2. Pastikan halaman sudah ter-load sempurna
3. Coba scroll manual di browser
4. Cek apakah ada CAPTCHA

### Error: CAPTCHA muncul
1. Selesaikan CAPTCHA manual
2. Tunggu beberapa menit sebelum mencoba lagi
3. Gunakan login manual

### Error: Browser tidak terbuka
1. Pastikan Chrome browser terinstall
2. Cek versi ChromeDriver
3. Restart komputer jika perlu

## 📈 Tips Penggunaan

### 1. Keyword yang Efektif
- Gunakan keyword spesifik: "laptop gaming" bukan hanya "laptop"
- Kombinasikan brand: "smartphone samsung galaxy"
- Gunakan kategori: "headphone wireless bluetooth"

### 2. Jumlah Produk Optimal
- Untuk testing: 5-10 produk
- Untuk analisis: 20-50 produk
- Untuk data besar: 100+ produk (perhatikan rate limiting)

### 3. Timing yang Tepat
- Hindari peak hours (jam kerja)
- Gunakan delay yang cukup antar request
- Jangan scrape terlalu sering

### 4. Data Quality
- Selalu validasi data hasil scraping
- Cek apakah semua field terisi
- Bandingkan dengan data manual

## 🔒 Keamanan dan Etika

### Best Practices
1. **Respect Rate Limits**: Jangan scrape terlalu cepat
2. **Use Legitimate Accounts**: Gunakan akun yang valid
3. **Follow ToS**: Patuhi Terms of Service Shopee
4. **Data Privacy**: Jangan share data pribadi
5. **Educational Use**: Gunakan untuk tujuan edukasi

### Legal Compliance
- Script ini dibuat untuk tujuan edukasi dan penelitian
- Pengguna bertanggung jawab penuh atas penggunaan
- Patuhi hukum dan regulasi yang berlaku
- Hormati hak cipta dan privasi

## 📞 Support

### Kontak
- **Email**: [email protected]
- **WhatsApp**: +62-813-1608-4860

### Dokumentasi
- **README.md**: Dokumentasi lengkap
- **config.py**: Konfigurasi detail
- **example_usage.py**: Contoh penggunaan

### Community
- GitHub Issues untuk bug report
- Stack Overflow untuk pertanyaan teknis
- Forum data mining untuk diskusi

---

**⚠️ Disclaimer**: Script ini dibuat untuk tujuan edukasi dan penelitian. Pengguna bertanggung jawab penuh atas penggunaan yang sesuai dengan Terms of Service website target.