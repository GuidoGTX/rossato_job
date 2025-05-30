import streamlit as st
import pandas as pd
import sqlite3
import os
from dotenv import load_dotenv
import plotly.express as px

# Load environment variables
load_dotenv(".env.vars")
DB_PATH = os.environ["DB_PATH"]

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    return conn

def fetch_car_reviews():
    conn = get_db_connection()
    query = "SELECT * FROM auto_reviews"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def main():
    st.title("Car Reviews Dashboard")
    
    # Fetch data from the database
    df = fetch_car_reviews()

    # KPI principali basati su Overall
    st.markdown("### KPI principali")
    overall_counts = df["Overall"].value_counts()
    col1, col2, col3 = st.columns(3)
    col1.metric("Totale recensioni", len(df))
    col2.metric("Valore Overall più comune", overall_counts.idxmax())
    col3.metric("Occorrenze valore più comune", overall_counts.max())

    # Pie chart distribuzione Overall
    st.markdown("### Distribuzione Overall")
    overall_df = overall_counts.reset_index()
    overall_df.columns = ["Overall", "Count"]
    fig_overall = px.pie(overall_df, names="Overall", values="Count")
    st.plotly_chart(fig_overall, use_container_width=True)

    # Bar chart: Overall per Brand
    st.markdown("### Distribuzione Overall per Brand")
    brand_overall = df.groupby(["Brand", "Overall"]).size().reset_index(name="Count")
    fig_brand = px.bar(brand_overall, x="Brand", y="Count", color="Overall", barmode="group")
    st.plotly_chart(fig_brand, use_container_width=True)

    # Tabella dati
    st.subheader("Car Reviews")
    st.dataframe(df)

if __name__ == "__main__":
    main()
