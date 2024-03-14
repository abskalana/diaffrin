import uuid

hostname = 'localhost'
username = 'finsharehub'
password = 'finsharehub$'
database = 'db_kolenda'

import  MySQLdb
import pandas as pd

stmt = "INSERT INTO diaffrin_api_entity (slug,city,locality,activity,property,contact_name,contact_phone,porte,coord, status, commune_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
df = pd.read_excel("data.xlsx")
df.fillna('--', inplace=True)
dbconnect = MySQLdb.connect(hostname, username, password, database)
cursor = dbconnect.cursor()

def insert_row(row):
    try:
        slug= str(uuid.uuid4().hex)
        city = row['ville'].lower()
        locality = row['locality']
        activity = row["activity"]
        property = row["property"]
        contact_name = row["contact_name"]
        contact_phone = row["contact_phone"]
        porte = row["porte"]
        coord = row["coord"]
        commune_id = 150202
        val = (slug,city,locality,activity,property,contact_name,contact_phone,porte,coord,commune_id)
        cursor.execute(stmt, val)
    except Exception as e:
        print(e)
i = 0
for index, row in df.iterrows():
    insert_row(row)
    print(i)
    i = i+1
dbconnect.commit()