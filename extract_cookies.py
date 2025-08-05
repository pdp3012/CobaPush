"""
Cookie Extractor untuk Shopee
Script untuk mengekstrak cookies dari browser Chrome
"""

import json
import sqlite3
import os
import shutil
import tempfile
from datetime import datetime
import platform

def get_chrome_cookies_path():
    """Mendapatkan path ke file cookies Chrome berdasarkan OS"""
    system = platform.system()
    
    if system == "Windows":
        return os.path.expanduser("~\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Network\\Cookies")
    elif system == "Darwin":  # macOS
        return os.path.expanduser("~/Library/Application Support/Google/Chrome/Default/Cookies")
    else:  # Linux
        return os.path.expanduser("~/.config/google-chrome/Default/Cookies")

def extract_shopee_cookies():
    """Mengekstrak cookies Shopee dari Chrome"""
    try:
        # Path ke file cookies Chrome
        cookies_path = get_chrome_cookies_path()
        
        if not os.path.exists(cookies_path):
            print(f"❌ File cookies Chrome tidak ditemukan di: {cookies_path}")
            print("💡 Pastikan Chrome sudah terinstall dan pernah mengakses Shopee")
            return False
        
        # Buat temporary copy dari file cookies (karena Chrome mungkin sedang menggunakan file asli)
        temp_cookies_path = tempfile.mktemp()
        shutil.copy2(cookies_path, temp_cookies_path)
        
        # Connect ke database cookies
        conn = sqlite3.connect(temp_cookies_path)
        cursor = conn.cursor()
        
        # Query cookies Shopee
        cursor.execute("""
            SELECT name, value, host_key, path, expires_utc, is_secure, is_httponly
            FROM cookies 
            WHERE host_key LIKE '%shopee.co.id%'
        """)
        
        cookies = cursor.fetchall()
        conn.close()
        
        # Clean up temporary file
        os.remove(temp_cookies_path)
        
        if not cookies:
            print("❌ Tidak ada cookies Shopee ditemukan")
            print("💡 Pastikan Anda sudah login ke Shopee di Chrome")
            return False
        
        # Convert ke format yang sesuai
        shopee_cookies = []
        for cookie in cookies:
            name, value, host_key, path, expires_utc, is_secure, is_httponly = cookie
            
            # Convert expires_utc (microseconds since 1601) to Unix timestamp
            if expires_utc:
                # Chrome uses microseconds since 1601, convert to Unix timestamp
                expires_unix = (expires_utc / 1000000) - 11644473600
            else:
                expires_unix = None
            
            cookie_data = {
                "name": name,
                "value": value,
                "domain": host_key,
                "path": path,
                "expirationDate": int(expires_unix) if expires_unix else None,
                "secure": bool(is_secure),
                "httpOnly": bool(is_httponly),
                "sameSite": "Strict"
            }
            
            shopee_cookies.append(cookie_data)
        
        # Save ke file
        with open("cookies.json", "w", encoding="utf-8") as f:
            json.dump(shopee_cookies, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Berhasil mengekstrak {len(shopee_cookies)} cookies Shopee")
        print(f"📁 Cookies disimpan ke: cookies.json")
        
        # Show sample cookies
        print("\n📋 Sample cookies yang diekstrak:")
        for i, cookie in enumerate(shopee_cookies[:3]):
            print(f"  {i+1}. {cookie['name']}: {cookie['value'][:20]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Error mengekstrak cookies: {str(e)}")
        return False

def manual_cookies_setup():
    """Panduan manual untuk setup cookies"""
    print("\n📖 PANDUAN MANUAL SETUP COOKIES")
    print("="*50)
    print("Jika auto-extract gagal, ikuti langkah berikut:")
    print()
    print("1. Buka Chrome dan login ke Shopee.co.id")
    print("2. Tekan F12 untuk membuka Developer Tools")
    print("3. Pilih tab 'Application' atau 'Storage'")
    print("4. Di sidebar kiri, expand 'Cookies'")
    print("5. Klik 'https://shopee.co.id'")
    print("6. Copy semua cookies yang ada")
    print("7. Buat file 'cookies.json' dengan format:")
    print()
    print("""[
  {
    "name": "nama_cookie",
    "value": "nilai_cookie",
    "domain": ".shopee.co.id",
    "path": "/",
    "expirationDate": 1735689600,
    "sameSite": "Strict",
    "secure": true,
    "httpOnly": false
  }
]""")
    print()
    print("8. Simpan file di folder yang sama dengan scraper")

def main():
    """Main function"""
    print("🍪 SHOPEE COOKIE EXTRACTOR")
    print("="*50)
    print("Script untuk mengekstrak cookies Shopee dari Chrome")
    print("="*50)
    
    # Check if Chrome is running
    print("⚠️ Pastikan Chrome ditutup sebelum mengekstrak cookies")
    input("Tekan Enter untuk melanjutkan...")
    
    # Extract cookies
    success = extract_shopee_cookies()
    
    if not success:
        print("\n" + "="*50)
        manual_cookies_setup()
    
    print("\n" + "="*50)
    print("🎯 SELESAI!")
    print("Sekarang Anda bisa menjalankan scraper dengan:")
    print("python enhanced_shopee_scraper.py")

if __name__ == "__main__":
    main()