
from core.scraper import read_part_numbers, write_results
from core.search import lookup_part_number
from core.driver import test_storage_access
from config import INPUT_CSV
from core.terminal import log
from colorama import Fore
import time


def main():
    start = time.time()
    log("\n📦 Starting Amazon Part Lookup with Proxy Support", Fore.CYAN)
    log("=======================================================", Fore.CYAN)

    if not test_storage_access():
        log("❌ Storage access test failed", Fore.RED)
        return

    log("✅ Storage access test completed", Fore.GREEN)
    part_numbers = read_part_numbers(INPUT_CSV)
    log(f"📥 Loaded {len(part_numbers)} part numbers", Fore.CYAN)

    results = []
    for idx, part in enumerate(part_numbers, 1):
        log(f"\n🔍 [{idx}/{len(part_numbers)}] Looking up: {part}".ljust(60), Fore.BLUE)
        try:
            title, url = lookup_part_number(part)
        except Exception as e:
            log(f"❌ Error looking up {part}: {e}", Fore.RED)
            title, url = None, None
        results.append({
            "PartNumber": part,
            "Title": title or "NOT FOUND",
            "URL": url or "N/A"
        })
        log(f"📊 Progress: {idx}/{len(part_numbers)} complete", Fore.LIGHTCYAN_EX)

    write_results(results)
    log("✅ Results written to part_lookup_output.csv", Fore.GREEN)
    log(f"\n⏱️ Finished in {round(time.time() - start)} seconds", Fore.LIGHTYELLOW_EX)


if __name__ == "__main__":
    main()
