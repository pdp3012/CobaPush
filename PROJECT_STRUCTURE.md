# Bukalapak Scraper - Project Structure

## 📁 Complete Project Structure

```
bukalapak-scraper/
├── 📄 README.md                           # Comprehensive documentation
├── 📄 PROJECT_STRUCTURE.md                # This file - project structure
├── 📄 requirements.txt                    # Python dependencies
│
├── 🔧 Core Scrapers
│   ├── 📄 bukalapak_scraper.py           # Main scraper (API + CSS combined)
│   ├── 📄 bukalapak_api_scraper.py       # API-only scraper
│   └── 📄 bukalapak_css_scraper.py       # CSS Selector-only scraper
│
├── 🚀 Execution Scripts
│   ├── 📄 run_scraper.py                 # Simple interactive runner
│   ├── 📄 run_all_scrapers.py            # Comprehensive batch runner
│   └── 📄 example_usage.py               # Detailed usage examples
│
├── 🧪 Testing & Validation
│   └── 📄 test_scraper.py                # Comprehensive testing suite
│
├── 📊 Data Output (Auto-generated)
│   ├── 📁 data/
│   │   ├── 📁 csv/                       # CSV output files
│   │   ├── 📁 json/                      # JSON output files
│   │   ├── 📁 logs/                      # Log files
│   │   └── 📁 reports/                   # Analysis reports
│   └── 📄 bukalapak_scraper.log          # Main log file
│
└── 📚 Documentation
    └── 📄 README.md                      # Main documentation
```

## 🎯 File Descriptions

### Core Scrapers

#### `bukalapak_scraper.py`
- **Purpose**: Main scraper combining API and CSS Selector approaches
- **Features**: 
  - Dual scraping methods (API + CSS)
  - Anti-detection mechanisms
  - Comprehensive data extraction
  - Statistics generation
  - Multiple export formats

#### `bukalapak_api_scraper.py`
- **Purpose**: Dedicated API scraper
- **Features**:
  - Multiple API endpoints
  - Trending products
  - Recommendations
  - Detailed product information
  - Advanced error handling

#### `bukalapak_css_scraper.py`
- **Purpose**: Dedicated CSS Selector scraper
- **Features**:
  - Multiple selector strategies
  - Fallback mechanisms
  - Stealth browser settings
  - Robust element detection

### Execution Scripts

#### `run_scraper.py`
- **Purpose**: Simple interactive scraper runner
- **Features**:
  - User-friendly interface
  - Method selection
  - Query input
  - Basic statistics

#### `run_all_scrapers.py`
- **Purpose**: Comprehensive batch execution
- **Features**:
  - All methods execution
  - Detailed reporting
  - Performance monitoring
  - Error tracking

#### `example_usage.py`
- **Purpose**: Detailed usage examples
- **Features**:
  - Multiple scenarios
  - Comparison analysis
  - Advanced configurations
  - Best practices

### Testing & Validation

#### `test_scraper.py`
- **Purpose**: Comprehensive testing suite
- **Features**:
  - Unit tests for each scraper
  - Data validation tests
  - Error handling tests
  - Performance benchmarks

### Configuration Files

#### `requirements.txt`
```
requests==2.31.0
beautifulsoup4==4.12.2
selenium==4.15.2
pandas==2.1.3
lxml==4.9.3
fake-useragent==1.4.0
webdriver-manager==4.0.1
```

## 🚀 Quick Start Guide

### 1. Installation
```bash
# Clone repository
git clone <repository-url>
cd bukalapak-scraper

# Install dependencies
pip install -r requirements.txt

# Install Chrome/Chromium (for Selenium)
# Ubuntu/Debian: sudo apt-get install chromium-browser
# macOS: brew install chromium
```

### 2. Simple Usage
```bash
# Run simple interactive scraper
python run_scraper.py

# Run comprehensive testing
python test_scraper.py

# Run all scrapers with detailed reporting
python run_all_scrapers.py
```

### 3. Advanced Usage
```python
# Import scrapers
from bukalapak_scraper import BukalapakScraper
from bukalapak_api_scraper import BukalapakAPIScraper
from bukalapak_css_scraper import BukalapakCSSScraper

# Use main scraper
scraper = BukalapakScraper(headless=True)
scraper.scrape_via_api(search_query="laptop", max_pages=3)
scraper.scrape_via_css_selector(search_query="laptop", max_pages=3)
scraper.save_to_csv("output.csv")
```

## 📊 Data Output Structure

### CSV Output Format
```csv
nama_produk,harga,jumlah_terjual,nama_toko,lokasi_toko,rating_produk,url_produk,metode_scraping,timestamp_scraping
Laptop Gaming Asus ROG,15000000,45,Toko Elektronik,Jakarta,4.5,https://...,API,2024-01-15T10:30:00
```

### JSON Output Format
```json
{
  "nama_produk": "Laptop Gaming Asus ROG",
  "harga": 15000000,
  "jumlah_terjual": 45,
  "nama_toko": "Toko Elektronik",
  "lokasi_toko": "Jakarta",
  "rating_produk": 4.5,
  "url_produk": "https://...",
  "metode_scraping": "API",
  "timestamp_scraping": "2024-01-15T10:30:00"
}
```

## 🛡️ Anti-Detection Features

### User Agent Rotation
- Automatic User-Agent rotation
- Realistic browser headers
- Session management

### Stealth Browser Settings
- Headless mode support
- Anti-automation detection
- Realistic browser behavior

### Rate Limiting
- Configurable delays
- Random timing
- Retry mechanisms

## 📈 Statistics & Analytics

### Available Metrics
- Total products scraped
- Average price analysis
- Rating distribution
- Store analysis
- Method comparison
- Success rates

### Report Types
- Comprehensive JSON reports
- Summary CSV reports
- Detailed text analysis
- Performance metrics

## 🔧 Configuration Options

### Delay Settings
```python
# Conservative (recommended)
scraper = BukalapakScraper(delay_range=(3, 7))

# Aggressive (risky)
scraper = BukalapakScraper(delay_range=(1, 2))
```

### Browser Settings
```python
# Headless mode (recommended)
scraper = BukalapakCSSScraper(headless=True)

# Visible browser (debugging)
scraper = BukalapakCSSScraper(headless=False)
```

## 🧪 Testing Framework

### Test Categories
1. **API Scraper Tests**
   - Search functionality
   - Data structure validation
   - Error handling

2. **CSS Scraper Tests**
   - Element detection
   - Selector fallbacks
   - Browser automation

3. **Main Scraper Tests**
   - Combined functionality
   - Statistics generation
   - Data saving

4. **Data Validation Tests**
   - Data quality checks
   - Field validation
   - Format verification

5. **Error Handling Tests**
   - Network failures
   - Invalid queries
   - Rate limiting

## 📝 Logging & Monitoring

### Log Levels
- **INFO**: General progress
- **WARNING**: Non-critical issues
- **ERROR**: Critical failures
- **DEBUG**: Detailed debugging

### Log Files
- `bukalapak_scraper.log`: Main application logs
- `data/logs/`: Detailed execution logs
- Console output: Real-time progress

## 🎯 Best Practices

### Performance
- Start with small datasets
- Monitor resource usage
- Use appropriate delays
- Implement proper error handling

### Data Quality
- Validate scraped data
- Check for missing fields
- Verify data consistency
- Monitor success rates

### Legal Compliance
- Respect robots.txt
- Don't overload servers
- Use for educational purposes
- Comply with terms of service

## 🔍 Troubleshooting

### Common Issues
1. **ChromeDriver not found**
   - Install webdriver-manager
   - Check Chrome installation

2. **Rate limiting**
   - Increase delay settings
   - Monitor response codes

3. **Element not found**
   - Check selector updates
   - Verify website changes

4. **API errors**
   - Verify endpoints
   - Check request headers

## 📞 Support & Maintenance

### Monitoring
- Regular testing
- Performance monitoring
- Error tracking
- Data quality checks

### Updates
- Selector maintenance
- API endpoint updates
- Dependency updates
- Feature enhancements

---

**Dibuat dengan ❤️ oleh Dosen Data Mining (30 tahun pengalaman)**
**Sertifikasi: International Data Mining Certification**