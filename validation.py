MAX_NAME_LENGTH = 50
MAX_CODE_LENGTH = 20
MAX_PHONE_LENGTH = 20


def validate_station(station_name, city):
    """Validates station name and city."""
    if not isinstance(station_name, str) or not station_name.strip():
        raise ValueError("Station name cannot be empty.")
    if len(station_name.strip()) > MAX_NAME_LENGTH:
        raise ValueError(f"Station name is too long (max {MAX_NAME_LENGTH} characters).")
        
    if not isinstance(city, str) or not city.strip():
        raise ValueError("City cannot be empty.")
    if len(city.strip()) > MAX_NAME_LENGTH:
        raise ValueError(f"City name is too long (max {MAX_NAME_LENGTH} characters).")
        
    return station_name.strip(), city.strip()


def validate_train(train_code, train_type, capacity):
    """Validates train code and type."""
    if not isinstance(train_code, str) or not train_code.strip():
        raise ValueError("Train code cannot be empty.")
    if len(train_code.strip()) > MAX_CODE_LENGTH:
        raise ValueError(f"Train code is too long (max {MAX_CODE_LENGTH} characters).")
        
    if not isinstance(train_type, str) or not train_type.strip():
        raise ValueError("Train type cannot be empty.")
    if len(train_type.strip()) > MAX_NAME_LENGTH:
        raise ValueError(f"Train type is too long (max {MAX_NAME_LENGTH} characters).")

    try:
        capacity_int = int(capacity)
    except (ValueError, TypeError):
        raise ValueError("Capacity must be a valid integer.")
        
    if capacity_int <= 0:
        raise ValueError("Capacity must be greater than zero.")
        
    return train_code.strip(), train_type.strip(), capacity_int
        

def validate_passenger(first_name, last_name, phone_number):
    """Validates passenger details."""
    if not isinstance(first_name, str) or not first_name.strip():
        raise ValueError("First name cannot be empty.")
    if len(first_name.strip()) > MAX_NAME_LENGTH:
        raise ValueError("First name is too long.")
        
    if not isinstance(last_name, str) or not last_name.strip():
        raise ValueError("Last name cannot be empty.")
    if len(last_name.strip()) > MAX_NAME_LENGTH:
        raise ValueError("Last name is too long.")
        
    if not isinstance(phone_number, str) or not phone_number.strip():
        raise ValueError("Phone number cannot be empty.")
    if len(phone_number.strip()) > MAX_PHONE_LENGTH:
        raise ValueError("Phone number is too long.")
        
    return first_name.strip(), last_name.strip(), phone_number.strip()


def validate_email(email):
    """Validates passenger email."""
    if not isinstance(email, str) or not email.strip():
        raise ValueError("Email cannot be empty.")
    if len(email.strip()) > 100:  # Aligned with VARCHAR(100) in the database
        raise ValueError("Email is too long.")
    
    email_cleaned = email.strip()
    # A simple and standard check for email format
    if "@" not in email_cleaned or "." not in email_cleaned:
        raise ValueError("Invalid email format. Must contain '@' and '.'")
        
    return email_cleaned


from datetime import datetime
def validate_schedule(departure_time, travel_date, arrival_time, train_id, dep_station_id, arr_station_id):
    """Validates schedule inputs and IDs."""
    if not travel_date:
        raise ValueError("Travel date must be specified.")
        
    if not isinstance(departure_time, str) or not departure_time.strip():
        raise ValueError("Departure time cannot be empty.")
    else:
        departure_time_obj = datetime.strptime(departure_time.strip(), "%H:%M:%S").time()

    if not isinstance(arrival_time, str) or not arrival_time.strip():
        raise ValueError("Arrival time cannot be empty.")
    else:
        arrival_time_obj = datetime.strptime(arrival_time.strip(), "%H:%M:%S").time()
        
    if not isinstance(train_id, int) or train_id <= 0:
        raise ValueError("Invalid Train ID.")
    if not isinstance(dep_station_id, int) or dep_station_id <= 0:
        raise ValueError("Invalid Departure Station ID.")
    if not isinstance(arr_station_id, int) or arr_station_id <= 0:
        raise ValueError("Invalid Arrival Station ID.")
        
    if dep_station_id == arr_station_id:
        raise ValueError("Departure and arrival stations cannot be the same.")
        
    if arrival_time_obj <= departure_time_obj:
        raise ValueError("Arrival time must be strictly greater than departure time.")
        
    return departure_time.strip(), str(travel_date), arrival_time.strip(), train_id, dep_station_id, arr_station_id


def validate_booking(passenger_id, schedule_id, number_of_tickets):
    """Validates passenger ID, schedule ID, and number of tickets."""
    
    if not isinstance(passenger_id, int) or passenger_id <= 0:
        raise ValueError("Invalid Passenger ID.")
        
    if not isinstance(schedule_id, int) or schedule_id <= 0:
        raise ValueError("Invalid Schedule ID.")
        
    try:
        tickets_int = int(number_of_tickets)
    except (ValueError, TypeError):
        raise ValueError("Number of tickets must be a valid integer.")
        
    if tickets_int <= 0:
        raise ValueError("Number of tickets must be at least 1.")
        
    return passenger_id, schedule_id, tickets_int