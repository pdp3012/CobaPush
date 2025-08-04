#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script untuk fungsi clean_dataframe
"""

import pandas as pd
import re
from scraping_kompas import clean_dataframe

def test_clean_dataframe():
    """Test fungsi clean_dataframe dengan berbagai skenario"""
    
    print("🧪 MULAI TESTING FUNGSI CLEAN_DATAFRAME")
    print("=" * 60)
    
    # Test case 1: Data normal (tidak perlu perbaikan)
    print("\n📋 Test Case 1: Data normal")
    print("-" * 30)
    df1 = pd.DataFrame({
        'judul_berita': ['Berita Pertama', 'Berita Kedua'],
        'link_berita': ['https://kompas.com/berita1', 'https://kompas.com/berita2'],
        'tanggal_rilis': ['2024-01-15', '2024-01-16'],
        'detail_konten': ['Konten berita pertama yang panjang...', 'Konten berita kedua yang panjang...']
    })
    print("Data sebelum pembersihan:")
    print(df1)
    cleaned_df1 = clean_dataframe(df1)
    print("\nData setelah pembersihan:")
    print(cleaned_df1)
    
    # Test case 2: link_berita bukan URL
    print("\n📋 Test Case 2: link_berita bukan URL")
    print("-" * 30)
    df2 = pd.DataFrame({
        'judul_berita': ['Berita Ketiga'],
        'link_berita': ['Ini bukan URL, ini teks biasa'],
        'tanggal_rilis': ['2024-01-17'],
        'detail_konten': ['Konten berita ketiga yang panjang...']
    })
    print("Data sebelum pembersihan:")
    print(df2)
    cleaned_df2 = clean_dataframe(df2)
    print("\nData setelah pembersihan:")
    print(cleaned_df2)
    
    # Test case 3: tanggal_rilis berisi URL
    print("\n📋 Test Case 3: tanggal_rilis berisi URL")
    print("-" * 30)
    df3 = pd.DataFrame({
        'judul_berita': ['Berita Keempat'],
        'link_berita': ['https://kompas.com/berita4'],
        'tanggal_rilis': ['https://kompas.com/tanggal'],
        'detail_konten': ['Konten berita keempat yang panjang...']
    })
    print("Data sebelum pembersihan:")
    print(df3)
    cleaned_df3 = clean_dataframe(df3)
    print("\nData setelah pembersihan:")
    print(cleaned_df3)
    
    # Test case 4: detail_konten berisi tanggal
    print("\n📋 Test Case 4: detail_konten berisi tanggal")
    print("-" * 30)
    df4 = pd.DataFrame({
        'judul_berita': ['Berita Kelima'],
        'link_berita': ['https://kompas.com/berita5'],
        'tanggal_rilis': ['2024-01-18'],
        'detail_konten': ['15 Januari 2024']
    })
    print("Data sebelum pembersihan:")
    print(df4)
    cleaned_df4 = clean_dataframe(df4)
    print("\nData setelah pembersihan:")
    print(cleaned_df4)
    
    # Test case 5: Kombinasi masalah
    print("\n📋 Test Case 5: Kombinasi masalah")
    print("-" * 30)
    df5 = pd.DataFrame({
        'judul_berita': ['Berita Keenam'],
        'link_berita': ['Ini bukan URL'],
        'tanggal_rilis': ['https://kompas.com/tanggal'],
        'detail_konten': ['Konten berita keenam yang panjang...']
    })
    print("Data sebelum pembersihan:")
    print(df5)
    cleaned_df5 = clean_dataframe(df5)
    print("\nData setelah pembersihan:")
    print(cleaned_df5)
    
    # Test case 6: Data kosong
    print("\n📋 Test Case 6: Data kosong")
    print("-" * 30)
    df6 = pd.DataFrame({
        'judul_berita': [''],
        'link_berita': [''],
        'tanggal_rilis': [''],
        'detail_konten': ['']
    })
    print("Data sebelum pembersihan:")
    print(df6)
    cleaned_df6 = clean_dataframe(df6)
    print("\nData setelah pembersihan:")
    print(cleaned_df6)
    
    print("\n✅ SEMUA TEST SELESAI")
    print("=" * 60)

if __name__ == "__main__":
    test_clean_dataframe()