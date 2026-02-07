import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
import urllib.parse

# Load environment variables
load_dotenv()

def get_db_engine():
    """Create database engine based on environment variables."""
    db_type = os.getenv("DB_TYPE", "sqlite")
    db_name = os.getenv("DB_NAME", "customer_behavior.db")
    db_user = os.getenv("DB_USER", "")
    db_password = os.getenv("DB_PASSWORD", "")
    db_host = os.getenv("DB_HOST", "localhost")
    db_port = os.getenv("DB_PORT", "")

    if db_type == "sqlite":
        print(f"Connecting to SQLite: {db_name}")
        return create_engine(f"sqlite:///{db_name}")
    
    elif db_type == "postgresql":
        print(f"Connecting to PostgreSQL: {db_name}")
        return create_engine(f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}")
    
    elif db_type == "mysql":
        print(f"Connecting to MySQL: {db_name}")
        return create_engine(f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}")
    
    elif db_type == "mssql":
        print(f"Connecting to MS SQL Server: {db_name}")
        driver = os.getenv("DB_DRIVER", "ODBC Driver 17 for SQL Server")
        driver_str = urllib.parse.quote_plus(driver)
        return create_engine(f"mssql+pyodbc://{db_user}:{db_password}@{db_host},{db_port}/{db_name}?driver={driver_str}")
    
    else:
        raise ValueError(f"Unsupported database type: {db_type}")

def run_etl():
    print("Starting ETL Process...")
    
    # 1. Load Data
    csv_file = 'customer_shopping_behavior.csv'
    if not os.path.exists(csv_file):
        raise FileNotFoundError(f"File not found: {csv_file}")
    
    print(f"Loading data from {csv_file}...")
    df = pd.read_csv(csv_file)
    print(f"Initial shape: {df.shape}")

    # 2. Data Cleaning & Transformation
    
    # Impute missing values in Review Rating with median of category
    if df['Review Rating'].isnull().sum() > 0:
        print("Imputing missing Review Ratings...")
        df['Review Rating'] = df.groupby('Category')['Review Rating'].transform(lambda x: x.fillna(x.median()))

    # Rename columns to snake case
    print("Renaming columns...")
    df.columns = df.columns.str.lower()
    df.columns = df.columns.str.replace(' ', '_')
    df = df.rename(columns={'purchase_amount_(usd)':'purchase_amount'})

    # Create age_group column
    print("Creating age_group column...")
    labels = ['Young Adult', 'Adult', 'Middle-aged', 'Senior']
    df['age_group'] = pd.qcut(df['age'], q=4, labels=labels)

    # Create purchase_frequency_days column
    print("Creating purchase_frequency_days column...")
    frequency_mapping = {
        'Fortnightly': 14,
        'Weekly': 7,
        'Monthly': 30,
        'Quarterly': 90,
        'Bi-Weekly': 14,
        'Annually': 365,
        'Every 3 Months': 90
    }
    df['purchase_frequency_days'] = df['frequency_of_purchases'].map(frequency_mapping)

    # Drop promo_code_used (redundant with discount_applied)
    if 'promo_code_used' in df.columns and 'discount_applied' in df.columns:
        if (df['discount_applied'] == df['promo_code_used']).all():
            print("Dropping redundant 'promo_code_used' column...")
            df = df.drop('promo_code_used', axis=1)

    print(f"Final shape: {df.shape}")
    print(f"Columns: {list(df.columns)}")

    # 3. Load to Database
    engine = get_db_engine()
    table_name = "customer"
    
    print(f"Loading data into table '{table_name}'...")
    try:
        df.to_sql(table_name, engine, if_exists="replace", index=False)
        print("Data successfully loaded!")
        
        # Verify
        with engine.connect() as conn:
            from sqlalchemy import text
            result = conn.execute(text(f"SELECT COUNT(*) FROM {table_name}"))
            count = result.scalar()
            print(f"Verification: Table '{table_name}' has {count} rows.")
            
    except Exception as e:
        print(f"Error loading to database: {e}")

if __name__ == "__main__":
    run_etl()
