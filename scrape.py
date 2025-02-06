import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
from dotenv import load_dotenv

# load environment variables
load_dotenv()
city = os.getenv("city")
query = os.getenv("query")

if not city or not query:
    raise ValueError("Configure and populate .env file with the intended values")

# configure Selenium WebDriver
def setup_driver():
    chrome_options = Options()
    # chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--enable-unsafe-webgl")
    chrome_options.add_argument("--enable-unsafe-swiftshader")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

# Scrape Facebook Marketplace listings
def get_marketplace_listings(cookies):
    driver = setup_driver()
    url = f"https://www.facebook.com/marketplace/{city}/search/?query={query}"
    driver.get(url) 

    # load cookies to bypass login
    for cookie in cookies:
        driver.add_cookie(cookie)
    driver.refresh()  # refresh to apply cookies
    time.sleep(5)

    listings = []
    items = driver.find_elements(By.XPATH, '/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div[2]/div/div/div[3]/div[1]/div[2]/div')  # Base XPath for listings
    for item in items:
        info = item.text.split("\n")
        # skipping empty uninitalized listings
        if item.text == "" or info[-1] == "Sponsored":
            continue  

        # grab all the elements we need
        link = item.find_element(By.XPATH, ".//a").get_attribute("href") 
        img = item.find_element(By.XPATH, ".//img").get_attribute("src") 

        listings.append({
            "id": re.search(r'/item/(\d+)', link).group(1),
            "title": info[-2], 
            "location": info[-1], 
            "price": info[0], 
            "link": link, 
            "img": img
            })
        
    driver.quit()
    return listings