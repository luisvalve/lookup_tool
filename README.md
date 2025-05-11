# lookup_tool
# 🔍 Amazon Part Lookup Tool

A modular Python scraping tool to search for Beck/Arnley automotive part numbers on Amazon, with proxy support and fallback search.

---

## 🚀 Features

- Uses undetected ChromeDriver to bypass Amazon bot detection.
- Reads part numbers from a CSV file.
- Supports rotating proxies.
- Structured logs via `loguru`.
- Graceful fallback to DuckDuckGo and Google (planned).
- Modular codebase (plug-and-play components).

---

## 📁 Project Structure

```

lookup\_tool/
├── **main**.py          # Entry point
├── config.py            # Centralized settings
├── utils.py             # Retry/sleep helpers
├── core/
│   ├── driver.py        # Chrome browser with proxy
│   ├── search.py        # Amazon search logic
│   └── logger.py        # Loguru-based logger

````

---

## 📦 Requirements

- Python 3.9+
- Chrome installed
- pip dependencies:
  ```bash
  pip install -r requirements.txt
````

`requirements.txt`:

```txt
selenium
undetected-chromedriver
loguru
```

---

## 🛠️ Usage

1. Put part numbers in `part_lookup_input.csv` (1 per line).
2. Configure your proxy in `config.py` (or disable).
3. Run the tool:

```bash
python -m lookup_tool
```

---

## 📑 Logs

Logs are saved to `logs/lookup.log` and displayed in terminal with colors.

---

## 🔧 Proxy Example

In `config.py`:

```python
USE_PROXY = True
PROXY_URL = "http://username:password@proxyhost:port"
```

---

## 📌 Notes

* Make sure your proxy provider supports Amazon scraping.
* To extend fallback search, implement logic in `search.py` for DuckDuckGo or Google.
* Headless mode can be enabled via `driver.py`.

---

## 🧪 Coming Soon

* Unit tests
* Google fallback
* Web interface

---

## 📄 License

MIT

```

---

Would you like me to generate the actual `requirements.txt` and `.gitignore` too?
```
