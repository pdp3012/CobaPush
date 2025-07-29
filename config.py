# Configuration file untuk Advanced Shopee Scraper
# Dibuat oleh: Dosen Data Mining dengan 30 tahun pengalaman

# ============================================================================
# SCRAPING CONFIGURATION
# ============================================================================

# Default settings untuk scraping
DEFAULT_MAX_PRODUCTS = 50
DEFAULT_DELAY_MIN = 2
DEFAULT_DELAY_MAX = 5
DEFAULT_TIMEOUT = 15
DEFAULT_MAX_RETRIES = 3

# ============================================================================
# ANTI-BOT CONFIGURATION
# ============================================================================

# User agents untuk rotating
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/121.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
]

# Chrome options untuk anti-detection
CHROME_OPTIONS = [
    '--no-sandbox',
    '--disable-dev-shm-usage',
    '--disable-blink-features=AutomationControlled',
    '--disable-web-security',
    '--allow-running-insecure-content',
    '--disable-features=VizDisplayCompositor',
    '--disable-ipc-flooding-protection',
    '--disable-extensions',
    '--disable-plugins',
    '--disable-images',
    '--disable-javascript',
    '--disable-gpu',
    '--disable-software-rasterizer',
    '--disable-background-timer-throttling',
    '--disable-backgrounding-occluded-windows',
    '--disable-renderer-backgrounding',
    '--disable-features=TranslateUI',
    '--headless'
]

# ============================================================================
# SELECTORS CONFIGURATION
# ============================================================================

# Multiple selectors untuk product elements
PRODUCT_SELECTORS = [
    "div[data-sqe='link']",
    ".shopee-search-item-result__item",
    "[data-testid='product-card']",
    ".col-xs-2-4",
    ".shopee-item-card",
    ".shopee-search-item-result__item-name"
]

# Selectors untuk nama produk
NAME_SELECTORS = [
    'div[data-sqe="name"]',
    '.ie3A\+n',
    '.Cve6sh',
    '[data-testid="product-card"] .ie3A\+n',
    '.shopee-search-item-result__item-name',
    '.shopee-item-card__text-name'
]

# Selectors untuk harga
PRICE_SELECTORS = [
    'div[data-sqe="price"]',
    '.vioxXd',
    '.ZEgDH9',
    '[data-testid="product-card"] .vioxXd',
    '.shopee-search-item-result__item-price',
    '.shopee-item-card__text-price'
]

# Selectors untuk rating
RATING_SELECTORS = [
    'div[data-sqe="rating"]',
    '.shopee-rating-stars__stars',
    '.shopee-rating-stars__stars--active',
    '[data-testid="product-card"] .shopee-rating-stars',
    '.shopee-item-card__rating'
]

# Selectors untuk jumlah terjual
SOLD_SELECTORS = [
    'div[data-sqe="sold"]',
    '.r6HknA',
    '.shopee-search-item-result__item-sold',
    '[data-testid="product-card"] .r6HknA',
    '.shopee-item-card__sold'
]

# Selectors untuk nama toko
SHOP_SELECTORS = [
    'div[data-sqe="shop"]',
    '.shopee-search-item-result__shop-name',
    '.shopee-search-item-result__item-shop',
    '[data-testid="product-card"] .shopee-search-item-result__shop-name',
    '.shopee-item-card__shop-name'
]

# Selectors untuk lokasi toko
LOCATION_SELECTORS = [
    'div[data-sqe="location"]',
    '.shopee-search-item-result__shop-location',
    '.shopee-search-item-result__item-location',
    '[data-testid="product-card"] .shopee-search-item-result__shop-location',
    '.shopee-item-card__shop-location'
]

# ============================================================================
# URL CONFIGURATION
# ============================================================================

# Base URL untuk Shopee
SHOPEE_BASE_URL = "https://shopee.co.id"
SHOPEE_SEARCH_URL = "https://shopee.co.id/search"

# ============================================================================
# OUTPUT CONFIGURATION
# ============================================================================

# Output format settings
CSV_ENCODING = 'utf-8-sig'
EXCEL_SHEET_NAME = 'Shopee Data'
DEFAULT_FILENAME_PREFIX = 'shopee'

# ============================================================================
# LOGGING CONFIGURATION
# ============================================================================

# Log levels
LOG_LEVEL = 'INFO'
LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'

# ============================================================================
# PERFORMANCE CONFIGURATION
# ============================================================================

# Performance settings
SCROLL_STEP_MIN = 300
SCROLL_STEP_MAX = 700
SCROLL_DELAY_MIN = 0.5
SCROLL_DELAY_MAX = 1.5

# Window size range
WINDOW_WIDTH_MIN = 1200
WINDOW_WIDTH_MAX = 1920
WINDOW_HEIGHT_MIN = 800
WINDOW_HEIGHT_MAX = 1080

# ============================================================================
# ERROR HANDLING CONFIGURATION
# ============================================================================

# Error handling settings
MAX_CONNECTION_RETRIES = 3
CONNECTION_TIMEOUT = 30
PAGE_LOAD_TIMEOUT = 15

# ============================================================================
# VALIDATION CONFIGURATION
# ============================================================================

# Validation settings
MIN_PRODUCT_NAME_LENGTH = 3
MAX_PRODUCT_NAME_LENGTH = 200
MIN_PRICE_VALUE = 0
MAX_PRICE_VALUE = 999999999

# ============================================================================
# EXAMPLE KEYWORDS
# ============================================================================

# Contoh keywords yang baik untuk testing
EXAMPLE_KEYWORDS = [
    "laptop gaming asus",
    "smartphone samsung galaxy",
    "baju muslim wanita",
    "sepatu nike air max",
    "cabai rawit merah",
    "beras organik premium",
    "handphone xiaomi",
    "laptop lenovo thinkpad",
    "sepatu adidas ultraboost",
    "baju pria formal"
]

# ============================================================================
# CATEGORY KEYWORDS
# ============================================================================

# Keywords berdasarkan kategori
CATEGORY_KEYWORDS = {
    "elektronik": [
        "laptop gaming",
        "smartphone",
        "tablet",
        "headphone",
        "speaker bluetooth"
    ],
    "fashion": [
        "baju muslim",
        "sepatu nike",
        "tas wanita",
        "jam tangan",
        "kemeja pria"
    ],
    "makanan": [
        "cabai rawit",
        "beras organik",
        "minyak goreng",
        "gula pasir",
        "tepung terigu"
    ],
    "kesehatan": [
        "vitamin c",
        "masker wajah",
        "sabun mandi",
        "sikat gigi",
        "handuk"
    ],
    "rumah_tangga": [
        "panci masak",
        "kompor gas",
        "kulkas mini",
        "blender",
        "rice cooker"
    ]
}

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def get_random_user_agent():
    """Get random user agent dari list"""
    import random
    return random.choice(USER_AGENTS)

def get_random_window_size():
    """Get random window size"""
    import random
    width = random.randint(WINDOW_WIDTH_MIN, WINDOW_WIDTH_MAX)
    height = random.randint(WINDOW_HEIGHT_MIN, WINDOW_HEIGHT_MAX)
    return width, height

def get_random_scroll_step():
    """Get random scroll step"""
    import random
    return random.randint(SCROLL_STEP_MIN, SCROLL_STEP_MAX)

def get_random_scroll_delay():
    """Get random scroll delay"""
    import random
    return random.uniform(SCROLL_DELAY_MIN, SCROLL_DELAY_MAX)

def validate_product_data(data):
    """Validate product data"""
    if not data:
        return False
    
    # Check required fields
    required_fields = ['Nama Produk', 'Harga']
    for field in required_fields:
        if field not in data or not data[field]:
            return False
    
    # Validate product name length
    if len(data['Nama Produk']) < MIN_PRODUCT_NAME_LENGTH:
        return False
    
    # Validate price
    try:
        price = int(data['Harga'])
        if price < MIN_PRICE_VALUE or price > MAX_PRICE_VALUE:
            return False
    except:
        return False
    
    return True

def get_category_keywords(category):
    """Get keywords untuk kategori tertentu"""
    return CATEGORY_KEYWORDS.get(category, [])

def get_all_keywords():
    """Get semua keywords dari semua kategori"""
    all_keywords = []
    for category_keywords in CATEGORY_KEYWORDS.values():
        all_keywords.extend(category_keywords)
    return all_keywords