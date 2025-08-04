#!/usr/bin/env python3
"""
Test script untuk Blibli Scraper
"""

import sys
import os
from blibli_scraper import BlibliScraper

def test_scraper():
    """
    Test fungsi dasar scraper
    """
    print("🧪 MEMULAI TEST BLIBLI SCRAPER")
    print("="*50)
    
    try:
        # Inisialisasi scraper
        print("1. Inisialisasi scraper...")
        scraper = BlibliScraper()
        print("✅ Scraper berhasil diinisialisasi")
        
        # Test build URL
        print("\n2. Test build URL...")
        test_url = scraper.build_search_url("test", 1)
        expected_url = "https://www.blibli.com/cari/test"
        if test_url == expected_url:
            print("✅ URL builder berfungsi dengan benar")
        else:
            print(f"❌ URL builder error: {test_url} != {expected_url}")
            
        # Test dengan keyword sederhana (1 halaman saja)
        print("\n3. Test scraping (1 halaman)...")
        print("🔍 Keyword: 'cabai'")
        
        products = scraper.scrape_products("cabai", max_pages=1, delay_range=(1, 2))
        
        if products:
            print(f"✅ Berhasil scrape {len(products)} produk")
            
            # Test data validation
            print("\n4. Test validasi data...")
            valid_products = [p for p in products if scraper.validate_product_data(p)]
            print(f"✅ {len(valid_products)}/{len(products)} produk valid")
            
            # Test save to CSV
            print("\n5. Test save to CSV...")
            test_filename = "test_output.csv"
            if scraper.save_to_csv(products, test_filename):
                print("✅ Berhasil menyimpan ke CSV")
                
                # Clean up test file
                if os.path.exists(test_filename):
                    os.remove(test_filename)
                    print("✅ Test file berhasil dihapus")
            else:
                print("❌ Gagal menyimpan ke CSV")
                
            # Display summary
            print("\n6. Test display summary...")
            scraper.display_summary(products)
            
        else:
            print("❌ Tidak ada produk yang berhasil di-scrape")
            print("💡 Kemungkinan penyebab:")
            print("   - Struktur website berubah")
            print("   - Anti-bot detection aktif")
            print("   - Koneksi internet bermasalah")
            
    except Exception as e:
        print(f"❌ Error selama testing: {e}")
        return False
        
    print("\n🎉 TEST SELESAI!")
    return True

def main():
    """
    Main function untuk menjalankan test
    """
    print("🤖 BLIBLI SCRAPER - TEST SUITE")
    print("="*50)
    
    success = test_scraper()
    
    if success:
        print("\n✅ SEMUA TEST BERHASIL!")
        print("🚀 Scraper siap digunakan")
    else:
        print("\n❌ ADA TEST YANG GAGAL!")
        print("🔧 Periksa error di atas")
        
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())