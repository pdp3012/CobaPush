#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script untuk fungsi clean_dataframe
"""

import pandas as pd
import re
from datetime import datetime

# Import fungsi clean_dataframe dari file utama
from scraping_kompas import clean_dataframe

def test_clean_dataframe():
    """Test fungsi clean_dataframe dengan berbagai skenario"""
    
    print("🧪 MULAI TESTING FUNGSI CLEAN_DATAFRAME")
    print("=" * 60)
    
    # Test Case 1: Data normal (tidak ada masalah)
    print("\n📋 TEST CASE 1: Data normal")
    print("-" * 30)
    
    df1 = pd.DataFrame({
        'judul_berita': ['Berita Pertama', 'Berita Kedua'],
        'link_berita': ['https://kompas.com/berita1', 'https://kompas.com/berita2'],
        'tanggal_rilis': ['2024-01-15', '2024-01-16'],
        'detail_konten': ['Ini adalah konten berita pertama yang panjang dan informatif.', 'Ini adalah konten berita kedua yang juga panjang dan informatif.']
    })
    
    print("Data sebelum pembersihan:")
    print(df1)
    
    cleaned_df1 = clean_dataframe(df1.copy())
    
    print("\nData setelah pembersihan:")
    print(cleaned_df1)
    
    # Test Case 2: link_berita bukan link (berisi teks)
    print("\n📋 TEST CASE 2: link_berita bukan link")
    print("-" * 30)
    
    df2 = pd.DataFrame({
        'judul_berita': ['Berita Ketiga'],
        'link_berita': ['Ini bukan link tapi teks'],
        'tanggal_rilis': ['2024-01-17'],
        'detail_konten': ['Ini adalah konten berita ketiga yang seharusnya dipindah ke tanggal_rilis.']
    })
    
    print("Data sebelum pembersihan:")
    print(df2)
    
    cleaned_df2 = clean_dataframe(df2.copy())
    
    print("\nData setelah pembersihan:")
    print(cleaned_df2)
    
    # Test Case 3: tanggal_rilis berisi link
    print("\n📋 TEST CASE 3: tanggal_rilis berisi link")
    print("-" * 30)
    
    df3 = pd.DataFrame({
        'judul_berita': ['Berita Keempat'],
        'link_berita': ['https://kompas.com/berita4'],
        'tanggal_rilis': ['https://kompas.com/link-salah'],
        'detail_konten': ['Ini adalah konten berita keempat yang seharusnya dipindah ke tanggal_rilis.']
    })
    
    print("Data sebelum pembersihan:")
    print(df3)
    
    cleaned_df3 = clean_dataframe(df3.copy())
    
    print("\nData setelah pembersihan:")
    print(cleaned_df3)
    
    # Test Case 4: detail_konten berisi tanggal
    print("\n📋 TEST CASE 4: detail_konten berisi tanggal")
    print("-" * 30)
    
    df4 = pd.DataFrame({
        'judul_berita': ['Berita Kelima'],
        'link_berita': ['https://kompas.com/berita5'],
        'tanggal_rilis': ['2024-01-18'],
        'detail_konten': ['2024-01-19 10:30 WIB']
    })
    
    print("Data sebelum pembersihan:")
    print(df4)
    
    cleaned_df4 = clean_dataframe(df4.copy())
    
    print("\nData setelah pembersihan:")
    print(cleaned_df4)
    
    # Test Case 5: Kombinasi masalah (link_berita bukan link + tanggal_rilis berisi link)
    print("\n📋 TEST CASE 5: Kombinasi masalah")
    print("-" * 30)
    
    df5 = pd.DataFrame({
        'judul_berita': ['Berita Keenam'],
        'link_berita': ['Ini bukan link'],
        'tanggal_rilis': ['https://kompas.com/link-salah-lagi'],
        'detail_konten': ['Ini adalah konten berita keenam yang seharusnya dipindah ke tanggal_rilis.']
    })
    
    print("Data sebelum pembersihan:")
    print(df5)
    
    cleaned_df5 = clean_dataframe(df5.copy())
    
    print("\nData setelah pembersihan:")
    print(cleaned_df5)
    
    # Test Case 6: Data kosong dan null
    print("\n📋 TEST CASE 6: Data kosong dan null")
    print("-" * 30)
    
    df6 = pd.DataFrame({
        'judul_berita': ['Berita Ketujuh', ''],
        'link_berita': ['', 'https://kompas.com/berita7'],
        'tanggal_rilis': ['2024-01-20', ''],
        'detail_konten': ['Ini adalah konten berita ketujuh.', '']
    })
    
    print("Data sebelum pembersihan:")
    print(df6)
    
    cleaned_df6 = clean_dataframe(df6.copy())
    
    print("\nData setelah pembersihan:")
    print(cleaned_df6)
    
    print("\n✅ SEMUA TEST CASE SELESAI")
    print("=" * 60)

if __name__ == "__main__":
    test_clean_dataframe()