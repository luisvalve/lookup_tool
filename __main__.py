from core.scraper import read_part_numbers, write_results
from core.search import lookup_part_number
from core.driver import init_driver, test_storage_access
from config import INPUT_CSV
from core.terminal import log
from colorama import Fore
import time
import csv


def write_results(results, output_file="part_lookup_output.csv"):
    with open(output_file, mode="w", newline="", encoding="utf-8") as f:
        fieldnames = ["PartNumber", "ASIN", "Title", "URL", "Bullets", "CharCount"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in results:
            writer.writerow(row)


def read_part_numbers(file_path):
    with open(file_path, newline='', encoding='utf-8') as f:
        return [row['PartNumber'].strip() for row in csv.DictReader(f)]


def main():
    start = time.time()
    log("\n📦 Starting Amazon Part Lookup with Proxy Support", Fore.CYAN)
    log("=======================================================", Fore.CYAN)

    driver = init_driver()
    test_storage_access(driver)
    driver.quit()

    part_numbers = read_part_numbers(INPUT_CSV)
    log(f"📥 Loaded {len(part_numbers)} part numbers", Fore.CYAN)

    results = []
    for idx, part in enumerate(part_numbers, 1):
        log(f"\n🔍 [{idx}/{len(part_numbers)}] Looking up: {part}".ljust(60), Fore.BLUE)
        try:
            info = lookup_part_number(part)
        except Exception as e:
            log(f"❌ Error looking up {part}: {e}", Fore.RED)
            info = None
        results.append({
            "PartNumber": part,
            "Title": info["Title"] if info else "NOT FOUND",
            "ASIN": info["ASIN"] if info else "N/A",
            "URL": info["URL"] if info else "N/A",
            "Bullets": info["Bullets"] if info else "N/A",
            "CharCount": info["CharCount"] if info else 0
        })
        log(f"📊 Progress: {idx}/{len(part_numbers)} complete", Fore.LIGHTCYAN_EX)

    write_results(results)
    log("✅ Results written to part_lookup_output.csv", Fore.GREEN)
    log(f"\n⏱️ Finished in {round(time.time() - start)} seconds", Fore.LIGHTYELLOW_EX)


if __name__ == "__main__":
    main()
