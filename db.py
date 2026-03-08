import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()
def connection():
    return psycopg2.connect(os.getenv("database_url"))

conn = connection()
cur = conn.cursor()
cur.execute("""
        CREATE TABLE IF NOT EXISTS urls (
            id SERIAL PRIMARY KEY,
            long_url TEXT NOT NULL,
            short_url VARCHAR(10) UNIQUE NOT NULL
        )
""")
conn.commit()
conn.close()


def save_url(short_url, long_url):
    conn = connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO urls (short_url, long_url) VALUES (%s, %s)", (short_url, long_url))
    conn.commit()
    conn.close()

def get_url(short_url):
    conn = connection()
    cur = conn.cursor()
    cur.execute("SELECT long_url FROM urls WHERE short_url = %s", (short_url,))
    result = cur.fetchone()
    conn.close()
    return result[0] if result else None

def url_exist(short_url):
    conn = connection()
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM urls WHERE short_url = %s", (short_url,))
    exists = cur.fetchone() is not None
    conn.close()
    return exists