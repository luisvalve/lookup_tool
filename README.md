# 🔍 Amazon Part Lookup Tool

A Python-based scraper that automates Amazon product lookups using part numbers, with proxy support and fallback search.

---

## 🚀 Features

- 🔍 Amazon + DuckDuckGo + Google fallback
- 🧠 Intelligent title match filtering
- 📄 CSV input/output
- 🧰 Modular Python code
- 🛡️ Proxy rotation with session IDs
- 🎭 Rotating user agents
- ✅ Pre-run Amazon access check
- 🧪 GitHub Actions CI

---

## 📦 Requirements

- Python 3.9 or higher
- Chrome installed locally
- Install dependencies:

```bash
pip install -r requirements.txt

# Step 1 — Install dependencies
pip install -r requirements.txt

# Step 2 — Add part numbers to the input CSV
# Make sure the file has a header row: PartNumber
cat part_lookup_input.csv
PartNumber
103-2110
103-2147
...

# Step 3 — Set your proxy credentials in config.py
# Example:
# PROXY_USER = "your_user"
# PROXY_PASS = "your_pass"
# PROXY_GATE = "gate.decodo.com"
# PROXY_PORT = "10001"

# Step 4 — Run the scraper
python3 __main__.py

# Output will be saved to:
part_lookup_output.csv
