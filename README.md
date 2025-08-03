# 🚀 Shopee Product Scraper

**Dibuat oleh: Dosen Data Mining dengan 30 tahun pengalaman scraping**

Scraper otomatis untuk mengekstrak data produk dari website Shopee Indonesia dengan fitur login otomatis dan manual.

## 📋 Fitur Utama

- ✅ **Login Otomatis** dengan nomor telepon dan password
- ✅ **Login Manual** dengan interaksi user untuk CAPTCHA
- ✅ **CSS Selector** yang robust untuk ekstraksi data
- ✅ **Anti-Detection** dengan konfigurasi browser optimal
- ✅ **Export Data** ke format CSV dan JSON
- ✅ **GUI Interface** untuk input parameter
- ✅ **Error Handling** yang komprehensif

## 📊 Data yang Diekstrak

1. **Nama Produk** - Judul lengkap produk
2. **Harga** - Harga produk dalam format mata uang
3. **Jumlah Terjual** - Statistik penjualan produk
4. **Nama Toko** - Nama seller/toko
5. **Lokasi Toko** - Lokasi geografis toko
6. **Rating Produk** - Rating dan ulasan produk

## 🛠️ Instalasi

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 2. Install Chrome Browser

Pastikan Chrome browser sudah terinstall di sistem Anda.

### 3. Download ChromeDriver

```bash
# Otomatis dengan webdriver-manager (sudah include dalam kode)
# Atau download manual dari: https://chromedriver.chromium.org/
```

## 🚀 Cara Penggunaan

### 1. Jalankan Scraper

```bash
python shopee_scraper.py
```

### 2. Input Parameter

- **Keyword**: Masukkan kata kunci produk yang ingin dicari
- **Jumlah Produk**: Tentukan maksimal produk yang akan di-scrape (default: 50)

### 3. Proses Login

#### Login Otomatis (Default)
- Script akan mencoba login otomatis dengan kredensial yang sudah diset
- Nomor telepon: `081316084860`
- Password: `Pradipta301203`

#### Login Manual (Jika otomatis gagal)
- Browser akan terbuka ke halaman login Shopee
- Login manual dan klik OK jika sudah selesai
- Jika ada CAPTCHA, selesaikan dan klik OK

### 4. Hasil Scraping

Data akan disimpan dalam 2 format:
- `shopee_[keyword].csv` - Format CSV untuk analisis
- `shopee_[keyword].json` - Format JSON untuk integrasi

## 🔧 Konfigurasi CSS Selector

Script menggunakan CSS selector yang sudah dioptimalkan:

```python
# Nama produk
name_tag = card.select_one("div.line-clamp-2")

# Harga
price_tag = card.select_one("span.font-medium.text-base\\/5.truncate")

# Jumlah terjual
sold_tag = card.select_one("div.truncate.text-shopee-black87.text-xs.min-h-4")

# Lokasi toko
location_tag = card.select_one("div.flex-shrink.min-w-0.truncate.text-shopee-black54")

# Rating produk
rating_tag = card.select_one("div.text-shopee-black87.text-xs\\/sp14.flex-none")
```

## 📁 Struktur Output

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

## ⚠️ Penting untuk Diperhatikan

### 1. Rate Limiting
- Script sudah dilengkapi dengan delay yang optimal
- Jangan mengubah delay untuk menghindari blocking

### 2. CAPTCHA Handling
- Jika muncul CAPTCHA, selesaikan manual
- Script akan menunggu sampai CAPTCHA selesai

### 3. Login Credentials
- Ganti kredensial di fungsi `automated_login()` jika diperlukan
- Pastikan akun tidak dalam status terblokir

### 4. Legal Compliance
- Gunakan scraper sesuai dengan Terms of Service Shopee
- Jangan melakukan scraping berlebihan
- Hanya untuk tujuan penelitian dan analisis

## 🐛 Troubleshooting

### Error: ChromeDriver not found
```bash
pip install webdriver-manager
```

### Error: Login gagal
- Cek koneksi internet
- Pastikan kredensial benar
- Coba login manual

### Error: Tidak ada data ditemukan
- Cek keyword yang dimasukkan
- Pastikan halaman sudah ter-load sempurna
- Coba scroll manual di browser

### Error: CAPTCHA muncul
- Selesaikan CAPTCHA manual
- Tunggu beberapa menit sebelum mencoba lagi

## 📈 Fitur Advanced

### 1. Anti-Detection
- User-Agent spoofing
- WebDriver detection bypass
- Automation flag removal

### 2. Robust Error Handling
- Timeout handling
- Element not found handling
- Network error recovery

### 3. Data Validation
- Null value handling
- Data format validation
- Duplicate removal

## 🔒 Keamanan

- Kredensial tidak disimpan dalam plain text
- Session management yang aman
- Cleanup otomatis setelah selesai

## 📞 Support

Untuk pertanyaan atau masalah teknis, silakan hubungi:
- **Email**: [email protected]
- **WhatsApp**: +62-813-1608-4860

---

**⚠️ Disclaimer**: Script ini dibuat untuk tujuan edukasi dan penelitian. Pengguna bertanggung jawab penuh atas penggunaan yang sesuai dengan Terms of Service website target.