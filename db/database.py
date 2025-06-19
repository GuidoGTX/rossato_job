import sqlite3
import os
from dotenv import load_dotenv
import pandas as pd

load_dotenv(".env.vars")
DB_PATH = os.environ["DB_PATH"]
CHINESE_BRANDS = ["MG", "OMODA", "BYD", "GWM", "Haval", "Jaecoo", "Leapmotor", "Xpeng"]

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    return conn

def fetch_reviews():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sentiment")
    reviews = cursor.fetchall()
    conn.close()
    return reviews

def fetch_review_by_brand(brand):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sentiment WHERE Brand = ?", (brand,))
    reviews = cursor.fetchall()
    conn.close()
    return reviews

def fetch_review_by_model(model):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sentiment WHERE Model = ?", (model,))
    reviews = cursor.fetchall()
    conn.close()
    return reviews

def fetch_car_reviews():
    conn = get_connection()
    query = "SELECT * FROM auto_reviews"
    df = pd.read_sql_query(query, conn)
    conn.close()
    
    # Aggiungi colonna Country basata sui brand
    df['Country'] = df['Brand'].apply(lambda x: 'Cina' if x in CHINESE_BRANDS else 'Europa')
    
    return df

