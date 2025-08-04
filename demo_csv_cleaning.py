#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Demo pembersihan data dari file CSV
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

def demo_csv_cleaning():
    """Demo pembersihan data dari file CSV"""
    
    print("🎯 DEMO PEMBERSIHAN DATA DARI FILE CSV")
    print("=" * 60)
    
    try:
        # Baca file CSV
        print("📖 Membaca file CSV...")
        df = pd.read_csv('contoh_data_sebelum_bersih.csv')
        
        print("\n📊 DATA SEBELUM PEMBERSIHAN:")
        print("-" * 40)
        print(df.to_string(index=False))
        
        # Lakukan pembersihan
        print("\n🧹 MEMULAI PROSES PEMBERSIHAN...")
        cleaned_df = clean_dataframe_simple(df)
        
        print("\n📊 DATA SETELAH PEMBERSIHAN:")
        print("-" * 40)
        print(cleaned_df.to_string(index=False))
        
        # Simpan hasil ke file baru
        output_filename = 'contoh_data_setelah_bersih.csv'
        cleaned_df.to_csv(output_filename, index=False, encoding='utf-8-sig')
        print(f"\n💾 Data bersih disimpan ke: {output_filename}")
        
        # Tampilkan perbandingan
        print("\n📈 PERBANDINGAN SEBELUM DAN SESUDAH:")
        print("-" * 40)
        for i in range(len(df)):
            print(f"\nBaris {i+1}:")
            print(f"  Sebelum: {df.iloc[i].to_dict()}")
            print(f"  Sesudah: {cleaned_df.iloc[i].to_dict()}")
        
    except FileNotFoundError:
        print("❌ File 'contoh_data_sebelum_bersih.csv' tidak ditemukan!")
        print("💡 Pastikan file tersebut ada di direktori yang sama.")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n✅ DEMO SELESAI")
    print("=" * 60)

if __name__ == "__main__":
    demo_csv_cleaning()