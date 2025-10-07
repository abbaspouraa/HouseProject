# Ontario House Deals Monitor

A Python/Selenium monitor that scans Ontario real-estate portals for “deal” signals (e.g., price-per-sqft, days-on-market), stores results, and emails a summary of promising listings.

## Features

- Headless Chrome scraping with retries/backoff.

- Basic scoring on price/DOM; de-dupe and drift-resistant selectors.

- HTML email daily digest (and per-listing alerts if desired).

- Shell script for scheduled runs.

## Repo layout

- main.py – orchestrates search, parse, score, notify. 

- google_chrom_driver.py – browser/session setup. 

- db_process.py – persistence and de-dupe. 

- send_email.py, gmail_script.py, email_template.html – alerting. 

- requirements.txt – dependencies. data_collection.sh – runner. 

## Quick start

1- Prereqs

  - Python 3.10+, Chrome + ChromeDriver

  - Email account (Gmail + App Password recommended)

2- Setup
```bash
git clone https://github.com/abbaspouraa/HouseProject.git
cd HouseProject
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

3- Config
Create .env (or set env vars another way):
```env
# Search parameters
CITY_LIST="Hamilton,Burlington,Oakville"
MIN_PRICE=350000
MAX_PRICE=1200000
MIN_BEDS=2
MAX_DAYS_ON_MARKET=21

# Email
ALERT_TO="me@example.com"
ALERT_FROM="me@example.com"
SMTP_HOST="smtp.gmail.com"
SMTP_PORT=587
SMTP_USER="me@example.com"
SMTP_PASS="your_app_password"

# Storage
DB_URL="sqlite:///houses.db"
# or DB_PATH="./houses.db"
```

4- Run it
```bash
python main.py
# or
bash data_collection.sh
```

5- Cron (daily digest)
```cron
0 7 * * * /usr/bin/bash /path/to/HouseProject/data_collection.sh >> /var/log/house_monitor.log 2>&1
```
## Scoring “deals”

- Price-per-sqft thresholds and DOM caps can be tuned in code.

- Add neighborhood filters and exclude obvious outliers (e.g., land-lease).

## Good-citizen scraping

- Respect robots.txt/ToS and local laws; authenticate only where permitted.

- Randomized delays; selector abstraction to handle page updates.

- Log provenance (URL, timestamp) for each record.

## Troubleshooting

- Selector breakage: update XPaths/CSS in one place and retry.

- Captcha: slow down; consider adding residential proxies only if compliant.

- Email: verify SMTP/App Password config.

## Roadmap

- Export CSV/Parquet and a simple dashboard/notebook.

- Optional push notifications or Slack/Discord webhooks.

- Basic ML scoring using historical comps.
