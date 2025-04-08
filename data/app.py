import streamlit as st
import pandas as pd

# Title
st.title("EV Charging Station Analytics")

# Load data
data = pd.read_csv("ev_stations_cleaned.csv")

# Show raw data
st.subheader("Raw Data")
st.dataframe(data.head(10))

# Show state-wise count
st.subheader("Number of Stations by State")
state_counts = data['state'].value_counts().reset_index()
state_counts.columns = ['State', 'Station Count']
st.bar_chart(state_counts.set_index('State'))
