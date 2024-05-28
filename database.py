import mysql.connector

config = {
    'user': 'your_database_user',
    'password': 'your_database_password',
    'host': 'your_mysql_hostname_or_ip',
    'database': 'your_database_name',
    'port': 3306
}

try:
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()

    # Execute a simple query (example)
    cursor.execute("SELECT VERSION()")
    result = cursor.fetchone()
    print("MySQL Version:", result[0])

except mysql.connector.Error as err:
    print(f"Error: {err}")

finally:
    if connection.is_connected():
        cursor.close()
        connection.close()