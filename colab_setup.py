# Setup untuk Google Colab
import subprocess
import sys

def install_chrome_driver():
    """Install Chrome driver untuk Google Colab"""
    print("Installing Chrome driver...")
    
    # Install Chrome
    !apt-get update
    !apt-get install -y wget unzip
    !wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add -
    !echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list
    !apt-get update
    !apt-get install -y google-chrome-stable
    
    # Install ChromeDriver
    !wget -O /tmp/chromedriver.zip https://chromedriver.storage.googleapis.com/120.0.6099.109/chromedriver_linux64.zip
    !unzip /tmp/chromedriver.zip -d /usr/local/bin/
    !chmod +x /usr/local/bin/chromedriver
    
    print("Chrome driver installation completed!")

def install_requirements():
    """Install semua requirements"""
    print("Installing required packages...")
    
    packages = [
        'requests==2.31.0',
        'beautifulsoup4==4.12.2',
        'selenium==4.15.2',
        'pandas==2.1.3',
        'openpyxl==3.1.2',
        'lxml==4.9.3',
        'urllib3==2.0.7'
    ]
    
    for package in packages:
        !pip install {package}
    
    print("All packages installed successfully!")

if __name__ == "__main__":
    print("Setting up Google Colab environment...")
    install_chrome_driver()
    install_requirements()
    print("Setup completed! You can now run the Shopee scraper.")