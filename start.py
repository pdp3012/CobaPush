#!/usr/bin/env python3
"""
Launcher untuk Shopee Scraper
Menu sederhana untuk menjalankan berbagai komponen scraper
"""

import os
import sys
import subprocess
import tkinter as tk
from tkinter import messagebox

def clear_screen():
    """Clear terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def show_menu():
    """Tampilkan menu utama"""
    clear_screen()
    print("🚀 SHOPEE PRODUCT SCRAPER - DATA MINING EXPERT")
    print("=" * 60)
    print("Dibuat oleh: Dosen Data Mining dengan 30 tahun pengalaman")
    print("=" * 60)
    print()
    print("📋 PILIHAN MENU:")
    print("1. 🖥️  GUI Application (Paling Mudah)")
    print("2. 💻 Command Line Scraper")
    print("3. 🔧 Script Utama (Interactive)")
    print("4. 🧪 Test Scraper")
    print("5. 📚 Contoh Penggunaan")
    print("6. 📖 Baca Dokumentasi")
    print("7. ⚙️  Install Dependencies")
    print("8. ❌ Keluar")
    print()
    print("=" * 60)

def run_gui():
    """Jalankan GUI application"""
    print("🖥️  Menjalankan GUI Application...")
    try:
        subprocess.run([sys.executable, "gui_scraper.py"])
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        input("Tekan Enter untuk kembali ke menu...")

def run_command_line():
    """Jalankan command line scraper"""
    print("💻 Command Line Scraper")
    print("-" * 40)
    print("Contoh penggunaan:")
    print("  python run_scraper.py 'laptop' -n 20")
    print("  python run_scraper.py 'smartphone' --no-login")
    print()
    
    keyword = input("Masukkan keyword (atau Enter untuk 'laptop'): ").strip()
    if not keyword:
        keyword = "laptop"
    
    num_products = input("Jumlah produk (atau Enter untuk 20): ").strip()
    if not num_products:
        num_products = "20"
    
    try:
        cmd = [sys.executable, "run_scraper.py", keyword, "-n", num_products]
        print(f"🚀 Menjalankan: {' '.join(cmd)}")
        subprocess.run(cmd)
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    input("Tekan Enter untuk kembali ke menu...")

def run_main_script():
    """Jalankan script utama"""
    print("🔧 Menjalankan Script Utama...")
    try:
        subprocess.run([sys.executable, "shopee_scraper.py"])
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        input("Tekan Enter untuk kembali ke menu...")

def run_test():
    """Jalankan test scraper"""
    print("🧪 Menjalankan Test Scraper...")
    try:
        subprocess.run([sys.executable, "test_scraper.py"])
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        input("Tekan Enter untuk kembali ke menu...")

def run_examples():
    """Jalankan contoh penggunaan"""
    print("📚 Menjalankan Contoh Penggunaan...")
    try:
        subprocess.run([sys.executable, "example_usage.py"])
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        input("Tekan Enter untuk kembali ke menu...")

def show_documentation():
    """Tampilkan dokumentasi"""
    clear_screen()
    print("📖 DOKUMENTASI SHOPEE SCRAPER")
    print("=" * 60)
    print()
    print("📁 File Dokumentasi:")
    print("  • README.md - Dokumentasi lengkap")
    print("  • CARA_PENGGUNAAN.md - Panduan penggunaan")
    print("  • config.py - Konfigurasi detail")
    print()
    print("📋 File Script:")
    print("  • shopee_scraper.py - Script utama")
    print("  • gui_scraper.py - GUI application")
    print("  • run_scraper.py - Command line interface")
    print("  • test_scraper.py - Testing suite")
    print("  • example_usage.py - Contoh penggunaan")
    print()
    print("🔧 Cara Cepat Mulai:")
    print("  1. Install dependencies: pip install -r requirements.txt")
    print("  2. Jalankan GUI: python gui_scraper.py")
    print("  3. Atau command line: python run_scraper.py 'laptop'")
    print()
    print("📞 Support:")
    print("  • Email: [email protected]")
    print("  • WhatsApp: +62-813-1608-4860")
    print()
    input("Tekan Enter untuk kembali ke menu...")

def install_dependencies():
    """Install dependencies"""
    print("⚙️  Installing Dependencies...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies berhasil diinstall!")
    except Exception as e:
        print(f"❌ Error installing dependencies: {str(e)}")
    
    input("Tekan Enter untuk kembali ke menu...")

def check_dependencies():
    """Cek apakah dependencies sudah terinstall"""
    required_packages = [
        'selenium',
        'beautifulsoup4',
        'webdriver-manager',
        'lxml',
        'requests'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("⚠️  Dependencies yang belum terinstall:")
        for package in missing_packages:
            print(f"  • {package}")
        print()
        response = input("Install dependencies sekarang? (y/n): ").lower()
        if response == 'y':
            install_dependencies()
        return False
    else:
        print("✅ Semua dependencies sudah terinstall!")
        return True

def main():
    """Fungsi utama"""
    while True:
        show_menu()
        
        # Cek dependencies di awal
        if not check_dependencies():
            print("⚠️  Beberapa dependencies belum terinstall.")
            print("Pilih menu 7 untuk install dependencies.")
            print()
        
        try:
            choice = input("Pilih menu (1-8): ").strip()
            
            if choice == '1':
                run_gui()
            elif choice == '2':
                run_command_line()
            elif choice == '3':
                run_main_script()
            elif choice == '4':
                run_test()
            elif choice == '5':
                run_examples()
            elif choice == '6':
                show_documentation()
            elif choice == '7':
                install_dependencies()
            elif choice == '8':
                print("👋 Terima kasih telah menggunakan Shopee Scraper!")
                print("📞 Untuk support: +62-813-1608-4860")
                break
            else:
                print("❌ Pilihan tidak valid! Pilih 1-8.")
                input("Tekan Enter untuk melanjutkan...")
                
        except KeyboardInterrupt:
            print("\n👋 Terima kasih telah menggunakan Shopee Scraper!")
            break
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            input("Tekan Enter untuk melanjutkan...")

if __name__ == "__main__":
    main()