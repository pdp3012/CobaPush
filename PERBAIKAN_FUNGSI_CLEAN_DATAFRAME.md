# Perbaikan Fungsi `clean_dataframe`

## Ringkasan Perbaikan

Fungsi `clean_dataframe` telah diperbaiki untuk menangani masalah struktur data yang tidak konsisten sebelum disimpan ke file CSV. Perbaikan ini memastikan bahwa setiap kolom berisi data yang sesuai dengan tipe datanya.

## Masalah yang Ditangani

### 1. Kolom `link_berita` Berisi Teks Bukan URL
**Masalah**: Kolom `link_berita` berisi teks biasa bukan URL yang valid.

**Contoh Masalah**:
```
judul_berita: "Berita Penting"
link_berita: "Ini bukan URL, ini teks biasa"  ← SALAH
tanggal_rilis: "2024-01-15"
detail_konten: "Konten berita..."
```

**Solusi**:
1. Gabungkan teks dari `link_berita` ke `judul_berita`
2. Geser data dari `tanggal_rilis` ke `link_berita`
3. Geser data dari `detail_konten` ke `tanggal_rilis`
4. Kosongkan `detail_konten`

**Hasil Setelah Perbaikan**:
```
judul_berita: "Berita Penting Ini bukan URL, ini teks biasa"
link_berita: "2024-01-15"  ← DIPERBAIKI
tanggal_rilis: "Konten berita..."  ← DIPERBAIKI
detail_konten: ""  ← DIKOSONGKAN
```

### 2. Kolom `tanggal_rilis` Berisi URL
**Masalah**: Kolom `tanggal_rilis` berisi URL bukan tanggal.

**Contoh Masalah**:
```
judul_berita: "Berita Penting"
link_berita: "https://kompas.com/berita"
tanggal_rilis: "https://kompas.com/tanggal"  ← SALAH
detail_konten: "Konten berita..."
```

**Solusi**:
1. Geser data dari `detail_konten` ke `tanggal_rilis`
2. Kosongkan `detail_konten`

**Hasil Setelah Perbaikan**:
```
judul_berita: "Berita Penting"
link_berita: "https://kompas.com/berita"
tanggal_rilis: "Konten berita..."  ← DIPERBAIKI
detail_konten: ""  ← DIKOSONGKAN
```

### 3. Kolom `detail_konten` Berisi Tanggal
**Masalah**: Kolom `detail_konten` berisi format tanggal bukan konten artikel.

**Contoh Masalah**:
```
judul_berita: "Berita Penting"
link_berita: "https://kompas.com/berita"
tanggal_rilis: "2024-01-15"
detail_konten: "15 Januari 2024"  ← SALAH
```

**Solusi**:
1. Kosongkan `detail_konten` jika isinya mirip format tanggal

**Hasil Setelah Perbaikan**:
```
judul_berita: "Berita Penting"
link_berita: "https://kompas.com/berita"
tanggal_rilis: "2024-01-15"
detail_konten: ""  ← DIKOSONGKAN
```

## Algoritma Pembersihan

### Langkah 1: Periksa Kolom `link_berita`
```python
if not url_pattern.match(current_link):
    # Gabungkan ke judul_berita
    new_title = f"{current_title} {current_link}"
    df.at[index, 'judul_berita'] = new_title
    
    # Geser data
    df.at[index, 'link_berita'] = current_date
    df.at[index, 'tanggal_rilis'] = current_content
    df.at[index, 'detail_konten'] = ""
```

### Langkah 2: Periksa Kolom `tanggal_rilis`
```python
if url_pattern.match(shifted_date):
    # Geser data dari detail_konten
    df.at[index, 'tanggal_rilis'] = shifted_content_to_date
    df.at[index, 'detail_konten'] = ""
```

### Langkah 3: Periksa Kolom `detail_konten`
```python
if len(shifted_content) < 100 and date_like_pattern.search(shifted_content):
    df.at[index, 'detail_konten'] = ""
```

### Langkah 4: Validasi Akhir
```python
# Periksa hasil akhir
final_link = str(df.at[index, 'link_berita']).strip()
if final_link and not url_pattern.match(final_link):
    print("Peringatan: link_berita masih bukan URL yang valid")

final_date = str(df.at[index, 'tanggal_rilis']).strip()
if final_date and url_pattern.match(final_date):
    print("Peringatan: tanggal_rilis masih berisi URL")
```

## Regex Patterns

### URL Pattern
```python
url_pattern = re.compile(
    r'^(?:http|ftp)s?://' # http:// atau https://
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' # domain...
    r'localhost|' # localhost...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...atau ip
    r'(?::\d+)?' # optional port
    r'(?:/?|[/?]\S+)$', re.IGNORECASE)
```

### Date Pattern
```python
date_like_pattern = re.compile(
    r'(\d{4}[/-]\d{1,2}[/-]\d{1,2})|'           # 2020/12/31, 2020-12-31
    r'(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})|'         # 12/31/2020, 12-31-2020, 31/12/20
    r'(\d{1,2}\s+(?:Januari|Februari|Maret|April|Mei|Juni|Juli|Agustus|September|Oktober|November|Desember)\s+\d{2,4})|' # 1 Januari 2020
    r'(\d{1,2}:\d{2}(?::\d{2})?\s*(?:WIB|WITA|WIT)?)|' # 10:30 WIB, 14:20:15 WITA
    r'(\d{1,2}:\d{2}(?::\d{2})?\s*(?:AM|PM)?)',     # 10:30 AM, 2:20:15 PM
    re.IGNORECASE)
```

## Fitur Baru

### 1. Logging Detail
- Setiap langkah pembersihan dicatat dengan detail
- Menampilkan data sebelum dan sesudah perbaikan
- Peringatan jika masih ada masalah setelah perbaikan

### 2. Error Handling
- Penanganan error untuk setiap baris data
- Program tidak berhenti jika ada error pada satu baris
- Pesan error yang informatif

### 3. Validasi Akhir
- Pemeriksaan hasil akhir untuk memastikan data sudah benar
- Peringatan jika masih ada masalah yang tidak bisa diperbaiki

## Contoh Penggunaan

### Dalam Program Utama
```python
def save_to_csv(dataframe, keyword):
    if not dataframe.empty:
        # Pembersihan data sebelum disimpan
        cleaned_dataframe = clean_dataframe(dataframe.copy())
        
        # Simpan ke CSV
        filename = f"berita_kompas_{keyword}_{timestamp}.csv"
        cleaned_dataframe.to_csv(filename, index=False, encoding='utf-8-sig')
        return filename
    return None
```

### Testing
```python
# Jalankan test
python test_clean_dataframe.py

# Atau demo sederhana
python demo_clean_dataframe.py

# Demo dengan file CSV
python demo_csv_cleaning.py
```

## File Terkait

1. `scraping_kompas.py` - Program utama dengan fungsi `clean_dataframe` yang diperbaiki
2. `test_clean_dataframe.py` - Test cases untuk fungsi pembersihan
3. `demo_clean_dataframe.py` - Demo fungsi pembersihan
4. `demo_csv_cleaning.py` - Demo pembersihan data dari file CSV
5. `contoh_data_sebelum_bersih.csv` - Contoh data bermasalah
6. `contoh_data_setelah_bersih.csv` - Hasil data setelah dibersihkan

## Keuntungan Perbaikan

1. **Data Konsisten**: Setiap kolom berisi data yang sesuai dengan tipe datanya
2. **Otomatis**: Tidak perlu intervensi manual untuk memperbaiki data
3. **Robust**: Menangani berbagai skenario masalah data
4. **Transparan**: Setiap langkah perbaikan dicatat dan ditampilkan
5. **Aman**: Menggunakan copy DataFrame untuk menghindari modifikasi data asli

## Catatan Penting

- Fungsi ini dipanggil otomatis sebelum data disimpan ke CSV
- Data asli tidak dimodifikasi, hanya salinan yang dibersihkan
- Jika ada masalah yang tidak bisa diperbaiki, akan ditampilkan peringatan
- Fungsi ini kompatibel dengan berbagai format tanggal dan URL