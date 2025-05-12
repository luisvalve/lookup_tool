import time
import random
import uuid
from bs4 import BeautifulSoup
from colorama import Fore
from selenium.webdriver.common.by import By
from core.driver import init_driver, get_free_proxy
from core.terminal import log
from config import REQUEST_DELAY_SECONDS, USE_PROXY


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


def lookup_part_number(part_number):
    driver = init_driver()
    from core.scraper import search_amazon, search_duckduckgo, search_google
    from urllib.parse import quote_plus

    for attempt in range(2):
        log(f"🔄 Attempt {attempt+1}/2", Fore.LIGHTBLACK_EX)
        url = search_amazon(driver, part_number)
        if url:
            info = extract_product_info(driver, url, part_number)
            if info and part_number.replace("-", "") in info["Title"].replace("-", ""):
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
