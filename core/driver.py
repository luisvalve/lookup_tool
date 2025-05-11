from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from undetected_chromedriver import Chrome, ChromeOptions

from config import USE_PROXY, PROXY_URL


def create_browser():
    options = ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.headless = False  # Set True to run in headless mode

    if USE_PROXY and PROXY_URL:
        options.add_argument(f'--proxy-server={PROXY_URL}')

    driver = Chrome(options=options)
    driver.set_page_load_timeout(30)
    return driver

