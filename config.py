# phase-1 database configs.
import pymysql,time
from datetime import datetime

HOST='database-1.canwco2ws99r.us-east-1.rds.amazonaws.com'
USER="admin"
PASS="Admin123"
# AZ={}
print ("Phase-1 Config loaded")

# phase-2
try:
    cur=pymysql.connect(host=HOST,
                        user=USER,
                        password=PASS,
                        connect_timeout=10).cursor()
    cur.execute("SELECT @@hostname")
    print(cur.fetchall())
except Exception as e:
    print("Error :",e)