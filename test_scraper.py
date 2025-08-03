#!/usr/bin/env python3
"""
Test Script untuk Shopee Scraper
Dibuat untuk testing dan debugging
"""

import time
import json
from shopee_scraper import ShopeeScraper

def test_login():
    """Test fungsi login"""
    print("🧪 Testing Login Functionality...")
    scraper = ShopeeScraper()
    
    try:
        # Test login otomatis
        success = scraper.automated_login("081316084860", "Pradipta301203")
        print(f"Login otomatis: {'✅ Berhasil' if success else '❌ Gagal'}")
        
        if not success:
            print("Mencoba login manual...")
            scraper.manual_login()
            
        return True
        
    except Exception as e:
        print(f"❌ Error dalam test login: {str(e)}")
        return False
    finally:
        scraper.close()

def test_css_selectors():
    """Test CSS selector dengan data dummy"""
    print("\n🧪 Testing CSS Selectors...")
    
    # HTML dummy untuk testing
    dummy_html = """
    <div data-sqe="link">
        <div class="line-clamp-2">Laptop Gaming Asus ROG Strix G15</div>
        <span class="font-medium text-base/5 truncate">Rp 15.000.000</span>
        <div class="truncate text-shopee-black87 text-xs min-h-4">Terjual 1rb+</div>
        <div class="flex-shrink min-w-0 truncate text-shopee-black54">Jakarta</div>
        <div class="text-shopee-black87 text-xs/sp14 flex-none">4.8 (2.5rb ulasan)</div>
    </div>
    """
    
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(dummy_html, 'html.parser')
    card = soup.find('div', {'data-sqe': 'link'})
    
    scraper = ShopeeScraper()
    result = scraper.extract_product_data(card)
    
    if result:
        print("✅ CSS Selector berfungsi dengan baik:")
        for key, value in result.items():
            print(f"  {key}: {value}")
    else:
        print("❌ CSS Selector gagal mengekstrak data")
        
    scraper.close()

def test_small_scrape():
    """Test scraping dengan jumlah kecil"""
    print("\n🧪 Testing Small Scrape...")
    
    scraper = ShopeeScraper()
    
    try:
        # Test dengan keyword sederhana
        keyword = "laptop"
        products = scraper.scrape_products(keyword, max_products=5)
        
        if products:
            print(f"✅ Berhasil scrape {len(products)} produk")
            print("\n📋 Sample data:")
            for i, product in enumerate(products[:2]):
                print(f"\nProduk {i+1}:")
                for key, value in product.items():
                    print(f"  {key}: {value}")
        else:
            print("❌ Tidak ada produk yang ditemukan")
            
    except Exception as e:
        print(f"❌ Error dalam test scrape: {str(e)}")
    finally:
        scraper.close()

def test_data_export():
    """Test export data ke file"""
    print("\n🧪 Testing Data Export...")
    
    # Data dummy untuk testing
    dummy_data = [
        {
            'nama_produk': 'Laptop Gaming Asus ROG',
            'harga': 'Rp 15.000.000',
            'jumlah_terjual': 'Terjual 1rb+',
            'nama_toko': 'TechStore',
            'lokasi_toko': 'Jakarta',
            'rating_produk': '4.8 (2.5rb ulasan)'
        },
        {
            'nama_produk': 'Laptop Gaming MSI',
            'harga': 'Rp 18.000.000',
            'jumlah_terjual': 'Terjual 500+',
            'nama_toko': 'GamingStore',
            'lokasi_toko': 'Bandung',
            'rating_produk': '4.7 (1.2rb ulasan)'
        }
    ]
    
    scraper = ShopeeScraper()
    
    try:
        # Test export CSV
        scraper.save_to_csv(dummy_data, "test_export.csv")
        
        # Test export JSON
        scraper.save_to_json(dummy_data, "test_export.json")
        
        print("✅ Export data berhasil")
        
    except Exception as e:
        print(f"❌ Error dalam export: {str(e)}")
    finally:
        scraper.close()

def main():
    """Fungsi utama untuk testing"""
    print("🧪 SHOPEE SCRAPER TEST SUITE")
    print("=" * 50)
    
    tests = [
        ("CSS Selectors", test_css_selectors),
        ("Data Export", test_data_export),
        ("Small Scrape", test_small_scrape),
        ("Login Test", test_login)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        print(f"\n🔍 Running: {test_name}")
        try:
            start_time = time.time()
            success = test_func()
            end_time = time.time()
            
            results[test_name] = {
                'success': success,
                'duration': end_time - start_time
            }
            
            print(f"⏱️  Duration: {end_time - start_time:.2f}s")
            
        except Exception as e:
            print(f"❌ Test failed: {str(e)}")
            results[test_name] = {
                'success': False,
                'error': str(e)
            }
    
    # Print summary
    print("\n📊 TEST SUMMARY")
    print("=" * 50)
    
    passed = 0
    total = len(tests)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result.get('success') else "❌ FAIL"
        duration = f"{result.get('duration', 0):.2f}s" if 'duration' in result else "N/A"
        print(f"{test_name}: {status} ({duration})")
        
        if result.get('success'):
            passed += 1
    
    print(f"\n🎯 Overall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Scraper ready for production use.")
    else:
        print("⚠️  Some tests failed. Please check the issues above.")

if __name__ == "__main__":
    main()