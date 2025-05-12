
from core.logger import logger
from core.scraper import read_part_numbers, write_results
from core.search import lookup_part_number
from core.driver import test_storage_access
from config import INPUT_CSV


def main():
    logger.info("\n📦 Starting Amazon Part Lookup with Proxy Support")
    logger.info("=======================================================")

    if not test_storage_access():
        logger.error("❌ Could not access Amazon. Check proxy/browser setup.")
        return

    part_numbers = read_part_numbers(INPUT_CSV)
    logger.info(f"📥 Loaded {len(part_numbers)} part numbers from {INPUT_CSV}")

    results = []
    for index, part_number in enumerate(part_numbers, 1):
        logger.info(f"\n🔍 [{index}/{len(part_numbers)}] Looking up: {part_number}")
        title, url = lookup_part_number(part_number)
        results.append({
            "PartNumber": part_number,
            "Title": title or "NOT FOUND",
            "URL": url or "N/A"
        })

    write_results(results)
    logger.info("✅ Results written to part_lookup_output.csv")


if __name__ == "__main__":
    main()
