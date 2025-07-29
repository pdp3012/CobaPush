# 🛍️ Shopee Scraper

Scraper otomatis untuk mengumpulkan data produk dari Shopee Indonesia dengan kemampuan anti-deteksi bot yang canggih.

## ✨ Fitur Utama

- 🔍 **Scraping berdasarkan keyword**: Masukkan keyword produk, scraper akan otomatis mencari di Shopee
- 🛡️ **Anti-bot detection**: Menggunakan teknik stealth untuk menghindari deteksi bot
- 📊 **Data lengkap**: Mengekstrak nama produk, harga, rating, jumlah terjual, nama toko, dan lokasi toko
- 💾 **Export Excel**: Data tersimpan dalam format Excel yang mudah dibaca
- 🚀 **Optimized for Colab**: Khusus dioptimalkan untuk Google Colab

## 📋 Data yang Di-scrape

1. **Nama Produk** - Nama lengkap produk
2. **Harga** - Harga produk dalam format Rupiah
3. **Rating** - Rating produk (skala 1-5)
4. **Jumlah Terjual** - Jumlah unit yang telah terjual
5. **Nama Toko** - Nama toko/seller
6. **Lokasi Toko** - Lokasi toko/seller

## 🚀 Cara Penggunaan

### Untuk Google Colab

1. **Buka Google Colab** dan buat notebook baru
2. **Upload file** `shopee_scraper_colab.py` ke Colab
3. **Jalankan cell** dengan kode scraper
4. **Masukkan input**:
   - Keyword produk (contoh: "cabai rawit")
   - Jumlah data yang diinginkan (default: 50)
5. **Tunggu proses** scraping selesai
6. **Download file Excel** dari panel file di sebelah kiri

### Untuk Local Environment

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Install Chrome browser** (jika belum ada)

3. **Jalankan scraper**:
   ```bash
   python shopee_scraper.py
   ```

4. **Masukkan input** sesuai permintaan

## 📁 File yang Dihasilkan

File Excel akan disimpan dengan format:
```
shopee_[keyword]_[timestamp].xlsx
```

Contoh: `shopee_cabai_rawit_20241201_143022.xlsx`

## 🔧 Teknik Anti-Deteksi

Scraper ini menggunakan berbagai teknik untuk menghindari deteksi bot:

- **Random User-Agent**: Menggunakan user-agent acak setiap kali request
- **Random Delays**: Delay acak antara request untuk menyerupai perilaku manusia
- **Stealth Headers**: Headers yang menyerupai browser asli
- **Multiple Selectors**: Menggunakan berbagai CSS selector untuk adaptasi dengan perubahan struktur website
- **Scroll Simulation**: Simulasi scroll halaman untuk memuat konten dinamis
- **Browser Fingerprinting**: Menyembunyikan tanda-tanda otomasi browser

## ⚠️ Penting untuk Diperhatikan

1. **Gunakan dengan bijak**: Jangan melakukan scraping berlebihan yang dapat membebani server Shopee
2. **Respect robots.txt**: Patuhi aturan crawling website
3. **Data untuk analisis**: Gunakan data yang di-scrape hanya untuk tujuan analisis dan penelitian
4. **Koneksi internet**: Pastikan koneksi internet stabil untuk hasil optimal
5. **Keyword spesifik**: Gunakan keyword yang spesifik untuk hasil yang lebih akurat

## 🛠️ Troubleshooting

### Error "Chrome driver tidak ditemukan"
- Pastikan Chrome browser terinstall
- Untuk Colab, kode sudah otomatis menginstall chromedriver

### Error "Tidak ada data yang ditemukan"
- Coba keyword yang berbeda
- Periksa koneksi internet
- Tunggu beberapa saat dan coba lagi

### Error "Timeout"
- Periksa koneksi internet
- Coba jumlah data yang lebih sedikit
- Tunggu beberapa saat sebelum mencoba lagi

### Data tidak lengkap
- Ini normal karena tidak semua produk memiliki informasi lengkap
- Scraper akan menandai data yang tidak tersedia dengan "N/A"

## 📊 Contoh Output

```
=== SHOPEE SCRAPER ===
Scraper otomatis untuk data produk Shopee
==================================================
🔍 Masukkan keyword produk yang ingin di-scrape: cabai rawit
📊 Masukkan jumlah data yang ingin didapatkan (default: 50): 30

🚀 Memulai scraping untuk: 'cabai rawit'
📊 Target jumlah data: 30
⏳ Mohon tunggu...

✅ Chrome driver berhasil diinisialisasi
🚀 Memulai scraping untuk keyword: 'cabai rawit'
📊 Target jumlah produk: 30
🌐 Mengakses URL: https://shopee.co.id/search?keyword=cabai%20rawit
✅ Halaman berhasil dimuat dengan selector: [data-sqe="link"]
✅ Berhasil menemukan 45 produk dengan selector: [data-sqe="link"]
📦 Total elemen yang ditemukan: 45
✅ Produk 1: Cabai Rawit Merah Segar 1kg...
✅ Produk 2: Cabai Rawit Hijau Fresh 500gr...
...
🎉 Berhasil mengekstrak 30 produk
💾 Data berhasil disimpan ke: shopee_cabai_rawit_20241201_143022.xlsx

📋 Preview data:
   nama_produk                    harga rating jumlah_terjual nama_toko lokasi_toko
0  Cabai Rawit Merah Segar 1kg  Rp 25,000   4.2/5        1,234    Toko Sayur    Jakarta
1  Cabai Rawit Hijau Fresh 500gr Rp 15,000   4.5/5          567   Fresh Market    Bandung

📊 Total data: 30 produk

📈 Statistik data:
- Produk dengan harga: 30
- Produk dengan rating: 28
- Produk dengan info terjual: 25

🎉 Scraping selesai! Data tersimpan di: shopee_cabai_rawit_20241201_143022.xlsx
📁 File dapat diunduh dari panel file di sebelah kiri
```

## 🔄 Versi

- **v1.0**: Versi awal dengan fitur dasar scraping
- **v1.1**: Penambahan anti-deteksi dan multiple selectors
- **v1.2**: Optimasi untuk Google Colab

## 📝 Lisensi

Kode ini dibuat untuk tujuan edukasi dan penelitian. Gunakan dengan bertanggung jawab dan patuhi Terms of Service Shopee.

## 🤝 Kontribusi

Jika menemukan bug atau ingin menambahkan fitur, silakan buat issue atau pull request.

---

**Disclaimer**: Scraper ini dibuat untuk tujuan edukasi. Pengguna bertanggung jawab penuh atas penggunaan tool ini dan harus mematuhi Terms of Service website yang di-scrape.