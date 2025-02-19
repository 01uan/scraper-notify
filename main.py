import json
import dbUtil
import notify
import time
from scrape import get_marketplace_listings

# load cookies from a JSON file
def load_cookies(file_path):
    with open(file_path, "r") as f:
        cookies_list = json.load(f)
    for cookie in cookies_list:
        if "sameSite" in cookie and cookie["sameSite"] not in ["Strict", "Lax", "None"]:
            del cookie["sameSite"]
    return cookies_list

def main():
    # initialize database
    db_path = "listings.db"
    dbUtil.initialize_db(db_path)

    while True:
        print("Scraping Marketplace...")

        # scrape listings
        scraped_listings = get_marketplace_listings(load_cookies("cookies.json"))

        # compare with database to find new listings
        new_listings = dbUtil.get_new_listings(db_path, scraped_listings)

        # notify about new listings
        if new_listings:
            notify.notify_new_listings(new_listings)

        # insert new listings into the database
        for listing in new_listings:
            dbUtil.insert_listing(db_path, listing)

        print(f"Checked for new listings. Sleeping for 5 minutes...")
        time.sleep(300)  # Wait for 5 minutes before running again

if __name__ == "__main__":
    main()