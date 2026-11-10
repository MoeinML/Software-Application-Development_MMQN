import streamlit as st
from train_operations import get_all_trains

st.title("Train Booking System")
st.subheader("Available Trains")

trains = get_all_trains()

for train in trains:
    st.write(train)