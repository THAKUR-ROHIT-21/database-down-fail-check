import pymysql

# Source database (recovery source)
src = pymysql.connect(
    host='Endpoint-1(dalate data endpoint)',
    user='User Name',
    password='Passwor',
    port=3306,
    database='project name'
)

# Destination database
dst = pymysql.connect(
    host='Endpoint where recover data',
    user='admin',
    password='admin123',
    port=3306,
    database='banking_db'
)

src_cur = src.cursor()
dst_cur = dst.cursor()

print("Data being recovered...")

# Fetch data from source
src_cur.execute("SELECT * FROM accounts")
rows = src_cur.fetchall()

# Insert into destination
for row in rows:
    dst_cur.execute("""
        INSERT IGNORE INTO accounts
        (id, name, email, mobile, acc_number, balance, created_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, row)

dst.commit()

print(f"{len(rows)} records recovered successfully.")

print("\nData in destination database:")

dst_cur.execute("SELECT * FROM accounts")
rows = dst_cur.fetchall()

for row in rows:
    print(row)
