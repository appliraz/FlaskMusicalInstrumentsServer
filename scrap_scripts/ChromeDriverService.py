from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
#from webdriver_manager.chrome import ChromeDriverManager
#import undetected_chromedriver as uc



"""
def getChromeOptions():
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Enable headless mode
    chrome_options.add_argument('--disable-gpu')  # Disable GPU acceleration (may be required in some cases)
    return chrome_options

"""
def getChromeOptions():
    chrome_options = Options()
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-crash-reporter")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-in-process-stack-traces")
    chrome_options.add_argument("--disable-logging")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disk-cache-size=0")
    chrome_options.add_argument("--log-level=3")
    chrome_options.add_argument("--output=/dev/null")
    chrome_options.add_argument("--user-data-dir=/tmp")


    return chrome_options

#chrome_driver = ChromeDriverManager().install()
chrome_options = getChromeOptions()
#service = Service(ChromeDriverManager().install())

def getSeleniumDriver():
    #driver = uc.Chrome(options=chrome_options)
    driver = webdriver.Chrome(options = chrome_options)
    #driver = webdriver.Chrome(chrome_driver)
    return driver

"""
def getSeleniumDriver():
    chrome_options = getChromeOptions()
    driver = webdriver.Chrome(getChromeDriverManager(), options=chrome_options)
    return driver
"""

def isWebdriver(loader):
    return type(loader) == webdriver.Chrome





