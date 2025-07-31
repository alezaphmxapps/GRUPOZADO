import sqlite3
import os

DB_FILE = "customer_data.db"
SCHEMA_FILE = os.path.join("database", "schema.sql")
SEED_FILE = os.path.join("database", "seed_data.sql")

def setup_database():
    """
    Sets up the database by creating the schema and seeding it with initial data.
    It first deletes the old database file if it exists.
    """
    # Remove the old database file to start fresh
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
        print(f"Removed old database file: {DB_FILE}")

    # Connect to the SQLite database (this will create the file)
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    print("Database created successfully.")

    # Read and execute the schema SQL script
    try:
        with open(SCHEMA_FILE, "r") as f:
            schema_sql = f.read()
        cursor.executescript(schema_sql)
        print(f"Successfully executed schema from {SCHEMA_FILE}")
    except Exception as e:
        print(f"Error executing schema script: {e}")
        conn.close()
        return

    # Read and execute the seed data SQL script
    try:
        with open(SEED_FILE, "r") as f:
            seed_sql = f.read()
        cursor.executescript(seed_sql)
        print(f"Successfully seeded data from {SEED_FILE}")
    except Exception as e:
        print(f"Error executing seed script: {e}")
        conn.close()
        return

    # Commit the changes and close the connection
    conn.commit()
    conn.close()
    print("Database setup complete. Connection closed.")

if __name__ == "__main__":
    # Ensure we are in the project root directory
    # This is a simple check, more robust checks might be needed
    if not os.path.isdir("database"):
        print("Error: This script must be run from the project root directory.")
    else:
        setup_database()
