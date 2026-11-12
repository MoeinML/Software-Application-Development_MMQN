import streamlit as st
from train_operations import get_all_bookings, get_all_trains

def run_app():
    st.title("Train Booking System")
    st.subheader("Available Trains")
    trains = get_all_trains()
    #for train in trains:
    #    st.write(train)
    df = pd.DataFrame(trains, columns=["Train ID", "Code", "Type"])
    st.dataframe(df, hide_index=True)

    st.subheader("Booking List")
    bookings = get_all_bookings()
    #for booking in bookings:
    #    st.write(booking)
    df = pd.DataFrame(bookings, columns=["Booking ID", "Date", "Status", "Price", "Passenger", "Schedule", "Seat"])
    st.dataframe(df, hide_index=True)


if __name__ == '__main__':
    run_app()
