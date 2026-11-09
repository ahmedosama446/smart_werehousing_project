import pyodbc

def get_connection():
    return pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=localhost;'
        'DATABASE=SmartWarehouseDB;'
        'Trusted_Connection=yes;'
    )


# try:
#     conn = get_connection()
#     print("Connection successful!")
#
#     cursor = conn.cursor()
#     cursor.execute("SELECT @@VERSION AS version")
#     row = cursor.fetchone()
#     print("SQL Server version:", row.version)
#
#     conn.close()
# except Exception as e:
#     print("Connection failed:", e)
