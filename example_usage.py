#!/usr/bin/env python3
"""
Contoh Penggunaan Shopee Scraper
Berbagai cara menggunakan scraper untuk kebutuhan berbeda
"""

from shopee_scraper import ShopeeScraper
import time

def example_basic_usage():
    """Contoh penggunaan dasar"""
    print("📚 Contoh 1: Penggunaan Dasar")
    print("-" * 40)
    
    scraper = ShopeeScraper()
    
    try:
        # Scrape produk laptop
        products = scraper.scrape_products("laptop", max_products=10)
        
        if products:
            print(f"✅ Berhasil scrape {len(products)} produk laptop")
            
            # Tampilkan 3 produk pertama
            for i, product in enumerate(products[:3]):
                print(f"\nProduk {i+1}:")
                print(f"  Nama: {product['nama_produk']}")
                print(f"  Harga: {product['harga']}")
                print(f"  Terjual: {product['jumlah_terjual']}")
                print(f"  Toko: {product['nama_toko']}")
                print(f"  Lokasi: {product['lokasi_toko']}")
                print(f"  Rating: {product['rating_produk']}")
        else:
            print("❌ Tidak ada produk yang ditemukan")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    finally:
        scraper.close()

def example_multiple_keywords():
    """Contoh scraping multiple keywords"""
    print("\n📚 Contoh 2: Multiple Keywords")
    print("-" * 40)
    
    keywords = ["smartphone", "headphone", "laptop"]
    all_products = {}
    
    scraper = ShopeeScraper()
    
    try:
        for keyword in keywords:
            print(f"🔍 Scraping keyword: {keyword}")
            products = scraper.scrape_products(keyword, max_products=5)
            all_products[keyword] = products
            print(f"✅ Ditemukan {len(products)} produk untuk '{keyword}'")
            time.sleep(2)  # Delay antar keyword
            
        # Simpan semua data
        for keyword, products in all_products.items():
            if products:
                filename = f"shopee_{keyword}.csv"
                scraper.save_to_csv(products, filename)
                print(f"💾 Data '{keyword}' tersimpan di {filename}")
                
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    finally:
        scraper.close()

def example_custom_extraction():
    """Contoh ekstraksi data custom"""
    print("\n📚 Contoh 3: Ekstraksi Data Custom")
    print("-" * 40)
    
    scraper = ShopeeScraper()
    
    try:
        # Scrape produk dengan jumlah besar
        products = scraper.scrape_products("gaming", max_products=20)
        
        if products:
            # Analisis data
            total_products = len(products)
            products_with_rating = [p for p in products if p['rating_produk'] != "Tidak ditemukan"]
            products_with_location = [p for p in products if p['lokasi_toko'] != "Tidak ditemukan"]
            
            print(f"📊 Analisis Data Gaming Products:")
            print(f"  Total produk: {total_products}")
            print(f"  Produk dengan rating: {len(products_with_rating)}")
            print(f"  Produk dengan lokasi: {len(products_with_location)}")
            
            # Cari produk dengan rating tinggi
            high_rated = []
            for product in products:
                rating_text = product['rating_produk']
                if rating_text != "Tidak ditemukan":
                    try:
                        # Extract rating number
                        rating = float(rating_text.split()[0])
                        if rating >= 4.5:
                            high_rated.append(product)
                    except:
                        continue
            
            print(f"  Produk rating tinggi (≥4.5): {len(high_rated)}")
            
            # Simpan produk rating tinggi
            if high_rated:
                scraper.save_to_csv(high_rated, "high_rated_gaming_products.csv")
                print("💾 Produk rating tinggi tersimpan di high_rated_gaming_products.csv")
                
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    finally:
        scraper.close()

def example_batch_processing():
    """Contoh batch processing untuk data besar"""
    print("\n📚 Contoh 4: Batch Processing")
    print("-" * 40)
    
    # List keyword untuk batch processing
    keywords = [
        "smartphone samsung",
        "smartphone iphone", 
        "smartphone xiaomi",
        "smartphone oppo",
        "smartphone vivo"
    ]
    
    scraper = ShopeeScraper()
    
    try:
        # Login sekali untuk semua keyword
        login_success = scraper.automated_login("081316084860", "Pradipta301203")
        if not login_success:
            scraper.manual_login()
        
        all_results = {}
        
        for i, keyword in enumerate(keywords, 1):
            print(f"🔄 Processing {i}/{len(keywords)}: {keyword}")
            
            try:
                products = scraper.scrape_products(keyword, max_products=10)
                all_results[keyword] = products
                print(f"✅ {len(products)} produk ditemukan")
                
            except Exception as e:
                print(f"❌ Error untuk keyword '{keyword}': {str(e)}")
                all_results[keyword] = []
            
            # Delay antar request
            if i < len(keywords):
                print("⏳ Menunggu 3 detik...")
                time.sleep(3)
        
        # Simpan semua hasil
        print("\n💾 Menyimpan semua hasil...")
        for keyword, products in all_results.items():
            if products:
                filename = f"batch_{keyword.replace(' ', '_')}.csv"
                scraper.save_to_csv(products, filename)
                print(f"  ✅ {filename}")
        
        # Summary
        total_products = sum(len(products) for products in all_results.values())
        print(f"\n📊 Total produk yang di-scrape: {total_products}")
        
    except Exception as e:
        print(f"❌ Error dalam batch processing: {str(e)}")
    finally:
        scraper.close()

def example_data_analysis():
    """Contoh analisis data hasil scraping"""
    print("\n📚 Contoh 5: Analisis Data")
    print("-" * 40)
    
    scraper = ShopeeScraper()
    
    try:
        # Scrape data untuk analisis
        products = scraper.scrape_products("laptop gaming", max_products=30)
        
        if products:
            print("📈 Analisis Data Laptop Gaming:")
            
            # Analisis harga
            prices = []
            for product in products:
                price_text = product['harga']
                if price_text != "Tidak ditemukan":
                    try:
                        # Extract angka dari harga
                        price_str = ''.join(filter(str.isdigit, price_text))
                        if price_str:
                            prices.append(int(price_str))
                    except:
                        continue
            
            if prices:
                avg_price = sum(prices) / len(prices)
                min_price = min(prices)
                max_price = max(prices)
                
                print(f"  💰 Analisis Harga:")
                print(f"    Rata-rata: Rp {avg_price:,.0f}")
                print(f"    Minimum: Rp {min_price:,.0f}")
                print(f"    Maximum: Rp {max_price:,.0f}")
                print(f"    Total produk: {len(prices)}")
            
            # Analisis lokasi
            locations = {}
            for product in products:
                location = product['lokasi_toko']
                if location != "Tidak ditemukan":
                    locations[location] = locations.get(location, 0) + 1
            
            if locations:
                print(f"\n  📍 Top Lokasi Toko:")
                sorted_locations = sorted(locations.items(), key=lambda x: x[1], reverse=True)
                for location, count in sorted_locations[:5]:
                    print(f"    {location}: {count} produk")
            
            # Analisis rating
            ratings = []
            for product in products:
                rating_text = product['rating_produk']
                if rating_text != "Tidak ditemukan":
                    try:
                        rating = float(rating_text.split()[0])
                        ratings.append(rating)
                    except:
                        continue
            
            if ratings:
                avg_rating = sum(ratings) / len(ratings)
                print(f"\n  ⭐ Analisis Rating:")
                print(f"    Rata-rata rating: {avg_rating:.2f}")
                print(f"    Rating tertinggi: {max(ratings):.1f}")
                print(f"    Rating terendah: {min(ratings):.1f}")
                
    except Exception as e:
        print(f"❌ Error dalam analisis: {str(e)}")
    finally:
        scraper.close()

def main():
    """Fungsi utama untuk menjalankan semua contoh"""
    print("🚀 CONTOH PENGGUNAAN SHOPEE SCRAPER")
    print("=" * 60)
    
    examples = [
        ("Penggunaan Dasar", example_basic_usage),
        ("Multiple Keywords", example_multiple_keywords),
        ("Ekstraksi Custom", example_custom_extraction),
        ("Batch Processing", example_batch_processing),
        ("Analisis Data", example_data_analysis)
    ]
    
    for i, (name, func) in enumerate(examples, 1):
        print(f"\n{i}. {name}")
        try:
            func()
        except KeyboardInterrupt:
            print("\n⏹️ Dihentikan oleh user")
            break
        except Exception as e:
            print(f"❌ Error dalam contoh {i}: {str(e)}")
        
        if i < len(examples):
            print("\n" + "="*60)
            input("Tekan Enter untuk melanjutkan ke contoh berikutnya...")
    
    print("\n🎉 Semua contoh selesai!")

if __name__ == "__main__":
    main()