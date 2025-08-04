#!/usr/bin/env python3
"""
Contoh penggunaan Blibli Scraper
"""

from blibli_scraper import BlibliScraper
import time

def example_basic_usage():
    """
    Contoh penggunaan dasar
    """
    print("🚀 CONTOH PENGGUNAAN DASAR")
    print("="*40)
    
    # Inisialisasi scraper
    scraper = BlibliScraper()
    
    # Scrape produk dengan keyword "laptop"
    keyword = "laptop"
    max_pages = 2
    
    print(f"🔍 Mencari produk: '{keyword}'")
    print(f"📄 Jumlah halaman: {max_pages}")
    
    # Jalankan scraping
    products = scraper.scrape_products(keyword, max_pages, delay_range=(2, 4))
    
    if products:
        print(f"\n✅ Berhasil scrape {len(products)} produk")
        
        # Tampilkan ringkasan
        scraper.display_summary(products)
        
        # Simpan ke file
        filename = f"{keyword}_products.csv"
        if scraper.save_to_csv(products, filename):
            print(f"💾 Data disimpan ke: {filename}")
    else:
        print("❌ Tidak ada produk yang ditemukan")

def example_multiple_keywords():
    """
    Contoh scraping multiple keywords
    """
    print("\n🚀 CONTOH MULTIPLE KEYWORDS")
    print("="*40)
    
    scraper = BlibliScraper()
    
    keywords = ["smartphone", "headphone", "mouse"]
    all_products = []
    
    for keyword in keywords:
        print(f"\n🔍 Scraping: {keyword}")
        products = scraper.scrape_products(keyword, max_pages=1, delay_range=(3, 5))
        
        if products:
            all_products.extend(products)
            print(f"✅ {len(products)} produk ditemukan")
        else:
            print("❌ Tidak ada produk")
            
        # Delay antar keyword
        time.sleep(2)
    
    if all_products:
        print(f"\n📊 TOTAL: {len(all_products)} produk dari semua keyword")
        scraper.save_to_csv(all_products, "multiple_keywords_products.csv")

def example_custom_extraction():
    """
    Contoh ekstraksi data custom
    """
    print("\n🚀 CONTOH EKSTRAKSI CUSTOM")
    print("="*40)
    
    scraper = BlibliScraper()
    
    # Scrape produk
    products = scraper.scrape_products("buku", max_pages=1, delay_range=(2, 3))
    
    if products:
        print(f"📚 Ditemukan {len(products)} buku")
        
        # Filter produk berdasarkan harga (contoh: hanya yang ada kata "Rp")
        products_with_price = [p for p in products if "Rp" in p.get('harga', '')]
        print(f"💰 {len(products_with_price)} produk dengan harga")
        
        # Tampilkan produk dengan rating
        products_with_rating = [p for p in products if p.get('rating')]
        print(f"⭐ {len(products_with_rating)} produk dengan rating")
        
        # Simpan hanya produk dengan harga
        if products_with_price:
            scraper.save_to_csv(products_with_price, "books_with_price.csv")

def main():
    """
    Main function untuk menjalankan contoh
    """
    print("🤖 BLIBLI SCRAPER - CONTOH PENGGUNAAN")
    print("="*50)
    
    try:
        # Contoh 1: Penggunaan dasar
        example_basic_usage()
        
        # Contoh 2: Multiple keywords
        example_multiple_keywords()
        
        # Contoh 3: Custom extraction
        example_custom_extraction()
        
        print("\n🎉 SEMUA CONTOH SELESAI!")
        print("📁 Cek file CSV yang dihasilkan")
        
    except KeyboardInterrupt:
        print("\n⚠️  Program dihentikan oleh user")
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main()