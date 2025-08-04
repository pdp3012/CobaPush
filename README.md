# 🤖 Blibli Scraper - Anti-Detection Version

Scraper untuk website Blibli yang telah dioptimasi untuk mengatasi masalah 403 Forbidden dan anti-bot detection.

## 🚀 Fitur Utama

### ✅ **Anti-Detection Features:**
- **Multiple User-Agent Rotation**: Menggunakan 5 User-Agent berbeda secara random
- **Advanced Headers**: Headers yang mirip browser asli
- **Session Management**: Session pooling dan connection management
- **Multiple URL Strategies**: 5 format URL berbeda untuk pencarian
- **API Fallback**: Menggunakan API endpoint sebagai alternatif
- **SSL Verification Disabled**: Mengatasi masalah SSL certificate
- **Random Delays**: Delay random untuk menghindari deteksi
- **Retry Mechanism**: 3 teknik alternatif jika request gagal

### 📊 **Data yang Diekstrak:**
- ✅ Nama Produk
- ✅ Harga
- ✅ Rating
- ✅ Jumlah Terjual
- ✅ Nama Toko
- ✅ Link Produk
- ✅ Timestamp

## 🛠️ Instalasi

### Dependencies:
```bash
pip install requests beautifulsoup4 pandas urllib3
```

### Atau install semua sekaligus:
```bash
pip install -r requirements.txt
```

## 📋 Cara Penggunaan

### 1. **Jalankan Scraper:**
```bash
python blibli_scraper.py
```

### 2. **Input yang Diperlukan:**
- **Keyword**: Kata kunci pencarian (minimal 2 karakter)
- **Jumlah Halaman**: 1-10 halaman (default: 3)

### 3. **Contoh Penggunaan:**
```
🔍 Masukkan keyword pencarian: cabai rawit
📄 Jumlah halaman (1-10, default=3): 2
```

## 🔧 Teknik Anti-Detection yang Digunakan

### 1. **Headers Optimization:**
```python
# Multiple User-Agent rotation
user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36...',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36...',
    # ... 3 more user agents
]

# Advanced browser headers
headers = {
    'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'DNT': '1',
    # ... more headers
}
```

### 2. **Multiple URL Strategies:**
```python
urls = [
    f"https://www.blibli.com/cari/{keyword}",
    f"https://www.blibli.com/search/{keyword}",
    f"https://www.blibli.com/search?q={keyword}",
    f"https://www.blibli.com/cari?q={keyword}",
    f"https://www.blibli.com/search/products?q={keyword}"
]
```

### 3. **Session Management:**
```python
# Connection pooling
adapter = requests.adapters.HTTPAdapter(
    pool_connections=10,
    pool_maxsize=10,
    max_retries=3
)
```

### 4. **Alternative Request Techniques:**
- **Technique 1**: Different headers
- **Technique 2**: SSL verification disabled
- **Technique 3**: Mobile User-Agent
- **Technique 4**: Alternative URL formats
- **Technique 5**: Advanced headers with Google referer

## 📊 Output Format

### CSV File Structure:
```csv
nama_produk,harga,rating,jumlah_terjual,nama_toko,link_produk,timestamp
"Cabai Rawit Hijau [250g]","Rp 24.200","4.5","590 terjual","FreshBox Flagship Store","https://www.blibli.com/p/...","2024-01-15 10:30:00"
```

### Console Output:
```
🚀 Memulai scraping untuk keyword: 'cabai rawit'
📋 Target maksimal halaman: 2
⏱️  Delay antar halaman: 3-7 detik

============================================================
📄 MEMPROSES HALAMAN 1
============================================================
🔄 Mencoba URL 1/5: https://www.blibli.com/cari/cabai%20rawit
🌐 Mengakses homepage untuk mendapatkan cookies...
🔄 Mengakses halaman (Percobaan 1)...
✅ Berhasil mengakses halaman (Size: 45678 bytes)
✅ Berhasil dengan URL: https://www.blibli.com/cari/cabai%20rawit
🔍 Menganalisis struktur halaman...
✅ Ditemukan 15 container produk
📦 Produk 1: Cabai Rawit Hijau Sayuran [250 g]... | Rp 24.200
📦 Produk 2: Cabai Rawit Merah Segar [500g]... | Rp 45.000
...
```

## ⚠️ Troubleshooting

### Jika Masih Mendapat 403 Forbidden:

1. **Coba dari Jaringan Berbeda:**
   - Gunakan WiFi yang berbeda
   - Coba dari mobile hotspot
   - Gunakan VPN

2. **Ubah Keyword:**
   - Gunakan keyword yang lebih umum
   - Hindari keyword yang terlalu spesifik

3. **Tunggu Sebentar:**
   - Blibli mungkin memblokir IP sementara
   - Tunggu 15-30 menit sebelum mencoba lagi

4. **Kurangi Jumlah Halaman:**
   - Mulai dengan 1 halaman dulu
   - Tingkatkan secara bertahap

### Error Messages:
```
🚫 403 Forbidden - Mencoba dengan teknik berbeda...
🔄 Mencoba dengan session baru...
⚠️  Session baru juga gagal: Connection timeout
```

## 🔒 Legal & Ethical Considerations

### ⚠️ **Peringatan Penting:**
- Gunakan scraper ini dengan bijak dan bertanggung jawab
- Patuhi Terms of Service Blibli
- Jangan melakukan scraping berlebihan
- Hormati rate limits website
- Gunakan data hanya untuk tujuan yang sah

### 📋 **Best Practices:**
- Scrape maksimal 3-5 halaman per session
- Tunggu minimal 5-10 menit antara session
- Jangan scrape lebih dari 100 produk per hari
- Monitor response dari website

## 🛠️ Customization

### Mengubah Delay:
```python
# Di fungsi scrape_products
delay_range=(5, 10)  # Delay 5-10 detik
```

### Mengubah User-Agents:
```python
# Di __init__
self.user_agents = [
    'Your Custom User-Agent 1',
    'Your Custom User-Agent 2',
    # ... tambahkan user agent custom
]
```

### Mengubah CSS Selectors:
```python
# Di extract_product_name
title_selectors = [
    'div.your-custom-selector',
    'span.your-custom-class',
    # ... tambahkan selector custom
]
```

## 📈 Performance Tips

1. **Optimasi untuk Google Colab:**
   - Gunakan GPU runtime jika tersedia
   - Monitor memory usage
   - Restart runtime jika memory penuh

2. **Optimasi untuk Local Machine:**
   - Gunakan SSD untuk penyimpanan
   - Pastikan koneksi internet stabil
   - Monitor CPU usage

3. **Batch Processing:**
   - Scrape multiple keywords dalam satu session
   - Simpan hasil ke file terpisah
   - Gunakan timestamp untuk naming file

## 🤝 Contributing

Jika Anda menemukan bug atau ingin menambahkan fitur:

1. Fork repository ini
2. Buat branch baru untuk fitur
3. Commit perubahan Anda
4. Push ke branch
5. Buat Pull Request

## 📄 License

Project ini dibuat untuk tujuan edukasi. Gunakan dengan bertanggung jawab.

---

**Dikembangkan dengan ❤️ untuk membantu penelitian dan analisis data e-commerce Indonesia**