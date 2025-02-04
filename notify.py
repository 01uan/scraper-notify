def notify_new_listings(new_listings):
    if new_listings:
        print("New listings found!")
        for listing in new_listings:
            print(f"Title: {listing['title']}, Price: {listing['price']}, Link: {listing['link']}")
    else:
        print("No new listings found.")