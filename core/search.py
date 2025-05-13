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
    """
    Extracts and validates product information from Amazon product page.
    
    Validation steps:
    1. Verify page loads completely (3s wait)
    2. Check if part number exists in title
    3. Extract product features and metadata
    
    Returns None if:
    - Page doesn't load
    - Part number not in title
    - Required elements missing
    """
    try:
        driver.get(url)
        time.sleep(3)  # Wait for dynamic content (TODO: Replace with explicit wait)
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")

        # Extract product title from the main product heading
        # Amazon consistently uses 'productTitle' ID for this element
        title_tag = soup.find(id="productTitle")
        title = title_tag.get_text(strip=True) if title_tag else "N/A"

        # Validate part number exists in title (ignore hyphen formatting)
        # Example: "103-2925" should match "1032925" or "103-2925"
        if part_number.replace("-", "") not in title.replace("-", ""):
            return None

        # Extract ASIN (Amazon Standard Identification Number)
        # Format: /dp/XXXXXXXXXX where X is alphanumeric
        asin = url.split("/dp/")[1].split("/")[0] if "/dp/" in url else "N/A"

        # Extract product feature bullets
        # These provide detailed product information and specifications
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
    """
    Standardizes Amazon product URLs to their canonical form.
    
    Transforms URLs to format: https://www.amazon.com/dp/ASIN
    - Removes tracking parameters
    - Removes session IDs
    - Extracts ASIN (10-character product ID)
    
    Example:
    Input:  https://www.amazon.com/Beck-Arnley-103-2925-Joint-Boot/dp/B000EOJ288?ref=...
    Output: https://www.amazon.com/dp/B000EOJ288
    """
    # Extract the ASIN pattern (/dp/XXXXXXXXXX) from the URL
    match = re.search(r"(/dp/[A-Z0-9]{10})", url)
    # Return canonical URL if ASIN found, otherwise return original URL
    return f"https://www.amazon.com{match.group(1)}" if match else url


def search_amazon(driver, part_number):
    """
    Performs direct Amazon search with specific optimizations.
    
    Search strategy:
    1. Use exact part number in quotes for precise matching
    2. Include brand name to filter relevant results
    3. Scroll to bottom to load all results
    
    Timing:
    - 3s initial wait: Allow for dynamic content load
    - 2s after scroll: Wait for lazy-loaded results
    """
    try:
        # Format query with exact part number match and brand
        # Example: "103-2925"+Beck+Arnley ensures part number is treated as one unit
        query = f'"{part_number}"+Beck+Arnley'
        url = f"https://www.amazon.com/s?k={query}"
        log(f"🔍 Searching: {url}", Fore.YELLOW)
        
        # Load search results page
        driver.get(url)
        time.sleep(3)  # Wait for initial content load
        
        # Scroll to trigger lazy loading of additional results
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Wait for lazy-loaded content
        
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
    """
    Fallback search using DuckDuckGo to find Amazon product.
    
    Strategy:
    1. Search DuckDuckGo with part number and site:amazon.com
    2. Extract Amazon product links from results
    3. Validate URLs contain product ASIN
    """
    try:
        # Use site-specific search to limit results to Amazon
        query = f'"{part_number}" Beck Arnley site:amazon.com'
        url = f"https://duckduckgo.com/?q={query.replace(' ', '+')}"
        log(f"🦆 DuckDuckGo fallback: {url}", Fore.MAGENTA)
        
        driver.get(url)
        time.sleep(3)  # Allow for results to load
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Wait for any dynamic content
        
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
    """
    Final fallback using Google search for Amazon products.
    
    Strategy:
    1. Use site-restricted search on Google
    2. Look for direct Amazon product links
    3. Validate found URLs contain ASIN
    """
    try:
        query = f'"{part_number}" Beck Arnley site:amazon.com'
        url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
        log(f"🌐 Google fallback: {url}", Fore.CYAN)
        
        driver.get(url)
        time.sleep(3)  # Allow for results to load
        
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
    """
    Reads part numbers from CSV file.
    Expects CSV with header 'PartNumber' and one number per line.
    """
    with open(file_path, newline='', encoding='utf-8') as f:
        return [row['PartNumber'].strip() for row in csv.DictReader(f)]


def lookup_part_number(part_number):
    """
    Multi-stage product lookup with fallback strategies.
    
    Search flow:
    1. Try Amazon direct search twice (with cookie reset)
    2. If no match, fallback to DuckDuckGo search on Amazon
    3. If still no match, try Google search as last resort
    
    Anti-detection measures:
    - Cookie clearing between attempts
    - Random delays between requests
    - Browser fingerprint masking
    """
    driver = init_driver()
    
    # Primary search: Try Amazon twice with fresh cookies
    # Two attempts help bypass temporary search anomalies
    for attempt in range(2):
        driver.delete_all_cookies()  # Reset session to avoid search history bias
        log(f"🔄 Attempt {attempt+1}/2", Fore.LIGHTBLACK_EX)
        url = search_amazon(driver, part_number)
        if url:
            info = extract_product_info(driver, url, part_number)
            if info:
                driver.quit()
                return info
        # Random delay to mimic human behavior
        time.sleep(random.uniform(*REQUEST_DELAY_SECONDS))

    # First fallback: DuckDuckGo search
    url = search_duckduckgo(driver, part_number)
    if url:
        info = extract_product_info(driver, url, part_number)
        if info:
            driver.quit()
            return info

    # Final fallback: Google search
    url = search_google(driver, part_number)
    if url:
        info = extract_product_info(driver, url, part_number)
        if info:
            driver.quit()
            return info

    driver.quit()
    return None
