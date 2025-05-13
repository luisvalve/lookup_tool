from selenium.webdriver.common.by import By
from urllib.parse import quote_plus, urlparse, urlunparse
import csv

def extract_product_info(driver, url, part_number):
    driver.get(url)
    title_elem = driver.find_elements(By.ID, "productTitle")
    if not title_elem:
        return None
    title = title_elem[0].text.strip()
    return {"Title": title, "URL": url}


def write_results(results, output_file="part_lookup_output.csv"):
    with open(output_file, mode="w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["PartNumber", "Title", "URL"])
        writer.writeheader()
        for row in results:
            writer.writerow(row)


def read_part_numbers(file_path):
    with open(file_path, newline="") as f:
        return [row[0] for row in csv.reader(f)]


def clean_amazon_url(url):
    parsed = urlparse(url)
    clean_path = parsed.path.split("/ref=")[0]
    return urlunparse((parsed.scheme, parsed.netloc, clean_path, '', '', ''))
