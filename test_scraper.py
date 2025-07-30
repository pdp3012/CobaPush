#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Script untuk Shopee Scraper
================================

File ini digunakan untuk testing dan debugging scraper Shopee.
"""

import sys
import time
from shopee_scraper_advanced import AdvancedShopeeScraper

def test_api_method():
    """Test API method"""
    print("🧪 Testing API Method...")
    
    scraper = AdvancedShopeeScraper()
    
    # Test dengan keyword sederhana
    keyword = "laptop"
    limit = 5
    
    try:
        products = scraper.get_shopee_api_data_v2(keyword, limit)
        
        if products:
            print(f"✅ API method berhasil! Dapat {len(products)} produk")
            for i, product in enumerate(products[:2], 1):
                print(f"  {i}. {product['nama_produk']}")
                print(f"     💰 {product['harga']}")
                print(f"     ⭐ {product['rating']}")
        else:
            print("❌ API method gagal - tidak ada data")
            
    except Exception as e:
        print(f"❌ API method error: {str(e)}")

def test_selenium_method():
    """Test Selenium fallback method"""
    print("\n🧪 Testing Selenium Method...")
    
    scraper = AdvancedShopeeScraper()
    
    # Test dengan keyword sederhana
    keyword = "smartphone"
    limit = 3
    
    try:
        products = scraper.fallback_scraping_advanced(keyword, limit)
        
        if products:
            print(f"✅ Selenium method berhasil! Dapat {len(products)} produk")
            for i, product in enumerate(products[:2], 1):
                print(f"  {i}. {product['nama_produk']}")
                print(f"     💰 {product['harga']}")
                print(f"     ⭐ {product['rating']}")
        else:
            print("❌ Selenium method gagal - tidak ada data")
            
    except Exception as e:
        print(f"❌ Selenium method error: {str(e)}")

def test_driver_setup():
    """Test Chrome driver setup"""
    print("\n🧪 Testing Chrome Driver Setup...")
    
    scraper = AdvancedShopeeScraper()
    
    try:
        driver = scraper.setup_driver_advanced()
        print("✅ Chrome driver berhasil dibuat")
        
        # Test basic navigation
        driver.get("https://www.google.com")
        print("✅ Navigasi ke Google berhasil")
        
        title = driver.title
        print(f"✅ Page title: {title}")
        
        driver.quit()
        print("✅ Driver berhasil ditutup")
        
    except Exception as e:
        print(f"❌ Driver setup error: {str(e)}")

def test_session_setup():
    """Test session setup"""
    print("\n🧪 Testing Session Setup...")
    
    scraper = AdvancedShopeeScraper()
    
    try:
        # Test basic request
        response = scraper.session.get("https://shopee.co.id")
        
        if response.status_code == 200:
            print("✅ Session setup berhasil")
            print(f"✅ Response status: {response.status_code}")
            print(f"✅ Content length: {len(response.content)} bytes")
        else:
            print(f"❌ Session setup gagal - status: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Session setup error: {str(e)}")

def test_data_parsing():
    """Test data parsing"""
    print("\n🧪 Testing Data Parsing...")
    
    # Sample data
    sample_data = {
        "items": [
            {
                "item_basic": {
                    "name": "Test Product",
                    "price_min": 1000000,
                    "price_max": 1000000,
                    "item_rating": {
                        "rating_star": 4.5,
                        "rating_count": [10, 20, 30]
                    },
                    "historical_sold": 100,
                    "discount": 10
                },
                "shop_basic": {
                    "name": "Test Shop",
                    "shop_location": "Jakarta"
                }
            }
        ]
    }
    
    scraper = AdvancedShopeeScraper()
    
    try:
        products = scraper.parse_api_response_v2(sample_data, 1)
        
        if products:
            print("✅ Data parsing berhasil")
            product = products[0]
            print(f"  Nama: {product['nama_produk']}")
            print(f"  Harga: {product['harga']}")
            print(f"  Rating: {product['rating']}")
            print(f"  Terjual: {product['jumlah_terjual']}")
            print(f"  Toko: {product['nama_toko']}")
            print(f"  Lokasi: {product['lokasi_toko']}")
            print(f"  Diskon: {product['diskon']}")
        else:
            print("❌ Data parsing gagal")
            
    except Exception as e:
        print(f"❌ Data parsing error: {str(e)}")

def test_full_scraping():
    """Test full scraping process"""
    print("\n🧪 Testing Full Scraping Process...")
    
    scraper = AdvancedShopeeScraper()
    
    # Test dengan keyword yang pasti ada
    keyword = "laptop"
    limit = 5
    
    try:
        print(f"🚀 Memulai scraping '{keyword}' sebanyak {limit} produk...")
        start_time = time.time()
        
        products = scraper.scrape_products(keyword, limit)
        
        end_time = time.time()
        duration = end_time - start_time
        
        if products:
            print(f"✅ Full scraping berhasil!")
            print(f"   ⏱️  Durasi: {duration:.2f} detik")
            print(f"   📦 Total produk: {len(products)}")
            print(f"   🎯 Target: {limit}")
            
            # Show first product
            if products:
                product = products[0]
                print(f"\n📋 Sample produk:")
                print(f"   Nama: {product['nama_produk']}")
                print(f"   Harga: {product['harga']}")
                print(f"   Rating: {product['rating']}")
                print(f"   Terjual: {product['jumlah_terjual']}")
                print(f"   Toko: {product['nama_toko']}")
                print(f"   Lokasi: {product['lokasi_toko']}")
        else:
            print("❌ Full scraping gagal - tidak ada data")
            
    except Exception as e:
        print(f"❌ Full scraping error: {str(e)}")

def run_all_tests():
    """Run all tests"""
    print("🧪 SHOPEE SCRAPER - TESTING SUITE")
    print("=" * 50)
    
    tests = [
        test_session_setup,
        test_driver_setup,
        test_api_method,
        test_selenium_method,
        test_data_parsing,
        test_full_scraping
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"❌ Test {test.__name__} failed: {str(e)}")
            failed += 1
        
        time.sleep(1)  # Delay between tests
    
    print(f"\n📊 TEST RESULTS:")
    print(f"   ✅ Passed: {passed}")
    print(f"   ❌ Failed: {failed}")
    print(f"   📈 Success Rate: {(passed/(passed+failed)*100):.1f}%")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        test_name = sys.argv[1]
        
        if test_name == "api":
            test_api_method()
        elif test_name == "selenium":
            test_selenium_method()
        elif test_name == "driver":
            test_driver_setup()
        elif test_name == "session":
            test_session_setup()
        elif test_name == "parsing":
            test_data_parsing()
        elif test_name == "full":
            test_full_scraping()
        else:
            print("❌ Test tidak dikenal!")
            print("Available tests: api, selenium, driver, session, parsing, full")
    else:
        run_all_tests()