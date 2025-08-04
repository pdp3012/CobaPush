#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Demo program untuk scraping berita Kompas dengan fungsi clean_dataframe yang sudah diperbaiki
"""

import pandas as pd
from scraping_kompas import scrape_kompas_news, clean_dataframe, save_to_csv

def demo_scraping():
    """Demo scraping dengan data yang sengaja dibuat bermasalah untuk menguji clean_dataframe"""
    
    print("🎯 DEMO SCRAPING KOMPAS DENGAN PEMBERSIHAN DATA")
    print("=" * 60)
    
    # Buat DataFrame dengan data yang bermasalah untuk menguji clean_dataframe
    print("\n📋 Membuat data contoh dengan masalah...")
    
    problematic_data = pd.DataFrame({
        'judul_berita': [
            'Berita Pertama',
            'Berita Kedua', 
            'Berita Ketiga',
            'Berita Keempat'
        ],
        'link_berita': [
            'https://kompas.com/berita1',  # ✅ Normal
            'Ini bukan link tapi teks',    # ❌ Bermasalah
            'https://kompas.com/berita3',  # ✅ Normal
            'https://kompas.com/berita4'   # ✅ Normal
        ],
        'tanggal_rilis': [
            '2024-01-15',                  # ✅ Normal
            '2024-01-16',                  # ✅ Normal
            'https://kompas.com/link-salah', # ❌ Bermasalah
            '2024-01-18'                   # ✅ Normal
        ],
        'detail_konten': [
            'Ini adalah konten berita pertama yang panjang dan informatif.',
            'Ini adalah konten berita kedua yang juga panjang dan informatif.',
            'Ini adalah konten berita ketiga yang seharusnya dipindah ke tanggal_rilis.',
            '2024-01-19 10:30 WIB'  # ❌ Bermasalah (tanggal di kolom konten)
        ]
    })
    
    print("Data sebelum pembersihan:")
    print(problematic_data)
    print("\n" + "="*60)
    
    # Terapkan fungsi clean_dataframe
    print("\n🛠️  Menerapkan fungsi clean_dataframe...")
    cleaned_data = clean_dataframe(problematic_data.copy())
    
    print("\nData setelah pembersihan:")
    print(cleaned_data)
    print("\n" + "="*60)
    
    # Analisis hasil
    print("\n📊 ANALISIS HASIL PEMBERSIHAN:")
    print("-" * 40)
    
    for idx, (before, after) in enumerate(zip(problematic_data.iterrows(), cleaned_data.iterrows())):
        print(f"\nBaris {idx}:")
        
        # Periksa perubahan di setiap kolom
        for col in ['judul_berita', 'link_berita', 'tanggal_rilis', 'detail_konten']:
            before_val = str(before[1][col]).strip()
            after_val = str(after[1][col]).strip()
            
            if before_val != after_val:
                print(f"  {col}: '{before_val[:30]}...' → '{after_val[:30]}...'")
            else:
                print(f"  {col}: Tidak berubah")
    
    # Simpan ke CSV untuk demonstrasi
    print("\n💾 Menyimpan hasil ke CSV...")
    filename = save_to_csv(cleaned_data, "demo_testing")
    
    if filename:
        print(f"✅ File berhasil disimpan: {filename}")
    
    print("\n🎉 Demo selesai!")
    print("=" * 60)

def demo_real_scraping():
    """Demo scraping real dengan keyword sederhana"""
    
    print("\n🌐 DEMO SCRAPING REAL KOMPAS")
    print("=" * 60)
    
    keyword = "teknologi"
    max_articles = 3
    
    print(f"🔍 Keyword: '{keyword}'")
    print(f"📊 Maksimal artikel: {max_articles}")
    
    try:
        # Lakukan scraping
        df_results = scrape_kompas_news(keyword, max_articles)
        
        if not df_results.empty:
            print(f"\n✅ Berhasil mengambil {len(df_results)} artikel")
            
            # Tampilkan preview
            print("\n📋 Preview hasil scraping:")
            print(df_results[['judul_berita', 'link_berita', 'tanggal_rilis']].head())
            
            # Simpan ke CSV
            filename = save_to_csv(df_results, keyword)
            if filename:
                print(f"\n💾 Data disimpan ke: {filename}")
        else:
            print("\n❌ Tidak ada data yang berhasil diambil")
            
    except Exception as e:
        print(f"\n❌ Error saat scraping: {e}")

if __name__ == "__main__":
    # Jalankan demo dengan data contoh
    demo_scraping()
    
    # Tanya user apakah ingin mencoba scraping real
    print("\n" + "="*60)
    response = input("\n🤔 Apakah Anda ingin mencoba scraping real? (y/n): ").strip().lower()
    
    if response in ['y', 'yes', 'ya']:
        demo_real_scraping()
    else:
        print("\n👋 Terima kasih telah mencoba demo!")