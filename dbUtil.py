import sqlite3

# initialize SQLite database
def initialize_db(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS listings (
            id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            location TEXT NOT NULL,
            price TEXT NOT NULL,
            link TEXT NOT NULL, 
            img TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# insert into
def insert_listing(db_path, listing):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO listings (id, title, location, price, link, img)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (listing["id"], listing["title"], listing["location"], listing["price"], listing["link"], listing["img"]))
        conn.commit()
        return True  # Successfully inserted
    except sqlite3.IntegrityError as e:
        print(f"IntegrityError: {e}")  # Debug print
        # Duplicate id (listing already exists)
        return False
    finally:
        conn.close()
        
# grab new 
def get_new_listings(db_path, scraped_listings):
    new_listings = []
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    for listing in scraped_listings:
        cursor.execute('SELECT * FROM listings WHERE id = ?', (listing["id"],))
        if not cursor.fetchone():  # If no matching id exists, it's a new listing
            new_listings.append(listing)
    conn.close()
    return new_listings