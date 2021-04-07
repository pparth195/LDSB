import pandas as pd
import numpy as np
import sqlite3

# Connect of create a database
conn = sqlite3.connect('LDSB')
c = conn.cursor()



# Create tables
def create_school_table():
	c.execute(
	'CREATE TABLE IF NOT EXISTS school(id integer PRIMARY KEY, name text NOT NULL, address text, site_name text)'
	)
def create_utility_table():
	c.execute(
	"""CREATE TABLE IF NOT EXISTS record(id integer PRIMARY KEY, provider text NOT NULL, date_of_bill date,
	utility text,address text, site_name text, start_date date, end_date date, total_amount integer,
	total_consumption integer, demand_kW integer, facility_size integer, eKWh integer, ratio integer)"""
	)







# TEST

# create_school_table()
# df = pd.read_csv("school_test.csv")
# df.to_sql('school', conn, if_exists='append', index=False)
# df2 = pd.read_sql("SELECT * FROM school LIMIT 5", conn)
# print(df2)

# create_utility_table()
# df = pd.read_csv("Book2.csv")
# df.to_sql('record', conn, if_exists='append', index=False)
# df2 = pd.read_sql("SELECT * FROM record LIMIT 5", conn)
# print(df2)