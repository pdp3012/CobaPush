"""
Test Script untuk Enhanced Shopee Scraper
Untuk testing dan validasi fungsi scraper
"""

import os
import sys
from enhanced_shopee_scraper import ShopeeScraper

def test_scraper_setup():
    """Test setup WebDriver"""
    print("🧪 Testing WebDriver Setup...")
    try:
        scraper = ShopeeScraper(headless=True)
        success = scraper.setup_driver()
        if success:
            print("✅ WebDriver setup berhasil")
            scraper.driver.quit()
            return True
        else:
            print("❌ WebDriver setup gagal")
            return False
    except Exception as e:
        print(f"❌ Error dalam setup: {str(e)}")
        return False

def test_cookies_loading():
    """Test loading cookies"""
    print("\n🧪 Testing Cookies Loading...")
    try:
        scraper = ShopeeScraper(headless=True)
        if scraper.setup_driver():
            success = scraper.load_cookies()
            scraper.driver.quit()
            if success:
                print("✅ Cookies loading berhasil")
                return True
            else:
                print("⚠️ Cookies loading gagal (mungkin file tidak ada)")
                return False
    except Exception as e:
        print(f"❌ Error dalam cookies loading: {str(e)}")
        return False

def test_small_scraping():
    """Test scraping dengan 1 halaman"""
    print("\n🧪 Testing Small Scraping (1 halaman)...")
    try:
        scraper = ShopeeScraper(headless=True)
        success = scraper.scrape_shopee(
            keyword="laptop",
            max_page=1,
            output_file="test_output.csv"
        )
        
        if success and os.path.exists("test_output.csv"):
            print("✅ Small scraping berhasil")
            # Clean up
            os.remove("test_output.csv")
            return True
        else:
            print("❌ Small scraping gagal")
            return False
    except Exception as e:
        print(f"❌ Error dalam small scraping: {str(e)}")
        return False

def main():
    """Main test function"""
    print("🧪 ENHANCED SHOPEE SCRAPER - TEST SUITE")
    print("="*50)
    
    tests = [
        ("WebDriver Setup", test_scraper_setup),
        ("Cookies Loading", test_cookies_loading),
        ("Small Scraping", test_small_scraping)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 Running: {test_name}")
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"❌ Test {test_name} error: {str(e)}")
    
    print("\n" + "="*50)
    print(f"📊 TEST RESULTS: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 SEMUA TEST BERHASIL! Scraper siap digunakan.")
    else:
        print("⚠️ Beberapa test gagal. Periksa konfigurasi sistem.")
    
    print("="*50)

if __name__ == "__main__":
    main()