import sqlite3
import os
from dotenv import load_dotenv

load_dotenv(".env.vars")
DB_PATH = os.environ["DB_PATH"]

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    return conn

def fetch_reviews():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM auto_reviews")
    reviews = cursor.fetchall()
    conn.close()
    return reviews

def fetch_review_by_brand(brand):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM auto_reviews WHERE Brand = ?", (brand,))
    reviews = cursor.fetchall()
    conn.close()
    return reviews

def fetch_review_by_model(model):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM auto_reviews WHERE Model = ?", (model,))
    reviews = cursor.fetchall()
    conn.close()
    return reviews