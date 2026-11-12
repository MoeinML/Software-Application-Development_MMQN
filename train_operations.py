from db import get_connection

# ==================== 1. STATION OPERATIONS ====================
def get_all_stations():
    connection = get_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM STATION ORDER BY station_id")
        return cursor.fetchall()
    finally:
        cursor.close()
        connection.close()

def add_station(station_name, city):
    connection = get_connection()
    cursor = connection.cursor()
    try:
        sql = "INSERT INTO STATION (station_name, city) VALUES (%s, %s)"
        cursor.execute(sql, (station_name, city))
        connection.commit()
        return True
    except Exception as e:
        connection.rollback()
        print(f"Error adding station: {e}")
        return False
    finally:
        cursor.close()
        connection.close()

def delete_station(station_id):
    connection = get_connection()
    cursor = connection.cursor()
    try:
        sql = "DELETE FROM STATION WHERE station_id = %s"
        cursor.execute(sql, (station_id,))
        connection.commit()
        return cursor.rowcount > 0
    except Exception as e:
        connection.rollback()
        print(f"Error deleting station: {e}")
        return False
    finally:
        cursor.close()
        connection.close()


# ==================== 2. TRAIN OPERATIONS ====================
def get_all_trains():
    connection = get_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM TRAIN ORDER BY train_id")
        return cursor.fetchall()
    finally:
        cursor.close()
        connection.close()

def add_train(train_code, train_type):
    connection = get_connection()
    cursor = connection.cursor()
    try:
        sql = "INSERT INTO TRAIN (train_code, train_type) VALUES (%s, %s)"
        cursor.execute(sql, (train_code, train_type))
        connection.commit()
        return True
    except Exception as e:
        connection.rollback()
        print(f"Error adding train: {e}")
        return False
    finally:
        cursor.close()
        connection.close()

def delete_train(train_id):
    connection = get_connection()
    cursor = connection.cursor()
    try:
        sql = "DELETE FROM TRAIN WHERE train_id = %s"
        cursor.execute(sql, (train_id,))
        connection.commit()
        return cursor.rowcount > 0
    except Exception as e:
        connection.rollback()
        print(f"Error deleting train: {e}")
        return False
    finally:
        cursor.close()
        connection.close()


# ==================== 3. PASSENGER OPERATIONS ====================
def get_all_passengers():
    connection = get_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM PASSENGER ORDER BY passenger_id")
        return cursor.fetchall()
    finally:
        cursor.close()
        connection.close()

def add_passenger(first_name, last_name, phone_number):
    connection = get_connection()
    cursor = connection.cursor()
    try:
        sql = "INSERT INTO PASSENGER (first_name, last_name, phone_number) VALUES (%s, %s, %s)"
        cursor.execute(sql, (first_name, last_name, phone_number))
        connection.commit()
        return True
    except Exception as e:
        connection.rollback()
        print(f"Error adding passenger: {e}")
        return False
    finally:
        cursor.close()
        connection.close()

def delete_passenger(passenger_id):
    connection = get_connection()
    cursor = connection.cursor()
    try:
        sql = "DELETE FROM PASSENGER WHERE passenger_id = %s"
        cursor.execute(sql, (passenger_id,))
        connection.commit()
        return cursor.rowcount > 0
    except Exception as e:
        connection.rollback()
        print(f"Error deleting passenger: {e}")
        return False
    finally:
        cursor.close()
        connection.close()


# ==================== 4. PASSENGER_EMAIL OPERATIONS ====================
def get_all_passenger_emails():
    connection = get_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM PASSENGER_EMAIL")
        return cursor.fetchall()
    finally:
        cursor.close()
        connection.close()

def add_passenger_email(passenger_id, email):
    connection = get_connection()
    cursor = connection.cursor()
    try:
        sql = "INSERT INTO PASSENGER_EMAIL (passenger_id, email) VALUES (%s, %s)"
        cursor.execute(sql, (passenger_id, email))
        connection.commit()
        return True
    except Exception as e:
        connection.rollback()
        print(f"Error adding passenger email: {e}")
        return False
    finally:
        cursor.close()
        connection.close()

def delete_passenger_email(passenger_id, email):
    connection = get_connection()
    cursor = connection.cursor()
    try:
        sql = "DELETE FROM PASSENGER_EMAIL WHERE passenger_id = %s AND email = %s"
        cursor.execute(sql, (passenger_id, email))
        connection.commit()
        return cursor.rowcount > 0
    except Exception as e:
        connection.rollback()
        print(f"Error deleting passenger email: {e}")
        return False
    finally:
        cursor.close()
        connection.close()


# ==================== 5. SEAT OPERATIONS ====================
def get_all_seats():
    connection = get_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM SEAT ORDER BY seat_id")
        return cursor.fetchall()
    finally:
        cursor.close()
        connection.close()

def add_seat(seat_number, carriage_number, seat_class, train_id):
    connection = get_connection()
    cursor = connection.cursor()
    try:
        sql = "INSERT INTO SEAT (seat_number, carriage_number, seat_class, train_id) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (seat_number, carriage_number, seat_class, train_id))
        connection.commit()
        return True
    except Exception as e:
        connection.rollback()
        print(f"Error adding seat: {e}")
        return False
    finally:
        cursor.close()
        connection.close()

def delete_seat(seat_id):
    connection = get_connection()
    cursor = connection.cursor()
    try:
        sql = "DELETE FROM SEAT WHERE seat_id = %s"
        cursor.execute(sql, (seat_id,))
        connection.commit()
        return cursor.rowcount > 0
    except Exception as e:
        connection.rollback()
        print(f"Error deleting seat: {e}")
        return False
    finally:
        cursor.close()
        connection.close()


# ==================== 6. SCHEDULE OPERATIONS ====================
def get_all_schedules():
    connection = get_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM SCHEDULE ORDER BY schedule_id")
        return cursor.fetchall()
    finally:
        cursor.close()
        connection.close()

def add_schedule(departure_time, travel_date, arrival_time, train_id, departure_station_id, arrival_station_id):
    connection = get_connection()
    cursor = connection.cursor()
    try:
        sql = """INSERT INTO SCHEDULE (departure_time, travel_date, arrival_time, train_id, departure_station_id, arrival_station_id) 
                 VALUES (%s, %s, %s, %s, %s, %s)"""
        cursor.execute(sql, (departure_time, travel_date, arrival_time, train_id, departure_station_id, arrival_station_id))
        connection.commit()
        return True
    except Exception as e:
        connection.rollback()
        print(f"Error adding schedule: {e}")
        return False
    finally:
        cursor.close()
        connection.close()

def delete_schedule(schedule_id):
    connection = get_connection()
    cursor = connection.cursor()
    try:
        sql = "DELETE FROM SCHEDULE WHERE schedule_id = %s"
        cursor.execute(sql, (schedule_id,))
        connection.commit()
        return cursor.rowcount > 0
    except Exception as e:
        connection.rollback()
        print(f"Error deleting schedule: {e}")
        return False
    finally:
        cursor.close()
        connection.close()


# ==================== 7. BOOKING OPERATIONS ====================
def get_all_bookings():
    connection = get_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM BOOKING ORDER BY booking_id")
        return cursor.fetchall()
    finally:
        cursor.close()
        connection.close()

def add_booking(booking_date, status, ticket_price, passenger_id, schedule_id, seat_id):
    connection = get_connection()
    cursor = connection.cursor()
    try:
        sql = """INSERT INTO BOOKING (booking_date, status, ticket_price, passenger_id, schedule_id, seat_id)
                 VALUES (%s, %s, %s, %s, %s, %s)"""
        cursor.execute(sql, (booking_date, status, ticket_price, passenger_id, schedule_id, seat_id))
        connection.commit()
        return True
    except Exception as e:
        connection.rollback()
        print(f"Error adding booking: {e}")
        return False
    finally:
        cursor.close()
        connection.close()

def delete_booking(booking_id):
    connection = get_connection()
    cursor = connection.cursor()
    try:
        sql = "DELETE FROM BOOKING WHERE booking_id = %s"
        cursor.execute(sql, (booking_id,))
        connection.commit()
        return cursor.rowcount > 0
    except Exception as e:
        connection.rollback()
        print(f"Error deleting booking: {e}")
        return False
    finally:
        cursor.close()
        connection.close()