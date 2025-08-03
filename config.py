"""
Konfigurasi untuk Shopee Scraper
Centralized configuration untuk semua pengaturan
"""

# ============================================================================
# LOGIN CREDENTIALS
# ============================================================================
LOGIN_CONFIG = {
    'phone': '081316084860',
    'password': 'Pradipta301203',
    'login_url': 'https://shopee.co.id/buyer/login'
}

# ============================================================================
# BROWSER CONFIGURATION
# ============================================================================
BROWSER_CONFIG = {
    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'timeout': 10,
    'implicit_wait': 5,
    'page_load_timeout': 30
}

# ============================================================================
# CSS SELECTORS
# ============================================================================
CSS_SELECTORS = {
    'product_name': 'div.line-clamp-2',
    'product_price': 'span.font-medium.text-base\\/5.truncate',
    'product_sold': 'div.truncate.text-shopee-black87.text-xs.min-h-4',
    'shop_location': 'div.flex-shrink.min-w-0.truncate.text-shopee-black54',
    'product_rating': 'div.text-shopee-black87.text-xs\\/sp14.flex-none',
    'shop_name': [
        'div.text-shopee-black87.text-xs.min-h-4',
        'div.flex-shrink.min-w-0.truncate.text-shopee-black87',
        'div[data-sqe="link"] div.text-shopee-black87'
    ]
}

# ============================================================================
# SCRAPING CONFIGURATION
# ============================================================================
SCRAPING_CONFIG = {
    'default_max_products': 50,
    'scroll_count': 5,
    'scroll_delay': 2,
    'page_load_delay': 5,
    'search_url_template': 'https://shopee.co.id/search?keyword={keyword}'
}

# ============================================================================
# OUTPUT CONFIGURATION
# ============================================================================
OUTPUT_CONFIG = {
    'csv_encoding': 'utf-8',
    'json_encoding': 'utf-8',
    'filename_template': 'shopee_{keyword}',
    'default_output_dir': './output'
}

# ============================================================================
# ERROR HANDLING
# ============================================================================
ERROR_CONFIG = {
    'max_retries': 3,
    'retry_delay': 2,
    'captcha_timeout': 60,
    'login_timeout': 30
}

# ============================================================================
# ANTI-DETECTION SETTINGS
# ============================================================================
ANTI_DETECTION_CONFIG = {
    'enable_stealth': True,
    'random_delays': True,
    'min_delay': 1,
    'max_delay': 3,
    'rotate_user_agents': False
}

# ============================================================================
# LOGGING CONFIGURATION
# ============================================================================
LOGGING_CONFIG = {
    'log_level': 'INFO',
    'log_file': 'shopee_scraper.log',
    'log_format': '%(asctime)s - %(levelname)s - %(message)s'
}

# ============================================================================
# VALIDATION RULES
# ============================================================================
VALIDATION_RULES = {
    'min_product_name_length': 3,
    'max_product_name_length': 200,
    'price_patterns': [
        r'Rp\s*\d{1,3}(?:\.\d{3})*',
        r'\d{1,3}(?:\.\d{3})*\s*Rp',
        r'IDR\s*\d{1,3}(?:\.\d{3})*'
    ],
    'rating_patterns': [
        r'\d+\.\d+',
        r'\d+\s*\(\d+[^)]*\)',
        r'\d+\s*stars?'
    ]
}

# ============================================================================
# DEBUG MODE
# ============================================================================
DEBUG_MODE = {
    'enabled': False,
    'save_html': False,
    'verbose_logging': False,
    'show_browser': True
}

# ============================================================================
# LEGAL COMPLIANCE
# ============================================================================
LEGAL_CONFIG = {
    'respect_robots_txt': True,
    'max_requests_per_minute': 30,
    'user_agent_disclosure': True,
    'terms_of_service_url': 'https://shopee.co.id/terms'
}