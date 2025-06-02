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
    query = "SELECT * FROM sentiment"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def main():
    st.set_page_config(page_title="Dashboard Auto Cinesi vs Europee", layout="wide")
    st.title("🚗 Dashboard: Perché le auto cinesi vendono più di quelle europee?")

    df = fetch_car_reviews()

    expected_cols = {"Brand", "Country", "Overall"}
    if not expected_cols.issubset(df.columns):
        st.error(f"Errore: il database deve contenere almeno le colonne: {expected_cols}")
        return

    # Filtri
    st.sidebar.header("🔎 Filtro Dati")
    country_filter = st.sidebar.multiselect("Seleziona Paesi", options=sorted(df["Country"].unique()), default=df["Country"].unique())
    brand_filter = st.sidebar.multiselect("Seleziona Brand", options=sorted(df["Brand"].unique()), default=df["Brand"].unique())

    filtered_df = df[(df["Country"].isin(country_filter)) & (df["Brand"].isin(brand_filter))]

    df_china = filtered_df[filtered_df["Country"].str.lower() == "cina"]
    df_europe = filtered_df[filtered_df["Country"].str.lower() == "europa"]

    # KPI comparativi
    st.markdown("### 📊 Confronto Quantitativo")
    col1, col2, col3 = st.columns(3)
    col1.metric("Recensioni Cinesi", len(df_china))
    col2.metric("Recensioni Europee", len(df_europe))
    diff = len(df_china) - len(df_europe)
    col3.metric("Differenza Recensioni", diff, delta_color="normal")

    # Distribuzione Overall
    st.markdown("### 🎯 Distribuzione dei voti 'Overall'")
    fig_overall = px.histogram(filtered_df, x="Overall", color="Country", barmode="group")
    st.plotly_chart(fig_overall, use_container_width=True)

    # Distribuzione brand
    st.markdown("### 🏷️ Frequenza per Brand")
    brand_counts = filtered_df.groupby(["Brand", "Country"]).size().reset_index(name="Conteggio")
    fig_brand = px.bar(brand_counts, x="Brand", y="Conteggio", color="Country", barmode="group")
    st.plotly_chart(fig_brand, use_container_width=True)

    # KPI qualitativi
    st.markdown("### 🧠 Possibili ragioni del successo delle auto cinesi")
    st.info("""
    In base ai dati delle recensioni raccolti, si osservano alcuni trend:
    - **Maggiore volume di recensioni** per i brand cinesi.
    - **Distribuzione dei voti "Overall" paragonabile o superiore** rispetto ai brand europei.
    - **Ampia varietà di modelli e diffusione commerciale** dei marchi cinesi nel segmento economico.

    Anche in assenza di dati numerici su prezzi e prestazioni, il volume e la valutazione positiva possono indicare:
    - Prezzi più accessibili
    - Miglior rapporto qualità/prezzo percepito
    - Maggiore innovazione o marketing più aggressivo
    """)

    # Tabella finale
    st.markdown("### 📄 Dettaglio recensioni filtrate")
    st.dataframe(filtered_df.sort_values(by="Overall", ascending=False), use_container_width=True)

if __name__ == "__main__":
    main()
