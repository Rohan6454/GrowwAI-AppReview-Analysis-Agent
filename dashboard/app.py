import streamlit as st
import pandas as pd
import sqlite3
import os
from pathlib import Path
import markdown

# Setup page config
st.set_page_config(page_title="App Review Insights", page_icon="📊", layout="wide")

BASE_DIR = Path(__file__).parent.parent
DB_PATH = BASE_DIR / "data" / "reviews.db"
REPORT_PATH = BASE_DIR / "data" / "weekly_report.md"

def load_data():
    if not DB_PATH.exists():
        return pd.DataFrame()
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM reviews ORDER BY review_date DESC", conn)
    conn.close()
    return df

st.title("📊 App Review Insights Dashboard")
st.markdown("Interact with the raw review data and view the latest AI-generated executive summaries.")

tab1, tab2 = st.tabs(["📑 Weekly Executive Report", "🔍 Review Explorer"])

with tab1:
    st.header("Latest AI Insights")
    if REPORT_PATH.exists():
        with open(REPORT_PATH, "r", encoding="utf-8") as f:
            content = f.read()
        st.markdown(content)
    else:
        st.warning("No weekly report found. Please run the AI pipeline first.")

with tab2:
    st.header("Raw Review Data Explorer")
    df = load_data()
    
    if df.empty:
        st.warning("No review data found in the database. Please run the data ingestion pipeline.")
    else:
        # Sidebar filters
        st.sidebar.header("Filter Reviews")
        
        # Source filter
        sources = df['source'].dropna().unique().tolist()
        selected_sources = st.sidebar.multiselect("App Store Source", sources, default=sources)
        
        # Rating filter
        ratings = sorted(df['rating'].dropna().unique().tolist())
        selected_ratings = st.sidebar.multiselect("Rating", ratings, default=ratings)
        
        # Filter dataframe
        filtered_df = df[
            (df['source'].isin(selected_sources)) &
            (df['rating'].isin(selected_ratings))
        ]
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Reviews (Filtered)", len(filtered_df))
        if not filtered_df.empty:
            col2.metric("Average Rating", f"{filtered_df['rating'].mean():.2f} ⭐")
            col3.metric("Sources", len(selected_sources))
        
        # Display table - only show columns that exist
        display_cols = [c for c in ['review_date', 'rating', 'source', 'review_title', 'review_text', 'author'] if c in filtered_df.columns]
        st.dataframe(
            filtered_df[display_cols], 
            use_container_width=True, 
            hide_index=True
        )
        
        st.markdown("---")
        # Export button
        csv = filtered_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="⬇️ Export Filtered Data as CSV",
            data=csv,
            file_name='filtered_app_reviews.csv',
            mime='text/csv',
            use_container_width=True
        )
