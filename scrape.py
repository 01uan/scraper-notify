import re
import time
import os
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

# load environment variables
load_dotenv()
city = os.getenv("city")
query = os.getenv("query")

if not city or not query:
    raise ValueError(".env file does not exist or does not contain city and query variables")

# Scrape Facebook Marketplace listings
def get_marketplace_listings(cookies):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Set headless=True to run in headless mode
        context = browser.new_context()

        # Load cookies to bypass login
        for cookie in cookies:
            context.add_cookies([cookie])

        page = context.new_page()
        url = f"https://www.facebook.com/marketplace/{city}/search?sortBy=creation_time_descend&query={query}&exact=false"
        page.goto(url)
        time.sleep(5)  # Wait for the page to load

        listings = []
        items = page.query_selector_all('xpath=/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div[2]/div/div/div[3]/div[1]/div[2]/div')  # Base selector for listings
        for item in items:
            info = item.inner_text().split("\n")
            # skipping empty uninitialized listings
            if item.inner_text() == "" or info[-1] == "Sponsored":
                continue  

            # grab all the elements we need
            link = item.query_selector("a").get_attribute("href")
            img = item.query_selector("img").get_attribute("src")

            listings.append({
                "id": re.search(r'/item/(\d+)', link).group(1),
                "title": info[-2],
                "location": info[-1],
                "price": info[0],
                "link": f"https://www.facebook.com{link}",
                "img": img
            })
        
        browser.close()
        return listings