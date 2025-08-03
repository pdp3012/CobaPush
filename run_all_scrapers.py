#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Run All Bukalapak Scrapers
Advanced Data Mining Tool - Comprehensive Execution Script
Dibuat oleh: Dosen Data Mining (30 tahun pengalaman)
"""

import time
import json
import pandas as pd
from datetime import datetime
import os
import sys

# Import all scrapers
from bukalapak_scraper import BukalapakScraper
from bukalapak_api_scraper import BukalapakAPIScraper
from bukalapak_css_scraper import BukalapakCSSScraper

class ComprehensiveScraperRunner:
    """
    Comprehensive runner untuk semua scraper Bukalapak
    """
    
    def __init__(self):
        self.start_time = datetime.now()
        self.results = {
            'start_time': self.start_time.isoformat(),
            'scrapers': {},
            'summary': {},
            'errors': []
        }
        
        # Create output directories
        self.create_directories()
        
    def create_directories(self):
        """Create output directories"""
        directories = ['data', 'data/csv', 'data/json', 'data/logs', 'data/reports']
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
            
    def print_header(self, title):
        """Print header yang menarik"""
        print("\n" + "="*80)
        print(f"🎯 {title}")
        print("="*80)
        
    def print_section(self, title):
        """Print section header"""
        print(f"\n📋 {title}")
        print("-" * 50)
        
    def run_main_scraper(self, queries, max_pages=2):
        """Run main scraper (API + CSS)"""
        self.print_section("MAIN SCRAPER (API + CSS)")
        
        try:
            scraper = BukalapakScraper(headless=True, delay_range=(2, 4))
            
            for query in queries:
                print(f"\n🔍 Scraping: {query}")
                
                # API scraping
                print("   📡 API scraping...")
                scraper.scrape_via_api(search_query=query, max_pages=max_pages)
                
                # CSS scraping
                print("   🎨 CSS scraping...")
                scraper.scrape_via_css_selector(search_query=query, max_pages=max_pages)
                
                # Save data
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                csv_file = f"data/csv/main_scraper_{query}_{timestamp}.csv"
                json_file = f"data/json/main_scraper_{query}_{timestamp}.json"
                
                scraper.save_to_csv(csv_file)
                scraper.save_to_json(json_file)
                
                # Get statistics
                stats = scraper.get_statistics()
                
                # Store results
                self.results['scrapers'][f'main_{query}'] = {
                    'method': 'API + CSS',
                    'query': query,
                    'total_products': stats.get('total_products', 0),
                    'avg_price': stats.get('avg_price', 0),
                    'avg_rating': stats.get('avg_rating', 0),
                    'total_sold': stats.get('total_sold', 0),
                    'unique_stores': stats.get('unique_stores', 0),
                    'api_method_count': stats.get('api_method_count', 0),
                    'css_method_count': stats.get('css_method_count', 0),
                    'csv_file': csv_file,
                    'json_file': json_file,
                    'timestamp': timestamp
                }
                
                print(f"   ✅ Completed: {stats.get('total_products', 0)} products")
                
                # Clear data
                scraper.clear_data()
                
        except Exception as e:
            error_msg = f"Main scraper error: {str(e)}"
            print(f"   ❌ {error_msg}")
            self.results['errors'].append(error_msg)
            
    def run_api_scraper(self, queries, max_pages=2):
        """Run API-only scraper"""
        self.print_section("API SCRAPER")
        
        try:
            scraper = BukalapakAPIScraper(delay_range=(2, 4))
            
            for query in queries:
                print(f"\n🔍 API Scraping: {query}")
                
                # Search products
                scraper.search_products(query=query, max_pages=max_pages)
                
                # Get trending products
                scraper.get_trending_products(max_pages=1)
                
                # Get recommendations
                scraper.get_recommendations(max_pages=1)
                
                # Save data
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                csv_file = f"data/csv/api_scraper_{query}_{timestamp}.csv"
                json_file = f"data/json/api_scraper_{query}_{timestamp}.json"
                
                scraper.save_to_csv(csv_file)
                scraper.save_to_json(json_file)
                
                # Get statistics
                stats = scraper.get_statistics()
                
                # Store results
                self.results['scrapers'][f'api_{query}'] = {
                    'method': 'API Only',
                    'query': query,
                    'total_products': stats.get('total_products', 0),
                    'avg_price': stats.get('avg_price', 0),
                    'avg_rating': stats.get('avg_rating', 0),
                    'total_sold': stats.get('total_sold', 0),
                    'unique_stores': stats.get('unique_stores', 0),
                    'unique_categories': stats.get('unique_categories', 0),
                    'products_with_discount': stats.get('products_with_discount', 0),
                    'verified_stores': stats.get('verified_stores', 0),
                    'official_stores': stats.get('official_stores', 0),
                    'csv_file': csv_file,
                    'json_file': json_file,
                    'timestamp': timestamp
                }
                
                print(f"   ✅ Completed: {stats.get('total_products', 0)} products")
                
                # Clear data
                scraper.clear_data()
                
        except Exception as e:
            error_msg = f"API scraper error: {str(e)}"
            print(f"   ❌ {error_msg}")
            self.results['errors'].append(error_msg)
            
    def run_css_scraper(self, queries, max_pages=2):
        """Run CSS-only scraper"""
        self.print_section("CSS SELECTOR SCRAPER")
        
        try:
            scraper = BukalapakCSSScraper(headless=True)
            
            for query in queries:
                print(f"\n🔍 CSS Scraping: {query}")
                
                # Scrape products
                scraper.scrape_products(search_query=query, max_pages=max_pages)
                
                # Save data
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                csv_file = f"data/csv/css_scraper_{query}_{timestamp}.csv"
                json_file = f"data/json/css_scraper_{query}_{timestamp}.json"
                
                scraper.save_to_csv(csv_file)
                scraper.save_to_json(json_file)
                
                # Get statistics
                stats = scraper.get_statistics()
                
                # Store results
                self.results['scrapers'][f'css_{query}'] = {
                    'method': 'CSS Selector Only',
                    'query': query,
                    'total_products': stats.get('total_products', 0),
                    'avg_price': stats.get('avg_price', 0),
                    'avg_rating': stats.get('avg_rating', 0),
                    'total_sold': stats.get('total_sold', 0),
                    'unique_stores': stats.get('unique_stores', 0),
                    'csv_file': csv_file,
                    'json_file': json_file,
                    'timestamp': timestamp
                }
                
                print(f"   ✅ Completed: {stats.get('total_products', 0)} products")
                
                # Clear data
                scraper.products_data = []
                
        except Exception as e:
            error_msg = f"CSS scraper error: {str(e)}"
            print(f"   ❌ {error_msg}")
            self.results['errors'].append(error_msg)
            
    def generate_summary_report(self):
        """Generate comprehensive summary report"""
        self.print_section("GENERATING SUMMARY REPORT")
        
        end_time = datetime.now()
        duration = end_time - self.start_time
        
        # Calculate summary statistics
        total_products = sum(scraper['total_products'] for scraper in self.results['scrapers'].values())
        total_queries = len(set(scraper['query'] for scraper in self.results['scrapers'].values()))
        total_methods = len(self.results['scrapers'])
        
        # Method breakdown
        method_counts = {}
        for scraper in self.results['scrapers'].values():
            method = scraper['method']
            method_counts[method] = method_counts.get(method, 0) + 1
            
        # Price analysis
        all_prices = [scraper['avg_price'] for scraper in self.results['scrapers'].values() if scraper['avg_price'] > 0]
        avg_price_overall = sum(all_prices) / len(all_prices) if all_prices else 0
        
        # Rating analysis
        all_ratings = [scraper['avg_rating'] for scraper in self.results['scrapers'].values() if scraper['avg_rating'] > 0]
        avg_rating_overall = sum(all_ratings) / len(all_ratings) if all_ratings else 0
        
        # Store summary
        self.results['summary'] = {
            'end_time': end_time.isoformat(),
            'duration_seconds': duration.total_seconds(),
            'duration_formatted': str(duration),
            'total_products': total_products,
            'total_queries': total_queries,
            'total_methods': total_methods,
            'method_breakdown': method_counts,
            'avg_price_overall': avg_price_overall,
            'avg_rating_overall': avg_rating_overall,
            'total_errors': len(self.results['errors']),
            'success_rate': ((total_methods - len(self.results['errors'])) / total_methods * 100) if total_methods > 0 else 0
        }
        
        # Print summary
        print(f"\n📊 COMPREHENSIVE SUMMARY REPORT")
        print(f"   ⏱️  Duration: {duration}")
        print(f"   📦 Total Products: {total_products:,}")
        print(f"   🔍 Total Queries: {total_queries}")
        print(f"   🛠️  Total Methods: {total_methods}")
        print(f"   💰 Average Price: Rp {avg_price_overall:,.0f}")
        print(f"   ⭐ Average Rating: {avg_rating_overall:.2f}")
        print(f"   ❌ Total Errors: {len(self.results['errors'])}")
        print(f"   ✅ Success Rate: {self.results['summary']['success_rate']:.1f}%")
        
        print(f"\n📋 Method Breakdown:")
        for method, count in method_counts.items():
            print(f"   {method}: {count}")
            
        if self.results['errors']:
            print(f"\n❌ Errors Encountered:")
            for error in self.results['errors']:
                print(f"   - {error}")
                
    def save_reports(self):
        """Save all reports"""
        self.print_section("SAVING REPORTS")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save comprehensive report
        report_file = f"data/reports/comprehensive_report_{timestamp}.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, ensure_ascii=False, indent=2)
        print(f"   📄 Comprehensive report: {report_file}")
        
        # Save summary CSV
        summary_data = []
        for scraper_id, scraper_data in self.results['scrapers'].items():
            summary_data.append({
                'scraper_id': scraper_id,
                'method': scraper_data['method'],
                'query': scraper_data['query'],
                'total_products': scraper_data['total_products'],
                'avg_price': scraper_data['avg_price'],
                'avg_rating': scraper_data['avg_rating'],
                'total_sold': scraper_data['total_sold'],
                'unique_stores': scraper_data['unique_stores'],
                'timestamp': scraper_data['timestamp']
            })
            
        if summary_data:
            summary_df = pd.DataFrame(summary_data)
            summary_csv = f"data/reports/summary_report_{timestamp}.csv"
            summary_df.to_csv(summary_csv, index=False, encoding='utf-8')
            print(f"   📊 Summary CSV: {summary_csv}")
            
        # Save detailed analysis
        analysis_file = f"data/reports/detailed_analysis_{timestamp}.txt"
        with open(analysis_file, 'w', encoding='utf-8') as f:
            f.write("BUKALAPAK SCRAPER - DETAILED ANALYSIS\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Duration: {self.results['summary']['duration_formatted']}\n\n")
            
            f.write("EXECUTION SUMMARY:\n")
            f.write(f"- Total Products Scraped: {self.results['summary']['total_products']:,}\n")
            f.write(f"- Total Queries: {self.results['summary']['total_queries']}\n")
            f.write(f"- Total Methods: {self.results['summary']['total_methods']}\n")
            f.write(f"- Success Rate: {self.results['summary']['success_rate']:.1f}%\n\n")
            
            f.write("METHOD BREAKDOWN:\n")
            for method, count in self.results['summary']['method_breakdown'].items():
                f.write(f"- {method}: {count}\n")
            f.write("\n")
            
            f.write("DETAILED RESULTS:\n")
            for scraper_id, scraper_data in self.results['scrapers'].items():
                f.write(f"\n{scraper_id}:\n")
                f.write(f"  Method: {scraper_data['method']}\n")
                f.write(f"  Query: {scraper_data['query']}\n")
                f.write(f"  Products: {scraper_data['total_products']}\n")
                f.write(f"  Avg Price: Rp {scraper_data['avg_price']:,.0f}\n")
                f.write(f"  Avg Rating: {scraper_data['avg_rating']:.2f}\n")
                f.write(f"  Total Sold: {scraper_data['total_sold']}\n")
                f.write(f"  Unique Stores: {scraper_data['unique_stores']}\n")
                
            if self.results['errors']:
                f.write("\nERRORS:\n")
                for error in self.results['errors']:
                    f.write(f"- {error}\n")
                    
        print(f"   📝 Detailed analysis: {analysis_file}")
        
    def run_comprehensive_scraping(self, queries=None, max_pages=2):
        """Run comprehensive scraping with all methods"""
        if queries is None:
            queries = ["laptop", "smartphone", "headphone", "gaming", "ultrabook"]
            
        self.print_header("COMPREHENSIVE BUKALAPAK SCRAPING")
        print("🎓 Dibuat oleh: Dosen Data Mining (30 tahun pengalaman)")
        print("🌟 Sertifikasi: International Data Mining Certification")
        print(f"⏰ Started at: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"🔍 Queries: {', '.join(queries)}")
        print(f"📄 Max pages per query: {max_pages}")
        
        try:
            # Run all scrapers
            self.run_main_scraper(queries, max_pages)
            self.run_api_scraper(queries, max_pages)
            self.run_css_scraper(queries, max_pages)
            
            # Generate reports
            self.generate_summary_report()
            self.save_reports()
            
            # Final summary
            self.print_header("COMPREHENSIVE SCRAPING COMPLETED")
            print("🎉 All scrapers completed successfully!")
            print(f"📊 Total products scraped: {self.results['summary']['total_products']:,}")
            print(f"✅ Success rate: {self.results['summary']['success_rate']:.1f}%")
            print(f"⏱️  Total duration: {self.results['summary']['duration_formatted']}")
            print(f"📁 Reports saved in: data/reports/")
            print(f"📊 Data files saved in: data/csv/ and data/json/")
            
        except KeyboardInterrupt:
            print("\n⚠️  Scraping interrupted by user")
            self.generate_summary_report()
            self.save_reports()
        except Exception as e:
            print(f"\n❌ Unexpected error: {e}")
            self.results['errors'].append(f"Unexpected error: {str(e)}")
            self.generate_summary_report()
            self.save_reports()

def main():
    """Main function"""
    runner = ComprehensiveScraperRunner()
    
    # Define queries to scrape
    queries = [
        "laptop",
        "smartphone", 
        "headphone",
        "gaming laptop",
        "ultrabook"
    ]
    
    # Run comprehensive scraping
    runner.run_comprehensive_scraping(queries=queries, max_pages=2)

if __name__ == "__main__":
    main()