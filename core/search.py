import time
import random
import uuid
from bs4 import BeautifulSoup
from colorama import Fore
from selenium.webdriver.common.by import By
from core.driver import init_driver, get_free_proxy
import re
from urllib.parse import quote_plus
from core.terminal import log
from config import REQUEST_DELAY_SECONDS, USE_PROXY
import csv


def extract_product_info(driver, url, part_number):
    try:
        driver.get(url)
        time.sleep(3)
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")

        # Title
        title_tag = soup.find(id="productTitle")
        title = title_tag.get_text(strip=True) if title_tag else "N/A"

        # Validate part number in title
        if part_number.replace("-", "") not in title.replace("-", ""):
            return None

        # ASIN
        asin = url.split("/dp/")[1].split("/")[0] if "/dp/" in url else "N/A"

        # Feature bullets
        bullets_div = soup.find("div", id="feature-bullets")
        bullets = []
        if bullets_div:
            for li in bullets_div.select("li span.a-list-item"):
                line = li.get_text(strip=True)
                if line:
                    bullets.append(line)
        bullet_text = " | ".join(bullets) if bullets else "N/A"
        char_count = len(bullet_text.replace("|", "").strip()) if bullet_text != "N/A" else 0

        return {
            "PartNumber": part_number,
            "ASIN": asin,
            "Title": title,
            "URL": url,
            "Bullets": bullet_text,
            "CharCount": char_count
        }

    except Exception as e:
        log(f"❌ Extract error for {part_number}: {e}", Fore.RED)
        return None


def clean_amazon_url(url):
    match = re.search(r"(/dp/[A-Z0-9]{10})", url)
    return f"https://www.amazon.com{match.group(1)}" if match else url


def search_amazon(driver, part_number):
    try:
        query = f'"{part_number}"+Beck+Arnley'
        url = f"https://www.amazon.com/s?k={query}"
        log(f"🔍 Searching: {url}", Fore.YELLOW)
        driver.get(url)
        time.sleep(3)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        links = driver.find_elements(By.CSS_SELECTOR, 'a[href*="/dp/"]')
        for link in links:
            href = link.get_attribute("href")
            if href and "/dp/" in href:
                return clean_amazon_url(href)
        return None
    except Exception as e:
        log(f"❌ Amazon search error: {e}", Fore.RED)
        return None


def search_duckduckgo(driver, part_number):
    try:
        query = f'"{part_number}" Beck Arnley site:amazon.com'
        url = f"https://duckduckgo.com/?q={query.replace(' ', '+')}"
        log(f"🦆 DuckDuckGo fallback: {url}", Fore.MAGENTA)
        driver.get(url)
        time.sleep(3)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        links = driver.find_elements(By.CSS_SELECTOR, "a[href*='amazon.com']")
        for link in links:
            href = link.get_attribute("href")
            if href and "/dp/" in href:
                return href
        return None
    except Exception as e:
        log(f"❌ DuckDuckGo error: {e}", Fore.RED)
        return None


def search_google(driver, part_number):
    try:
        query = f'"{part_number}" Beck Arnley site:amazon.com'
        url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
        log(f"🌐 Google fallback: {url}", Fore.CYAN)
        driver.get(url)
        time.sleep(3)
        links = driver.find_elements(By.CSS_SELECTOR, "a")
        for link in links:
            href = link.get_attribute("href")
            if href and "amazon.com" in href and "/dp/" in href:
                return href
        return None
    except Exception as e:
        log(f"❌ Google error: {e}", Fore.RED)
        return None


def read_part_numbers(file_path):
    with open(file_path, newline='', encoding='utf-8') as f:
        return [row['PartNumber'].strip() for row in csv.DictReader(f)]


def lookup_part_number(part_number):
    driver = init_driver()
    
    for attempt in range(2):
        driver.delete_all_cookies()
        log(f"🔄 Attempt {attempt+1}/2", Fore.LIGHTBLACK_EX)
        url = search_amazon(driver, part_number)
        if url:
            info = extract_product_info(driver, url, part_number)
            if info:
                driver.quit()
                return info
        time.sleep(random.uniform(*REQUEST_DELAY_SECONDS))

    url = search_duckduckgo(driver, part_number)
    if url:
        info = extract_product_info(driver, url, part_number)
        if info:
            driver.quit()
            return info

    url = search_google(driver, part_number)
    if url:
        info = extract_product_info(driver, url, part_number)
        if info:
            driver.quit()
            return info

    driver.quit()
    return None
