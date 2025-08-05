"""
Data Analyzer untuk Hasil Scraping Shopee
Script untuk menganalisis dan memvisualisasikan data hasil scraping
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import re
from datetime import datetime
import os
import glob

# Set style untuk plot
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

class ShopeeDataAnalyzer:
    def __init__(self, data_file=None):
        """
        Inisialisasi Data Analyzer
        
        Args:
            data_file (str): Path ke file CSV hasil scraping
        """
        self.data_file = data_file
        self.df = None
        self.analysis_results = {}
        
    def load_data(self, data_file=None):
        """Load data dari file CSV"""
        if data_file:
            self.data_file = data_file
        
        if not self.data_file:
            # Cari file CSV terbaru
            csv_files = glob.glob("*.csv")
            if not csv_files:
                print("❌ Tidak ada file CSV ditemukan")
                return False
            
            # Ambil file terbaru
            self.data_file = max(csv_files, key=os.path.getctime)
            print(f"📁 Menggunakan file: {self.data_file}")
        
        try:
            self.df = pd.read_csv(self.data_file, encoding='utf-8-sig')
            print(f"✅ Data berhasil dimuat: {len(self.df)} baris")
            return True
        except Exception as e:
            print(f"❌ Gagal memuat data: {str(e)}")
            return False
    
    def clean_data(self):
        """Membersihkan dan memproses data"""
        if self.df is None:
            print("❌ Data belum dimuat")
            return False
        
        print("🧹 Membersihkan data...")
        
        # Remove duplicates
        initial_count = len(self.df)
        self.df = self.df.drop_duplicates()
        print(f"   - Duplikasi dihapus: {initial_count - len(self.df)} baris")
        
        # Clean price data
        self.df['price_clean'] = self.df['price'].apply(self.extract_price)
        
        # Clean sold data
        self.df['sold_clean'] = self.df['sold'].apply(self.extract_sold_count)
        
        # Clean rating data
        self.df['rating_clean'] = self.df['rating'].apply(self.extract_rating)
        
        # Extract location city
        self.df['city'] = self.df['location'].apply(self.extract_city)
        
        print("✅ Data cleaning selesai")
        return True
    
    def extract_price(self, price_str):
        """Extract harga dari string"""
        if pd.isna(price_str) or price_str == 'N/A':
            return None
        
        # Remove currency symbols and extract numbers
        price_clean = re.sub(r'[^\d]', '', str(price_str))
        try:
            return int(price_clean) if price_clean else None
        except:
            return None
    
    def extract_sold_count(self, sold_str):
        """Extract jumlah terjual dari string"""
        if pd.isna(sold_str) or sold_str == 'Tidak ditemukan':
            return None
        
        # Extract numbers from "Terjual 1rb+" format
        match = re.search(r'(\d+)', str(sold_str))
        if match:
            return int(match.group(1))
        return None
    
    def extract_rating(self, rating_str):
        """Extract rating dari string"""
        if pd.isna(rating_str) or rating_str == 'Tidak ditemukan':
            return None
        
        # Extract percentage from "width: 80%" format
        match = re.search(r'(\d+)%', str(rating_str))
        if match:
            return int(match.group(1)) / 20  # Convert to 5-star scale
        return None
    
    def extract_city(self, location_str):
        """Extract kota dari lokasi"""
        if pd.isna(location_str) or location_str == 'Tidak ditemukan':
            return 'Unknown'
        
        # Extract city from location string
        parts = str(location_str).split(',')
        if len(parts) > 0:
            return parts[0].strip()
        return location_str
    
    def basic_statistics(self):
        """Menghitung statistik dasar"""
        if self.df is None:
            print("❌ Data belum dimuat")
            return
        
        print("\n📊 STATISTIK DASAR")
        print("="*50)
        
        # Total products
        total_products = len(self.df)
        print(f"Total produk: {total_products:,}")
        
        # Price statistics
        price_stats = self.df['price_clean'].describe()
        print(f"\n💰 STATISTIK HARGA:")
        print(f"   Rata-rata: Rp {price_stats['mean']:,.0f}")
        print(f"   Median: Rp {price_stats['50%']:,.0f}")
        print(f"   Min: Rp {price_stats['min']:,.0f}")
        print(f"   Max: Rp {price_stats['max']:,.0f}")
        
        # Rating statistics
        rating_stats = self.df['rating_clean'].describe()
        print(f"\n⭐ STATISTIK RATING:")
        print(f"   Rata-rata: {rating_stats['mean']:.2f}/5")
        print(f"   Median: {rating_stats['50%']:.2f}/5")
        
        # Top cities
        top_cities = self.df['city'].value_counts().head(5)
        print(f"\n🏙️ TOP 5 KOTA:")
        for city, count in top_cities.items():
            print(f"   {city}: {count:,} produk")
        
        # Categories
        if 'kategori' in self.df.columns:
            categories = self.df['kategori'].value_counts()
            print(f"\n📂 KATEGORI:")
            for cat, count in categories.items():
                print(f"   {cat}: {count:,} produk")
    
    def create_visualizations(self, save_plots=True):
        """Membuat visualisasi data"""
        if self.df is None:
            print("❌ Data belum dimuat")
            return
        
        print("\n📈 Membuat visualisasi...")
        
        # Create figure with subplots
        fig, axes = plt.subplots(2, 3, figsize=(18, 12))
        fig.suptitle('Analisis Data Shopee Scraping', fontsize=16, fontweight='bold')
        
        # 1. Price Distribution
        axes[0, 0].hist(self.df['price_clean'].dropna(), bins=30, alpha=0.7, color='skyblue')
        axes[0, 0].set_title('Distribusi Harga')
        axes[0, 0].set_xlabel('Harga (Rp)')
        axes[0, 0].set_ylabel('Frekuensi')
        
        # 2. Rating Distribution
        axes[0, 1].hist(self.df['rating_clean'].dropna(), bins=20, alpha=0.7, color='gold')
        axes[0, 1].set_title('Distribusi Rating')
        axes[0, 1].set_xlabel('Rating (1-5)')
        axes[0, 1].set_ylabel('Frekuensi')
        
        # 3. Top Cities
        top_cities = self.df['city'].value_counts().head(10)
        axes[0, 2].barh(range(len(top_cities)), top_cities.values, color='lightgreen')
        axes[0, 2].set_yticks(range(len(top_cities)))
        axes[0, 2].set_yticklabels(top_cities.index)
        axes[0, 2].set_title('Top 10 Kota')
        axes[0, 2].set_xlabel('Jumlah Produk')
        
        # 4. Price vs Rating Scatter
        axes[1, 0].scatter(self.df['price_clean'], self.df['rating_clean'], alpha=0.6, color='purple')
        axes[1, 0].set_title('Harga vs Rating')
        axes[1, 0].set_xlabel('Harga (Rp)')
        axes[1, 0].set_ylabel('Rating (1-5)')
        
        # 5. Sold Count Distribution
        sold_data = self.df['sold_clean'].dropna()
        if len(sold_data) > 0:
            axes[1, 1].hist(sold_data, bins=20, alpha=0.7, color='orange')
            axes[1, 1].set_title('Distribusi Jumlah Terjual')
            axes[1, 1].set_xlabel('Jumlah Terjual')
            axes[1, 1].set_ylabel('Frekuensi')
        else:
            axes[1, 1].text(0.5, 0.5, 'Data tidak tersedia', ha='center', va='center')
            axes[1, 1].set_title('Distribusi Jumlah Terjual')
        
        # 6. Categories (if available)
        if 'kategori' in self.df.columns:
            categories = self.df['kategori'].value_counts()
            axes[1, 2].pie(categories.values, labels=categories.index, autopct='%1.1f%%')
            axes[1, 2].set_title('Distribusi Kategori')
        else:
            axes[1, 2].text(0.5, 0.5, 'Data kategori tidak tersedia', ha='center', va='center')
            axes[1, 2].set_title('Distribusi Kategori')
        
        plt.tight_layout()
        
        if save_plots:
            plot_file = f"analisis_shopee_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            plt.savefig(plot_file, dpi=300, bbox_inches='tight')
            print(f"📊 Plot disimpan: {plot_file}")
        
        plt.show()
    
    def generate_report(self):
        """Generate laporan analisis"""
        if self.df is None:
            print("❌ Data belum dimuat")
            return
        
        print("\n📋 GENERATING REPORT...")
        
        # Basic stats
        total_products = len(self.df)
        avg_price = self.df['price_clean'].mean()
        avg_rating = self.df['rating_clean'].mean()
        top_city = self.df['city'].mode()[0] if len(self.df['city'].mode()) > 0 else 'Unknown'
        
        # Create report
        report = f"""
ANALISIS DATA SHOPEE SCRAPING
{'='*50}

📊 STATISTIK UMUM:
- Total produk: {total_products:,}
- Rata-rata harga: Rp {avg_price:,.0f}
- Rata-rata rating: {avg_rating:.2f}/5
- Kota terpopuler: {top_city}

💰 ANALISIS HARGA:
- Harga tertinggi: Rp {self.df['price_clean'].max():,.0f}
- Harga terendah: Rp {self.df['price_clean'].min():,.0f}
- Median harga: Rp {self.df['price_clean'].median():,.0f}

⭐ ANALISIS RATING:
- Rating tertinggi: {self.df['rating_clean'].max():.1f}/5
- Rating terendah: {self.df['rating_clean'].min():.1f}/5
- Produk dengan rating > 4: {len(self.df[self.df['rating_clean'] > 4]):,}

🏙️ ANALISIS LOKASI:
{self.df['city'].value_counts().head(5).to_string()}

📅 WAKTU SCRAPING:
- Data di-scrape pada: {self.df['scraped_at'].iloc[0] if 'scraped_at' in self.df.columns else 'Tidak tersedia'}

{'='*50}
        """
        
        # Save report
        report_file = f"laporan_analisis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"📄 Laporan disimpan: {report_file}")
        print(report)

def main():
    """Main function"""
    print("📊 SHOPEE DATA ANALYZER")
    print("="*50)
    print("Dikembangkan oleh: Dosen Data Mining (30 tahun pengalaman)")
    print("="*50)
    
    # Initialize analyzer
    analyzer = ShopeeDataAnalyzer()
    
    # Load data
    if not analyzer.load_data():
        return
    
    # Clean data
    analyzer.clean_data()
    
    # Generate analysis
    analyzer.basic_statistics()
    analyzer.create_visualizations()
    analyzer.generate_report()
    
    print("\n🎉 ANALISIS SELESAI!")
    print("📁 Cek file plot dan laporan yang dihasilkan")

if __name__ == "__main__":
    main()