#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Demo fungsi clean_dataframe
"""

import pandas as pd
import re

def is_url(text):
    """Fungsi sederhana untuk mengecek apakah string adalah URL"""
    url_pattern = re.compile(
        r'^(?:http|ftp)s?://' # http:// atau https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' # domain...
        r'localhost|' # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...atau ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return bool(url_pattern.match(str(text).strip()))

def is_date_like(text):
    """Fungsi sederhana untuk mengecek apakah string mirip tanggal"""
    date_pattern = re.compile(
        r'(\d{4}[/-]\d{1,2}[/-]\d{1,2})|'           # 2020/12/31, 2020-12-31
        r'(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})|'         # 12/31/2020, 12-31-2020, 31/12/20
        r'(\d{1,2}\s+(?:Januari|Februari|Maret|April|Mei|Juni|Juli|Agustus|September|Oktober|November|Desember)\s+\d{2,4})|' # 1 Januari 2020
        r'(\d{1,2}:\d{2}(?::\d{2})?\s*(?:WIB|WITA|WIT)?)|' # 10:30 WIB, 14:20:15 WITA
        r'(\d{1,2}:\d{2}(?::\d{2})?\s*(?:AM|PM)?)',     # 10:30 AM, 2:20:15 PM
        re.IGNORECASE)
    return bool(date_pattern.search(str(text).strip()))

def clean_dataframe_simple(df):
    """
    Versi sederhana dari fungsi clean_dataframe untuk demo
    """
    print("🔍 Memulai pembersihan dan perbaikan DataFrame...")
    
    # Buat salinan DataFrame untuk menghindari modifikasi langsung
    df_cleaned = df.copy()
    
    for index, row in df_cleaned.iterrows():
        try:
            print(f"  🔍 Memproses baris {index}...")
            
            # --- Langkah 1: Periksa kolom link_berita ---
            if 'link_berita' in df_cleaned.columns:
                current_link = str(row.get('link_berita', '')).strip()
                if current_link and not is_url(current_link):
                    # Bukan link yang valid
                    print(f"    -> 'link_berita' bukan link: '{current_link[:50]}...'")
                    
                    # a. Gabungkan isi link_berita ke judul_berita
                    current_title = str(row.get('judul_berita', ''))
                    new_title = f"{current_title} {current_link}".strip()
                    df_cleaned.at[index, 'judul_berita'] = new_title
                    print(f"       a. Judul diperbarui: '{new_title[:50]}...'")
                    
                    # b. Geser data dari tanggal_rilis ke link_berita
                    current_date = str(row.get('tanggal_rilis', ''))
                    df_cleaned.at[index, 'link_berita'] = current_date
                    print(f"       b. link_berita diisi dengan data dari tanggal_rilis: '{current_date[:50]}...'")
                    
                    # c. Geser data dari detail_konten ke tanggal_rilis
                    current_content = str(row.get('detail_konten', ''))
                    df_cleaned.at[index, 'tanggal_rilis'] = current_content
                    print(f"       c. tanggal_rilis diisi dengan data dari detail_konten: '{current_content[:50]}...'")
                    
                    # d. Kosongkan detail_konten
                    df_cleaned.at[index, 'detail_konten'] = ""
                    print(f"       d. detail_konten dikosongkan.")
                    
            # --- Langkah 2: Periksa kolom tanggal_rilis (yang mungkin sudah digeser) ---
            if 'tanggal_rilis' in df_cleaned.columns:
                shifted_date = str(df_cleaned.at[index, 'tanggal_rilis']).strip() 
                if shifted_date and is_url(shifted_date):
                    # Isinya adalah link
                    print(f"    -> 'tanggal_rilis' berisi link: '{shifted_date[:50]}...'")
                    
                    # a. Geser data dari detail_konten ke tanggal_rilis
                    shifted_content_to_date = str(df_cleaned.at[index, 'detail_konten']).strip()
                    df_cleaned.at[index, 'tanggal_rilis'] = shifted_content_to_date
                    print(f"       a. tanggal_rilis diisi dengan data dari detail_konten: '{shifted_content_to_date[:50]}...'")
                    
                    # b. Kosongkan detail_konten
                    df_cleaned.at[index, 'detail_konten'] = ""
                    print(f"       b. detail_konten dikosongkan.")
                    
            # --- Langkah 3: Periksa kolom detail_konten (yang mungkin sudah digeser) ---
            if 'detail_konten' in df_cleaned.columns:
                shifted_content = str(df_cleaned.at[index, 'detail_konten']).strip()
                # Jika isinya pendek dan mirip tanggal, anggap bukan konten utuh
                if shifted_content and len(shifted_content) < 100 and is_date_like(shifted_content):
                    print(f"    -> 'detail_konten' mirip tanggal: '{shifted_content[:50]}...'")
                    df_cleaned.at[index, 'detail_konten'] = ""
                    print(f"       a. detail_konten dikosongkan.")
            
            # --- Langkah 4: Validasi akhir untuk memastikan data sudah benar ---
            # Periksa apakah link_berita sekarang berisi URL yang valid
            final_link = str(df_cleaned.at[index, 'link_berita']).strip()
            if final_link and not is_url(final_link):
                print(f"    ⚠️  Peringatan: 'link_berita' masih bukan URL yang valid: '{final_link[:50]}...'")
            
            # Periksa apakah tanggal_rilis berisi format tanggal yang masuk akal
            final_date = str(df_cleaned.at[index, 'tanggal_rilis']).strip()
            if final_date and is_url(final_date):
                print(f"    ⚠️  Peringatan: 'tanggal_rilis' masih berisi URL: '{final_date[:50]}...'")
                      
        except Exception as e:
            print(f"⚠️  Error saat memproses baris {index} dalam pembersihan: {e}")
            
    print("✅ Pembersihan dan perbaikan DataFrame selesai.")
    return df_cleaned

def demo_clean_dataframe():
    """Demo fungsi clean_dataframe dengan berbagai skenario"""
    
    print("🎯 DEMO FUNGSI CLEAN_DATAFRAME")
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
    cleaned_df1 = clean_dataframe_simple(df1)
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
    cleaned_df2 = clean_dataframe_simple(df2)
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
    cleaned_df3 = clean_dataframe_simple(df3)
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
    cleaned_df4 = clean_dataframe_simple(df4)
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
    cleaned_df5 = clean_dataframe_simple(df5)
    print("\nData setelah pembersihan:")
    print(cleaned_df5)
    
    print("\n✅ DEMO SELESAI")
    print("=" * 60)

if __name__ == "__main__":
    demo_clean_dataframe()