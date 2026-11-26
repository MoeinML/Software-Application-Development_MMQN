import os

import mysql.connector
from dotenv import load_dotenv

load_dotenv()


def run_connection_check():
    password = os.getenv("MYSQL_PASSWORD")
    if not password:
        raise ValueError("MYSQL_PASSWORD is not set in .env")

    print("MySQL Connector imported successfully!")

    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password=password,
        database="trainbookingsystem",
    )
    print("Connected to MySQL successfully!")

    try:
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM passenger")
        for passenger in cursor.fetchall():
            print(passenger)

        cursor.execute("SELECT * FROM passenger WHERE passenger_id = 1")
        print(cursor.fetchone())

        insert_sql = (
            "INSERT INTO passenger (first_name, last_name, phone_number) "
            "VALUES (%s, %s, %s)"
        )
        values = [
            ("Hop", "Le", "+358787878787"),
            ("Binh", "Do", "+358787878787"),
            ("Quan", "Pham", "+358787878787"),
        ]
        cursor.executemany(insert_sql, values)
        connection.commit()
        print("New passenger ID:", cursor.lastrowid)

        delete_sql = "DELETE FROM passenger WHERE phone_number = %s"
        cursor.execute(delete_sql, ("+358787878787",))
        connection.commit()
        print(cursor.rowcount, "record(s) deleted")

        cursor.execute("SELECT * FROM passenger ORDER BY passenger_id")
        for row in cursor.fetchall():
            print(row)

        cursor.close()
    finally:
        connection.close()


if __name__ == "__main__":
    run_connection_check()