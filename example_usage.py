#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Contoh Penggunaan Shopee Product Scraper
========================================

File ini berisi contoh penggunaan scraper Shopee untuk berbagai keyword.
"""

from shopee_scraper_advanced import AdvancedShopeeScraper
import time

def example_scraping():
    """Contoh penggunaan scraper dengan berbagai keyword"""
    
    # Initialize scraper
    scraper = AdvancedShopeeScraper()
    
    # List keyword yang ingin di-scrape
    keywords = [
        "laptop",
        "smartphone",
        "sepatu",
        "baju",
        "makanan"
    ]
    
    print("🚀 MULAI CONTOH SCRAPING")
    print("=" * 50)
    
    for keyword in keywords:
        print(f"\n📦 Scraping untuk keyword: '{keyword}'")
        print("-" * 30)
        
        try:
            # Scrape 10 produk untuk setiap keyword
            products = scraper.scrape_products(keyword, 10)
            
            if products:
                print(f"✅ Berhasil scrape {len(products)} produk")
                
                # Tampilkan 3 produk pertama sebagai contoh
                for i, product in enumerate(products[:3], 1):
                    print(f"  {i}. {product['nama_produk']}")
                    print(f"     💰 {product['harga']}")
                    print(f"     ⭐ {product['rating']}")
                    print(f"     📦 Terjual: {product['jumlah_terjual']}")
                    print(f"     🏪 {product['nama_toko']}")
                    print()
                
                # Save to CSV
                filename = scraper.save_to_csv(products, f"shopee_{keyword}.csv")
                print(f"💾 Data tersimpan di: {filename}")
                
            else:
                print("❌ Tidak ada data yang ditemukan")
                
        except Exception as e:
            print(f"❌ Error: {str(e)}")
        
        # Delay antara scraping untuk menghindari rate limiting
        time.sleep(2)
    
    print("\n🎉 CONTOH SCRAPING SELESAI!")

def single_keyword_scraping():
    """Contoh scraping untuk satu keyword dengan jumlah besar"""
    
    scraper = AdvancedShopeeScraper()
    
    keyword = "cabai rawit"
    limit = 50
    
    print(f"🚀 Scraping '{keyword}' sebanyak {limit} produk")
    print("=" * 50)
    
    products = scraper.scrape_products(keyword, limit)
    
    if products:
        # Display results
        scraper.display_results(products)
        
        # Save to Excel
        filename = scraper.save_to_excel(products, f"shopee_{keyword.replace(' ', '_')}.xlsx")
        print(f"\n💾 Data tersimpan di: {filename}")
        
        # Show statistics
        print(f"\n📊 STATISTIK:")
        print(f"   Total produk: {len(products)}")
        
        # Calculate average price
        prices = []
        for product in products:
            price_str = product['harga']
            if price_str != 'N/A':
                # Extract numeric price
                price_nums = [int(s) for s in price_str.split() if s.replace(',', '').isdigit()]
                if price_nums:
                    prices.append(price_nums[0])
        
        if prices:
            avg_price = sum(prices) / len(prices)
            print(f"   Rata-rata harga: Rp {avg_price:,.0f}")
        
        # Count shops
        shops = set(product['nama_toko'] for product in products if product['nama_toko'] != 'N/A')
        print(f"   Jumlah toko: {len(shops)}")
        
    else:
        print("❌ Tidak ada data yang ditemukan")

def custom_scraping():
    """Contoh scraping dengan parameter custom"""
    
    scraper = AdvancedShopeeScraper()
    
    # Custom parameters
    keyword = input("🔍 Masukkan keyword: ").strip()
    limit = int(input("📊 Jumlah produk (max 100): "))
    format_choice = input("📁 Format file (csv/excel): ").strip().lower()
    
    print(f"\n🚀 Memulai scraping...")
    products = scraper.scrape_products(keyword, limit)
    
    if products:
        scraper.display_results(products)
        
        if format_choice == 'excel':
            filename = scraper.save_to_excel(products)
        else:
            filename = scraper.save_to_csv(products)
        
        print(f"\n✅ Selesai! File: {filename}")
    else:
        print("❌ Tidak ada data")

if __name__ == "__main__":
    print("🛍️ SHOPEE SCRAPER - CONTOH PENGGUNAAN")
    print("=" * 50)
    print("1. Contoh scraping multiple keywords")
    print("2. Single keyword dengan statistik")
    print("3. Custom scraping")
    
    choice = input("\nPilih contoh (1/2/3): ").strip()
    
    if choice == "1":
        example_scraping()
    elif choice == "2":
        single_keyword_scraping()
    elif choice == "3":
        custom_scraping()
    else:
        print("❌ Pilihan tidak valid!")