# 🛍️ Advanced Shopee Product Scraper - Google Colab Example
# Dibuat oleh: Dosen Data Mining dengan 30 tahun pengalaman

# ============================================================================
# CELL 1: Install Dependencies
# ============================================================================
"""
# Jalankan cell ini terlebih dahulu untuk menginstall semua dependencies

!pip install requests==2.31.0 beautifulsoup4==4.12.2 selenium==4.15.2 pandas==2.1.3 openpyxl==3.1.2 lxml==4.9.3 urllib3==2.0.7
"""

# ============================================================================
# CELL 2: Setup Chrome dan ChromeDriver
# ============================================================================
"""
# Install Chrome browser dan ChromeDriver untuk automation

!apt-get update
!apt-get install -y wget unzip
!wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add -
!echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list
!apt-get update
!apt-get install -y google-chrome-stable

# Install ChromeDriver
!wget -O /tmp/chromedriver.zip https://chromedriver.storage.googleapis.com/120.0.6099.109/chromedriver_linux64.zip
!unzip /tmp/chromedriver.zip -d /usr/local/bin/
!chmod +x /usr/local/bin/chromedriver

print("✅ Chrome dan ChromeDriver berhasil diinstall!")
"""

# ============================================================================
# CELL 3: Upload Scraper Files
# ============================================================================
"""
# Upload file advanced_shopee_scraper.py ke Google Colab

from google.colab import files
uploaded = files.upload()

print("✅ File berhasil diupload!")
"""

# ============================================================================
# CELL 4: Import Scraper
# ============================================================================
"""
# Import dan inisialisasi Advanced Shopee Scraper

from advanced_shopee_scraper import AdvancedShopeeScraper

print("✅ Advanced Shopee Scraper berhasil diimport!")
"""

# ============================================================================
# CELL 5: Basic Usage Example
# ============================================================================
"""
# Contoh penggunaan dasar scraper

# Inisialisasi scraper
scraper = AdvancedShopeeScraper()

# Konfigurasi scraping
keyword = "cabai rawit"  # Ganti dengan keyword yang diinginkan
max_products = 20  # Jumlah produk yang ingin di-scrape

print(f"🔍 Keyword: {keyword}")
print(f"📊 Target produk: {max_products}")
print("🚀 Memulai scraping...")
"""

# ============================================================================
# CELL 6: Start Scraping
# ============================================================================
"""
# Mulai proses scraping

import time

start_time = time.time()
products_data = scraper.scrape_shopee(keyword, max_products)
end_time = time.time()

execution_time = end_time - start_time
print(f"\\n⏱️ Waktu eksekusi: {execution_time:.2f} detik")
"""

# ============================================================================
# CELL 7: Display Results
# ============================================================================
"""
# Tampilkan hasil scraping dan simpan ke file

if products_data:
    # Display sample data
    import pandas as pd
    
    df = pd.DataFrame(products_data)
    print("📋 SAMPLE DATA YANG BERHASIL DI-SCRAPE:")
    print("=" * 70)
    print(df.head(10).to_string(index=False))
    
    # Save to files
    timestamp = pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')
    filename_base = f"shopee_{keyword.replace(' ', '_')}_{len(products_data)}_products_{timestamp}"
    
    # Save CSV
    csv_filename = f"{filename_base}.csv"
    scraper.save_to_csv(products_data, csv_filename)
    
    # Save Excel
    excel_filename = f"{filename_base}.xlsx"
    scraper.save_to_excel(products_data, excel_filename)
    
    # Statistics
    print(f"\\n📈 STATISTIK SCRAPING:")
    print(f"✅ Total data: {len(products_data)} produk")
    print(f"📁 File CSV: {csv_filename}")
    print(f"📁 File Excel: {excel_filename}")
    print(f"⏱️ Waktu: {execution_time:.2f} detik")
    print(f"🚀 Rata-rata: {len(products_data)/execution_time:.2f} produk/detik")
    
else:
    print("❌ Tidak ada data yang berhasil di-scrape.")
"""

# ============================================================================
# CELL 8: Download Files
# ============================================================================
"""
# Download file hasil scraping

if products_data:
    from google.colab import files
    
    # Download CSV
    files.download(csv_filename)
    
    # Download Excel
    files.download(excel_filename)
    
    print("✅ Files berhasil didownload!")
"""

# ============================================================================
# CELL 9: Advanced Usage - Multiple Keywords
# ============================================================================
"""
# Scraping multiple keywords

keywords = ["laptop gaming", "smartphone", "baju muslim", "sepatu nike"]
max_products_per_keyword = 15

all_data = []

for keyword in keywords:
    print(f"\\n🔍 Scraping: {keyword}")
    print("=" * 50)
    
    scraper = AdvancedShopeeScraper()
    data = scraper.scrape_shopee(keyword, max_products_per_keyword)
    
    if data:
        # Add keyword info to data
        for item in data:
            item['Keyword'] = keyword
        all_data.extend(data)
        print(f"✅ Berhasil scrape {len(data)} produk untuk {keyword}")
    else:
        print(f"❌ Gagal scrape {keyword}")
    
    # Delay between keywords
    import time
    time.sleep(5)

print(f"\\n🎉 Total semua data: {len(all_data)} produk")
"""

# ============================================================================
# CELL 10: Save Combined Data
# ============================================================================
"""
# Save all data from multiple keywords

if all_data:
    import pandas as pd
    from datetime import datetime
    
    df_all = pd.DataFrame(all_data)
    
    # Save combined data
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    combined_filename = f"shopee_combined_data_{len(all_data)}_products_{timestamp}.csv"
    
    df_all.to_csv(combined_filename, index=False, encoding='utf-8-sig')
    print(f"💾 Combined data saved: {combined_filename}")
    
    # Display summary
    print("\\n📊 SUMMARY BY KEYWORD:")
    summary = df_all.groupby('Keyword').size().reset_index(name='Count')
    print(summary.to_string(index=False))
    
    # Download combined file
    from google.colab import files
    files.download(combined_filename)
"""

# ============================================================================
# CELL 11: Troubleshooting
# ============================================================================
"""
# Check setup jika mengalami masalah

import subprocess

print("🔍 Checking setup...")

# Check Chrome
try:
    chrome_version = subprocess.check_output(['google-chrome', '--version'], stderr=subprocess.STDOUT)
    print(f"✅ Chrome: {chrome_version.decode().strip()}")
except:
    print("❌ Chrome not found")

# Check ChromeDriver
try:
    chromedriver_version = subprocess.check_output(['chromedriver', '--version'], stderr=subprocess.STDOUT)
    print(f"✅ ChromeDriver: {chromedriver_version.decode().strip()}")
except:
    print("❌ ChromeDriver not found")

# Check Python packages
import pkg_resources
required_packages = ['requests', 'beautifulsoup4', 'selenium', 'pandas', 'openpyxl']

for package in required_packages:
    try:
        version = pkg_resources.get_distribution(package).version
        print(f"✅ {package}: {version}")
    except:
        print(f"❌ {package}: Not installed")
"""

# ============================================================================
# CELL 12: Interactive Mode
# ============================================================================
"""
# Jalankan scraper dalam mode interactive

# Import dan jalankan main function
from advanced_shopee_scraper import main

# Jalankan interactive mode
main()
"""

# ============================================================================
# USAGE INSTRUCTIONS
# ============================================================================

"""
📋 INSTRUKSI PENGGUNAAN DI GOOGLE COLAB:

1. Buka Google Colab (colab.research.google.com)
2. Buat notebook baru
3. Copy-paste setiap cell di atas ke cell terpisah
4. Jalankan cell secara berurutan:
   - Cell 1: Install dependencies
   - Cell 2: Setup Chrome dan ChromeDriver
   - Cell 3: Upload file advanced_shopee_scraper.py
   - Cell 4: Import scraper
   - Cell 5-8: Basic usage
   - Cell 9-10: Advanced usage (optional)
   - Cell 11: Troubleshooting (jika ada masalah)
   - Cell 12: Interactive mode (alternative)

🔧 TIPS PENGGUNAAN:
- Pastikan koneksi internet stabil
- Gunakan keyword yang spesifik untuk hasil yang lebih baik
- Jangan scrape terlalu banyak data sekaligus (max 100 produk per session)
- Tunggu 5-10 menit antara scraping sessions
- Jika gagal, coba keyword yang berbeda atau tunggu beberapa menit

⚠️ TROUBLESHOOTING:
- Jika Chrome/ChromeDriver error, restart runtime dan jalankan ulang cell 2
- Jika import error, pastikan file advanced_shopee_scraper.py sudah diupload
- Jika scraping gagal, coba keyword yang berbeda atau kurangi jumlah produk
- Jika file tidak bisa didownload, coba refresh halaman dan jalankan ulang cell 8

🎯 CONTOH KEYWORD YANG BAIK:
- "laptop gaming asus"
- "smartphone samsung galaxy"
- "baju muslim wanita"
- "sepatu nike air max"
- "cabai rawit merah"
- "beras organik premium"
"""