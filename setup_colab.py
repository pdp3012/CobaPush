# Setup untuk Google Colab - Shopee Scraper
# Jalankan cell ini terlebih dahulu sebelum menggunakan scraper

import subprocess
import sys
import os

def install_packages():
    """Install semua package yang diperlukan"""
    packages = [
        'selenium',
        'beautifulsoup4',
        'pandas',
        'openpyxl',
        'requests',
        'lxml'
    ]
    
    print("📦 Installing required packages...")
    for package in packages:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"✅ {package} installed successfully")
        except subprocess.CalledProcessError:
            print(f"❌ Failed to install {package}")

def setup_chrome_driver():
    """Setup Chrome driver untuk Google Colab"""
    print("🔧 Setting up Chrome driver...")
    
    # Install Chrome
    !apt-get update
    !apt-get install -y wget unzip
    
    # Download Chrome
    !wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add -
    !echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list
    !apt-get update
    !apt-get install -y google-chrome-stable
    
    # Download ChromeDriver
    !wget -O /tmp/chromedriver.zip https://chromedriver.storage.googleapis.com/$(curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE)/chromedriver_linux64.zip
    !unzip /tmp/chromedriver.zip -d /usr/local/bin/
    !chmod +x /usr/local/bin/chromedriver
    
    print("✅ Chrome driver setup completed")

def setup_environment():
    """Setup environment untuk scraping"""
    print("🌍 Setting up environment...")
    
    # Set environment variables
    os.environ['WDM_LOG_LEVEL'] = '0'
    os.environ['WDM_LOCAL'] = '1'
    
    print("✅ Environment setup completed")

def main():
    """Setup utama untuk Google Colab"""
    print("🚀 SHOPEE SCRAPER SETUP FOR GOOGLE COLAB")
    print("=" * 50)
    
    try:
        # Install packages
        install_packages()
        
        # Setup Chrome driver
        setup_chrome_driver()
        
        # Setup environment
        setup_environment()
        
        print("\n🎉 Setup completed successfully!")
        print("✅ You can now use the Shopee scraper")
        
    except Exception as e:
        print(f"❌ Setup failed: {e}")

if __name__ == "__main__":
    main()

# Alternatif setup yang lebih sederhana
def quick_setup():
    """Setup cepat untuk Google Colab"""
    print("⚡ Quick setup for Google Colab...")
    
    # Install packages
    !pip install selenium beautifulsoup4 pandas openpyxl requests lxml
    
    # Install Chrome
    !apt-get update
    !apt-get install -y wget unzip
    !wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add -
    !echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list
    !apt-get update
    !apt-get install -y google-chrome-stable
    
    # Download ChromeDriver
    !wget -O /tmp/chromedriver.zip https://chromedriver.storage.googleapis.com/$(curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE)/chromedriver_linux64.zip
    !unzip /tmp/chromedriver.zip -d /usr/local/bin/
    !chmod +x /usr/local/bin/chromedriver
    
    print("✅ Quick setup completed!")

# Jalankan quick setup
quick_setup()