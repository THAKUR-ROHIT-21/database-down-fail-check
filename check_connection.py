HOST = 'database-1.cd0e8sw4y86e.us-east-2.rds.amazonaws.com'
USER = 'admin'
PASS = 'rohit1234'

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