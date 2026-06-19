HOST = 'Enter Endpoint'
USER = 'Endpoint user'
PASS = 'Endpoint password'

import pymysql

conn = pymysql.connect(
    host=HOST,
    user=USER,
    password=PASS
)

cur = conn.cursor()

cur.execute("SHOW VARIABLES LIKE 'max_connections';")

result = cur.fetchone() 

print(f"Connections: {result[1]}")

cur.close()
conn.close()
