# Scraping Berita Kompas

Program untuk mengumpulkan data berita dari Kompas.com dengan fitur pembersihan data otomatis.

## Deskripsi

Program ini dibuat untuk keperluan riset dan pengumpulan data berita dari Kompas.com. Program ini dilengkapi dengan fitur pembersihan data otomatis yang akan memperbaiki struktur data sebelum disimpan ke file CSV.

## Fitur Utama

- 🔍 Pencarian berita berdasarkan keyword
- 📊 Ekstraksi data: judul, link, tanggal, dan konten
- 🧹 Pembersihan data otomatis
- 📁 Penyimpanan ke file CSV
- ⚡ Validasi relevansi artikel
- 🛡️ Penanganan error yang robust

## Instalasi

1. Clone atau download repository ini
2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Penggunaan

Jalankan program dengan perintah:
```bash
python scraping_kompas.py
```

Atau:
```bash
python3 scraping_kompas.py
```

## Fitur Pembersihan Data

Program ini memiliki sistem pembersihan data otomatis yang akan:

### 1. Perbaikan Kolom `link_berita`
- **Masalah**: Kolom berisi teks bukan URL
- **Solusi**: 
  - Gabungkan teks ke kolom `judul_berita`
  - Geser data dari `tanggal_rilis` ke `link_berita`
  - Geser data dari `detail_konten` ke `tanggal_rilis`
  - Kosongkan `detail_konten`

### 2. Perbaikan Kolom `tanggal_rilis`
- **Masalah**: Kolom berisi URL bukan tanggal
- **Solusi**:
  - Geser data dari `detail_konten` ke `tanggal_rilis`
  - Kosongkan `detail_konten`

### 3. Perbaikan Kolom `detail_konten`
- **Masalah**: Kolom berisi tanggal bukan konten
- **Solusi**:
  - Kosongkan kolom jika isinya mirip format tanggal

## Struktur Output

File CSV yang dihasilkan akan memiliki kolom:
- `judul_berita`: Judul artikel
- `link_berita`: URL artikel (valid)
- `tanggal_rilis`: Tanggal publikasi
- `detail_konten`: Konten artikel

## Testing

Untuk menjalankan test fungsi pembersihan data:
```bash
python test_clean_dataframe.py
```

## Kredensial

- **Dibuat oleh**: Pradipta Deska Pryanda
- **Diperbaiki dan dikembangkan oleh**: Dosen Data Mining
- **Tahun**: 2024

## Catatan Penting

- Program ini dibuat untuk keperluan riset
- Gunakan data dengan bijak dan sesuai etika riset
- Pastikan koneksi internet stabil saat menjalankan program
- Keyword yang spesifik akan memberikan hasil yang lebih baik

## Troubleshooting

### Error SSL
Program sudah dilengkapi dengan penanganan error SSL untuk environment seperti Google Colab.

### Error Dependencies
Pastikan semua dependencies terinstall dengan benar:
```bash
pip install -r requirements.txt
```

### Error Koneksi
- Periksa koneksi internet
- Coba keyword yang berbeda
- Pastikan tidak ada firewall yang memblokir akses

## Lisensi

Program ini dibuat untuk keperluan edukasi dan riset.