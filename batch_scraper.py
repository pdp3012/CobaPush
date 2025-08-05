"""
Batch Scraper untuk Shopee
Script untuk menjalankan scraping dengan multiple keywords
"""

import os
import time
import json
from datetime import datetime
from enhanced_shopee_scraper import ShopeeScraper

def load_config():
    """Load konfigurasi dari file config.json"""
    config_file = "config.json"
    
    if os.path.exists(config_file):
        with open(config_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        # Default config
        default_config = {
            "keywords": ["laptop", "smartphone", "headphone"],
            "max_pages_per_keyword": 3,
            "delay_between_keywords": 10,
            "output_directory": "hasil_scraping",
            "headless": True,
            "cookies_file": "cookies.json"
        }
        
        # Save default config
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(default_config, f, indent=2, ensure_ascii=False)
        
        print(f"📝 File config.json dibuat dengan konfigurasi default")
        return default_config

def create_output_directory(directory):
    """Membuat direktori output jika belum ada"""
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"📁 Direktori {directory} dibuat")

def run_batch_scraping():
    """Menjalankan batch scraping"""
    print("🔄 BATCH SHOPEE SCRAPER")
    print("="*50)
    print("Dikembangkan oleh: Dosen Data Mining (30 tahun pengalaman)")
    print("="*50)
    
    # Load config
    config = load_config()
    
    # Create output directory
    create_output_directory(config["output_directory"])
    
    # Initialize scraper
    scraper = ShopeeScraper(
        headless=config["headless"],
        cookies_file=config["cookies_file"]
    )
    
    total_keywords = len(config["keywords"])
    successful_scrapes = 0
    failed_scrapes = 0
    
    print(f"\n📋 Konfigurasi:")
    print(f"   - Keywords: {len(config['keywords'])}")
    print(f"   - Max pages per keyword: {config['max_pages_per_keyword']}")
    print(f"   - Output directory: {config['output_directory']}")
    print(f"   - Headless mode: {config['headless']}")
    
    print(f"\n🚀 Memulai batch scraping...")
    print("="*50)
    
    for i, keyword in enumerate(config["keywords"], 1):
        print(f"\n🔄 [{i}/{total_keywords}] Scraping keyword: '{keyword}'")
        
        # Generate output filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = os.path.join(
            config["output_directory"],
            f"shopee_{keyword}_{timestamp}.csv"
        )
        
        try:
            # Run scraping
            success = scraper.scrape_shopee(
                keyword=keyword,
                max_page=config["max_pages_per_keyword"],
                output_file=output_file
            )
            
            if success:
                successful_scrapes += 1
                print(f"✅ Berhasil scrape '{keyword}' -> {output_file}")
            else:
                failed_scrapes += 1
                print(f"❌ Gagal scrape '{keyword}'")
                
        except Exception as e:
            failed_scrapes += 1
            print(f"❌ Error scraping '{keyword}': {str(e)}")
        
        # Delay between keywords
        if i < total_keywords:
            delay = config["delay_between_keywords"]
            print(f"⏳ Menunggu {delay} detik sebelum keyword berikutnya...")
            time.sleep(delay)
    
    # Summary
    print("\n" + "="*50)
    print("📊 BATCH SCRAPING SUMMARY")
    print("="*50)
    print(f"✅ Berhasil: {successful_scrapes}/{total_keywords}")
    print(f"❌ Gagal: {failed_scrapes}/{total_keywords}")
    print(f"📁 Output directory: {config['output_directory']}")
    
    if successful_scrapes > 0:
        print(f"\n🎉 BATCH SCRAPING SELESAI!")
        print(f"📂 Cek hasil di folder: {config['output_directory']}")
    else:
        print(f"\n💥 SEMUA SCRAPING GAGAL!")
        print(f"📊 Cek file log: scraping.log untuk detail error")

def create_sample_config():
    """Membuat file config.json dengan contoh konfigurasi"""
    sample_config = {
        "keywords": [
            "laptop gaming",
            "smartphone android",
            "headphone wireless",
            "smartwatch",
            "camera digital"
        ],
        "max_pages_per_keyword": 2,
        "delay_between_keywords": 15,
        "output_directory": "hasil_scraping",
        "headless": True,
        "cookies_file": "cookies.json"
    }
    
    with open("config.json", "w", encoding="utf-8") as f:
        json.dump(sample_config, f, indent=2, ensure_ascii=False)
    
    print("📝 File config.json dibuat dengan contoh konfigurasi")
    print("✏️ Edit file config.json sesuai kebutuhan Anda")

def main():
    """Main function"""
    print("🔄 BATCH SHOPEE SCRAPER")
    print("="*50)
    
    # Check if config exists
    if not os.path.exists("config.json"):
        print("📝 File config.json tidak ditemukan")
        create_sample_config()
        print("\n💡 Edit config.json sesuai kebutuhan, lalu jalankan lagi script ini")
        return
    
    # Run batch scraping
    run_batch_scraping()

if __name__ == "__main__":
    main()