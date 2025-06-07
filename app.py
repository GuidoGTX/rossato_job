import streamlit as st
import pandas as pd
import sqlite3
import os
from dotenv import load_dotenv
import plotly.express as px
import plotly.graph_objects as go

# Load environment variables
load_dotenv(".env.vars")
DB_PATH = os.environ["DB_PATH"]

# Brand cinesi identificati
CHINESE_BRANDS = ["MG", "OMODA", "BYD", "GWM", "Haval", "Jaecoo", "Leapmotor", "Xpeng"]

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    return conn

def fetch_car_reviews():
    conn = get_db_connection()
    query = "SELECT * FROM auto_reviews"
    df = pd.read_sql_query(query, conn)
    conn.close()
    
    # Aggiungi colonna Country basata sui brand
    df['Country'] = df['Brand'].apply(lambda x: 'Cina' if x in CHINESE_BRANDS else 'Europa')
    
    return df

def main():
    st.set_page_config(page_title="Perché le Auto Cinesi Dominano l'Europa", layout="wide")
    
    # Header con messaggi chiave
    st.title("🚗 **Analisi Competitiva: Il Successo delle Auto Cinesi in Europa**")
    st.markdown("""
    <div style='background-color: #0338a1; padding: 20px; border-radius: 10px; margin-bottom: 20px;'>
    <h3 style='margin-top: 0;'>🎯 Obiettivo dell'analisi</h3>
    <p><strong>Comprendere i fattori che stanno permettendo ai brand cinesi di conquistare quote di mercato in Europa 
    attraverso l'analisi del sentiment dei consumatori reali.</strong></p>
    </div>
    """, unsafe_allow_html=True)

    df = fetch_car_reviews()

    if "Brand" not in df.columns or "Overall" not in df.columns:
        st.error("Errore: il database deve contenere almeno le colonne 'Brand' e 'Overall'")
        return

    # Sidebar con filtri
    st.sidebar.header("🔧 Controlli Analisi")
    
    # Selettore target audience
    target_audience = st.sidebar.selectbox("👥 Target Audience", [
        "📈 Manager Brand Europei", 
    ])
    
    # Filtri
    available_brands = sorted(df["Brand"].unique())
    chinese_brands_available = [b for b in available_brands if b in CHINESE_BRANDS]
    european_brands_available = [b for b in available_brands if b not in CHINESE_BRANDS]
    
    st.sidebar.subheader("🔎 Filtro Brand")
    show_chinese = st.sidebar.checkbox("Brand Cinesi", value=True)
    show_european = st.sidebar.checkbox("Brand Europei", value=True)
    
    # Filtra i dati
    brands_to_show = []
    if show_chinese:
        brands_to_show.extend(chinese_brands_available)
    if show_european:
        brands_to_show.extend(european_brands_available)
    
    filtered_df = df[df["Brand"].isin(brands_to_show)]
    df_china = filtered_df[filtered_df["Country"] == "Cina"]
    df_europe = filtered_df[filtered_df["Country"] == "Europa"]

    # Metriche chiave in evidenza
    st.markdown("### 📊 **Metriche Competitive Chiave**")
    col1, col2, col3, col4 = st.columns(4)
    
    avg_rating_china = df_china["Overall"].mean() if len(df_china) > 0 else 0
    avg_rating_europe = df_europe["Overall"].mean() if len(df_europe) > 0 else 0
    volume_china = len(df_china)
    volume_europe = len(df_europe)
    
    with col1:
        st.metric("📈 Rating Medio Cinesi", f"{avg_rating_china:.2f}", 
                 delta=f"{avg_rating_china - avg_rating_europe:+.2f}" if avg_rating_europe > 0 else None)
    
    with col2:
        st.metric("📈 Rating Medio Europei", f"{avg_rating_europe:.2f}")
    
    with col3:
        st.metric("🔢 Volume Recensioni Cinesi", volume_china)
    
    with col4:
        st.metric("🔢 Volume Recensioni Europei", volume_europe)

    # Tabs principali
    tab1, tab2, tab3, tab4 = st.tabs(["🎯 Analisi Competitiva", "📊 Performance Brand", "💡 Insight Strategici", "📋 Raccomandazioni"])

    with tab1:
        st.markdown("### 🥊 **Confronto Diretto: Cina vs Europa**")
        
        # Distribuzione ratings
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📊 Distribuzione Valutazioni Overall")
            fig_dist = px.histogram(filtered_df, x="Overall", color="Country", 
                                  barmode="group", nbins=10,
                                  color_discrete_map={"Cina": "#ff6b6b", "Europa": "#4ecdc4"})
            fig_dist.update_layout(title="Distribuzione Rating per Origine")
            st.plotly_chart(fig_dist, use_container_width=True)
        
        with col2:
            st.markdown("#### 📈 Rating Medio per Paese")
            avg_by_country = filtered_df.groupby("Country")["Overall"].agg(['mean', 'count']).reset_index()
            fig_avg = px.bar(avg_by_country, x="Country", y="mean",
                           color="Country", 
                           color_discrete_map={"Cina": "#ff6b6b", "Europa": "#4ecdc4"},
                           text="mean")
            fig_avg.update_traces(texttemplate='%{text:.2f}', textposition='outside')
            fig_avg.update_layout(title="Rating Medio per Origine", showlegend=False)
            st.plotly_chart(fig_avg, use_container_width=True)

        # Analisi quote di mercato nelle recensioni
        st.markdown("#### 🏆 **Quote di Mercato nelle Recensioni Online**")
        market_share = filtered_df["Country"].value_counts()
        fig_pie = px.pie(values=market_share.values, names=market_share.index,
                        color_discrete_map={"Cina": "#ff6b6b", "Europa": "#4ecdc4"})
        fig_pie.update_layout(title="Distribuzione Volume Recensioni")
        st.plotly_chart(fig_pie, use_container_width=True)

    with tab2:
        st.markdown("### 🏷️ **Performance per Brand**")
        
        # Top brand per rating
        brand_performance = filtered_df.groupby(["Brand", "Country"]).agg({
            "Overall": ["mean", "count"]
        }).round(2)
        brand_performance.columns = ["Rating_Medio", "Num_Recensioni"]
        brand_performance = brand_performance.reset_index()
        
        fig_brand_rating = px.scatter(brand_performance, x="Num_Recensioni", y="Rating_Medio",
                                    color="Country", size="Num_Recensioni",
                                    hover_data=["Brand"],
                                    color_discrete_map={"Cina": "#ff6b6b", "Europa": "#4ecdc4"})
        fig_brand_rating.update_layout(title="Rating vs Volume Recensioni per Brand")
        st.plotly_chart(fig_brand_rating, use_container_width=True)
        
        # Tabella performance
        st.markdown("#### 📋 **Classifica Brand per Performance**")
        brand_performance_sorted = brand_performance.sort_values("Rating_Medio", ascending=False)
        st.dataframe(brand_performance_sorted, use_container_width=True)

    with tab3:
        st.markdown("### 💡 **Insight Strategici**")
        
        # Messaggi specifici per audience
        if target_audience == "🏢 Dealer/Concessionari Europei":
            st.error("""
            ### ⚠️ **Allarme Competitivo per Concessionari**
            
            **I numeri parlano chiaro:**
            - I brand cinesi ottengono rating medi **più alti** con volumi **crescenti**
            - I clienti sono **soddisfatti** dell'esperienza cinese
            - **Rapporto qualità-prezzo** percepito come superiore
            
            **Azione richiesta:** Rivedere strategie pricing e value proposition dei brand europei
            """)
            
        elif target_audience == "📈 Manager Brand Europei":
            st.warning("""
            ### 📊 **Critical Market Intelligence**
            
            **Gap Competitivo Identificato:**
            - Rating superiori cinesi = **customer satisfaction** più alta
            - Volume recensioni = **brand awareness** e **market penetration**
            - Trend negativo per brand tradizionali europei
            
            **Strategic Priority:** Innovation in value delivery and customer experience
            """)
            
        elif target_audience == "🧠 Analisti di Mercato":
            st.info("""
            ### 🔬 **Market Disruption Analysis**
            
            **Fattori di Successo Cinesi:**
            1. **Quality Perception** - Rating consistently above European average
            2. **Market Volume** - High review volumes indicate strong adoption
            3. **Customer Advocacy** - Positive sentiment driving organic growth
            
            **Implicazioni:** Shift paradigmatico nel mercato automotive europeo
            """)
            
        else:  # Investitori
            st.success("""
            ### 💰 **Investment Thesis Validation**
            
            **Chinese Automotive Sector Strengths:**
            - **Customer Satisfaction** superiore ai competitor europei
            - **Market Penetration** accelerata via digital channels
            - **Brand Equity** building attraverso positive user experience
            
            **ROI Outlook:** Chinese brands positioned for continued European expansion
            """)

    with tab4:
        st.markdown("### 📋 **Action Plan per Brand Europei**")
        
        # Raccomandazioni prioritarie
        st.markdown("""
        <div style='background-color: #fff3cd; padding: 15px; border-radius: 8px; margin-bottom: 15px;'>
        <h4 style='color: #856404; margin-top: 0;'>🚨 Priorità Immediate (0-6 mesi)</h4>
        <ul style='color: black;'>
        <li><strong>Audit Competitivo:</strong> Analisi dettagliata value proposition cinesi</li>
        <li><strong>Price Review:</strong> Riallineamento pricing strategy per competere</li>
        <li><strong>Customer Experience:</strong> Identificazione gap nell'esperienza cliente</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style='background-color: #d1ecf1; padding: 15px; border-radius: 8px; margin-bottom: 15px;'>
        <h4 style='color: #0c5460; margin-top: 0;'>🎯 Strategie Medium-Term (6-18 mesi)</h4>
        <ul style='color: black;'>
        <li><strong>Innovation Acceleration:</strong> R&D focus su tecnologie competitive</li>
        <li><strong>Digital Transformation:</strong> Miglioramento customer journey digitale</li>
        <li><strong>Brand Positioning:</strong> Differenziazione su premium quality/heritage</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
        
        # Metriche da monitorare
        st.markdown("#### 📊 **KPI da Monitorare**")
        kpi_metrics = pd.DataFrame({
            "Metrica": ["Rating Medio", "Volume Recensioni", "Market Share Reviews", "Sentiment Score"],
            "Target": [">4.0", "Crescita 15% MoM", ">40%", ">70% Positive"],
            "Attuale Europei": [f"{avg_rating_europe:.2f}", f"{volume_europe}", 
                              f"{(volume_europe/(volume_europe+volume_china)*100):.1f}%" if volume_china+volume_europe > 0 else "N/A", "Da calcolare"]
        })
        st.dataframe(kpi_metrics, use_container_width=True)

if __name__ == "__main__":
    main()