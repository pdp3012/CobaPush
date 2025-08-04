# Pembaruan Fungsi clean_dataframe

## Ringkasan Perbaikan

Fungsi `clean_dataframe` telah diperbaiki untuk menangani masalah pergeseran data antar kolom dengan lebih baik. Perbaikan ini memastikan bahwa data yang disimpan ke CSV memiliki struktur yang benar dan konsisten.

## Masalah yang Diperbaiki

### 1. Kolom `link_berita` berisi teks bukan link
**Sebelum:** Data tetap seperti itu tanpa perbaikan
**Sesudah:** 
- Teks dari `link_berita` digabungkan ke `judul_berita`
- Data dari `tanggal_rilis` dipindah ke `link_berita`
- Data dari `detail_konten` dipindah ke `tanggal_rilis`
- `detail_konten` dikosongkan

### 2. Kolom `tanggal_rilis` berisi link
**Sebelum:** Data tetap seperti itu tanpa perbaikan
**Sesudah:**
- Data dari `detail_konten` dipindah ke `tanggal_rilis`
- `detail_konten` dikosongkan

### 3. Kolom `detail_konten` berisi tanggal
**Sebelum:** Data tetap seperti itu tanpa perbaikan
**Sesudah:**
- `detail_konten` dikosongkan karena berisi tanggal bukan konten artikel

## Algoritma Pembersihan

### Langkah 1: Periksa Kolom `link_berita`
```python
if not url_pattern.match(current_link) and current_link:
    # Gabungkan ke judul_berita
    # Geser tanggal_rilis ke link_berita
    # Geser detail_konten ke tanggal_rilis
    # Kosongkan detail_konten
```

### Langkah 2: Periksa Kolom `tanggal_rilis`
```python
if url_pattern.match(current_date) and current_date:
    # Geser detail_konten ke tanggal_rilis
    # Kosongkan detail_konten
```

### Langkah 3: Periksa Kolom `detail_konten`
```python
if not is_valid_content(current_content) and current_content:
    # Kosongkan detail_konten
```

## Fungsi Helper

### `is_valid_content(text)`
Memeriksa apakah teks adalah konten artikel yang valid:
- Minimal 10 karakter
- Bukan URL
- Bukan tanggal (jika pendek < 50 karakter)

## Contoh Hasil Perbaikan

### Test Case 1: Data Normal
```
Sebelum: [judul, link, tanggal, konten] ✅
Sesudah:  [judul, link, tanggal, konten] ✅ (tidak berubah)
```

### Test Case 2: link_berita bukan link
```
Sebelum: [judul, "teks", tanggal, konten]
Sesudah:  [judul+teks, tanggal, konten, ""]
```

### Test Case 3: tanggal_rilis berisi link
```
Sebelum: [judul, link, "http://...", konten]
Sesudah:  [judul, link, konten, ""]
```

### Test Case 4: detail_konten berisi tanggal
```
Sebelum: [judul, link, tanggal, "2024-01-19"]
Sesudah:  [judul, link, tanggal, ""]
```

## Keunggulan Perbaikan

1. **Otomatis:** Tidak perlu intervensi manual
2. **Konsisten:** Semua baris diproses dengan aturan yang sama
3. **Aman:** Menggunakan copy DataFrame untuk menghindari perubahan data asli
4. **Informatif:** Memberikan log detail untuk setiap perbaikan
5. **Robust:** Menangani berbagai skenario data yang bermasalah

## Penggunaan

Fungsi ini dipanggil otomatis dalam `save_to_csv()` sebelum data disimpan ke file CSV:

```python
def save_to_csv(dataframe, keyword):
    if not dataframe.empty:
        # Pembersihan data sebelum penyimpanan
        cleaned_dataframe = clean_dataframe(dataframe.copy())
        
        # Simpan ke CSV
        cleaned_dataframe.to_csv(filename, index=False, encoding='utf-8-sig')
```

## Testing

File `test_clean_dataframe.py` berisi 6 test case yang mencakup berbagai skenario:
1. Data normal
2. link_berita bukan link
3. tanggal_rilis berisi link
4. detail_konten berisi tanggal
5. Kombinasi masalah
6. Data kosong dan null

Untuk menjalankan test:
```bash
python test_clean_dataframe.py
```