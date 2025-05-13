# 🔍 Amazon Part Lookup Tool

A sophisticated Python-based scraper that automates Amazon product lookups using part numbers. Features intelligent search strategies, proxy support, and multi-source fallback mechanisms. Built as a personal project to demonstrate web automation and data extraction capabilities.

[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/downloads/)
[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

---

## 🎯 Project Overview

This personal project demonstrates my expertise in:
- Building robust web automation systems
- Implementing intelligent search algorithms
- Handling rate limiting and anti-bot measures
- Creating efficient data processing pipelines

## 🚀 Features

### Core Functionality
- 🔍 Multi-platform search strategy
  - Primary Amazon search
  - DuckDuckGo fallback
  - Google fallback
- 🧠 Intelligent matching
  - Part number validation
  - Title match filtering
  - Product verification

### Technical Features
- 📄 Data Processing
  - CSV input/output support
  - Structured data extraction
  - Batch processing
- 🛡️ Anti-Detection Measures
  - Proxy rotation with session IDs
  - User agent rotation
  - Browser fingerprint masking
- 🧪 Quality Assurance
  - Pre-run access validation
  - Error handling and logging

## 🏗 Project Structure

```
project/
├── core/           # Core functionality
│   ├── driver.py   # Browser automation
│   ├── search.py   # Search strategies
│   ├── scraper.py  # Data extraction
│   └── terminal.py # UI/logging
├── tests/          # Test suite
├── __main__.py     # Entry point
├── config.py       # Configuration
└── requirements.txt # Dependencies
```

## 📦 Requirements

### Prerequisites
- Python 3.9 or higher
- Chrome browser installed
- Active internet connection
- Proxy service credentials (optional but recommended)

### Dependencies
All required packages are listed in `requirements.txt`:
- selenium>=4.10.0 (Browser automation)
- undetected-chromedriver>=3.5.5 (Anti-detection)
- loguru>=0.7.2 (Logging)
- colorama>=0.4.6 (Terminal output)

## 🚦 Usage Guide

1. **Setup Environment**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Input**
   - Prepare your input CSV file:
   ```csv
   PartNumber
   103-2110
   103-2147
   ```

3. **Configure Proxy (Recommended)**
   - Edit `config.py`:
   ```python
   PROXY_USER = "your_user"
   PROXY_PASS = "your_pass"
   PROXY_GATE = "gate.decodo.com"
   PROXY_PORT = "10001"
   ```

4. **Run the Scraper**
   ```bash
   python3 __main__.py
   ```

## 📊 Output Format

The tool generates a CSV file (`part_lookup_output.csv`) with the following columns:
- `PartNumber`: Original part number
- `ASIN`: Amazon's product identifier
- `Title`: Product title
- `URL`: Product page URL
- `Bullets`: Product features
- `CharCount`: Feature text length

Example output:
```csv
PartNumber,ASIN,Title,URL,Bullets,CharCount
103-2925,B000EOJ288,Beck/Arnley 103-2925 Cv Joint Boot Kit,https://www.amazon.com/dp/B000EOJ288,"Matches OE form, fit and function...",216
```

## 🔧 Configuration

Key configuration options in `config.py`:
```python
# Proxy Settings
USE_PROXY = True
REQUEST_DELAY_SECONDS = (2.5, 4.5)

# Input/Output
INPUT_CSV = "part_lookup_input.csv"
```

## 📈 Performance

Demonstrated capabilities:
- Average lookup time: 8-10 seconds per part
- Success rate: >95% with valid part numbers
- Resource usage: ~200MB RAM per instance

## 🛠 Technical Highlights

### Search Strategy Implementation
- Multi-stage search process
- Intelligent fallback system
- Robust error handling

### Anti-Detection System
- Dynamic proxy rotation
- Browser fingerprint masking
- Request rate management

## 🙏 Acknowledgments

Built using:
- Selenium WebDriver
- undetected-chromedriver
- Python's rich ecosystem

---

*This is a personal project created to demonstrate web automation and data processing capabilities. The code and documentation showcase my approach to solving real-world automation challenges.*
