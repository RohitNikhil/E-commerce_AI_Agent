import sqlite3

# Connecting to the database
conn = sqlite3.connect("SQL_Database/ecommerce.db")
cursor = conn.cursor()

# Listing all the tables
print("Tables in the database:")
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
for table in cursor.fetchall():
    print(table[0])

print("\n Sample data from product_ad_sales:")
cursor.execute("SELECT * FROM product_ad_sales LIMIT 5;")
rows = cursor.fetchall()
for row in rows:
    print(row)

print("\n Sample data from product_total_sales:")
cursor.execute("SELECT * FROM product_total_sales LIMIT 5;")
rows = cursor.fetchall()
for row in rows:
    print(row)

print("\n Sample data from product_eligibility:")
cursor.execute("SELECT * FROM product_eligibility LIMIT 5;")
rows = cursor.fetchall()
for row in rows:
    print(row)

conn.close()
