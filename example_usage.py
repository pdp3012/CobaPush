#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Contoh Penggunaan Bukalapak Scraper
Advanced Data Mining Tool - Dosen Data Mining (30 tahun pengalaman)
"""

import time
import pandas as pd
from datetime import datetime

# Import scrapers
from bukalapak_scraper import BukalapakScraper
from bukalapak_api_scraper import BukalapakAPIScraper
from bukalapak_css_scraper import BukalapakCSSScraper

def print_header(title):
    """Print header yang menarik"""
    print("\n" + "="*60)
    print(f"🎯 {title}")
    print("="*60)

def print_section(title):
    """Print section header"""
    print(f"\n📋 {title}")
    print("-" * 40)

def save_with_timestamp(base_filename, data, save_func):
    """Save data dengan timestamp"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{base_filename}_{timestamp}"
    return save_func(filename)

def main():
    """Main function dengan berbagai contoh penggunaan"""
    
    print_header("BUKALAPAK SCRAPER - CONTOH PENGGUNAAN")
    print("Dibuat oleh: Dosen Data Mining (30 tahun pengalaman)")
    print("Sertifikasi: International Data Mining Certification")
    
    # Test queries
    test_queries = ["laptop", "smartphone", "headphone"]
    
    # ============================================================================
    # CONTOH 1: MAIN SCRAPER (Kombinasi API + CSS)
    # ============================================================================
    print_section("CONTOH 1: MAIN SCRAPER (Kombinasi API + CSS)")
    
    print("🚀 Inisialisasi Main Scraper...")
    main_scraper = BukalapakScraper(headless=True, delay_range=(2, 4))
    
    for query in test_queries[:1]:  # Test dengan 1 query saja
        print(f"\n🔍 Scraping untuk: {query}")
        
        # Scraping via API
        print("   📡 Scraping via API...")
        main_scraper.scrape_via_api(search_query=query, max_pages=1)
        
        # Scraping via CSS Selector
        print("   🎨 Scraping via CSS Selector...")
        main_scraper.scrape_via_css_selector(search_query=query, max_pages=1)
        
        # Save data
        print("   💾 Menyimpan data...")
        csv_file = save_with_timestamp(f"main_scraper_{query}", main_scraper.products_data, 
                                     lambda f: main_scraper.save_to_csv(f"{f}.csv"))
        json_file = save_with_timestamp(f"main_scraper_{query}", main_scraper.products_data,
                                      lambda f: main_scraper.save_to_json(f"{f}.json"))
        
        # Show statistics
        stats = main_scraper.get_statistics()
        print(f"\n   📊 Statistik untuk {query}:")
        for key, value in stats.items():
            print(f"      {key}: {value}")
            
        # Clear data
        main_scraper.clear_data()
        
    # ============================================================================
    # CONTOH 2: API SCRAPER (Hanya API)
    # ============================================================================
    print_section("CONTOH 2: API SCRAPER (Hanya API)")
    
    print("🚀 Inisialisasi API Scraper...")
    api_scraper = BukalapakAPIScraper(delay_range=(2, 4))
    
    for query in test_queries[:1]:
        print(f"\n🔍 API Scraping untuk: {query}")
        
        # Search products
        print("   🔎 Searching products...")
        api_scraper.search_products(query=query, max_pages=1)
        
        # Get trending products
        print("   📈 Getting trending products...")
        api_scraper.get_trending_products(max_pages=1)
        
        # Get recommendations
        print("   💡 Getting recommendations...")
        api_scraper.get_recommendations(max_pages=1)
        
        # Save data
        print("   💾 Menyimpan data...")
        csv_file = save_with_timestamp(f"api_scraper_{query}", api_scraper.products_data,
                                     lambda f: api_scraper.save_to_csv(f"{f}.csv"))
        json_file = save_with_timestamp(f"api_scraper_{query}", api_scraper.products_data,
                                      lambda f: api_scraper.save_to_json(f"{f}.json"))
        
        # Show statistics
        stats = api_scraper.get_statistics()
        print(f"\n   📊 Statistik API untuk {query}:")
        for key, value in stats.items():
            print(f"      {key}: {value}")
            
        # Clear data
        api_scraper.clear_data()
        
    # ============================================================================
    # CONTOH 3: CSS SELECTOR SCRAPER (Hanya CSS)
    # ============================================================================
    print_section("CONTOH 3: CSS SELECTOR SCRAPER (Hanya CSS)")
    
    print("🚀 Inisialisasi CSS Scraper...")
    css_scraper = BukalapakCSSScraper(headless=True)
    
    for query in test_queries[:1]:
        print(f"\n🔍 CSS Scraping untuk: {query}")
        
        # Scrape products
        print("   🎨 Scraping products dengan CSS Selector...")
        css_scraper.scrape_products(search_query=query, max_pages=1)
        
        # Save data
        print("   💾 Menyimpan data...")
        csv_file = save_with_timestamp(f"css_scraper_{query}", css_scraper.products_data,
                                     lambda f: css_scraper.save_to_csv(f"{f}.csv"))
        json_file = save_with_timestamp(f"css_scraper_{query}", css_scraper.products_data,
                                      lambda f: css_scraper.save_to_json(f"{f}.json"))
        
        # Show statistics
        stats = css_scraper.get_statistics()
        print(f"\n   📊 Statistik CSS untuk {query}:")
        for key, value in stats.items():
            print(f"      {key}: {value}")
            
        # Clear data
        css_scraper.products_data = []
        
    # ============================================================================
    # CONTOH 4: COMPARISON ANALYSIS
    # ============================================================================
    print_section("CONTOH 4: COMPARISON ANALYSIS")
    
    print("📊 Membandingkan hasil dari berbagai metode scraping...")
    
    # Collect data from all methods
    all_data = []
    
    # API data
    api_scraper = BukalapakAPIScraper(delay_range=(1, 2))
    api_scraper.search_products(query="laptop", max_pages=1)
    for item in api_scraper.products_data:
        item['metode'] = 'API'
        all_data.append(item)
    api_scraper.clear_data()
    
    # CSS data
    css_scraper = BukalapakCSSScraper(headless=True)
    css_scraper.scrape_products(search_query="laptop", max_pages=1)
    for item in css_scraper.products_data:
        item['metode'] = 'CSS_Selector'
        all_data.append(item)
    css_scraper.products_data = []
    
    # Create comparison DataFrame
    if all_data:
        df = pd.DataFrame(all_data)
        
        print(f"\n📈 Perbandingan Metode Scraping:")
        print(f"   Total produk: {len(df)}")
        print(f"   API method: {len(df[df['metode'] == 'API'])}")
        print(f"   CSS method: {len(df[df['metode'] == 'CSS_Selector'])}")
        
        # Price comparison
        if 'harga' in df.columns:
            api_prices = df[df['metode'] == 'API']['harga']
            css_prices = df[df['metode'] == 'CSS_Selector']['harga']
            
            print(f"\n💰 Perbandingan Harga:")
            print(f"   API - Rata-rata: {api_prices.mean():,.0f}")
            print(f"   CSS - Rata-rata: {css_prices.mean():,.0f}")
            print(f"   API - Min: {api_prices.min():,.0f}")
            print(f"   CSS - Min: {css_prices.min():,.0f}")
            print(f"   API - Max: {api_prices.max():,.0f}")
            print(f"   CSS - Max: {css_prices.max():,.0f}")
        
        # Save comparison
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        comparison_file = f"comparison_analysis_{timestamp}.csv"
        df.to_csv(comparison_file, index=False, encoding='utf-8')
        print(f"\n💾 Comparison data saved to: {comparison_file}")
        
    # ============================================================================
    # CONTOH 5: ADVANCED USAGE
    # ============================================================================
    print_section("CONTOH 5: ADVANCED USAGE")
    
    print("🔧 Contoh penggunaan lanjutan...")
    
    # Custom configuration
    print("\n⚙️  Custom Configuration:")
    print("   - Delay range: 3-7 seconds (lebih aman)")
    print("   - Headless mode: True")
    print("   - Max pages: 2")
    
    custom_scraper = BukalapakScraper(headless=True, delay_range=(3, 7))
    
    # Multiple queries with different strategies
    advanced_queries = ["gaming laptop", "ultrabook", "workstation"]
    
    for i, query in enumerate(advanced_queries):
        print(f"\n🎯 Advanced scraping {i+1}/3: {query}")
        
        # API scraping
        custom_scraper.scrape_via_api(search_query=query, max_pages=1)
        
        # CSS scraping
        custom_scraper.scrape_via_css_selector(search_query=query, max_pages=1)
        
        # Save with detailed naming
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"advanced_{query.replace(' ', '_')}_{timestamp}"
        custom_scraper.save_to_csv(f"{filename}.csv")
        
        # Show progress
        stats = custom_scraper.get_statistics()
        print(f"   ✅ Completed: {stats.get('total_products', 0)} products")
        
        # Clear for next query
        custom_scraper.clear_data()
        
    # ============================================================================
    # CONTOH 6: ERROR HANDLING
    # ============================================================================
    print_section("CONTOH 6: ERROR HANDLING")
    
    print("🛡️  Demonstrasi error handling...")
    
    try:
        # Test dengan query yang mungkin tidak ada hasil
        test_scraper = BukalapakAPIScraper(delay_range=(1, 2))
        test_scraper.search_products(query="xyz123nonexistent", max_pages=1)
        
        if test_scraper.products_data:
            print("   ⚠️  Unexpected: Found products for non-existent query")
        else:
            print("   ✅ Expected: No products found for non-existent query")
            
        test_scraper.clear_data()
        
    except Exception as e:
        print(f"   ❌ Error handled: {e}")
        
    # ============================================================================
    # SUMMARY
    # ============================================================================
    print_section("SUMMARY")
    
    print("🎉 Contoh penggunaan selesai!")
    print("\n📋 Yang telah didemonstrasikan:")
    print("   ✅ Main Scraper (API + CSS)")
    print("   ✅ API Scraper (hanya API)")
    print("   ✅ CSS Scraper (hanya CSS)")
    print("   ✅ Comparison Analysis")
    print("   ✅ Advanced Usage")
    print("   ✅ Error Handling")
    
    print("\n💡 Tips penggunaan:")
    print("   - Mulai dengan query sederhana")
    print("   - Monitor logs untuk error")
    print("   - Gunakan delay yang cukup")
    print("   - Validasi data yang di-scrape")
    print("   - Simpan data secara berkala")
    
    print("\n🔗 File yang dihasilkan:")
    print("   - CSV files dengan timestamp")
    print("   - JSON files dengan timestamp")
    print("   - Comparison analysis file")
    print("   - Log file: bukalapak_scraper.log")
    
    print_header("SELESAI - BUKALAPAK SCRAPER")
    print("Terima kasih telah menggunakan Advanced Data Mining Tool!")
    print("Dibuat dengan ❤️ oleh Dosen Data Mining (30 tahun pengalaman)")

if __name__ == "__main__":
    main()