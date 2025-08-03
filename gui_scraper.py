#!/usr/bin/env python3
"""
GUI Application untuk Shopee Scraper
Interface grafis sederhana untuk memudahkan penggunaan
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import threading
import time
from shopee_scraper import ShopeeScraper
import os

class ShopeeScraperGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🚀 Shopee Product Scraper - Data Mining Expert")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # Variabel
        self.scraper = None
        self.is_running = False
        
        # Setup GUI
        self.setup_gui()
        
    def setup_gui(self):
        """Setup komponen GUI"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="🚀 Shopee Product Scraper", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Input Section
        input_frame = ttk.LabelFrame(main_frame, text="📝 Input Parameters", padding="10")
        input_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        input_frame.columnconfigure(1, weight=1)
        
        # Keyword
        ttk.Label(input_frame, text="Keyword Produk:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.keyword_var = tk.StringVar(value="laptop")
        self.keyword_entry = ttk.Entry(input_frame, textvariable=self.keyword_var, width=40)
        self.keyword_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=5)
        
        # Max Products
        ttk.Label(input_frame, text="Jumlah Maksimal Produk:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.max_products_var = tk.IntVar(value=50)
        self.max_products_spinbox = ttk.Spinbox(input_frame, from_=1, to=1000, 
                                               textvariable=self.max_products_var, width=10)
        self.max_products_spinbox.grid(row=1, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
        # Login Options
        ttk.Label(input_frame, text="Metode Login:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.login_method_var = tk.StringVar(value="auto")
        login_frame = ttk.Frame(input_frame)
        login_frame.grid(row=2, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
        ttk.Radiobutton(login_frame, text="Otomatis", variable=self.login_method_var, 
                       value="auto").pack(side=tk.LEFT, padx=(0, 10))
        ttk.Radiobutton(login_frame, text="Manual", variable=self.login_method_var, 
                       value="manual").pack(side=tk.LEFT)
        
        # Control Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, columnspan=3, pady=10)
        
        self.start_button = ttk.Button(button_frame, text="🚀 Mulai Scraping", 
                                      command=self.start_scraping)
        self.start_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.stop_button = ttk.Button(button_frame, text="⏹️ Stop", 
                                     command=self.stop_scraping, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.clear_button = ttk.Button(button_frame, text="🗑️ Clear Log", 
                                      command=self.clear_log)
        self.clear_button.pack(side=tk.LEFT)
        
        # Progress Section
        progress_frame = ttk.LabelFrame(main_frame, text="📊 Progress", padding="10")
        progress_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        progress_frame.columnconfigure(0, weight=1)
        
        self.progress_var = tk.StringVar(value="Siap untuk memulai...")
        ttk.Label(progress_frame, textvariable=self.progress_var).grid(row=0, column=0, sticky=tk.W)
        
        self.progress_bar = ttk.Progressbar(progress_frame, mode='indeterminate')
        self.progress_bar.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(5, 0))
        
        # Log Section
        log_frame = ttk.LabelFrame(main_frame, text="📋 Log Output", padding="10")
        log_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=15, width=80)
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Results Section
        results_frame = ttk.LabelFrame(main_frame, text="📁 Hasil", padding="10")
        results_frame.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E))
        results_frame.columnconfigure(1, weight=1)
        
        ttk.Label(results_frame, text="File Output:").grid(row=0, column=0, sticky=tk.W)
        self.output_var = tk.StringVar(value="Belum ada hasil")
        output_label = ttk.Label(results_frame, textvariable=self.output_var, 
                                foreground="blue", cursor="hand2")
        output_label.grid(row=0, column=1, sticky=tk.W, padx=(10, 0))
        output_label.bind("<Button-1>", self.open_output_folder)
        
        # Status bar
        self.status_var = tk.StringVar(value="Siap")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, 
                              relief=tk.SUNKEN, anchor=tk.W)
        status_bar.grid(row=6, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
        
    def log_message(self, message):
        """Tambah pesan ke log"""
        timestamp = time.strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()
        
    def clear_log(self):
        """Clear log output"""
        self.log_text.delete(1.0, tk.END)
        
    def update_progress(self, message):
        """Update progress message"""
        self.progress_var.set(message)
        self.root.update_idletasks()
        
    def update_status(self, message):
        """Update status bar"""
        self.status_var.set(message)
        self.root.update_idletasks()
        
    def start_scraping(self):
        """Mulai proses scraping dalam thread terpisah"""
        if self.is_running:
            return
            
        keyword = self.keyword_var.get().strip()
        if not keyword:
            messagebox.showerror("Error", "Keyword tidak boleh kosong!")
            return
            
        max_products = self.max_products_var.get()
        if max_products < 1:
            messagebox.showerror("Error", "Jumlah produk harus lebih dari 0!")
            return
            
        # Disable controls
        self.is_running = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.progress_bar.start()
        
        # Start scraping in separate thread
        thread = threading.Thread(target=self.scraping_thread, 
                                args=(keyword, max_products))
        thread.daemon = True
        thread.start()
        
    def scraping_thread(self, keyword, max_products):
        """Thread untuk menjalankan scraping"""
        try:
            self.log_message("🚀 Memulai proses scraping...")
            self.update_progress("Inisialisasi scraper...")
            self.update_status("Menjalankan scraper...")
            
            # Initialize scraper
            self.scraper = ShopeeScraper()
            
            # Login process
            if self.login_method_var.get() == "auto":
                self.log_message("🔐 Mencoba login otomatis...")
                self.update_progress("Login otomatis...")
                
                login_success = self.scraper.automated_login("081316084860", "Pradipta301203")
                if not login_success:
                    self.log_message("❌ Login otomatis gagal, beralih ke manual...")
                    self.update_progress("Login manual...")
                    self.scraper.manual_login()
                else:
                    self.log_message("✅ Login otomatis berhasil!")
            else:
                self.log_message("🔐 Menggunakan login manual...")
                self.update_progress("Login manual...")
                self.scraper.manual_login()
            
            # Start scraping
            self.log_message(f"🔍 Mencari produk dengan keyword: '{keyword}'")
            self.update_progress("Scraping produk...")
            
            products = self.scraper.scrape_products(keyword, max_products)
            
            if products:
                # Save results
                self.log_message("💾 Menyimpan hasil...")
                self.update_progress("Menyimpan data...")
                
                filename_base = f"shopee_{keyword.replace(' ', '_')}"
                csv_file = f"{filename_base}.csv"
                json_file = f"{filename_base}.json"
                
                self.scraper.save_to_csv(products, csv_file)
                self.scraper.save_to_json(products, json_file)
                
                self.log_message(f"✅ Berhasil scrape {len(products)} produk")
                self.log_message(f"💾 Data tersimpan di: {csv_file} dan {json_file}")
                
                # Update output display
                self.output_var.set(f"{csv_file}, {json_file}")
                
                # Show sample data
                self.log_message("\n📋 Sample data:")
                for i, product in enumerate(products[:3]):
                    self.log_message(f"\nProduk {i+1}:")
                    for key, value in product.items():
                        self.log_message(f"  {key}: {value}")
                        
            else:
                self.log_message("❌ Tidak ada produk yang ditemukan")
                
        except Exception as e:
            self.log_message(f"❌ Error: {str(e)}")
            messagebox.showerror("Error", f"Terjadi error: {str(e)}")
            
        finally:
            # Cleanup
            if self.scraper:
                self.scraper.close()
                
            # Re-enable controls
            self.is_running = False
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
            self.progress_bar.stop()
            self.update_progress("Selesai")
            self.update_status("Siap")
            
    def stop_scraping(self):
        """Stop proses scraping"""
        if self.is_running:
            self.log_message("⏹️ Menghentikan scraping...")
            self.is_running = False
            if self.scraper:
                self.scraper.close()
                
    def open_output_folder(self):
        """Buka folder output"""
        try:
            import subprocess
            import platform
            
            if platform.system() == "Windows":
                subprocess.run(["explorer", "."])
            elif platform.system() == "Darwin":  # macOS
                subprocess.run(["open", "."])
            else:  # Linux
                subprocess.run(["xdg-open", "."])
                
        except Exception as e:
            messagebox.showerror("Error", f"Tidak dapat membuka folder: {str(e)}")

def main():
    """Fungsi utama"""
    root = tk.Tk()
    app = ShopeeScraperGUI(root)
    
    # Center window
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f"{width}x{height}+{x}+{y}")
    
    root.mainloop()

if __name__ == "__main__":
    main()