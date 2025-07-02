import sqlite3
import pandas as pd


conn = sqlite3.connect('appointments.db')  # Replace with your database filename


query = "SELECT * FROM appointments;"  # Replace with your table name

df = pd.read_sql_query(query, conn)

conn.commit()
print(df)