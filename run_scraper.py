#!/usr/bin/env python3
"""
Simple Runner untuk Shopee Scraper
Penggunaan: python run_scraper.py [keyword] [jumlah_produk]
"""

import sys
import argparse
from shopee_scraper import ShopeeScraper

def main():
    parser = argparse.ArgumentParser(description='Shopee Product Scraper')
    parser.add_argument('keyword', help='Keyword produk yang ingin dicari')
    parser.add_argument('-n', '--num_products', type=int, default=50, 
                       help='Jumlah maksimal produk (default: 50)')
    parser.add_argument('--no-login', action='store_true',
                       help='Skip login otomatis, langsung manual')
    
    args = parser.parse_args()
    
    print("🚀 Shopee Product Scraper")
    print(f"🔍 Keyword: {args.keyword}")
    print(f"📦 Max Products: {args.num_products}")
    print("=" * 50)
    
    scraper = ShopeeScraper()
    
    try:
        if args.no_login:
            print("🔐 Menggunakan login manual...")
            scraper.manual_login()
        else:
            print("🔐 Mencoba login otomatis...")
            login_success = scraper.automated_login("081316084860", "Pradipta301203")
            if not login_success:
                print("🔐 Login otomatis gagal, beralih ke manual...")
                scraper.manual_login()
        
        # Mulai scraping
        products = scraper.scrape_products(args.keyword, args.num_products)
        
        if products:
            # Simpan data
            filename_base = f"shopee_{args.keyword.replace(' ', '_')}"
            scraper.save_to_csv(products, f"{filename_base}.csv")
            scraper.save_to_json(products, f"{filename_base}.json")
            
            print(f"\n✅ Berhasil scrape {len(products)} produk")
            print(f"💾 Data tersimpan di: {filename_base}.csv dan {filename_base}.json")
        else:
            print("❌ Tidak ada produk yang ditemukan")
            
    except KeyboardInterrupt:
        print("\n⏹️ Scraping dihentikan oleh user")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    finally:
        scraper.close()

if __name__ == "__main__":
    main()