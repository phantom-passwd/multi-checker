# Proxy Scraper & Email/Password Extractor

This repository contains two separate Python tools designed for scraping proxies and extracting email-password combinations from text files.

## Features

### 1. Proxy Scraper
- Scrapes proxies and supports different proxy categories (`HTTP`, `HTTPS`, `SOCKS4`, `SOCKS5`).
- Cleans and validates proxy formats !!
- Checks Proxies.
- Removes non-working proxies.

### 2. Email/Password
- Extracts email and password pairs from a given file.
- Filters out invalid entries from the extracted data.
- Saves and clean format to an output file.
- Provides logs !!

## Requirements

Make sure you have the following Python packages installed:
- `requests`
- `beautifulsoup4`
- `colorama`
- `clear`
You can install them using:
```bash
pip install requests beautifulsoup4 colorama clear
```

## Usage

### Proxy Scraper

1. Clone the repository:
   ```bash
   git clone https://github.com/phantom-passwd/multi-checker.git
   ```
2. Navigate to the project directory:
   ```bash
   cd multi-checker/SCRAPPER
   ```
3. Run the Proxy Scraper:
   ```bash
   python scrapper.py
   ```
   - The script will scrape proxies from various sources, and save the results in separate files (e.g., `http_proxies.txt`, `socks5_proxies.txt`, etc.)
     
### Email/Password Extractor

1. Make sure you have Update the `input_file`  in the `EmailPasswordExtractor` class with the path to your input file:
   ```python
   self.input_file = 'INPUT_FILE_PATH_HERE_BROOOOOOOOO.txt'  # Update this path
   ```
2. Run the Email/Password Extractor:
   ```bash
   python CONVERT.py
   ```
   - The script will extract valid email:password pairs from the specified input file and save them in `sorted.txt`.
   - It also logs the extraction process !!!
