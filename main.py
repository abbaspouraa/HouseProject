import re
import os
import json
from time import sleep
import google_chrom_driver
from dotenv import load_dotenv
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common import NoSuchElementException, TimeoutException

load_dotenv('.env')
user_name = os.getenv('USER_NAME')
password = os.getenv('PASSWORD')
AREAS = os.getenv('AREAS').split(";")

driver = google_chrom_driver.get_driver()
login_url = 'https://realtor.ca/'

def login():
    driver.get(login_url)

    WebDriverWait(driver, 30).until(
        ec.element_to_be_clickable((By.ID, 'headerSignInText'))
    ).click()
    WebDriverWait(driver, 3).until(
        ec.element_to_be_clickable((By.ID, 'signInWithEmailText'))
    ).click()

    driver.find_element(By.ID, 'signInEmailTxt').send_keys(user_name)
    driver.find_element(By.ID, 'signInPasswordTxt').send_keys(password)
    login_button = WebDriverWait(driver, 3).until(
        ec.element_to_be_clickable((By.ID, 'btnSignIn'))
    )
    login_button.click()
    WebDriverWait(driver, 30).until(
        ec.element_to_be_clickable((By.ID, "headerMyAccountText"))
    )
    print("[INFO] Logged in!")


def search_houses(area_name: str) -> list:
    driver.get(login_url)
    driver.find_element(By.ID, 'homeSearchTxt').send_keys(area_name)
    driver.find_element(By.ID, 'homeSearchBtn').click()
    try:
        WebDriverWait(driver, 10).until(
            ec.element_to_be_clickable((By.XPATH, '//div/div/div/div[2]/div[2]/button[1]'))
        ).click()
    except TimeoutException:
        pass

    # Setup filters
    # House
    driver.find_element(By.ID, 'mapSearchMoreBtn').click()
    driver.find_element(By.ID, 'select2-ddlBuildingType-container').click()
    driver.find_element(By.XPATH, "//li[contains(text(), 'House')]").click()
    # Max price
    driver.find_element(By.ID, 'select2-ddlMaxPrice-container').click()
    driver.find_element(By.XPATH, "//li[contains(text(), '1,500,000')]").click()
    # Click on search
    driver.find_element(By.ID, 'mapMoreFiltersSearchBtn').click()

    items = []
    total_paginator = int(driver.find_elements(By.CLASS_NAME, "paginationTotalPagesNum")[-1].text.replace('+', ''))

    for _ in range(total_paginator):
        print(f"\r[INFO] Extracting data. Page {_+1}/{total_paginator}", end='', flush=True)
        sleep(3)
        house_elements = WebDriverWait(driver, 12).until(
            ec.presence_of_all_elements_located((By.CLASS_NAME, "listingCardOuterBody"))
        )
        for house_element in house_elements:
            image_element = house_element.find_element(By.XPATH, ".//img")
            url = house_element.find_element(By.XPATH, "./parent::a")
            price_element = house_element.find_element(By.XPATH, ".//div[@class='listingCardPrice']")
            address_element = house_element.find_element(By.XPATH, ".//div[@class='listingCardAddress']")
            bedroom_element = house_element.find_element(By.XPATH, ".//div[2]/div[2]/div[1]/div")
            bathroom_element = house_element.find_element(By.XPATH, ".//div[2]/div[2]/div[2]/div")
            sq_ft_element = house_element.find_element(By.XPATH, ".//div[2]/div[2]/div[3]/div")

            item = {
                'price': price_element.text,
                'address': address_element.text,
                'bedroom': bedroom_element.text,
                'bathroom': bathroom_element.text,
                'sq_ft': sq_ft_element.text,
                'image': image_element.get_attribute('src'),
                'url': url.get_attribute('href')
            }
            items.append(item)

        try:
            next_page_element = driver.find_elements(By.XPATH, "//a[@aria-label='Go to the next page']")[-1]
            next_page_element.click()
        except NoSuchElementException:
            break
    return items


def main():
    print("[INFO] Starting web scraping")
    login()
    data = {}
    for area in AREAS:
        result = search_houses(area)
        data[area] = result
        print(f"\n[INFO] Collected initial data for {area}")

    # data = populate_data(data)
    driver.quit()
    print("[INFO] Storing data...")
    with open("output/data.json", 'w') as file:
        json.dump(data, file, indent=4)



if __name__ == "__main__":
    main()
