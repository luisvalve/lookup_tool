# lookup_tool/core/driver.py
from selenium.webdriver.chrome.options import Options
from undetected_chromedriver import Chrome
from core.logger import logger
import random

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.5672.92 Safari/537.36"
]


def random_user_agent():
    return random.choice(USER_AGENTS)


def init_driver(proxy=None):
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-extensions")
    options.add_argument("--start-maximized")

    user_agent = random_user_agent()
    options.add_argument(f"--user-agent={user_agent}")

    if proxy:
        options.add_argument(f"--proxy-server={proxy}")
        logger.info(f"🌍 Proxy applied to browser: {proxy}")

    driver = Chrome(options=options)
    driver.set_page_load_timeout(30)
    return driver
