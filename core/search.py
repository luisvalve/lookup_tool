
import time
import random
import uuid
from colorama import Fore
from core.driver import init_driver
from core.logger import logger
from core.scraper import search_amazon, search_duckduckgo, search_google, extract_product_info
from config import REQUEST_DELAY_SECONDS, USE_PROXY, PROXY_USER, PROXY_PASS, PROXY_GATE, PROXY_PORT


def get_free_proxy():
    session = uuid.uuid4().hex[:8]
    return f"http://{PROXY_USER}-session-{session}:{PROXY_PASS}@{PROXY_GATE}:{PROXY_PORT}"


def lookup_part_number(part_number):
    driver = init_driver()

    for attempt in range(2):
        logger.info(f"🔄 Attempt {attempt+1}/2", extra={"color": Fore.LIGHTBLACK_EX})
        url = search_amazon(driver, part_number)
        if url:
            info = extract_product_info(driver, url, part_number)
            if info and part_number.replace("-", "") in info["Title"].replace("-", ""):
                driver.quit()
                return info["Title"], url
        time.sleep(random.uniform(*REQUEST_DELAY_SECONDS))

    url = search_duckduckgo(driver, part_number)
    if url:
        info = extract_product_info(driver, url, part_number)
        if info:
            driver.quit()
            return info["Title"], url

    url = search_google(driver, part_number)
    if url:
        info = extract_product_info(driver, url, part_number)
        if info:
            driver.quit()
            return info["Title"], url

    driver.quit()

    if USE_PROXY:
        for attempt in range(2):
            logger.info(f"🔁 Proxy Attempt {attempt+1}/2")
            proxy_url = get_free_proxy()
            proxy_driver = init_driver(proxy=proxy_url)
            try:
                url = search_amazon(proxy_driver, part_number)
                if url:
                    info = extract_product_info(proxy_driver, url, part_number)
                    if info and part_number.replace("-", "") in info["Title"].replace("-", ""):
                        proxy_driver.quit()
                        return info["Title"], url
            except Exception as e:
                logger.warning(f"Proxy search error: {e}")
            finally:
                proxy_driver.quit()

    logger.error(f"❌ All lookups failed for {part_number}. Marking as PRODUCT MISSING.")
    return None, None
