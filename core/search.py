import time
import random
import uuid
from bs4 import BeautifulSoup
from colorama import Fore
from selenium.webdriver.common.by import By
from core.driver import init_driver
from core.terminal import log
from core.scraper import search_duckduckgo, search_google
from config import REQUEST_DELAY_SECONDS, USE_PROXY, PROXY_USER, PROXY_PASS, PROXY_GATE, PROXY_PORT


def get_free_proxy():
    session = uuid.uuid4().hex[:8]
    return f"http://{PROXY_USER}-session-{session}:{PROXY_PASS}@{PROXY_GATE}:{PROXY_PORT}"


def log_duckduckgo_fallback(url):
    log(f"🦆 DuckDuckGo fallback: {url}", Fore.MAGENTA)


def log_google_fallback(url):
    log(f"🌐 Google fallback: {url}", Fore.YELLOW)


def log_proxy_attempt(attempt):
    log(f"🔁 Proxy Attempt {attempt+1}/2", Fore.LIGHTBLACK_EX)


def log_proxy_error(e):
    log(f"❌ Proxy search error: {e}", Fore.RED)


def log_missing():
    log(f"❌ PRODUCT MISSING", Fore.RED)


def search_amazon(driver, part_number):
    try:
        query = f'"{part_number}"+Beck+Arnley'
        url = f"https://www.amazon.com/s?k={query}"
        log(f"🔍 Searching: {url}", Fore.CYAN)
        driver.get(url)
        time.sleep(3)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        links = driver.find_elements(By.CSS_SELECTOR, 'a[href*="/dp/"]')
        for link in links:
            href = link.get_attribute("href")
            if href and "/dp/" in href:
                return extract_product_info(driver, href, part_number), href
        return None, None
    except Exception as e:
        log(f"❌ Amazon search error: {e}", Fore.RED)
        return None, None
    return None


def extract_product_info(driver, url, part_number):
    try:
        driver.get(url)
        time.sleep(3)
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")

        title_elem = soup.find(id="productTitle")
        brand_elem = soup.find(id="bylineInfo") or soup.find("a", id="brand")
        bullets_elem = soup.find("div", id="feature-bullets")

        if not title_elem:
            return None

        title = title_elem.get_text(strip=True)
        if part_number.replace("-", "") not in title.replace("-", ""):
            return None
        brand = brand_elem.get_text(strip=True) if brand_elem else "N/A"
        bullets = [li.get_text(strip=True) for li in bullets_elem.find_all("li") if li] if bullets_elem else []

        asin = url.split("/dp/")[1].split("/")[0] if "/dp/" in url else "N/A"

        return {
            "Title": title,
            "Brand": brand,
            "ASIN": asin,
            "Bullets": bullets,
            "URL": url
        }
    except Exception as e:
        log(f"❌ Extract error for {part_number}: {e}", Fore.RED)
        return None


def lookup_part_number(part_number):
    driver = init_driver()

    for attempt in range(2):
        log(f"🔄 Attempt {attempt+1}/2", Fore.LIGHTBLACK_EX)
        info, url = search_amazon(driver, part_number)
        if info:
            if info:
                driver.quit()
                return info["Title"], url
        time.sleep(random.uniform(*REQUEST_DELAY_SECONDS))

    url = search_duckduckgo(driver, part_number)
    if url:
        log_duckduckgo_fallback(url)
        info = extract_product_info(driver, url, part_number)
        if info:
            driver.quit()
            return info["Title"], url

    url = search_google(driver, part_number)
    if url:
        log_google_fallback(url)
        info = extract_product_info(driver, url, part_number)
        if info:
            driver.quit()
            return info["Title"], url

    driver.quit()

    if USE_PROXY:
        for attempt in range(2):
            log_proxy_attempt(attempt)
            proxy_url = get_free_proxy()
            proxy_driver = init_driver(proxy=proxy_url)
            try:
                info, url = search_amazon(proxy_driver, part_number)
                if info:
                    if info:
                        proxy_driver.quit()
                        return info["Title"], url
            except Exception as e:
                log_proxy_error(e)
            finally:
                proxy_driver.quit()

    log_missing()
    return None, None
