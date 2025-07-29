# Setup untuk Google Colab
# Jalankan cell ini terlebih dahulu sebelum menjalankan scraper

import subprocess
import sys

def install_requirements():
    """Install semua dependencies yang diperlukan"""
    print("Installing dependencies...")
    
    packages = [
        'selenium==4.15.2',
        'pandas==2.1.3',
        'requests==2.31.0',
        'fake-useragent==1.4.0',
        'webdriver-manager==4.0.1',
        'beautifulsoup4==4.12.2',
        'lxml==4.9.3'
    ]
    
    for package in packages:
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
            print(f"✓ {package} installed successfully")
        except subprocess.CalledProcessError:
            print(f"✗ Failed to install {package}")

def setup_chrome_driver():
    """Setup Chrome driver untuk Colab"""
    print("Setting up Chrome driver...")
    
    # Install Chrome
    !apt-get update
    !apt-get install -y wget unzip
    !wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add -
    !echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list
    !apt-get update
    !apt-get install -y google-chrome-stable
    
    # Install ChromeDriver
    !wget -N https://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_linux64.zip
    !unzip -o chromedriver_linux64.zip
    !chmod +x chromedriver
    !mv chromedriver /usr/local/bin/
    
    print("✓ Chrome and ChromeDriver setup completed")

def setup_environment():
    """Setup complete environment"""
    print("=== SETUP GOOGLE COLAB ENVIRONMENT ===")
    
    # Install dependencies
    install_requirements()
    
    # Setup Chrome driver
    setup_chrome_driver()
    
    print("\n=== SETUP SELESAI ===")
    print("Sekarang Anda dapat menjalankan scraper!")

# Jalankan setup
if __name__ == "__main__":
    setup_environment()