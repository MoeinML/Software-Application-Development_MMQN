import streamlit as st
import pandas as pd
from datetime import datetime
import time
import logging
from train_operations import (
    get_all_stations, add_station, update_station, delete_station,
    get_all_trains, add_train, update_train, delete_train,
    get_all_passengers, add_passenger, add_passenger_with_email_transaction, update_passenger, delete_passenger,
    get_all_passenger_emails, add_passenger_email, update_passenger_email, delete_passenger_email,
    get_all_bookings, add_booking, update_booking, delete_booking,
    get_all_schedules, get_all_schedules_with_capacity, add_schedule, update_schedule, delete_schedule
)
logger = logging.getLogger(__name__)

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
        station_name = st.text_input("Station Name", key="add_st_name")
        city = st.text_input("City", key="add_st_city")
        submitted = st.form_submit_button("Add Station")
        
        if submitted:
            try:
                success = add_station(station_name, city)
                if success:
                    st.success("Station added successfully!")
                    time.sleep(1.2)
                    st.experimental_rerun()
                else:
                    st.error("Failed to add station. Check if station name already exists.")
            except ValueError as ve:
                st.error(f"Validation Error: {ve}")
            except Exception as e:
                logger.exception("Failed to save station to database")
                st.error("A database error occurred. Please try again.")

    # Display existing stations
    st.subheader("Existing Stations")
    stations = get_all_stations()
    if stations:
        df_stations = pd.DataFrame(stations, columns=["Station ID", "Station Name", "City"])
        st.dataframe(df_stations, hide_index=True)
        
        col_del, col_upd = st.columns(2)
        
        # Delete station form
        with col_del:
            with st.form("delete_station_form"):
                st.subheader("Delete Station")
                station_ids = [s[0] for s in stations]
                selected_station_id = st.selectbox("Select Station ID to Delete", station_ids, key="del_st_sel")
                delete_submitted = st.form_submit_button("Delete Station", use_container_width=True)
                if delete_submitted:
                    try:
                        if delete_station(selected_station_id):
                            st.success(f"Station {selected_station_id} deleted successfully!")
                            time.sleep(1.2)
                            st.experimental_rerun()
                    except ValueError as ve:
                        st.error(f"Deletion Error: {ve}")
                    except Exception as e:
                        st.error("Error deleting station (it might be used in schedules).")
        
        # Update station section
        with col_upd:
            st.subheader("Update Station")
            station_dict = {s[0]: s for s in stations}
            selected_update_id = st.selectbox("Select Station ID to Update", list(station_dict.keys()), key="upd_st_id")
            curr_st = station_dict[selected_update_id]
            
            up_station_name = st.text_input("Station Name", value=curr_st[1], key="up_st_name")
            up_city = st.text_input("City", value=curr_st[2], key="up_st_city")
            
            if st.button("Update Station", use_container_width=True, key="btn_update_st"):
                try:
                    success = update_station(selected_update_id, up_station_name, up_city)
                    if success:
                        st.success(f"Station {selected_update_id} updated successfully!")
                        time.sleep(1.2)
                        st.experimental_rerun()
                    else:
                        st.error("Failed to update station.")
                except ValueError as ve:
                    st.error(f"Validation Error: {ve}")
                except Exception as e:
                    logger.exception("Failed to update station")
                    st.error("A database error occurred.")
    else:
        st.info("No stations found in the database.")


# ==================== 2. TRAINS TAB ====================
with tab_trains:
    st.header("Manage Trains")
    
    # Add train form
    with st.form("add_train_form"):
        st.subheader("Add New Train")
        train_code = st.text_input("Train Code (e.g., IC121)", key="add_tr_code")
        train_type = st.text_input("Train Type (e.g., InterCity)", key="add_tr_type")
        capacity = st.number_input("Capacity", min_value=1, value=150, step=1, key="add_tr_cap")
        submitted = st.form_submit_button("Add Train")
        
        if submitted:
            try:
                success = add_train(train_code, train_type, capacity)
                if success:
                    st.success("Train added successfully!")
                    time.sleep(1.2)
                    st.experimental_rerun()
                else:
                    st.error("Failed to add train (Train code might already exist).")
            except ValueError as ve:
                st.error(f"Validation Error: {ve}")
            except Exception as e:
                logger.exception("Failed to save train to database")
                st.error("A database error occurred. Please try again.")

    # Display existing trains
    st.subheader("Existing Trains")
    trains = get_all_trains()
    if trains:
        df_trains = pd.DataFrame(trains, columns=["Train ID", "Train Code", "Train Type", "Capacity"])
        st.dataframe(df_trains, hide_index=True)
        
        col_del_t, col_upd_t = st.columns(2)
                
        # Delete train form
        with col_del_t:
            with st.form("delete_train_form"):
                st.subheader("Delete Train")
                train_ids = [t[0] for t in trains]
                selected_train_id = st.selectbox("Select Train ID to Delete", train_ids, key="del_tr_sel")
                delete_submitted = st.form_submit_button("Delete Train", use_container_width=True)
                if delete_submitted:
                    try:
                        if delete_train(selected_train_id):
                            st.success(f"Train {selected_train_id} deleted successfully!")
                            time.sleep(1.2)
                            st.experimental_rerun()
                    except ValueError as ve:
                        st.error(f"Deletion Error: {ve}")
                    except Exception as e:
                        st.error("Error deleting train (it might be used in schedules).")
        
        # Update train section
        with col_upd_t:
            st.subheader("Update Train")
            train_dict = {t[0]: t for t in trains}
            selected_upd_train_id = st.selectbox("Select Train ID to Update", list(train_dict.keys()), key="upd_tr_id_field")
            curr_tr = train_dict[selected_upd_train_id]
            
            up_train_code = st.text_input("Train Code", value=curr_tr[1], key="up_tr_code")
            up_train_type = st.text_input("Train Type", value=curr_tr[2], key="up_tr_type")
            up_capacity = st.number_input("Capacity", min_value=1, value=int(curr_tr[3]), step=1, key="up_tr_cap")
            
            if st.button("Update Train", use_container_width=True, key="btn_update_tr"):
                try:
                    success = update_train(selected_upd_train_id, up_train_code, up_train_type, up_capacity)
                    if success:
                        st.success(f"Train {selected_upd_train_id} updated successfully!")
                        time.sleep(1.2)
                        st.experimental_rerun()
                    else:
                        st.error("Failed to update train.")
                except ValueError as ve:
                    st.error(f"Validation Error: {ve}")
                except Exception as e:
                    logger.exception("Failed to update train")
                    st.error("A database error occurred.")
    else:
        st.info("No trains found in the database.")


# ==================== 3. PASSENGERS TAB ====================
with tab_passengers:
    st.markdown("### Manage Passengers & Emails")
    
    col1, col2 = st.columns(2)
    
    # Column 1: Add New Passenger with email
    with col1:
        with st.form("add_passenger_form"):
            st.subheader("Add New Passenger")
            first_name = st.text_input("First Name")
            last_name = st.text_input("Last Name")
            phone_number = st.text_input("Phone Number")
            submitted = st.form_submit_button("Add Passenger", use_container_width=True)

        if submitted:
            try:
                success = add_passenger(first_name, last_name, phone_number)
                if success:
                    st.success("Passenger added successfully!")
                    time.sleep(1.2)
                    st.experimental_rerun()
                else:
                    st.error("Failed to add passenger.")
            except ValueError as ve:
                st.error(f"Validation Error: {ve}")
            except Exception as e:
                logger.exception("Failed to save passenger to database")
                st.error("A database error occurred. Please try again.")

    # Column 2: Add Email to Passenger
    with col2:
        with st.form("add_email_form"):
            st.subheader("Add Email to Passenger")
            passengers_list = get_all_passengers()
            if passengers_list:
                passenger_options = {p[0]: f"{p[0]} - {p[1]} {p[2]}" for p in passengers_list}
                selected_pid = st.selectbox("Select Passenger", options=list(passenger_options.keys()), format_func=lambda x: passenger_options[x], key="add_em_pid")
                email_input = st.text_input("Email Address", key="add_em_addr")
                email_submitted = st.form_submit_button("Add Email", use_container_width=True)
                
                if email_submitted:
                    try:
                        success = add_passenger_email(selected_pid, email_input)
                        if success:
                            st.success("Email added successfully!")
                            time.sleep(1.2)
                            st.experimental_rerun()
                    except ValueError as ve:
                        st.error(f"Validation Error: {ve}")
                    except Exception as e:
                        logger.exception("Failed to save email to database")
                        st.error("A database error occurred. Please try again.")
            else:
                st.info("Please add a passenger first.")

    # Add New Passenger with email
    # ==================== TASK B: TRANSACTION FORM ====================
    with st.expander("🧪 Advanced Feature: Transaction Test (Task B)"):
        st.subheader("Add Passenger with Email (Atomic Transaction)")
        st.write("This form demonstrates atomicity: both records are inserted together, or none if an error occurs.")
            
        with st.form("transaction_passenger_form"):
            trx_fname = st.text_input("First Name", key="trx_p_fn")
            trx_lname = st.text_input("Last Name", key="trx_p_ln")
            trx_phone = st.text_input("Phone Number", key="trx_p_ph")
            trx_email = st.text_input("Email Address (Try duplicate to test rollback)", key="trx_p_em")
                
            trx_submitted = st.form_submit_button("Execute Transaction", use_container_width=True)
                
            if trx_submitted:
                try:
                    # Call the transaction function (validation and rollback are handled inside)
                    add_passenger_with_email_transaction(trx_fname, trx_lname, trx_phone, trx_email)
                    st.success("Transaction committed successfully! Both passenger and email were saved.")
                    time.sleep(1.2)
                    st.experimental_rerun()
                except ValueError as ve:
                    # Catch validation or rollback errors raised from the backend and show them cleanly
                    st.error(f"{ve}")
                except Exception as e:
                    logger.exception("Unexpected database transaction error")
                    st.error("A critical database error occurred during the transaction.")
    
    st.markdown("---")

    # Display existing data
    passengers = get_all_passengers()
    emails_data = get_all_passenger_emails()

    table_col1, table_col2 = st.columns(2)
    
    with table_col1:
        st.subheader("Existing Passengers")
        if passengers:
            df_passengers = pd.DataFrame(passengers, columns=["Passenger ID", "First Name", "Last Name", "Phone"])
            st.dataframe(df_passengers, hide_index=True)
        else:
            st.info("No passengers found.")

    with table_col2:
        st.subheader("Existing Passenger Emails")
        if emails_data:
            df_emails = pd.DataFrame(emails_data, columns=["Passenger ID", "Email"])
            st.dataframe(df_emails, hide_index=True)
        else:
            st.info("No emails found.")

    st.markdown("---")

    del_col1, del_col2 = st.columns(2)
    
    with del_col1:
        with st.form("delete_passenger_form"):
            st.subheader("Delete Passenger")
            if passengers:
                passenger_ids = [p[0] for p in passengers]
                selected_passenger_id = st.selectbox("Select Passenger ID", passenger_ids, key="del_p_sel")
                delete_submitted = st.form_submit_button("Delete Passenger", use_container_width=True)
                if delete_submitted:
                    try:
                        if delete_passenger(selected_passenger_id):
                            st.success(f"Passenger {selected_passenger_id} deleted successfully!")
                            time.sleep(1.2)
                            st.experimental_rerun()
                    except ValueError as ve:
                        st.error(f"Deletion Error: {ve}")
                    except Exception as e:
                        st.error("Error deleting passenger.")
            else:
                st.info("No passengers available.")

        # Update Passenger Section
        st.subheader("Update Passenger")
        if passengers:
            pass_dict = {p[0]: p for p in passengers}
            upd_p_id = st.selectbox("Select Passenger ID to Update", list(pass_dict.keys()), key="upd_p_sel_box")
            curr_p = pass_dict[upd_p_id]
            
            up_fname = st.text_input("First Name", value=curr_p[1], key="up_p_fn")
            up_lname = st.text_input("Last Name", value=curr_p[2], key="up_p_ln")
            up_phone = st.text_input("Phone Number", value=curr_p[3], key="up_p_ph")
            
            if st.button("Update Passenger", use_container_width=True, key="btn_update_p"):
                try:
                    if update_passenger(upd_p_id, up_fname, up_lname, up_phone):
                        st.success("Passenger updated successfully!")
                        time.sleep(1.2)
                        st.experimental_rerun()
                except ValueError as ve:
                    st.error(f"Validation Error: {ve}")
                except Exception as e:
                    logger.exception("Failed to update passenger")
                    st.error("A database error occurred.")
        else:
            st.info("No passengers available.")
    
    with del_col2:
        with st.form("delete_email_form"):
            st.subheader("Delete Passenger Email")
            if emails_data:
                email_options = {(e[0], e[1]): f"ID {e[0]} - {e[1]}" for e in emails_data}
                selected_email_key = st.selectbox("Select Email to Delete", options=list(email_options.keys()), format_func=lambda x: email_options[x], key="del_em_sel")
                email_delete_submitted = st.form_submit_button("Delete Email", use_container_width=True)
                
                if email_delete_submitted:
                    pid_to_del, email_to_del = selected_email_key
                    if delete_passenger_email(pid_to_del, email_to_del):
                        st.success(f"Email deleted successfully!")
                        time.sleep(1.2)
                        st.experimental_rerun()
                    else:
                        st.error("Error deleting email.")
            else:
                st.info("No emails available.")

        # Update Email Section
        st.subheader("Update Passenger Email")
        if emails_data:
            email_options_upd = {(e[0], e[1]): f"ID {e[0]} - {e[1]}" for e in emails_data}
            selected_upd_email_key = st.selectbox("Select Email to Update", options=list(email_options_upd.keys()), key="upd_email_sel_box", format_func=lambda x: email_options_upd[x])
            
            old_pid, old_email = selected_upd_email_key
            new_email_input = st.text_input("New Email Address", value=old_email, key="up_em_addr")
            
            if st.button("Update Email", use_container_width=True, key="btn_update_em"):
                try:
                    if update_passenger_email(old_pid, old_email, new_email_input):
                        st.success("Email updated successfully!")
                        time.sleep(1.2)
                        st.experimental_rerun()
                except ValueError as ve:
                    st.error(f"Validation Error: {ve}")
                except Exception as e:
                    logger.exception("Failed to update email")
                    st.error("A database error occurred.")
        else:
            st.info("No emails available.")


# ==================== 4. SCHEDULES TAB ====================
with tab_schedules:
    st.header("Manage Schedules")
    
    trains = get_all_trains()
    stations = get_all_stations()
    
    # Add schedule form
    with st.form("add_schedule_form"):
        st.subheader("Add New Schedule")
        travel_date = st.date_input("Travel Date", key="add_sch_date")
        departure_time = st.text_input("Departure Time", value="08:00:00", key="add_sch_dep")
        arrival_time = st.text_input("Arrival Time", value="12:00:00", key="add_sch_arr")
       
        train_options = {t[1]: t[0] for t in trains} if trains else {}
        station_options = {s[1]: s[0] for s in stations} if stations else {}
        
        selected_train_code = st.selectbox("Train", list(train_options.keys()) if train_options else ["No Trains Available"], key="add_sch_tr")
        selected_dep_station = st.selectbox("Departure Station", list(station_options.keys()) if station_options else ["No Stations Available"], key="add_sch_depst")
        selected_arr_station = st.selectbox("Arrival Station", list(station_options.keys()) if station_options else ["No Stations Available"], key="add_sch_arrst")
        
        submitted = st.form_submit_button("Add Schedule")
        
        if submitted:
            if not trains or not stations:
                st.error("Please add at least one train and two stations first.")
            else:
                train_id = train_options[selected_train_code]
                dep_id = station_options[selected_dep_station]
                arr_id = station_options[selected_arr_station]
                
                try:
                    success = add_schedule(departure_time, travel_date, arrival_time, train_id, dep_id, arr_id)
                    if success:
                        st.success("Schedule added successfully!")
                        time.sleep(1.2)
                        st.experimental_rerun()
                    else:
                        st.error("Failed to add schedule.")
                except ValueError as ve:
                    st.error(f"Validation Error: {ve}")
                except Exception as e:
                    logger.exception("Failed to save schedule to database")
                    st.error("A database error occurred. Please try again.")

    # Display existing schedules
    st.subheader("Existing Schedules")
    schedules = get_all_schedules()
    if schedules:
        df_schedules = pd.DataFrame(schedules, columns=["Schedule ID", "Dep Time", "Travel Date", "Arr Time", "Train ID", "Dep Station ID", "Arr Station ID"])
        st.dataframe(df_schedules, hide_index=True)
        
        col_del_sch, col_upd_sch = st.columns(2)
        
        # Delete schedule form
        with col_del_sch:
            with st.form("delete_schedule_form"):
                st.subheader("Delete Schedule")
                schedule_ids = [s[0] for s in schedules]
                selected_schedule_id = st.selectbox("Select Schedule ID to Delete", schedule_ids, key="del_sch_sel")
                delete_submitted = st.form_submit_button("Delete Schedule", use_container_width=True)
                if delete_submitted:
                    try:
                        if delete_schedule(selected_schedule_id):
                            st.success(f"Schedule {selected_schedule_id} deleted successfully!")
                            time.sleep(1.2)
                            st.experimental_rerun()
                    except ValueError as ve:
                        st.error(f"Deletion Error: {ve}")
                    except Exception as e:
                        st.error("Error deleting schedule.")
        
        # Update schedule section
        with col_upd_sch:
            st.subheader("Update Schedule")
            sch_dict = {s[0]: s for s in schedules}
            selected_upd_sch_id = st.selectbox("Select Schedule ID to Update", list(sch_dict.keys()), key="upd_sch_sel_box")
            curr_sch = sch_dict[selected_upd_sch_id]
            
            up_travel_date = st.date_input("Travel Date", value=datetime.strptime(str(curr_sch[2]), "%Y-%m-%d").date() if isinstance(curr_sch[2], str) or hasattr(curr_sch[2], "strftime") else curr_sch[2], key="up_sch_date")
            up_dep_time = st.text_input("Departure Time", value=str(curr_sch[1]), key="up_sch_dep")
            up_arr_time = st.text_input("Arrival Time", value=str(curr_sch[3]), key="up_sch_arr")
            
            train_list = list(trains)
            station_list = list(stations)
            
            train_options_u = {t[1]: t[0] for t in train_list} if train_list else {}
            station_options_u = {s[1]: s[0] for s in station_list} if station_list else {}
            
            curr_train_code = next((t[1] for t in train_list if t[0] == curr_sch[4]), list(train_options_u.keys())[0] if train_options_u else "")
            train_keys = list(train_options_u.keys())
            train_index = train_keys.index(curr_train_code) if curr_train_code in train_keys else 0
            
            curr_dep_name = next((s[1] for s in station_list if s[0] == curr_sch[5]), "")
            station_keys = list(station_options_u.keys())
            dep_index = station_keys.index(curr_dep_name) if curr_dep_name in station_keys else 0
            
            curr_arr_name = next((s[1] for s in station_list if s[0] == curr_sch[6]), "")
            arr_index = station_keys.index(curr_arr_name) if curr_arr_name in station_keys else (1 if len(station_keys) > 1 else 0)
            
            up_sel_train = st.selectbox("Train", train_keys if train_keys else ["No Trains"], index=train_index, key="up_sch_tr")
            up_sel_dep = st.selectbox("Departure Station", station_keys if station_keys else ["No Stations"], index=dep_index, key="up_sch_depst")
            up_sel_arr = st.selectbox("Arrival Station", station_keys if station_keys else ["No Stations"], index=arr_index, key="up_sch_arrst")
            
            if st.button("Update Schedule", use_container_width=True, key="btn_update_sch"):
                if not trains or not stations:
                    st.error("Please ensure trains and stations exist.")
                else:
                    t_id = train_options_u[up_sel_train]
                    d_id = station_options_u[up_sel_dep]
                    a_id = station_options_u[up_sel_arr]
                    try:
                        if update_schedule(selected_upd_sch_id, up_dep_time, up_travel_date, up_arr_time, t_id, d_id, a_id):
                            st.success("Schedule updated successfully!")
                            time.sleep(1.2)
                            st.experimental_rerun()
                    except ValueError as ve:
                        st.error(f"Validation Error: {ve}")
                    except Exception as e:
                        logger.exception("Failed to update schedule")
                        st.error("A database error occurred.")
    else:
        st.info("No schedules found in the database.")


# ==================== 5. BOOKINGS TAB ====================
with tab_bookings:
    st.header("Manage Bookings")
    
    passengers = get_all_passengers()
    schedules = get_all_schedules_with_capacity()
    
    # Add booking form
    with st.form("add_booking_form"):
        st.subheader("Add New Booking")
        
        passenger_options = {f"{p[1]} {p[2]} (ID: {p[0]})": p[0] for p in passengers} if passengers else {}
        selected_passenger = st.selectbox("Passenger", list(passenger_options.keys()) if passenger_options else ["No Passengers Available"], key="add_book_pass")
        
        schedule_options = {}
        if schedules:
            for s in schedules:
                label = f"Train: {s[4]} | {s[5]} ➔ {s[6]} | Date: {s[2]} | Departure: {s[1]} | Available Seats: {s[7]}"
                schedule_options[label] = s[0]
                
        selected_schedule = st.selectbox("Schedule & Available Capacity", list(schedule_options.keys()) if schedule_options else ["No Schedules Available"], key="add_book_sched")
        
        num_tickets = st.number_input("Number of Tickets", min_value=1, step=1, value=1, key="add_book_num")
        
        submitted = st.form_submit_button("Add Booking")
        
        if submitted:
            if not passengers or not schedules:
                st.error("Please add passengers and schedules first.")
            else:
                passenger_id = passenger_options[selected_passenger]
                schedule_id = schedule_options[selected_schedule]
                
                booking_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                try:
                    success = add_booking(booking_date, passenger_id, schedule_id, num_tickets)
                    if success:
                        st.success("Booking added successfully!")
                        time.sleep(1.2)
                        st.experimental_rerun()
                    else:
                        st.error("Failed to add booking. Check available capacity.")
                except ValueError as ve:
                    st.error(f"Validation Error: {ve}")
                except Exception as e:
                    logger.exception("Failed to save booking to database")
                    st.error("A database error occurred. Please try again.")

    # Display existing bookings
    st.subheader("Existing Bookings")
    bookings = get_all_bookings()
    if bookings:
        df_bookings = pd.DataFrame(bookings, columns=["Booking ID", "Booking Date", "Passenger ID", "Schedule ID", "Tickets Count"])
        st.dataframe(df_bookings, hide_index=True)
        
        col_del_b, col_upd_b = st.columns(2)
        
        # Delete booking form
        with col_del_b:
            with st.form("delete_booking_form"):
                st.subheader("Delete Booking")
                booking_ids = [b[0] for b in bookings]
                selected_booking_id = st.selectbox("Select Booking ID to Delete", booking_ids, key="del_book_sel")
                delete_submitted = st.form_submit_button("Delete Booking", use_container_width=True)
                if delete_submitted:
                    if delete_booking(selected_booking_id):
                        st.success(f"Booking {selected_booking_id} deleted successfully!")
                        time.sleep(1.2)
                        st.experimental_rerun()
                    else:
                        st.error("Error deleting booking.")
        
        # Update booking section (بدون st.form برای مدیریت راحت‌تر ایندکس‌ها)
        with col_upd_b:
            st.subheader("Update Booking")
            book_dict = {b[0]: b for b in bookings}
            selected_upd_b_id = st.selectbox("Select Booking ID to Update", list(book_dict.keys()), key="upd_book_sel_box")
            curr_book = book_dict[selected_upd_b_id]
            
            pass_options_u = {f"{p[1]} {p[2]} (ID: {p[0]})": p[0] for p in passengers} if passengers else {}
            sched_options_u = {}
            if schedules:
                for s in schedules:
                    lbl = f"Train: {s[4]} | {s[5]} ➔ {s[6]} | Date: {s[2]} | Departure: {s[1]}"
                    sched_options_u[lbl] = s[0]
            
            pass_keys = list(pass_options_u.keys())
            curr_p_key = next((k for k, v in pass_options_u.items() if v == curr_book[2]), pass_keys[0] if pass_keys else "")
            p_index = pass_keys.index(curr_p_key) if curr_p_key in pass_keys else 0
            
            sched_keys = list(sched_options_u.keys())
            curr_s_key = next((k for k, v in sched_options_u.items() if v == curr_book[3]), sched_keys[0] if sched_keys else "")
            s_index = sched_keys.index(curr_s_key) if curr_s_key in sched_keys else 0
            
            up_sel_pass = st.selectbox("Passenger", pass_keys if pass_keys else ["No Passengers"], index=p_index, key="up_book_pass")
            up_sel_sched = st.selectbox("Schedule", sched_keys if sched_keys else ["No Schedules"], index=s_index, key="up_book_sched")
            up_num_tickets = st.number_input("Number of Tickets", min_value=1, value=int(curr_book[4]), step=1, key="up_book_num")
            
            if st.button("Update Booking", use_container_width=True, key="btn_update_book"):
                if not passengers or not schedules:
                    st.error("Please ensure passengers and schedules exist.")
                else:
                    p_id = pass_options_u[up_sel_pass]
                    sch_id = sched_options_u[up_sel_sched]
                    b_date = curr_book[1] if curr_book[1] else datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    try:
                        if update_booking(selected_upd_b_id, b_date, p_id, sch_id, up_num_tickets):
                            st.success("Booking updated successfully!")
                            time.sleep(1.2)
                            st.experimental_rerun()
                    except ValueError as ve:
                        st.error(f"Validation Error: {ve}")
                    except Exception as e:
                        logger.exception("Failed to update booking")
                        st.error("A database error occurred.")
    else:
        st.info("No bookings found in the database.")
