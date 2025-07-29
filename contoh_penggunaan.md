# 📖 Contoh Penggunaan Shopee Scraper

## 🚀 Cara Menggunakan di Google Colab

### Langkah 1: Buka Google Colab
1. Buka [Google Colab](https://colab.research.google.com/)
2. Buat notebook baru
3. Pastikan runtime type adalah **Python 3**

### Langkah 2: Copy-Paste Kode
Copy seluruh kode dari file `simple_shopee_scraper.py` dan paste ke cell pertama di Colab.

### Langkah 3: Jalankan Kode
1. Klik tombol **Play** atau tekan **Shift + Enter**
2. Tunggu proses instalasi dependencies selesai
3. Masukkan input sesuai permintaan

### Langkah 4: Input Data
```
🔍 Masukkan keyword produk: cabai rawit
📊 Jumlah data (default 50): 30
```

### Langkah 5: Tunggu Proses
```
🚀 Memulai scraping: 'cabai rawit'
📊 Target: 30 produk
⏳ Mohon tunggu...

✅ Chrome driver berhasil diinisialisasi
🚀 Memulai scraping untuk: 'cabai rawit'
📊 Target: 30 produk
🌐 Mengakses: https://shopee.co.id/search?keyword=cabai%20rawit
✅ Ditemukan 45 produk dengan selector: [data-sqe="link"]
📦 Total elemen ditemukan: 45
📜 Scrolling halaman...
✅ 1: Cabai Rawit Merah Segar 1kg Fresh...
✅ 2: Cabai Rawit Hijau Fresh 500gr...
✅ 3: Cabai Rawit Merah Premium Grade A...
...
🎉 Berhasil mengekstrak 30 produk
🔒 Browser ditutup
💾 Data tersimpan: shopee_cabai_rawit_20241201_143022.xlsx

📋 Preview data:
   nama_produk                    harga rating jumlah_terjual nama_toko lokasi_toko
0  Cabai Rawit Merah Segar 1kg  Rp 25,000   4.2/5        1,234    Toko Sayur    Jakarta
1  Cabai Rawit Hijau Fresh 500gr Rp 15,000   4.5/5          567   Fresh Market    Bandung
2  Cabai Rawit Merah Premium...  Rp 30,000   4.8/5        2,345   Fresh Farm    Surabaya

📊 Total: 30 produk

🎉 Selesai! File: shopee_cabai_rawit_20241201_143022.xlsx
📁 Download dari panel file di sebelah kiri
```

### Langkah 6: Download File
1. Buka panel **Files** di sebelah kiri Colab
2. Cari file dengan nama `shopee_[keyword]_[timestamp].xlsx`
3. Klik kanan file → **Download**

## 📊 Contoh Data yang Dihasilkan

| Nama Produk | Harga | Rating | Jumlah Terjual | Nama Toko | Lokasi Toko |
|-------------|-------|--------|----------------|-----------|-------------|
| Cabai Rawit Merah Segar 1kg | Rp 25,000 | 4.2/5 | 1,234 | Toko Sayur | Jakarta |
| Cabai Rawit Hijau Fresh 500gr | Rp 15,000 | 4.5/5 | 567 | Fresh Market | Bandung |
| Cabai Rawit Merah Premium Grade A | Rp 30,000 | 4.8/5 | 2,345 | Fresh Farm | Surabaya |
| Cabai Rawit Organik 250gr | Rp 18,000 | 4.0/5 | 890 | Organic Store | Yogyakarta |
| Cabai Rawit Merah Import | Rp 35,000 | 4.6/5 | 1,567 | Import Market | Medan |

## 🔍 Contoh Keyword yang Bisa Dicoba

### Makanan & Minuman
- `cabai rawit`
- `beras premium`
- `minyak goreng`
- `gula pasir`
- `susu segar`
- `roti tawar`
- `mie instan`
- `air mineral`

### Elektronik
- `smartphone samsung`
- `laptop gaming`
- `headphone wireless`
- `powerbank 10000mah`
- `charger fast charging`
- `kabel usb c`

### Fashion
- `kaos polos`
- `celana jeans`
- `sepatu sneakers`
- `tas ransel`
- `jam tangan`
- `kacamata hitam`

### Kesehatan & Kecantikan
- `vitamin c`
- `sabun mandi`
- `shampoo anti ketombe`
- `sikat gigi`
- `handuk mandi`
- `parfum pria`

### Rumah Tangga
- `panci masak`
- `piring makan`
- `gelas minum`
- `sapu lantai`
- `detergen baju`
- `tissue`

## ⚠️ Tips Penggunaan

### 1. Keyword yang Efektif
- **Gunakan keyword spesifik**: `cabai rawit merah` lebih baik dari `cabai`
- **Hindari keyword terlalu umum**: `laptop` terlalu luas, gunakan `laptop asus gaming`
- **Gunakan bahasa Indonesia**: `smartphone` lebih baik dari `handphone`

### 2. Jumlah Data
- **Mulai dengan jumlah kecil**: 20-30 produk untuk testing
- **Tingkatkan secara bertahap**: 50-100 untuk data yang lebih lengkap
- **Jangan terlalu banyak**: Max 200 produk untuk menghindari overload

### 3. Waktu Terbaik
- **Jam sibuk**: 10:00-22:00 WIB untuk data yang lebih akurat
- **Hindari jam maintenance**: 02:00-06:00 WIB
- **Weekend**: Data lebih lengkap di akhir pekan

### 4. Troubleshooting

#### Error "Chrome driver tidak ditemukan"
```
❌ Error: Message: unknown error: cannot find Chrome binary
```
**Solusi**: 
- Restart runtime Colab
- Jalankan ulang kode dari awal

#### Error "Tidak ada data yang ditemukan"
```
❌ Tidak ada data yang berhasil di-scrape
```
**Solusi**:
- Coba keyword yang berbeda
- Periksa koneksi internet
- Tunggu 5-10 menit sebelum mencoba lagi

#### Error "Timeout"
```
❌ Error: timeout
```
**Solusi**:
- Kurangi jumlah data (10-20 produk)
- Coba di waktu yang berbeda
- Periksa koneksi internet

#### Data tidak lengkap
```
📊 Total: 30 produk
- Produk dengan harga: 25
- Produk dengan rating: 20
- Produk dengan info terjual: 18
```
**Ini normal** karena tidak semua produk memiliki informasi lengkap.

## 🎯 Contoh Penggunaan Lengkap

### Contoh 1: Scraping Produk Makanan
```
🔍 Masukkan keyword produk: beras premium
📊 Jumlah data (default 50): 25

🚀 Memulai scraping: 'beras premium'
📊 Target: 25 produk
⏳ Mohon tunggu...

✅ Chrome driver berhasil diinisialisasi
🚀 Memulai scraping untuk: 'beras premium'
📊 Target: 25 produk
🌐 Mengakses: https://shopee.co.id/search?keyword=beras%20premium
✅ Ditemukan 38 produk dengan selector: [data-sqe="link"]
📦 Total elemen ditemukan: 38
📜 Scrolling halaman...
✅ 1: Beras Premium IR64 5kg...
✅ 2: Beras Premium Pandan Wangi 2kg...
...
🎉 Berhasil mengekstrak 25 produk
💾 Data tersimpan: shopee_beras_premium_20241201_150000.xlsx
```

### Contoh 2: Scraping Produk Elektronik
```
🔍 Masukkan keyword produk: smartphone samsung
📊 Jumlah data (default 50): 40

🚀 Memulai scraping: 'smartphone samsung'
📊 Target: 40 produk
⏳ Mohon tunggu...

✅ Chrome driver berhasil diinisialisasi
🚀 Memulai scraping untuk: 'smartphone samsung'
📊 Target: 40 produk
🌐 Mengakses: https://shopee.co.id/search?keyword=smartphone%20samsung
✅ Ditemukan 52 produk dengan selector: [data-sqe="link"]
📦 Total elemen ditemukan: 52
📜 Scrolling halaman...
✅ 1: Samsung Galaxy A54 5G 128GB...
✅ 2: Samsung Galaxy S23 Ultra 256GB...
...
🎉 Berhasil mengekstrak 40 produk
💾 Data tersimpan: shopee_smartphone_samsung_20241201_160000.xlsx
```

## 📈 Analisis Data

Setelah mendapatkan file Excel, Anda bisa:

1. **Analisis Harga**:
   - Harga tertinggi dan terendah
   - Rata-rata harga pasar
   - Distribusi harga

2. **Analisis Rating**:
   - Produk dengan rating tertinggi
   - Rata-rata rating kategori
   - Korelasi rating dengan harga

3. **Analisis Penjualan**:
   - Produk terlaris
   - Tren penjualan
   - Market share

4. **Analisis Lokasi**:
   - Distribusi geografis
   - Konsentrasi seller
   - Regional pricing

## 🔄 Update dan Maintenance

- **Periksa secara berkala**: Struktur website Shopee bisa berubah
- **Update selectors**: Jika scraping gagal, mungkin perlu update CSS selectors
- **Monitor error**: Catat error yang sering muncul untuk perbaikan
- **Backup data**: Simpan data penting sebelum melakukan scraping ulang

---

**Selamat mencoba! 🎉**