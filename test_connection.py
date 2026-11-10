import mysql.connector
from getpass import getpass

print("MySQL Connector imported successfully!")

#
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password=getpass("Enter password: "),
    database="trainbookingsystem")
print("Connected to MySQL successfully!")

#
cursor = connection.cursor()

# get all results with rows
cursor.execute("SELECT * FROM passenger")
passengers = cursor.fetchall()
for passenger in passengers:
    print(passenger)

# know only one result will be returned
cursor.execute("SELECT * FROM passenger where passenger_id = 1")
passenger = cursor.fetchone()
print(passenger)

# insert a new record
sql = "INSERT INTO passenger (first_name, last_name, phone_number) VALUES (%s, %s, %s)"

# insert many records
values = [("Hop", "Le", "+358787878787"),
    ("Binh", "Do", "+358787878787"),
    ("Quan", "Pham", "+358787878787")]
cursor.executemany(sql, values)

connection.commit()
print("New passenger ID:", cursor.lastrowid)


sql = "DELETE FROM passenger WHERE phone_number= %s"
values = ("+358787878787",)
cursor.execute(sql, values)
connection.commit()
print(cursor.rowcount, "record(s) deleted")

# verify
cursor.execute("SELECT * FROM passenger ORDER BY passenger_id")
for passenger in cursor.fetchall():
    print(passenger)

cursor.close()
connection.close()

