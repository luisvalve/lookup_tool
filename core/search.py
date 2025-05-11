import time
from selenium.webdriver.common.by import By
from core.driver import create_browser
from core.logger import logger
from core.parser import extract_title_and_url


def lookup_part_number(part_number):
    driver = create_browser()
    try:
        query = f'{part_number} Beck Arnley'
        url = f'https://www.amazon.com/s?k="{part_number}"+Beck+Arnley'
        logger.info(f"Searching Amazon: {url}")
        driver.get(url)
        time.sleep(3)  # Let page load

        result = extract_title_and_url(driver, part_number)
        if result:
            title, product_url = result
            logger.success(f"✅ Title: {title}")
            return title, product_url

    except Exception as e:
        logger.error(f"❌ Exception during lookup: {str(e)}")
    finally:
        driver.quit()

    return None, None
