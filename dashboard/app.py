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

@st.cache_data(ttl=60) # Reduced cache to 60s to prevent stale empty data
def load_data():
    db_url = os.environ.get("DATABASE_URL")
    try:
        if not db_url and "DATABASE_URL" in st.secrets:
            db_url = st.secrets.get("DATABASE_URL")
    except Exception:
        pass # Ignore if st.secrets doesn't exist
    
    if db_url:
        import sqlalchemy
        try:
            # Handle standard postgresql:// vs postgres:// URL scheme
            if db_url.startswith("postgres://"):
                db_url = db_url.replace("postgres://", "postgresql://", 1)
            engine = sqlalchemy.create_engine(db_url)
            df = pd.read_sql_query("SELECT * FROM reviews ORDER BY review_date DESC", engine)
            return df
        except Exception as e:
            st.error(f"Error connecting to cloud database: {e}")
            return pd.DataFrame()
            
    # Fallback to local SQLite database
    if not DB_PATH.exists():
        return pd.DataFrame()
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM reviews ORDER BY review_date DESC", conn)
    conn.close()
    return df

def load_report():
    db_url = os.environ.get("DATABASE_URL")
    if db_url:
        import sqlalchemy
        from sqlalchemy import text
        try:
            if db_url.startswith("postgres://"):
                db_url = db_url.replace("postgres://", "postgresql://", 1)
            engine = sqlalchemy.create_engine(db_url)
            with engine.connect() as conn:
                result = conn.execute(text("SELECT content FROM reports ORDER BY generated_at DESC LIMIT 1")).fetchone()
                if result:
                    return result[0]
        except Exception as e:
            st.error(f"Error fetching report from cloud database: {e}")
            
    # Fallback to local file
    if REPORT_PATH.exists():
        with open(REPORT_PATH, "r", encoding="utf-8") as f:
            return f.read()
    
    # Fallback to local SQLite DB if file missing
    if DB_PATH.exists():
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("SELECT content FROM reports ORDER BY generated_at DESC LIMIT 1")
            result = cursor.fetchone()
            conn.close()
            if result:
                return result[0]
        except:
            pass
            
    return None

st.title("📊 App Review Insights Dashboard")
st.markdown("Interact with the raw review data and view the latest AI-generated executive summaries.")

if st.button("🔄 Refresh Data"):
    st.cache_data.clear()
    st.rerun()

tab1, tab2 = st.tabs(["📑 Weekly Executive Report", "🔍 Review Explorer"])

with tab1:
    st.header("Latest AI Insights")
    report_content = load_report()
    if report_content:
        st.markdown(report_content)
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
