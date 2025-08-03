#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple Bukalapak Scraper Runner
Advanced Data Mining Tool - Simple Execution Script
"""

import sys
from bukalapak_scraper import BukalapakScraper
from bukalapak_api_scraper import BukalapakAPIScraper
from bukalapak_css_scraper import BukalapakCSSScraper

def main():
    """Simple scraper runner"""
    print("=" * 60)
    print("BUKALAPAK SCRAPER - SIMPLE RUNNER")
    print("Dibuat oleh: Dosen Data Mining (30 tahun pengalaman)")
    print("=" * 60)
    
    # Get user input
    print("\nPilih metode scraping:")
    print("1. Main Scraper (API + CSS)")
    print("2. API Scraper (hanya API)")
    print("3. CSS Scraper (hanya CSS)")
    
    choice = input("\nMasukkan pilihan (1-3): ").strip()
    
    if choice not in ['1', '2', '3']:
        print("❌ Pilihan tidak valid!")
        return
        
    # Get search query
    query = input("Masukkan kata kunci pencarian: ").strip()
    if not query:
        query = "laptop"  # default query
        
    # Get number of pages
    try:
        max_pages = int(input("Masukkan jumlah halaman (default: 2): ").strip() or "2")
    except ValueError:
        max_pages = 2
        
    print(f"\n🚀 Memulai scraping untuk: {query}")
    print(f"📄 Jumlah halaman: {max_pages}")
    
    try:
        if choice == '1':
            # Main scraper
            scraper = BukalapakScraper(headless=True, delay_range=(2, 4))
            
            print("📡 Scraping via API...")
            scraper.scrape_via_api(search_query=query, max_pages=max_pages)
            
            print("🎨 Scraping via CSS Selector...")
            scraper.scrape_via_css_selector(search_query=query, max_pages=max_pages)
            
        elif choice == '2':
            # API scraper
            scraper = BukalapakAPIScraper(delay_range=(2, 4))
            scraper.search_products(query=query, max_pages=max_pages)
            
        elif choice == '3':
            # CSS scraper
            scraper = BukalapakCSSScraper(headless=True)
            scraper.scrape_products(search_query=query, max_pages=max_pages)
            
        # Save data
        print("💾 Menyimpan data...")
        csv_file = scraper.save_to_csv(f"bukalapak_{query}.csv")
        json_file = scraper.save_to_json(f"bukalapak_{query}.json")
        
        # Show statistics
        stats = scraper.get_statistics()
        print(f"\n📊 Statistik:")
        for key, value in stats.items():
            print(f"   {key}: {value}")
            
        print(f"\n✅ Scraping selesai!")
        print(f"📁 File tersimpan: {csv_file}, {json_file}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        
if __name__ == "__main__":
    main()