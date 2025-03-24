import sqlite3

# Connect to SQLite database (or create it)
conn = sqlite3.connect("reviews.db")
cursor = conn.cursor()

# Create table if it doesn't exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS reviews (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        airline TEXT,
        review TEXT,
        sentiment TEXT,
        fake_review TEXT,
        date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
""")

# Commit and close
conn.commit()
conn.close()

print("Database setup complete!")
