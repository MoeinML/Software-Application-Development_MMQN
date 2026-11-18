from db import get_connection
from validation import (
    validate_station,
    validate_train,
    validate_passenger,
    validate_schedule,
    validate_booking,
    validate_email
)
from mysql.connector import IntegrityError

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
    # Validation step
    station_name, city = validate_station(station_name, city)
    
    connection = get_connection()
    cursor = connection.cursor()
    try:
        sql = "INSERT INTO STATION (station_name, city) VALUES (%s, %s)"
        cursor.execute(sql, (station_name, city))
        connection.commit()
        return True
    # Check for duplicate entry constraint violation
    except IntegrityError:
        connection.rollback()
        raise ValueError(f"Station '{station_name}' already exists!")
    except Exception as e:
        connection.rollback()
        print(f"Error adding station: {e}")
        return False
    finally:
        cursor.close()
        connection.close()

def update_station(station_id, station_name, city):
    station_name, city = validate_station(station_name, city)
    
    connection = get_connection()
    cursor = connection.cursor()
    try:
        sql = "UPDATE STATION SET station_name = %s, city = %s WHERE station_id = %s"
        cursor.execute(sql, (station_name, city, station_id))
        connection.commit()
        return True
    except IntegrityError:
        connection.rollback()
        raise ValueError(f"Station '{station_name}' already exists!")
    except Exception as e:
        connection.rollback()
        print(f"Error updating station: {e}")
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
    except IntegrityError:
        connection.rollback()
        raise ValueError("Cannot delete this station because it is currently used in schedules!")
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

def add_train(train_code, train_type, capacity):
    # Validation step
    train_code, train_type, capacity = validate_train(train_code, train_type, capacity)    
    connection = get_connection()
    cursor = connection.cursor()
    try:
        sql = "INSERT INTO TRAIN (train_code, train_type, capacity) VALUES (%s, %s, %s)"
        cursor.execute(sql, (train_code, train_type, capacity))
        connection.commit()
        return True
    # Check for duplicate entry constraint violation
    except IntegrityError:
        connection.rollback()
        raise ValueError(f"Train with code '{train_code}' already exists!")
    except Exception as e:
        connection.rollback()
        print(f"Error adding train: {e}")
        return False
    finally:
        cursor.close()
        connection.close()

def update_train(train_id, train_code, train_type, capacity):
    train_code, train_type, capacity = validate_train(train_code, train_type, capacity)
    
    connection = get_connection()
    cursor = connection.cursor()
    try:
        sql = "UPDATE TRAIN SET train_code = %s, train_type = %s, capacity = %s WHERE train_id = %s"
        cursor.execute(sql, (train_code, train_type, capacity, train_id))
        connection.commit()
        return True
    except IntegrityError:
        connection.rollback()
        raise ValueError(f"Train with code '{train_code}' already exists!")
    except Exception as e:
        connection.rollback()
        print(f"Error updating train: {e}")
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
    except IntegrityError:
        connection.rollback()
        raise ValueError("Cannot delete this train because it is currently used in schedules!")
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
    # Validation step
    first_name, last_name, phone_number = validate_passenger(first_name, last_name, phone_number)
    
    connection = get_connection()
    cursor = connection.cursor()
    try:
        sql = "INSERT INTO PASSENGER (first_name, last_name, phone_number) VALUES (%s, %s, %s)"
        cursor.execute(sql, (first_name, last_name, phone_number))
        connection.commit()
        return True
    # Check for duplicate entry constraint violation
    except IntegrityError:
        connection.rollback()
        raise ValueError(f"Passenger with phone number '{phone_number}' already exists!")
    except Exception as e:
        connection.rollback()
        print(f"Error adding passenger: {e}")
        return False
    finally:
        cursor.close()
        connection.close()

def add_passenger_with_email_transaction(first_name, last_name, phone_number, email):
    """
    Task B: Transaction-based operation.
    Inserts a new passenger and their email within a single atomic transaction.
    If any step fails, it rolls back all changes to maintain database integrity.
    """
    # Validation step: validate passenger details and email format
    first_name, last_name, phone_number = validate_passenger(first_name, last_name, phone_number)
    email = validate_email(email)

    connection = get_connection()
    cursor = connection.cursor()
    try:
        # Start the transaction explicitly
        connection.start_transaction()

        # Step 1: Insert passenger into the PASSENGER table
        sql_passenger = "INSERT INTO PASSENGER (first_name, last_name, phone_number) VALUES (%s, %s, %s)"
        cursor.execute(sql_passenger, (first_name, last_name, phone_number))
        
        # Retrieve the auto-generated passenger_id for the second step
        passenger_id = cursor.lastrowid

        # Step 2: Insert the email into the PASSENGER_EMAIL table using the new passenger_id
        sql_email = "INSERT INTO PASSENGER_EMAIL (passenger_id, email) VALUES (%s, %s)"
        cursor.execute(sql_email, (passenger_id, email))

        # Commit both changes if everything is successful
        connection.commit()
        return True

    except IntegrityError as ie:
        # Rollback if there's a duplicate phone number or duplicate email constraint violation
        connection.rollback()
        raise ValueError(f"Database constraint violation (Duplicate phone or email): {ie}")
    except Exception as e:
        # Rollback all changes if any other error occurs
        connection.rollback()
        raise ValueError(f"Transaction failed and rolled back! Technical Error: {e}")
    finally:
        # Ensure database resources are properly closed
        cursor.close()
        connection.close()

def update_passenger(passenger_id, first_name, last_name, phone_number):
    first_name, last_name, phone_number = validate_passenger(first_name, last_name, phone_number)
    
    connection = get_connection()
    cursor = connection.cursor()
    try:
        sql = "UPDATE PASSENGER SET first_name = %s, last_name = %s, phone_number = %s WHERE passenger_id = %s"
        cursor.execute(sql, (first_name, last_name, phone_number, passenger_id))
        connection.commit()
        return True
    except IntegrityError:
        connection.rollback()
        raise ValueError(f"Passenger with phone number '{phone_number}' already exists!")
    except Exception as e:
        connection.rollback()
        print(f"Error updating passenger: {e}")
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
    except IntegrityError:
        connection.rollback()
        raise ValueError("Cannot delete this passenger because they are referenced in booking!")
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
    # Validation step
    email = validate_email(email)

    connection = get_connection()
    cursor = connection.cursor()
    try:
        sql = "INSERT INTO PASSENGER_EMAIL (passenger_id, email) VALUES (%s, %s)"
        cursor.execute(sql, (passenger_id, email))
        connection.commit()
        return True
    # Check for duplicate entry constraint violation
    except IntegrityError:
        connection.rollback()
        raise ValueError(f"This email address already exists for this passenger!")
    except Exception as e:
        connection.rollback()
        print(f"Error adding passenger email: {e}")
        return False
    finally:
        cursor.close()
        connection.close()

def update_passenger_email(passenger_id, old_email, new_email):
    new_email = validate_email(new_email)
    
    connection = get_connection()
    cursor = connection.cursor()
    try:
        sql = "UPDATE PASSENGER_EMAIL SET email = %s WHERE passenger_id = %s AND email = %s"
        cursor.execute(sql, (new_email, passenger_id, old_email))
        connection.commit()
        return True
    except IntegrityError:
        connection.rollback()
        raise ValueError("This email address already exists for this passenger!")
    except Exception as e:
        connection.rollback()
        print(f"Error updating passenger email: {e}")
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


# ==================== 5. SCHEDULE OPERATIONS ====================
def get_all_schedules():
    connection = get_connection()
    cursor = connection.cursor()
    try:
        sql = """
            SELECT 
                schedule_id, 
                TIME_FORMAT(departure_time, '%H:%i:%s'), 
                travel_date, 
                TIME_FORMAT(arrival_time, '%H:%i:%s'), 
                train_id, 
                departure_station_id, 
                arrival_station_id 
            FROM SCHEDULE 
            ORDER BY schedule_id
        """
        cursor.execute(sql)
        return cursor.fetchall()
    finally:
        cursor.close()
        connection.close()

def get_all_schedules_with_capacity():
    connection = get_connection()
    cursor = connection.cursor()
    try:
        sql = """
            SELECT 
                s.schedule_id,
                TIME_FORMAT(s.departure_time, '%H:%i:%s'),
                s.travel_date,
                TIME_FORMAT(s.arrival_time, '%H:%i:%s'),
                t.train_code,
                dep_st.station_name AS dep_station,
                arr_st.station_name AS arr_station,
                (t.capacity - COALESCE(SUM(b.number_of_tickets), 0)) AS available_seats
            FROM SCHEDULE s
            JOIN TRAIN t ON s.train_id = t.train_id
            JOIN STATION dep_st ON s.departure_station_id = dep_st.station_id
            JOIN STATION arr_st ON s.arrival_station_id = arr_st.station_id
            LEFT JOIN BOOKING b ON s.schedule_id = b.schedule_id
            GROUP BY s.schedule_id, s.departure_time, s.travel_date, s.arrival_time, t.train_code, t.capacity, dep_st.station_name, arr_st.station_name
            ORDER BY s.travel_date, s.departure_time
        """
        cursor.execute(sql)
        return cursor.fetchall()
    finally:
        cursor.close()
        connection.close()

def add_schedule(departure_time, travel_date, arrival_time, train_id, departure_station_id, arrival_station_id):
    # Validation step
    departure_time, travel_date, arrival_time, train_id, departure_station_id, arrival_station_id = validate_schedule(
        departure_time, travel_date, arrival_time, train_id, departure_station_id, arrival_station_id
    )
    
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

def update_schedule(schedule_id, departure_time, travel_date, arrival_time, train_id, departure_station_id, arrival_station_id):
    departure_time, travel_date, arrival_time, train_id, departure_station_id, arrival_station_id = validate_schedule(
        departure_time, travel_date, arrival_time, train_id, departure_station_id, arrival_station_id
    )
    
    connection = get_connection()
    cursor = connection.cursor()
    try:
        sql = """
            UPDATE SCHEDULE 
            SET departure_time = %s, travel_date = %s, arrival_time = %s, 
                train_id = %s, departure_station_id = %s, arrival_station_id = %s 
            WHERE schedule_id = %s
        """
        cursor.execute(sql, (departure_time, travel_date, arrival_time, train_id, departure_station_id, arrival_station_id, schedule_id))
        connection.commit()
        return True
    except Exception as e:
        connection.rollback()
        print(f"Error updating schedule: {e}")
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
    except IntegrityError:
        connection.rollback()
        raise ValueError("Cannot delete this schedule because there are active bookings for it!")
    except Exception as e:
        connection.rollback()
        print(f"Error deleting schedule: {e}")
        return False
    finally:
        cursor.close()
        connection.close()

# ==================== 6. BOOKING OPERATIONS ====================
def get_all_bookings():
    connection = get_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT booking_id, booking_date, passenger_id, schedule_id, number_of_tickets FROM BOOKING ORDER BY booking_id")
        return cursor.fetchall()
    finally:
        cursor.close()
        connection.close()

def add_booking(booking_date, passenger_id, schedule_id, number_of_tickets):
    # Validation step
    passenger_id, schedule_id, number_of_tickets = validate_booking(passenger_id, schedule_id, number_of_tickets)
    
    connection = get_connection()
    cursor = connection.cursor()
    try:
        capacity_check_sql = """
            SELECT 
                t.capacity AS total_capacity, COALESCE(SUM(b.number_of_tickets), 0) AS booked_tickets
            FROM SCHEDULE s
            JOIN TRAIN t ON s.train_id = t.train_id
            LEFT JOIN BOOKING b ON s.schedule_id = b.schedule_id
            WHERE s.schedule_id = %s
            GROUP BY t.capacity
        """
        cursor.execute(capacity_check_sql, (schedule_id,))
        result = cursor.fetchone()
        
        if not result:
            raise ValueError("Selected schedule does not exist.")
            
        total_capacity, booked_tickets = result
        available_seats = total_capacity - booked_tickets
        
        if number_of_tickets > available_seats:
            raise ValueError(f"Not enough capacity! Only {available_seats} seats remaining.")

        sql = """INSERT INTO BOOKING (booking_date, passenger_id, schedule_id, number_of_tickets)
                 VALUES (%s, %s, %s, %s)"""
        cursor.execute(sql, (booking_date, passenger_id, schedule_id, number_of_tickets))
        connection.commit()
        return True
        
    except ValueError as ve:
        connection.rollback()
        raise ve
    except Exception as e:
        connection.rollback()
        print(f"Error adding booking: {e}")
        return False
    finally:
        cursor.close()
        connection.close()

def update_booking(booking_id, booking_date, passenger_id, schedule_id, number_of_tickets):
    passenger_id, schedule_id, number_of_tickets = validate_booking(passenger_id, schedule_id, number_of_tickets)
    
    connection = get_connection()
    cursor = connection.cursor()
    try:
        capacity_check_sql = """
            SELECT 
                t.capacity AS total_capacity, 
                COALESCE(SUM(b.number_of_tickets), 0) AS booked_tickets
            FROM SCHEDULE s
            JOIN TRAIN t ON s.train_id = t.train_id
            LEFT JOIN BOOKING b ON s.schedule_id = b.schedule_id AND b.booking_id != %s
            WHERE s.schedule_id = %s
            GROUP BY t.capacity
        """
        cursor.execute(capacity_check_sql, (booking_id, schedule_id))
        result = cursor.fetchone()
        
        if not result:
            raise ValueError("Selected schedule does not exist.")
            
        total_capacity, booked_tickets = result
        available_seats = total_capacity - booked_tickets
        
        if number_of_tickets > available_seats:
            raise ValueError(f"Not enough capacity! Only {available_seats} seats remaining.")

        sql = """
            UPDATE BOOKING 
            SET booking_date = %s, passenger_id = %s, schedule_id = %s, number_of_tickets = %s 
            WHERE booking_id = %s
        """
        cursor.execute(sql, (booking_date, passenger_id, schedule_id, number_of_tickets, booking_id))
        connection.commit()
        return True
        
    except ValueError as ve:
        connection.rollback()
        raise ve
    except Exception as e:
        connection.rollback()
        print(f"Error updating booking: {e}")
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