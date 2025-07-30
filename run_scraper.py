#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Shopee Scraper Runner
=====================

Script sederhana untuk menjalankan Shopee scraper dengan mudah.
"""

import sys
import os

def main():
    """Main function untuk menjalankan scraper"""
    
    print("🛍️ SHOPEE PRODUCT SCRAPER")
    print("=" * 50)
    
    # Check if advanced scraper exists
    if os.path.exists("shopee_scraper_advanced.py"):
        from shopee_scraper_advanced import AdvancedShopeeScraper
        scraper_class = AdvancedShopeeScraper
        print("✅ Using Advanced Scraper")
    elif os.path.exists("shopee_scraper.py"):
        from shopee_scraper import ShopeeScraper
        scraper_class = ShopeeScraper
        print("✅ Using Basic Scraper")
    else:
        print("❌ Scraper file not found!")
        print("Please make sure shopee_scraper.py or shopee_scraper_advanced.py exists")
        return
    
    # Initialize scraper
    try:
        scraper = scraper_class()
        print("✅ Scraper initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize scraper: {str(e)}")
        return
    
    # Get user input
    print("\n📝 INPUT PARAMETERS:")
    print("-" * 30)
    
    keyword = input("🔍 Keyword produk: ").strip()
    if not keyword:
        print("❌ Keyword tidak boleh kosong!")
        return
    
    try:
        limit = int(input("📊 Jumlah data (1-100): "))
        if not (1 <= limit <= 100):
            print("❌ Jumlah data harus antara 1-100!")
            return
    except ValueError:
        print("❌ Jumlah data harus berupa angka!")
        return
    
    # File format choice
    print("\n📁 Pilih format output:")
    print("1. CSV (default)")
    print("2. Excel")
    choice = input("Pilihan (1/2): ").strip()
    
    # Start scraping
    print(f"\n🚀 Memulai scraping...")
    print(f"   Keyword: {keyword}")
    print(f"   Target: {limit} produk")
    print(f"   Format: {'Excel' if choice == '2' else 'CSV'}")
    print("-" * 50)
    
    try:
        products = scraper.scrape_products(keyword, limit)
        
        if products:
            # Display results
            scraper.display_results(products)
            
            # Save to file
            if choice == "2":
                filename = scraper.save_to_excel(products)
            else:
                filename = scraper.save_to_csv(products)
            
            print(f"\n✅ SCRAPING SELESAI!")
            print(f"📈 Total produk: {len(products)}")
            print(f"💾 File tersimpan: {filename}")
            
            # Show statistics
            print(f"\n📊 STATISTIK:")
            
            # Count shops
            shops = set(p['nama_toko'] for p in products if p['nama_toko'] != 'N/A')
            print(f"   🏪 Jumlah toko: {len(shops)}")
            
            # Count locations
            locations = set(p['lokasi_toko'] for p in products if p['lokasi_toko'] != 'N/A')
            print(f"   📍 Jumlah lokasi: {len(locations)}")
            
            # Price range
            prices = []
            for p in products:
                price_str = p['harga']
                if price_str != 'N/A':
                    # Extract first price number
                    import re
                    price_nums = re.findall(r'\d+', price_str.replace(',', ''))
                    if price_nums:
                        prices.append(int(price_nums[0]))
            
            if prices:
                min_price = min(prices)
                max_price = max(prices)
                avg_price = sum(prices) / len(prices)
                print(f"   💰 Harga terendah: Rp {min_price:,.0f}")
                print(f"   💰 Harga tertinggi: Rp {max_price:,.0f}")
                print(f"   💰 Rata-rata harga: Rp {avg_price:,.0f}")
            
        else:
            print("❌ Tidak ada data yang berhasil di-scrape!")
            print("\n💡 Tips:")
            print("   - Coba keyword yang berbeda")
            print("   - Periksa koneksi internet")
            print("   - Kurangi jumlah data")
            
    except KeyboardInterrupt:
        print("\n⏹️ Scraping dihentikan oleh user")
    except Exception as e:
        print(f"\n❌ Error during scraping: {str(e)}")
        print("\n💡 Tips troubleshooting:")
        print("   - Pastikan semua dependencies terinstall")
        print("   - Coba restart program")
        print("   - Periksa koneksi internet")

def quick_scrape():
    """Quick scrape dengan parameter default"""
    
    print("⚡ QUICK SCRAPE MODE")
    print("=" * 30)
    
    # Default parameters
    keyword = "laptop"
    limit = 10
    
    print(f"Keyword: {keyword}")
    print(f"Limit: {limit}")
    
    # Check scraper file
    if os.path.exists("shopee_scraper_advanced.py"):
        from shopee_scraper_advanced import AdvancedShopeeScraper
        scraper = AdvancedShopeeScraper()
    elif os.path.exists("shopee_scraper.py"):
        from shopee_scraper import ShopeeScraper
        scraper = ShopeeScraper()
    else:
        print("❌ Scraper file not found!")
        return
    
    try:
        print(f"\n🚀 Quick scraping '{keyword}'...")
        products = scraper.scrape_products(keyword, limit)
        
        if products:
            print(f"✅ Berhasil scrape {len(products)} produk")
            scraper.display_results(products)
            
            filename = scraper.save_to_csv(products)
            print(f"💾 Data tersimpan: {filename}")
        else:
            print("❌ Tidak ada data")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "quick":
            quick_scrape()
        else:
            print("Usage: python run_scraper.py [quick]")
    else:
        main()