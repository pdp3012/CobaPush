#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bukalapak API Scraper - Advanced Implementation
Fokus pada API scraping dengan multiple endpoints dan error handling
"""

import requests
import json
import time
import re
import pandas as pd
from fake_useragent import UserAgent
import logging
from datetime import datetime
import random
from urllib.parse import urlencode, quote

class BukalapakAPIScraper:
    """
    Advanced API Scraper untuk Bukalapak
    Menggunakan multiple API endpoints dan strategies
    """
    
    def __init__(self, delay_range=(1, 3)):
        self.api_base = "https://api.bukalapak.com"
        self.session = requests.Session()
        self.ua = UserAgent()
        self.delay_range = delay_range
        self.products_data = []
        
        # API endpoints
        self.endpoints = {
            'search': '/products',
            'category': '/categories/{category_id}/products',
            'product_detail': '/products/{product_id}',
            'store': '/stores/{store_id}',
            'trending': '/trending/products',
            'recommendations': '/recommendations/products'
        }
        
        # Setup session
        self._setup_session()
        
    def _setup_session(self):
        """Setup session dengan headers yang realistic"""
        headers = {
            'User-Agent': self.ua.random,
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9,id;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'Cache-Control': 'no-cache',
            'Pragma': 'no-cache',
            'Referer': 'https://www.bukalapak.com/',
            'Origin': 'https://www.bukalapak.com'
        }
        self.session.headers.update(headers)
        
    def _random_delay(self):
        """Random delay untuk menghindari rate limiting"""
        delay = random.uniform(*self.delay_range)
        time.sleep(delay)
        
    def _make_api_request(self, endpoint, params=None, retries=3):
        """
        Make API request dengan retry mechanism
        
        Args:
            endpoint (str): API endpoint
            params (dict): Query parameters
            retries (int): Number of retries
            
        Returns:
            dict: API response data
        """
        url = f"{self.api_base}{endpoint}"
        
        for attempt in range(retries):
            try:
                # Update User-Agent untuk setiap request
                self.session.headers['User-Agent'] = self.ua.random
                
                response = self.session.get(url, params=params, timeout=30)
                
                if response.status_code == 200:
                    return response.json()
                elif response.status_code == 429:  # Rate limited
                    wait_time = (attempt + 1) * 10
                    print(f"Rate limited. Waiting {wait_time} seconds...")
                    time.sleep(wait_time)
                else:
                    print(f"API request failed with status {response.status_code}")
                    
            except requests.exceptions.RequestException as e:
                print(f"Request error (attempt {attempt + 1}): {e}")
                if attempt < retries - 1:
                    time.sleep(5)
                    
        return None
        
    def search_products(self, query="", category_id=None, max_pages=5, limit=50):
        """
        Search products via API
        
        Args:
            query (str): Search query
            category_id (str): Category ID
            max_pages (int): Maximum pages to scrape
            limit (int): Products per page
        """
        print(f"Searching products: query='{query}', category_id='{category_id}'")
        
        for page in range(1, max_pages + 1):
            print(f"Scraping page {page}")
            
            # Prepare parameters
            params = {
                'page': page,
                'limit': limit
            }
            
            if query:
                params['keywords'] = query
                
            if category_id:
                endpoint = self.endpoints['category'].format(category_id=category_id)
            else:
                endpoint = self.endpoints['search']
                
            # Make API request
            data = self._make_api_request(endpoint, params)
            
            if not data:
                print(f"No data received for page {page}")
                break
                
            # Extract products
            products = data.get('data', [])
            if not products:
                print(f"No products found on page {page}")
                break
                
            print(f"Found {len(products)} products on page {page}")
            
            # Process each product
            for product in products:
                product_info = self._extract_product_info(product)
                if product_info:
                    self.products_data.append(product_info)
                    
            # Check if there are more pages
            if len(products) < limit:
                print("Reached last page")
                break
                
            self._random_delay()
            
        print(f"Search completed. Total products: {len(self.products_data)}")
        
    def get_trending_products(self, max_pages=3):
        """Get trending products"""
        print("Getting trending products...")
        
        for page in range(1, max_pages + 1):
            params = {
                'page': page,
                'limit': 50
            }
            
            data = self._make_api_request(self.endpoints['trending'], params)
            
            if not data:
                break
                
            products = data.get('data', [])
            if not products:
                break
                
            for product in products:
                product_info = self._extract_product_info(product)
                if product_info:
                    product_info['source'] = 'trending'
                    self.products_data.append(product_info)
                    
            self._random_delay()
            
    def get_recommendations(self, max_pages=3):
        """Get recommended products"""
        print("Getting recommended products...")
        
        for page in range(1, max_pages + 1):
            params = {
                'page': page,
                'limit': 50
            }
            
            data = self._make_api_request(self.endpoints['recommendations'], params)
            
            if not data:
                break
                
            products = data.get('data', [])
            if not products:
                break
                
            for product in products:
                product_info = self._extract_product_info(product)
                if product_info:
                    product_info['source'] = 'recommendations'
                    self.products_data.append(product_info)
                    
            self._random_delay()
            
    def get_product_details(self, product_ids):
        """
        Get detailed information for specific products
        
        Args:
            product_ids (list): List of product IDs
        """
        print(f"Getting details for {len(product_ids)} products...")
        
        for product_id in product_ids:
            endpoint = self.endpoints['product_detail'].format(product_id=product_id)
            data = self._make_api_request(endpoint)
            
            if data:
                product_info = self._extract_detailed_product_info(data)
                if product_info:
                    self.products_data.append(product_info)
                    
            self._random_delay()
            
    def _extract_product_info(self, product_data):
        """
        Extract basic product information from API response
        
        Args:
            product_data (dict): Product data from API
            
        Returns:
            dict: Extracted product information
        """
        try:
            # Basic product info
            product_info = {
                'product_id': product_data.get('id', ''),
                'nama_produk': product_data.get('name', ''),
                'harga': self._extract_price(product_data),
                'harga_asli': product_data.get('original_price', 0),
                'diskon': self._extract_discount(product_data),
                'jumlah_terjual': self._extract_sold_count(product_data),
                'stok': product_data.get('stock', 0),
                'kondisi': product_data.get('condition', ''),
                'kategori': self._extract_category(product_data),
                'rating_produk': self._extract_rating(product_data),
                'jumlah_review': self._extract_review_count(product_data),
                'url_produk': self._extract_product_url(product_data),
                'gambar_produk': self._extract_images(product_data),
                'deskripsi_singkat': product_data.get('description', '')[:200],
                'berat': self._extract_weight(product_data),
                'dimensi': self._extract_dimensions(product_data),
                'garansi': product_data.get('warranty', ''),
                'metode_pengiriman': self._extract_shipping_methods(product_data),
                'lokasi_pengiriman': self._extract_shipping_locations(product_data),
                'estimasi_pengiriman': product_data.get('shipping_estimate', ''),
                'metode_scraping': 'API',
                'timestamp_scraping': datetime.now().isoformat()
            }
            
            # Store information
            store_data = product_data.get('store', {})
            if store_data:
                product_info.update({
                    'nama_toko': store_data.get('name', ''),
                    'store_id': store_data.get('id', ''),
                    'lokasi_toko': store_data.get('location', ''),
                    'rating_toko': store_data.get('rating', {}).get('average', 0),
                    'jumlah_rating_toko': store_data.get('rating', {}).get('count', 0),
                    'jumlah_produk_toko': store_data.get('products_count', 0),
                    'member_sejak': store_data.get('member_since', ''),
                    'url_toko': store_data.get('url', ''),
                    'verified_store': store_data.get('verified', False),
                    'official_store': store_data.get('official', False)
                })
                
            # Data validation
            if product_info['nama_produk'] and product_info['harga'] > 0:
                return product_info
            return None
            
        except Exception as e:
            print(f"Error extracting product info: {e}")
            return None
            
    def _extract_detailed_product_info(self, product_data):
        """Extract detailed product information"""
        basic_info = self._extract_product_info(product_data)
        
        if basic_info:
            # Add detailed information
            basic_info.update({
                'spesifikasi': product_data.get('specifications', {}),
                'varian': product_data.get('variants', []),
                'ulasan': self._extract_reviews(product_data),
                'pertanyaan': product_data.get('questions', []),
                'kebijakan_return': product_data.get('return_policy', ''),
                'kebijakan_garansi': product_data.get('warranty_policy', ''),
                'informasi_pengiriman': product_data.get('shipping_info', {}),
                'informasi_pembayaran': product_data.get('payment_info', {}),
                'informasi_promo': product_data.get('promo_info', {}),
                'informasi_stok': product_data.get('stock_info', {}),
                'informasi_rating': product_data.get('rating_info', {}),
                'informasi_toko_detil': product_data.get('store_info', {})
            })
            
        return basic_info
        
    def _extract_price(self, product_data):
        """Extract price information"""
        try:
            price = product_data.get('price', 0)
            if isinstance(price, (int, float)):
                return price
            return 0
        except:
            return 0
            
    def _extract_discount(self, product_data):
        """Extract discount information"""
        try:
            original_price = product_data.get('original_price', 0)
            current_price = product_data.get('price', 0)
            
            if original_price > current_price > 0:
                discount_amount = original_price - current_price
                discount_percentage = (discount_amount / original_price) * 100
                return {
                    'amount': discount_amount,
                    'percentage': round(discount_percentage, 2)
                }
            return {'amount': 0, 'percentage': 0}
        except:
            return {'amount': 0, 'percentage': 0}
            
    def _extract_sold_count(self, product_data):
        """Extract sold count"""
        try:
            sold_count = product_data.get('sold_count', 0)
            if isinstance(sold_count, (int, float)):
                return sold_count
            return 0
        except:
            return 0
            
    def _extract_category(self, product_data):
        """Extract category information"""
        try:
            category = product_data.get('category', {})
            return {
                'id': category.get('id', ''),
                'name': category.get('name', ''),
                'url': category.get('url', ''),
                'parent': category.get('parent', {})
            }
        except:
            return {'id': '', 'name': '', 'url': '', 'parent': {}}
            
    def _extract_rating(self, product_data):
        """Extract rating information"""
        try:
            rating = product_data.get('rating', {})
            return {
                'average': rating.get('average', 0),
                'count': rating.get('count', 0),
                'distribution': rating.get('distribution', {})
            }
        except:
            return {'average': 0, 'count': 0, 'distribution': {}}
            
    def _extract_review_count(self, product_data):
        """Extract review count"""
        try:
            rating = product_data.get('rating', {})
            return rating.get('count', 0)
        except:
            return 0
            
    def _extract_product_url(self, product_data):
        """Extract product URL"""
        try:
            return product_data.get('url', '')
        except:
            return ''
            
    def _extract_images(self, product_data):
        """Extract product images"""
        try:
            images = product_data.get('images', [])
            return [img.get('url', '') for img in images if img.get('url')]
        except:
            return []
            
    def _extract_weight(self, product_data):
        """Extract product weight"""
        try:
            return product_data.get('weight', 0)
        except:
            return 0
            
    def _extract_dimensions(self, product_data):
        """Extract product dimensions"""
        try:
            dimensions = product_data.get('dimensions', {})
            return {
                'length': dimensions.get('length', 0),
                'width': dimensions.get('width', 0),
                'height': dimensions.get('height', 0)
            }
        except:
            return {'length': 0, 'width': 0, 'height': 0}
            
    def _extract_shipping_methods(self, product_data):
        """Extract shipping methods"""
        try:
            shipping = product_data.get('shipping', {})
            return shipping.get('methods', [])
        except:
            return []
            
    def _extract_shipping_locations(self, product_data):
        """Extract shipping locations"""
        try:
            shipping = product_data.get('shipping', {})
            return shipping.get('locations', [])
        except:
            return []
            
    def _extract_reviews(self, product_data):
        """Extract product reviews"""
        try:
            reviews = product_data.get('reviews', [])
            return [{
                'user': review.get('user', ''),
                'rating': review.get('rating', 0),
                'comment': review.get('comment', ''),
                'date': review.get('date', ''),
                'verified': review.get('verified', False)
            } for review in reviews]
        except:
            return []
            
    def save_to_csv(self, filename="bukalapak_api_products.csv"):
        """Save data to CSV"""
        try:
            df = pd.DataFrame(self.products_data)
            df.to_csv(filename, index=False, encoding='utf-8')
            print(f"Data saved to {filename}")
            return filename
        except Exception as e:
            print(f"Error saving CSV: {e}")
            return None
            
    def save_to_json(self, filename="bukalapak_api_products.json"):
        """Save data to JSON"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.products_data, f, ensure_ascii=False, indent=2)
            print(f"Data saved to {filename}")
            return filename
        except Exception as e:
            print(f"Error saving JSON: {e}")
            return None
            
    def get_statistics(self):
        """Get statistics from scraped data"""
        if not self.products_data:
            return {}
            
        df = pd.DataFrame(self.products_data)
        
        stats = {
            'total_products': len(self.products_data),
            'avg_price': df['harga'].mean(),
            'max_price': df['harga'].max(),
            'min_price': df['harga'].min(),
            'avg_rating': df['rating_produk'].apply(lambda x: x.get('average', 0) if isinstance(x, dict) else x).mean(),
            'total_sold': df['jumlah_terjual'].sum(),
            'unique_stores': df['nama_toko'].nunique(),
            'unique_categories': df['kategori'].apply(lambda x: x.get('name', '') if isinstance(x, dict) else x).nunique(),
            'products_with_discount': len(df[df['diskon'].apply(lambda x: x.get('amount', 0) > 0 if isinstance(x, dict) else False)]),
            'verified_stores': len(df[df['verified_store'] == True]),
            'official_stores': len(df[df['official_store'] == True])
        }
        
        return stats
        
    def clear_data(self):
        """Clear stored data"""
        self.products_data = []
        print("Data cleared")

def main():
    """Main function untuk demonstrasi API scraper"""
    print("=" * 60)
    print("BUKALAPAK API SCRAPER")
    print("Advanced Implementation dengan Multiple Endpoints")
    print("=" * 60)
    
    # Initialize scraper
    scraper = BukalapakAPIScraper(delay_range=(2, 4))
    
    # Test queries
    test_queries = ["laptop", "smartphone", "headphone"]
    
    for query in test_queries:
        print(f"\n{'='*40}")
        print(f"API SCRAPING: {query.upper()}")
        print(f"{'='*40}")
        
        # Search products
        scraper.search_products(query=query, max_pages=2)
        
        # Get trending products
        scraper.get_trending_products(max_pages=1)
        
        # Get recommendations
        scraper.get_recommendations(max_pages=1)
        
        # Save data
        csv_file = scraper.save_to_csv(f"bukalapak_api_{query}.csv")
        json_file = scraper.save_to_json(f"bukalapak_api_{query}.json")
        
        # Show statistics
        stats = scraper.get_statistics()
        print(f"\nStatistics for {query}:")
        for key, value in stats.items():
            print(f"  {key}: {value}")
            
        # Clear data for next query
        scraper.clear_data()
        
    print("\nAPI Scraping completed!")

if __name__ == "__main__":
    main()