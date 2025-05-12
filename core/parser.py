from selenium.webdriver.common.by import By
from core.logger import logger

def extract_title_and_url(driver, part_number):
    results = driver.find_elements(By.CSS_SELECTOR, 'h2 a')
    if results:
        first_title = results[0].text.strip()
        first_url = results[0].get_attribute('href')
        if part_number.replace('-', '') in first_title.replace('-', ''):
            return first_title, first_url
        else:
            logger.warning(f"❌ Mismatch: Title does not match {part_number}")
    else:
        logger.warning("❌ No product links found on Amazon")
    return None
