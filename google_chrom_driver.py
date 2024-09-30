from selenium import webdriver
import undetected_chromedriver as uc
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

def get_driver() -> webdriver.Chrome:
    # Adding preferences to Chrome options
    options = webdriver.ChromeOptions()
    user_agent = "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:70.0) Gecko/20100101 Firefox/70.0"
    options.add_argument(f"user-agent={user_agent}")
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--disable-infobars')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-extensions')
    options.add_argument('--start-maximized')
    options.add_argument('--disable-popup-blocking')
    options.add_argument('--incognito')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--allow-running-insecure-content')
    options.add_argument('--disable-web-security')
    options.add_argument('--disable-site-isolation-trials')
    options.add_argument('--disable-features=IsolateOrigins,site-per-process')
    # options.add_argument('--headless')  # Use '--headless' for standard headless mode
    # options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')

    # Modify request headers
    capabilities = DesiredCapabilities.CHROME
    capabilities["goog:loggingPrefs"] = {"performance": "ALL"}

    # prefs = {
    #     "profile.managed_default_content_settings.images": 2,  # Disable images
    #     "profile.managed_default_content_settings.videos": 2,  # Disable videos
    # }
    # options.add_experimental_option("prefs", prefs)

    # Create the driver
    driver = uc.Chrome(options=options, desired_capabilities=capabilities, version_main=127)

    # Prevent detection via 'navigator.webdriver'
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    return driver
