import csv
from config import INPUT_CSV, WAIT_BETWEEN_REQUESTS
from core.search import lookup_part_number
from core.logger import logger
from utils import sleep


def load_parts(path):
    with open(path, newline='') as f:
        return [row[0] for row in csv.reader(f)]


def main():
    logger.info("\n📦 Starting Amazon Part Lookup with Proxy Support")
    logger.info("=======================================================")

    part_numbers = load_parts(INPUT_CSV)
    logger.info(f"📥 Loaded {len(part_numbers)} part numbers from {INPUT_CSV}")

    for index, part_number in enumerate(part_numbers, 1):
        logger.info(f"\n🔍 [{index}/{len(part_numbers)}] Looking up: {part_number}")
        lookup_part_number(part_number)
        sleep(WAIT_BETWEEN_REQUESTS)


if __name__ == '__main__':
    main()
