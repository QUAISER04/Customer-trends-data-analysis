# Customer Trends & Shopping Behavior Analysis

A comprehensive data analytics project analyzing customer shopping behavior using **Python**, **SQL**, and **Streamlit**.

## 📌 Project Overview
This project simulates an end-to-end data analytics workflow to translate raw retail data into strategic business intelligence. It covers:
-   **Data Cleaning & ETL**: Processing raw CSV data using Python.
-   **Database Management**: Storing structured data in a SQL database (SQLite/PostgreSQL).
-   **Data Analysis**: Executing complex SQL queries to uncover insights.
-   **Visualization**: Interactive Dashboard using Streamlit.

## 🛠️ Tech Stack
-   **Language**: Python 3.10+
-   **Database**: SQLite (Default), PostgreSQL, MySQL, or MS SQL Server
-   **Libraries**: Pandas, SQLAlchemy, Plotly, Streamlit
-   **Analysis**: SQL (Aggregations, Joins, Window Functions)

## 🚀 How to Run

### 1. Setup Environment
```bash
# Clone the repository
git clone https://github.com/quaisershahid/customer-trends-data-analysis-SQL-Python-PowerBI.git
cd customer-trends-data-analysis-SQL-Python-PowerBI

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Database
The project uses **SQLite** by default (no setup required).
To use other databases, rename `.env.example` to `.env` and update credentials.

### 3. Run ETL Pipeline
Clean the raw data and populate the database:
```bash
python src/etl_pipeline.py
```

### 4. Launch Dashboard
Visualize the insights interactively:
```bash
streamlit run src/dashboard.py
```

## 📊 Key Insights
-   **Revenue Analysis**: Breakdown by gender, age group, and location.
-   **Product Performance**: Top-rated items and category popularity.
-   **Customer Behavior**: Subscription impact on spending and retention analysis.

## 👨‍💻 About the Author
Hey, I’m Quaiser Shahid.

### 🚀 Stay Connected
If you enjoyed this project and want to keep learning and growing as a data analyst, let’s stay in touch!

## 📜 License
MIT License
