import streamlit as st
import pandas as pd
from datetime import datetime
import time
from train_operations import (
    get_all_stations, add_station, delete_station,
    get_all_trains, add_train, delete_train,
    get_all_passengers, add_passenger, delete_passenger,
    get_all_bookings, add_booking, delete_booking,
    get_all_schedules, add_schedule, delete_schedule
)

# Page configuration
st.set_page_config(page_title="Train Booking System", layout="wide")

st.title("🚂 Train Booking Management System")
st.write("HAMK University - Software Application Development Project")

# Create tabs for different database entities
tab_stations, tab_trains, tab_passengers, tab_schedules, tab_bookings = st.tabs([
    "📍 Stations", "🚆 Trains", "👥 Passengers", "🕒 Schedules", "🎫 Bookings"
])

# ==================== 1. STATIONS TAB ====================
with tab_stations:
    st.header("Manage Stations")
    
    # Add station form
    with st.form("add_station_form"):
        st.subheader("Add New Station")
        station_name = st.text_input("Station Name")
        city = st.text_input("City")
        submitted = st.form_submit_button("Add Station")
        
        if submitted:
            if not station_name.strip() or not city.strip():
                st.error("Station name and city cannot be empty.")
            else:
                success = add_station(station_name.strip(), city.strip())
                if success:
                    st.success("Station added successfully!")
                    time.sleep(1.5)
                    st.experimental_rerun()
                else:
                    st.error("Failed to add station. Please check database constraints.")

    # Display existing stations
    st.subheader("Existing Stations")
    stations = get_all_stations()
    if stations:
        df_stations = pd.DataFrame(stations, columns=["Station ID", "Station Name", "City"])
        st.dataframe(df_stations, hide_index=True)
        
        # Delete station form
        with st.form("delete_station_form"):
            station_ids = [s[0] for s in stations]
            selected_station_id = st.selectbox("Select Station ID to Delete", station_ids)
            delete_submitted = st.form_submit_button("Delete Station")
            if delete_submitted:
                if delete_station(selected_station_id):
                    st.success(f"Station {selected_station_id} deleted successfully!")
                    time.sleep(1.5)
                    st.experimental_rerun()
                else:
                    st.error("Error deleting station.")
    else:
        st.info("No stations found in the database.")


# ==================== 2. TRAINS TAB ====================
with tab_trains:
    st.header("Manage Trains")
    
    # Add train form
    with st.form("add_train_form"):
        st.subheader("Add New Train")
        train_code = st.text_input("Train Code (e.g., IC121)")
        train_type = st.text_input("Train Type (e.g., InterCity)")
        submitted = st.form_submit_button("Add Train")
        
        if submitted:
            if not train_code.strip() or not train_type.strip():
                st.error("Train code and type cannot be empty.")
            else:
                success = add_train(train_code.strip(), train_type.strip())
                if success:
                    st.success("Train added successfully!")
                    time.sleep(1.5)
                    st.experimental_rerun()
                else:
                    st.error("Failed to add train (Train code might already exist).")

    # Display existing trains
    st.subheader("Existing Trains")
    trains = get_all_trains()
    if trains:
        df_trains = pd.DataFrame(trains, columns=["Train ID", "Train Code", "Train Type"])
        st.dataframe(df_trains, hide_index=True)
        
        # Delete train form
        with st.form("delete_train_form"):
            train_ids = [t[0] for t in trains]
            selected_train_id = st.selectbox("Select Train ID to Delete", train_ids)
            delete_submitted = st.form_submit_button("Delete Train")
            if delete_submitted:
                if delete_train(selected_train_id):
                    st.success(f"Train {selected_train_id} deleted successfully!")
                    time.sleep(1.5)
                    st.experimental_rerun()
                else:
                    st.error("Error deleting train.")
    else:
        st.info("No trains found in the database.")


# ==================== 3. PASSENGERS TAB ====================
with tab_passengers:
    st.header("Manage Passengers")
    
    # Add passenger form
    with st.form("add_passenger_form"):
        st.subheader("Add New Passenger")
        first_name = st.text_input("First Name")
        last_name = st.text_input("Last Name")
        phone_number = st.text_input("Phone Number")
        submitted = st.form_submit_button("Add Passenger")
        
        if submitted:
            if not first_name.strip() or not last_name.strip() or not phone_number.strip():
                st.error("All passenger fields must be filled.")
            else:
                success = add_passenger(first_name.strip(), last_name.strip(), phone_number.strip())
                if success:
                    st.success("Passenger added successfully!")
                    time.sleep(1.5)
                    st.experimental_rerun()
                else:
                    st.error("Failed to add passenger.")

    # Display existing passengers
    st.subheader("Existing Passengers")
    passengers = get_all_passengers()
    if passengers:
        df_passengers = pd.DataFrame(passengers, columns=["Passenger ID", "First Name", "Last Name", "Phone"])
        st.dataframe(df_passengers, hide_index=True)
        
        # Delete passenger form
        with st.form("delete_passenger_form"):
            passenger_ids = [p[0] for p in passengers]
            selected_passenger_id = st.selectbox("Select Passenger ID to Delete", passenger_ids)
            delete_submitted = st.form_submit_button("Delete Passenger")
            if delete_submitted:
                if delete_passenger(selected_passenger_id):
                    st.success(f"Passenger {selected_passenger_id} deleted successfully!")
                    time.sleep(1.5)
                    st.experimental_rerun()
                else:
                    st.error("Error deleting passenger.")
    else:
        st.info("No passengers found in the database.")


# ==================== 4. SCHEDULES TAB ====================
with tab_schedules:
    st.header("Manage Schedules")
    
    trains = get_all_trains()
    stations = get_all_stations()
    
    # Add schedule form
    with st.form("add_schedule_form"):
        st.subheader("Add New Schedule")
        travel_date = st.date_input("Travel Date")
        departure_time = st.text_input("Departure Time", value="08:00:00")
        arrival_time = st.text_input("Arrival Time", value="12:00:00")
       
        train_options = {t[1]: t[0] for t in trains} if trains else {}
        station_options = {s[1]: s[0] for s in stations} if stations else {}
        
        selected_train_code = st.selectbox("Train", list(train_options.keys()) if train_options else ["No Trains Available"])
        selected_dep_station = st.selectbox("Departure Station", list(station_options.keys()) if station_options else ["No Stations Available"])
        selected_arr_station = st.selectbox("Arrival Station", list(station_options.keys()) if station_options else ["No Stations Available"])
        
        submitted = st.form_submit_button("Add Schedule")
        
        if submitted:
            if not trains or not stations:
                st.error("Please add at least one train and two stations first.")
            else:
                train_id = train_options[selected_train_code]
                dep_id = station_options[selected_dep_station]
                arr_id = station_options[selected_arr_station]
                
                if dep_id == arr_id:
                    st.error("Departure and arrival stations cannot be the same.")
                else:
                    success = add_schedule(departure_time, str(travel_date), arrival_time, train_id, dep_id, arr_id)
                    if success:
                        st.success("Schedule added successfully!")
                        time.sleep(1.5)
                        st.experimental_rerun()
                    else:
                        st.error("Failed to add schedule.")

    # Display existing schedules
    st.subheader("Existing Schedules")
    schedules = get_all_schedules()
    if schedules:
        df_schedules = pd.DataFrame(schedules, columns=["Schedule ID", "Dep Time", "Travel Date", "Arr Time", "Train ID", "Dep Station ID", "Arr Station ID"])
        st.dataframe(df_schedules, hide_index=True)
        
        # Delete schedule form
        with st.form("delete_schedule_form"):
            schedule_ids = [s[0] for s in schedules]
            selected_schedule_id = st.selectbox("Select Schedule ID to Delete", schedule_ids)
            delete_submitted = st.form_submit_button("Delete Schedule")
            if delete_submitted:
                if delete_schedule(selected_schedule_id):
                    st.success(f"Schedule {selected_schedule_id} deleted successfully!")
                    time.sleep(1.5)
                    st.experimental_rerun()
                else:
                    st.error("Error deleting schedule.")
    else:
        st.info("No schedules found in the database.")


# ==================== 5. BOOKINGS TAB ====================
with tab_bookings:
    st.header("Manage Bookings")
    
    passengers = get_all_passengers()
    schedules = get_all_schedules()
    
    # Add booking form
    with st.form("add_booking_form"):
        st.subheader("Add New Booking")
        status = st.selectbox("Status", ["Confirmed", "Pending", "Cancelled"])
        ticket_price = st.number_input("Ticket Price (€)", min_value=0.0, step=1.0, value=50.0)
        
        passenger_options = {f"{p[1]} {p[2]} (ID: {p[0]})": p[0] for p in passengers} if passengers else {}
        schedule_options = {f"Schedule ID: {s[0]} (Date: {s[2]})": s[0] for s in schedules} if schedules else {}
        
        selected_passenger = st.selectbox("Passenger", list(passenger_options.keys()) if passenger_options else ["No Passengers Available"])
        selected_schedule = st.selectbox("Schedule", list(schedule_options.keys()) if schedule_options else ["No Schedules Available"])
        seat_id_input = st.number_input("Seat ID (Optional, leave 0 if none)", min_value=0, step=1, value=0)
        
        submitted = st.form_submit_button("Add Booking")
        
        if submitted:
            if not passengers or not schedules:
                st.error("Please add passengers and schedules first.")
            else:
                passenger_id = passenger_options[selected_passenger]
                schedule_id = schedule_options[selected_schedule]
                seat_id = seat_id_input if seat_id_input > 0 else None
                
                booking_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                success = add_booking(booking_date, status, ticket_price, passenger_id, schedule_id, seat_id)
                if success:
                    st.success("Booking added successfully!")
                    time.sleep(1.5)
                    st.experimental_rerun()
                else:
                    st.error("Failed to add booking.")

    # Display existing bookings
    st.subheader("Existing Bookings")
    bookings = get_all_bookings()
    if bookings:
        df_bookings = pd.DataFrame(bookings, columns=["Booking ID", "Booking Date", "Status", "Price", "Passenger ID", "Schedule ID", "Seat ID"])
        st.dataframe(df_bookings, hide_index=True)
        
        # Delete booking form
        with st.form("delete_booking_form"):
            booking_ids = [b[0] for b in bookings]
            selected_booking_id = st.selectbox("Select Booking ID to Delete", booking_ids)
            delete_submitted = st.form_submit_button("Delete Booking")
            if delete_submitted:
                if delete_booking(selected_booking_id):
                    st.success(f"Booking {selected_booking_id} deleted successfully!")
                    time.sleep(1.5)
                    st.experimental_rerun()
                else:
                    st.error("Error deleting booking.")
    else:
        st.info("No bookings found in the database.")