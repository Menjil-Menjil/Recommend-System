import pymysql

# Establish the connection
connection = pymysql.connect(
    host='menjil-be.cykbbebpgzgm.ap-northeast-2.rds.amazonaws.com:12000',       # usually localhost or an IP address
    user='root',   # your username
    password='root1234',  # your password
    database='menjil' # the database you want to connect to
)

# Create a cursor object
cursor = connection.cursor()

# Fetch data from the table
cursor.execute("SELECT * FROM users LIMIT;")
rows = cursor.fetchall()

print("Data:")
for row in rows:
    print(row)

# Close the cursor and connection
cursor.close()
connection.close()
