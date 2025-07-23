import sqlite3
import pandas as pd
import os

# Directory paths
DB_PATH = os.path.join("SQL_Database", "ecommerce.db")
DATA_DIR = "Data"

# CSV file paths
ad_sales_csv = os.path.join(DATA_DIR, "Product-Level Ad Sales and Metrics (mapped) - Product-Level Ad Sales and Metrics (mapped).csv")
total_sales_csv = os.path.join(DATA_DIR, "Product-Level Total Sales and Metrics (mapped) - Product-Level Total Sales and Metrics (mapped).csv")
eligibility_csv = os.path.join(DATA_DIR, "Product-Level Eligibility Table (mapped) - Product-Level Eligibility Table (mapped).csv")

# Connecting to database (creates it if it doesn't exist)
conn = sqlite3.connect(DB_PATH)

# Creates the tables from schema.sql
with open(os.path.join("SQL_Database", "schema.sql"), "r") as f:
    conn.executescript(f.read())

# Loads CSVs into pandas DataFrames
ad_sales_df = pd.read_csv(ad_sales_csv)
total_sales_df = pd.read_csv(total_sales_csv)
eligibility_df = pd.read_csv(eligibility_csv)

# Inserting the data into tables
ad_sales_df.to_sql("product_ad_sales", conn, if_exists="replace", index=False)
total_sales_df.to_sql("product_total_sales", conn, if_exists="replace", index=False)
eligibility_df.to_sql("product_eligibility", conn, if_exists="replace", index=False)

conn.commit()
conn.close()

print("Database created and data seeded successfully!")
