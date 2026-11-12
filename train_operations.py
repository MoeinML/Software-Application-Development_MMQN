from db import get_connection

## query
def get_all_bookings():
    connection = get_connection()
    cursor = connection.cursor()
    try:
        cursor.execute(
            "SELECT * FROM booking ORDER BY booking_id"
        )
        result = cursor.fetchall()
        return result
    finally:
        cursor.close()
        connection.close()

def get_all_trains():
    connection = get_connection()
    cursor = connection.cursor()
    
    try:
        cursor.execute(
            "SELECT * FROM train ORDER BY train_id"
        )
        trains = cursor.fetchall()
        return trains
    finally:
        cursor.close()
        connection.close()

## add
#
def add_booking(booking_date, status, ticket_price, passenger_id, schedule_id, seat_id):
    connection = get_connection()
    cursor = connection.cursor()
    try:
        sql = """INSERT INTO BOOKING (booking_date, status, ticket_price, passenger_id, schedule_id, seat_id)
        VALUES (%s, %s, %s, %s, %s, %s)"""
        cursor.execute(sql, (booking_date, status, ticket_price, passenger_id, schedule_id, seat_id))
        connection.commit()
    finally:
        cursor.close()
        connection.close()

#
def add_schedule(departure_time, travel_date, arrival_time, train_id, departure_station_id, arrival_station_id):
    connection = get_connection()
    cursor = connection.cursor()
    try:
        sql = """INSERT INTO SCHEDULE (departure_time, travel_date, arrival_time, train_id, departure_station_id, arrival_station_id) VALUES
        VALUES (%s, %s, %s, %s, %s, %s)"""
        cursor.execute(sql, (departure_time, travel_date, arrival_time, train_id, departure_station_id, arrival_station_id))
        connection.commit()
    finally:
        cursor.close()
        connection.close()

#
def add_station(station_name, city):
    connection = get_connection()
    cursor = connection.cursor()
    try:
        sql = """INSERT INTO STATION (station_name, city) VALUES
        VALUES (%s, %s)"""
        cursor.execute(sql, (station_name, city))
        connection.commit()
    finally:
        cursor.close()
        connection.close()

#
def add_train(train_code, train_type):
    connection = get_connection()
    cursor = connection.cursor()
    try:
        sql = """INSERT INTO TRAIN (train_code, train_type) VALUES
        VALUES (%s, %s)"""
        cursor.execute(sql, (train_code, train_type))
        connection.commit()
    finally:
        cursor.close()
        connection.close()

#
def add_passenger(first_name, last_name, phone_number):
    connection = get_connection()
    cursor = connection.cursor()
    try:
        sql = """INSERT INTO PASSENGER (first_name, last_name, phone_number) VALUES
        VALUES (%s, %s, %s)"""
        cursor.execute(sql, (first_name, last_name, phone_number))
        connection.commit()
    finally:
        cursor.close()
        connection.close()

#
def add_email(passenger_id, email):
    connection = get_connection()
    cursor = connection.cursor()
    try:
        sql = """INSERT INTO PASSENGER_EMAIL (passenger_id, email) VALUES
        VALUES (%s, %s)"""
        cursor.execute(sql, (passenger_id, email))
        connection.commit()
    finally:
        cursor.close()
        connection.close()

#
def add_seat(seat_number, carriage_number, seat_class, train_id):
    connection = get_connection()
    cursor = connection.cursor()
    try:
        sql = """INSERT INTO SEAT (seat_number, carriage_number, seat_class, train_id) VALUES
        VALUES (%s, %s, %s, %s)"""
        cursor.execute(sql, (seat_number, carriage_number, seat_class, train_id))
        connection.commit()
    finally:
        cursor.close()
        connection.close()

## delete
#
def delete_booking(booking_id):
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            sql = "DELETE FROM booking WHERE booking_id = %s"
            cursor.execute(sql, (booking_id,))
        connection.commit()
        return cursor.rowcount > 0
    except Exception as e:
        connection.rollback()
        print(f"Error deleting booking: {e}")
        return False
    finally:
        connection.close()

## update
