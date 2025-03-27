import pymysql

try:
    connection = pymysql.connect(
        host="localhost",
        user="root",
        password="@Aditi123", 
        database="ppt_access_control",
        cursorclass=pymysql.cursors.DictCursor
    )
    print("✅ Connected to MySQL successfully!")
    connection.close()
except Exception as e:
    print(f"❌ MySQL connection failed: {e}")
