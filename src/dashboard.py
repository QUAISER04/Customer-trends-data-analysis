import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
import plotly.express as px

# Load environment variables
load_dotenv()

# Page Config
st.set_page_config(
    page_title="Customer Trends Dashboard",
    page_icon="🛍️",
    layout="wide"
)

# Database Connection
@st.cache_resource
def get_connection():
    db_type = os.getenv("DB_TYPE", "sqlite")
    db_name = os.getenv("DB_NAME", "customer_behavior.db")
    
    if db_type == "sqlite":
        return create_engine(f"sqlite:///{db_name}")
    
    # Add other connections if needed (logic similar to etl_pipeline)
    return create_engine(f"sqlite:///{db_name}")

try:
    engine = get_connection()
except Exception as e:
    st.error(f"Failed to connect to database: {e}")
    st.stop()

# Title
st.title("🛍️ Customer Trends & Shopping Behavior Analysis")
st.markdown("### Insights driven by SQL & Python")

# Sidebar
st.sidebar.header("Filter Options")
gender_filter = st.sidebar.multiselect(
    "Select Gender:",
    options=["Male", "Female"],
    default=["Male", "Female"]
)

# --- Q1: Revenue by Gender ---
st.header("1. Total Revenue by Gender")
if gender_filter:
    query_q1 = f"""
        SELECT gender, SUM(purchase_amount) as revenue
        FROM customer
        WHERE gender IN ({','.join([f"'{g}'" for g in gender_filter])})
        GROUP BY gender
    """
    df_q1 = pd.read_sql(query_q1, engine)
    col1, col2 = st.columns(2)
    with col1:
        st.dataframe(df_q1)
    with col2:
        fig_q1 = px.pie(df_q1, values='revenue', names='gender', title='Revenue Share by Gender', hole=0.4)
        st.plotly_chart(fig_q1, use_container_width=True)
else:
    st.info("Please select at least one gender.")


# --- Q3: Top 5 Products ---
st.header("2. Top 5 Products by Rating")
query_q3 = """
    SELECT item_purchased, round(avg(review_rating),2) as avg_rating
    from customer
    group by item_purchased
    order by avg_rating desc
    limit 5
"""
df_q3 = pd.read_sql(query_q3, engine)
fig_q3 = px.bar(df_q3, x='item_purchased', y='avg_rating', color='avg_rating', title="Highest Rated Products")
st.plotly_chart(fig_q3, use_container_width=True)


# --- Q5: Subscription Impact ---
st.header("3. Subscription Status vs Spending")
query_q5 = """
    SELECT subscription_status,
        COUNT(customer_id) AS total_customers,
        ROUND(AVG(purchase_amount),2) AS avg_spend,
        ROUND(SUM(purchase_amount),2) AS total_revenue
    FROM customer
    GROUP BY subscription_status
"""
df_q5 = pd.read_sql(query_q5, engine)
col3, col4 = st.columns(2)
with col3:
    fig_q5_spend = px.bar(df_q5, x='subscription_status', y='avg_spend', title="Average Spend per Customer")
    st.plotly_chart(fig_q5_spend, use_container_width=True)
with col4:
    fig_q5_rev = px.bar(df_q5, x='subscription_status', y='total_revenue', title="Total Revenue Contribution")
    st.plotly_chart(fig_q5_rev, use_container_width=True)


# --- Q10: Age Group Revenue ---
st.header("4. Revenue by Age Group")
query_q10 = """
    SELECT age_group, SUM(purchase_amount) AS total_revenue
    FROM customer
    GROUP BY age_group
    ORDER BY total_revenue DESC
"""
df_q10 = pd.read_sql(query_q10, engine)
fig_q10 = px.bar(df_q10, x='age_group', y='total_revenue', color='age_group', title="Revenue Distribution by Age")
st.plotly_chart(fig_q10, use_container_width=True)


# --- Raw Data ---
st.header("Raw Data Sample")
if st.checkbox("Show Raw Data"):
    df_raw = pd.read_sql("SELECT * FROM customer LIMIT 100", engine)
    st.dataframe(df_raw)

# Footer
st.markdown("---")
st.markdown("Created by **Quaiser Shahid** | Customer Trends Analysis Project")
