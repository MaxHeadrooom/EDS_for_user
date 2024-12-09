from connector import get_connection

try:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM db."Организация"')
        results = cursor.fetchall()
        for row in results:
            print(row)
except Exception as e:
    print(f"Error occurred: {e}")
