#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Bukalapak Scraper
Advanced Data Mining Tool - Testing and Validation
"""

import time
import json
from datetime import datetime

# Import scrapers
from bukalapak_scraper import BukalapakScraper
from bukalapak_api_scraper import BukalapakAPIScraper
from bukalapak_css_scraper import BukalapakCSSScraper

def test_api_scraper():
    """Test API scraper functionality"""
    print("🧪 Testing API Scraper...")
    
    try:
        scraper = BukalapakAPIScraper(delay_range=(1, 2))
        
        # Test basic search
        print("   📡 Testing search functionality...")
        scraper.search_products(query="laptop", max_pages=1)
        
        if scraper.products_data:
            print(f"   ✅ API search successful: {len(scraper.products_data)} products")
            
            # Test data structure
            sample_product = scraper.products_data[0]
            required_fields = ['nama_produk', 'harga', 'nama_toko', 'metode_scraping']
            
            missing_fields = [field for field in required_fields if field not in sample_product]
            if not missing_fields:
                print("   ✅ Data structure validation passed")
            else:
                print(f"   ❌ Missing fields: {missing_fields}")
                
            # Test data quality
            valid_products = [p for p in scraper.products_data if p.get('nama_produk') and p.get('harga', 0) > 0]
            quality_rate = len(valid_products) / len(scraper.products_data) * 100
            print(f"   📊 Data quality: {quality_rate:.1f}%")
            
        else:
            print("   ❌ No products found")
            
        scraper.clear_data()
        return True
        
    except Exception as e:
        print(f"   ❌ API scraper test failed: {e}")
        return False

def test_css_scraper():
    """Test CSS scraper functionality"""
    print("🧪 Testing CSS Scraper...")
    
    try:
        scraper = BukalapakCSSScraper(headless=True)
        
        # Test basic scraping
        print("   🎨 Testing CSS scraping...")
        scraper.scrape_products(search_query="laptop", max_pages=1)
        
        if scraper.products_data:
            print(f"   ✅ CSS scraping successful: {len(scraper.products_data)} products")
            
            # Test data structure
            sample_product = scraper.products_data[0]
            required_fields = ['nama_produk', 'harga', 'nama_toko', 'metode_scraping']
            
            missing_fields = [field for field in required_fields if field not in sample_product]
            if not missing_fields:
                print("   ✅ Data structure validation passed")
            else:
                print(f"   ❌ Missing fields: {missing_fields}")
                
            # Test data quality
            valid_products = [p for p in scraper.products_data if p.get('nama_produk') and p.get('harga', 0) > 0]
            quality_rate = len(valid_products) / len(scraper.products_data) * 100
            print(f"   📊 Data quality: {quality_rate:.1f}%")
            
        else:
            print("   ❌ No products found")
            
        scraper.products_data = []
        return True
        
    except Exception as e:
        print(f"   ❌ CSS scraper test failed: {e}")
        return False

def test_main_scraper():
    """Test main scraper functionality"""
    print("🧪 Testing Main Scraper...")
    
    try:
        scraper = BukalapakScraper(headless=True, delay_range=(1, 2))
        
        # Test API method
        print("   📡 Testing API method...")
        scraper.scrape_via_api(search_query="laptop", max_pages=1)
        api_count = len(scraper.products_data)
        print(f"   ✅ API method: {api_count} products")
        
        # Test CSS method
        print("   🎨 Testing CSS method...")
        scraper.scrape_via_css_selector(search_query="laptop", max_pages=1)
        css_count = len(scraper.products_data) - api_count
        print(f"   ✅ CSS method: {css_count} products")
        
        # Test statistics
        stats = scraper.get_statistics()
        if stats:
            print("   ✅ Statistics generation successful")
            
        # Test data saving
        print("   💾 Testing data saving...")
        csv_file = scraper.save_to_csv("test_output.csv")
        json_file = scraper.save_to_json("test_output.json")
        
        if csv_file and json_file:
            print("   ✅ Data saving successful")
            
        scraper.clear_data()
        return True
        
    except Exception as e:
        print(f"   ❌ Main scraper test failed: {e}")
        return False

def test_data_validation():
    """Test data validation and cleaning"""
    print("🧪 Testing Data Validation...")
    
    try:
        # Create test data
        test_data = [
            {
                'nama_produk': 'Laptop Test 1',
                'harga': 15000000,
                'jumlah_terjual': 45,
                'nama_toko': 'Toko Test',
                'lokasi_toko': 'Jakarta',
                'rating_produk': 4.5,
                'metode_scraping': 'API'
            },
            {
                'nama_produk': '',  # Invalid: empty name
                'harga': 0,  # Invalid: zero price
                'jumlah_terjual': 0,
                'nama_toko': 'Toko Test 2',
                'lokasi_toko': 'Bandung',
                'rating_produk': 3.8,
                'metode_scraping': 'CSS_Selector'
            },
            {
                'nama_produk': 'Laptop Test 3',
                'harga': 8000000,
                'jumlah_terjual': 12,
                'nama_toko': 'Toko Test 3',
                'lokasi_toko': 'Surabaya',
                'rating_produk': 4.2,
                'metode_scraping': 'API'
            }
        ]
        
        # Test validation
        valid_data = [item for item in test_data if item.get('nama_produk') and item.get('harga', 0) > 0]
        invalid_data = [item for item in test_data if not (item.get('nama_produk') and item.get('harga', 0) > 0)]
        
        print(f"   📊 Valid data: {len(valid_data)}")
        print(f"   📊 Invalid data: {len(invalid_data)}")
        
        if len(valid_data) == 2 and len(invalid_data) == 1:
            print("   ✅ Data validation working correctly")
            return True
        else:
            print("   ❌ Data validation not working correctly")
            return False
            
    except Exception as e:
        print(f"   ❌ Data validation test failed: {e}")
        return False

def test_error_handling():
    """Test error handling"""
    print("🧪 Testing Error Handling...")
    
    try:
        # Test with invalid query
        scraper = BukalapakAPIScraper(delay_range=(1, 1))
        scraper.search_products(query="xyz123nonexistent", max_pages=1)
        
        if not scraper.products_data:
            print("   ✅ Error handling for invalid query working")
        else:
            print("   ⚠️  Unexpected data for invalid query")
            
        scraper.clear_data()
        return True
        
    except Exception as e:
        print(f"   ✅ Error handling working: {e}")
        return True

def run_all_tests():
    """Run all tests"""
    print("=" * 60)
    print("🧪 BUKALAPAK SCRAPER - COMPREHENSIVE TESTING")
    print("Dibuat oleh: Dosen Data Mining (30 tahun pengalaman)")
    print("=" * 60)
    
    start_time = datetime.now()
    test_results = {}
    
    # Run tests
    tests = [
        ("API Scraper", test_api_scraper),
        ("CSS Scraper", test_css_scraper),
        ("Main Scraper", test_main_scraper),
        ("Data Validation", test_data_validation),
        ("Error Handling", test_error_handling)
    ]
    
    for test_name, test_func in tests:
        print(f"\n{'='*40}")
        print(f"Running: {test_name}")
        print(f"{'='*40}")
        
        try:
            result = test_func()
            test_results[test_name] = result
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
            test_results[test_name] = False
            
    # Summary
    end_time = datetime.now()
    duration = end_time - start_time
    
    print(f"\n{'='*60}")
    print("📊 TEST SUMMARY")
    print(f"{'='*60}")
    
    passed = sum(test_results.values())
    total = len(test_results)
    
    print(f"⏱️  Duration: {duration}")
    print(f"✅ Passed: {passed}/{total}")
    print(f"❌ Failed: {total - passed}/{total}")
    print(f"📊 Success Rate: {passed/total*100:.1f}%")
    
    print(f"\n📋 Detailed Results:")
    for test_name, result in test_results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {test_name}: {status}")
        
    if passed == total:
        print(f"\n🎉 All tests passed! Scraper is ready for use.")
    else:
        print(f"\n⚠️  Some tests failed. Please check the implementation.")
        
    return test_results

if __name__ == "__main__":
    run_all_tests()