import streamlit as st
import pandas as pd

# Title
st.title("EV Charging Station Analytics")

# Load data (EV stations cleaned data)
data = pd.read_csv("ev_stations_cleaned.csv")

# Show raw data
st.subheader("Raw Data")
st.dataframe(data.head(10))

# Load population data
population_data = pd.read_csv("state_population_csv.csv")

# Show raw population data
st.subheader("State Population Data")
st.dataframe(population_data.head(10))

# Merge EV stations data with population data
merged_data = pd.merge(data, population_data, left_on="state", right_on="STATE", how="left")

# Create a new column 'Number of Stations' by counting stations per state
station_counts = merged_data.groupby('state').size().reset_index(name='Number of Stations')

# Merge the counts back to the merged_data
merged_data = pd.merge(merged_data, station_counts, on='state')

# Handle missing values by filling NaNs with 0 or some default value
merged_data['Number of Stations'].fillna(0, inplace=True)
merged_data['POPESTIMATE2019'].fillna(0, inplace=True)

# Show state-wise count
st.subheader("Number of Stations by State")
state_counts = merged_data['state'].value_counts().reset_index()
state_counts.columns = ['State', 'Station Count']
st.bar_chart(state_counts.set_index('State'))

# Show dropdown for charger type selection
connector_types = data['ev_connector_types'].unique()  # Get unique connector types from the dataset
selected_connector = st.selectbox("Select Connector Type", connector_types)  # Dropdown menu for selection

# Filter data based on the selected connector type
filtered_data = data[data['ev_connector_types'] == selected_connector]

# Display the filtered data
st.write(f"Showing data for Connector Type: {selected_connector}")
st.dataframe(filtered_data)  # Display the filtered data in a table

# Bar Chart for number of stations by state (after filtering)
st.subheader(f"Number of Stations for {selected_connector} Connector Type")
station_counts_filtered = filtered_data['state'].value_counts().reset_index()
station_counts_filtered.columns = ['State', 'Number of Stations']
st.bar_chart(station_counts_filtered.set_index('State'))

# Calculate EV station density (stations per population)
# We need to make sure 'Population' column exists and it's numeric
merged_data['Population'] = pd.to_numeric(merged_data['POPESTIMATE2019'], errors='coerce')  # Convert population to numeric, handling any errors

# Ensure no division by 0
merged_data['EV Station Density'] = merged_data['Number of Stations'] / merged_data['Population'].replace(0, 1)  # Replacing 0 population with 1 to avoid division by zero

# Display the new merged data with EV Station Density
st.write(merged_data[['state', 'EV Station Density']])

# Show bar chart of EV Station Density by state
st.subheader("EV Station Density by State")
st.bar_chart(merged_data.set_index('state')['EV Station Density'])

# Allow users to select a metric to visualize
metric = st.selectbox("Select Metric to Visualize", ["EV Station Density", "POPESTIMATE2019", "Number of Stations"])

# Show bar chart based on the selected metric
st.subheader(f"{metric} by State")
st.bar_chart(merged_data.set_index('state')[metric])
