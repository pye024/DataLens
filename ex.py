import pandas as pd
import streamlit as st
import plotly.express as px
import numpy as np

# --- 1. Data Loading and Initial Inspection ---
# Provided columns and their types
columns_info = {
    'trip_duration': 'float64', 'distance_traveled': 'float64',
    'num_of_passengers': 'float64', 'fare': 'float64', 'tip': 'int64',
    'miscellaneous_fees': 'float64', 'total_fare': 'float64',
    'surge_applied': 'int64'
}

# Provided sample data
sample_data = {'trip_duration': {101792: 1590.0, 93511: 1345.0, 207770: 432.0, 175916: 453.0, 19870: 1408.0, 75408: 765.0, 85282: 22.0, 195264: 645.0, 90812: 578.0, 34827: 619.0, 143137: 271.0, 2288: 489.0, 104575: 1146.0, 192438: 893.0, 84105: 846.0, 72387: 481.0, 43018: 500.0, 171828: 1339.0, 90774: 470.0, 16638: 378.0, 94401: 346.0, 180761: 473.0, 169469: 1597.0, 3573: 655.0, 185222: 1385.0, 107083: 949.0, 202946: 1704.0, 128257: 1324.0, 165370: 1656.0, 133200: 358.0}, 'distance_traveled': {101792: 8.92, 93511: 9.74, 207770: 2.14, 175916: 2.25, 19870: 4.44, 75408: 2.01, 85282: 0.06, 195264: 3.96, 90812: 2.0, 34827: 2.53, 143137: 1.42, 2288: 2.72, 104575: 2.74, 192438: 2.74, 84105: 3.8, 72387: 2.12, 43018: 1.45, 171828: 4.86, 90774: 2.57, 16638: 1.92, 94401: 2.4, 180761: 2.45, 169469: 12.07, 3573: 4.65, 185222: 17.64, 107083: 3.81, 202946: 5.92, 128257: 5.5, 165370: 4.51, 133200: 2.24}, 'num_of_passengers': {101792: 1.0, 93511: 1.0, 207770: 1.0, 175916: 1.0, 19870: 1.0, 75408: 2.0, 85282: 1.0, 195264: 1.0, 90812: 1.0, 34827: 1.0, 143137: 1.0, 2288: 1.0, 104575: 1.0, 192438: 1.0, 84105: 1.0, 72387: 1.0, 43018: 2.0, 171828: 1.0, 90774: 1.0, 16638: 1.0, 94401: 1.0, 180761: 1.0, 169469: 3.0, 3573: 1.0, 185222: 1.0, 107083: 5.0, 202946: 1.0, 128257: 1.0, 165370: 1.0, 133200: 1.0}, 'fare': {101792: 172.5, 93511: 153.75, 207770: 52.5, 175916: 56.25, 19870: 123.75, 75408: 67.5, 85282: 52.5, 195264: 71.25, 90812: 60.0, 34827: 63.75, 143137: 37.5, 2288: 60.0, 104575: 97.5, 192438: 78.75, 84105: 82.5, 72387: 52.5, 43018: 52.5, 171828: 112.5, 90774: 56.25, 16638: 48.75, 94401: 48.75, 180761: 56.25, 169469: 195.0, 3573: 82.5, 185222: 232.5, 107083: 90.0, 202946: 150.0, 128257: 120.0, 165370: 131.25, 133200: 48.75}, 'tip': {101792: 0, 93511: 46, 207770: 0, 175916: 17, 19870: 0, 75408: 16, 85282: 11, 195264: 0, 90812: 16, 34827: 18, 143137: 0, 2288: 27, 104575: 21, 192438: 0, 84105: 16, 72387: 0, 43018: 24, 171828: 151, 90774: 16, 16638: 0, 94401: 12, 180761: 0, 169469: 22, 3573: 0, 185222: 0, 107083: 23, 202946: 0, 128257: 15, 165370: 32, 133200: 8}, 'miscellaneous_fees': {101792: 9.75, 93511: 30.42500000000001, 207770: 6.0, 175916: 30.700000000000003, 19870: 6.0, 75408: 13.700000000000005, 85282: 2.200000000000003, 195264: 13.5, 90812: 6.5, 34827: 26.700000000000003, 143137: 6.0, 2288: 30.52500000000001, 104575: 5.625, 192438: 6.0, 84105: 26.974999999999994, 72387: 6.0, 43018: 26.25, 171828: 13.850000000000025, 90774: 5.6000000000000085, 16638: 6.0, 94401: 13.950000000000005, 180761: 6.000000000000007, 169469: 26.82499999999999, 3573: 6.0, 185222: 9.75, 107083: 26.94999999999999, 202946: 6.0, 128257: 34.125, 165370: 26.125, 133200: 29.875}, 'total_fare': {101792: 182.25, 93511: 230.175, 207770: 58.5, 175916: 103.95, 19870: 129.75, 75408: 97.2, 85282: 65.7, 195264: 84.75, 90812: 82.5, 34827: 108.45, 143137: 43.5, 2288: 117.525, 104575: 124.125, 192438: 84.75, 84105: 125.475, 72387: 58.5, 43018: 102.75, 171828: 277.35, 90774: 77.85000000000001, 16638: 54.75, 94401: 74.7, 180761: 62.25000000000001, 169469: 243.825, 3573: 88.5, 185222: 242.25, 107083: 139.95, 202946: 156.0, 128257: 169.125, 165370: 189.375, 133200: 86.625}, 'surge_applied': {101792: 0, 93511: 1, 207770: 0, 175916: 1, 19870: 0, 75408: 0, 85282: 0, 195264: 0, 90812: 0, 34827: 1, 143137: 0, 2288: 1, 104575: 0, 192438: 0, 84105: 1, 72387: 0, 43018: 1, 171828: 0, 90774: 0, 16638: 0, 94401: 0, 180761: 0, 169469: 1, 3573: 0, 185222: 0, 107083: 1, 202946: 0, 128257: 1, 165370: 1, 133200: 1}}

# Create DataFrame
df = pd.DataFrame(sample_data)

# Ensure correct data types, especially for 'num_of_passengers'
for col, dtype in columns_info.items():
    if col == 'num_of_passengers':
        df[col] = df[col].astype(int) # Passengers should be integer counts
    elif dtype == 'int64': # Keep other int64 as int
         df[col] = df[col].astype(int)
    else: # Apply other specified dtypes
        df[col] = df[col].astype(dtype)

# --- 2. Feature Engineering (Derived Metrics) ---
# Calculate Tip Percentage, handling potential division by zero
df['tip_percentage'] = (df['tip'] / df['total_fare'] * 100).replace([np.inf, -np.inf], np.nan).fillna(0)
# Calculate Fare per Minute, handling potential division by zero
df['fare_per_minute'] = (df['fare'] / (df['trip_duration'] / 60)).replace([np.inf, -np.inf], np.nan).fillna(0)
# Calculate Fare per Distance, handling potential division by zero
df['fare_per_distance'] = (df['fare'] / df['distance_traveled']).replace([np.inf, -np.inf], np.nan).fillna(0)

# Map surge_applied to descriptive labels for better visualization
df['surge_applied_label'] = df['surge_applied'].map({0: 'No Surge', 1: 'Surge Applied'})

# --- Streamlit Application Layout ---
st.set_page_config(layout="wide")
st.title("Transportation Service Data Analytics Dashboard 📊")
st.markdown("---")

# --- Overall Dashboard Section (KPIs) ---
st.header("Overall Performance Metrics (KPIs)")

# Calculate KPIs
total_trips = df.shape[0]
total_revenue = df['total_fare'].sum()
avg_trip_duration_min = (df['trip_duration'] / 60).mean() # Convert seconds to minutes
avg_distance_traveled = df['distance_traveled'].mean()
avg_fare_per_trip = df['fare'].mean()
avg_tip_per_trip = df['tip'].mean()
avg_tip_percentage = df['tip_percentage'].mean()
surge_applied_rate = df['surge_applied'].mean() * 100 # Percentage of trips with surge

# Display KPIs using st.metric
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(label="Total Trips", value=f"{total_trips}")
    st.metric(label="Avg. Trip Duration", value=f"{avg_trip_duration_min:.2f} min")
with col2:
    st.metric(label="Total Revenue", value=f"${total_revenue:,.2f}")
    st.metric(label="Avg. Distance Traveled", value=f"{avg_distance_traveled:.2f}")
with col3:
    st.metric(label="Average Fare per Trip", value=f"${avg_fare_per_trip:,.2f}")
    st.metric(label="Average Tip %", value=f"{avg_tip_percentage:.2f}%")
with col4:
    st.metric(label="Average Tip per Trip", value=f"${avg_tip_per_trip:,.2f}")
    st.metric(label="Surge Applied Rate", value=f"{surge_applied_rate:.2f}%")

st.markdown("---")

# --- Data Overview and Summary Statistics ---
st.subheader("Data Overview & Summary Statistics")
st.write("Here's a glimpse of the raw data:")
st.dataframe(df.head())

st.write("Summary Statistics for Numeric Columns:")
# Select only numeric columns for summary statistics, excluding derived ones for base description
numeric_cols_for_describe = ['trip_duration', 'distance_traveled', 'num_of_passengers',
                             'fare', 'tip', 'miscellaneous_fees', 'total_fare']
st.dataframe(df[numeric_cols_for_describe].describe().transpose())

# Compute additional summary statistics: Sum and Median
st.write("Additional Summary Statistics (Sum and Median):")
summary_stats_df = pd.DataFrame({
    'Sum': df[numeric_cols_for_describe].sum(),
    'Median': df[numeric_cols_for_describe].median()
})
st.dataframe(summary_stats_df)


st.markdown("---")

# --- Exploratory Data Analysis (EDA) and Visualizations ---
st.header("Exploratory Data Analysis")

# Distribution of Total Fare
st.subheader("Distribution of Total Fare")
fig_total_fare = px.histogram(df, x='total_fare', nbins=15, title='Distribution of Total Fare',
                              labels={'total_fare': 'Total Fare ($)'},
                              template='plotly_white')
st.plotly_chart(fig_total_fare, use_container_width=True)

# Distribution of Trip Duration
st.subheader("Distribution of Trip Duration (in minutes)")
fig_duration = px.histogram(df, x=(df['trip_duration'] / 60), nbins=15, title='Distribution of Trip Duration',
                            labels={'x': 'Trip Duration (minutes)'},
                            template='plotly_white')
st.plotly_chart(fig_duration, use_container_width=True)

# Distribution of Distance Traveled
st.subheader("Distribution of Distance Traveled")
fig_distance = px.histogram(df, x='distance_traveled', nbins=15, title='Distribution of Distance Traveled',
                            labels={'distance_traveled': 'Distance Traveled'},
                            template='plotly_white')
st.plotly_chart(fig_distance, use_container_width=True)

# Number of Passengers Distribution
st.subheader("Distribution of Number of Passengers")
# Ensure 'num_of_passengers' is treated as a categorical for counting
passenger_counts = df['num_of_passengers'].value_counts().sort_index().reset_index()
passenger_counts.columns = ['Number of Passengers', 'Number of Trips']
fig_passengers = px.bar(passenger_counts,
                        x='Number of Passengers', y='Number of Trips',
                        title='Trips by Number of Passengers',
                        template='plotly_white')
st.plotly_chart(fig_passengers, use_container_width=True)

# Relationship between Distance, Duration and Total Fare
st.subheader("Relationship between Trip Characteristics and Fare")
col_dist_fare, col_dur_fare = st.columns(2)
with col_dist_fare:
    fig_dist_fare = px.scatter(df, x='distance_traveled', y='total_fare',
                               hover_data=['trip_duration', 'num_of_passengers', 'tip_percentage'],
                               title='Total Fare vs. Distance Traveled',
                               labels={'distance_traveled': 'Distance Traveled', 'total_fare': 'Total Fare ($)'},
                               template='plotly_white')
    st.plotly_chart(fig_dist_fare, use_container_width=True)
with col_dur_fare:
    fig_dur_fare = px.scatter(df, x=(df['trip_duration'] / 60), y='total_fare',
                              hover_data=['distance_traveled', 'num_of_passengers', 'tip_percentage'],
                              title='Total Fare vs. Trip Duration',
                              labels={'x': 'Trip Duration (minutes)', 'total_fare': 'Total Fare ($)'},
                              template='plotly_white')
    st.plotly_chart(fig_dur_fare, use_container_width=True)

# Impact of Surge Pricing
st.subheader("Impact of Surge Pricing")
surge_fare_comparison = df.groupby('surge_applied_label')['total_fare'].mean().reset_index()
fig_surge_fare = px.bar(surge_fare_comparison, x='surge_applied_label', y='total_fare',
                        title='Average Total Fare by Surge Pricing Status',
                        labels={'surge_applied_label': 'Surge Pricing', 'total_fare': 'Average Total Fare ($)'},
                        color='surge_applied_label',
                        template='plotly_white')
st.plotly_chart(fig_surge_fare, use_container_width=True)

# Tip Analysis
st.subheader("Tip Analysis")
fig_tip_dist = px.histogram(df, x='tip_percentage', nbins=20, title='Distribution of Tip Percentage',
                            labels={'tip_percentage': 'Tip Percentage (%)'},
                            template='plotly_white')
st.plotly_chart(fig_tip_dist, use_container_width=True)

# Average Fare and Tip by Number of Passengers
st.subheader("Average Fare and Tip by Number of Passengers")
avg_fare_tip_by_passengers = df.groupby('num_of_passengers').agg(
    avg_total_fare=('total_fare', 'mean'),
    avg_tip=('tip', 'mean'),
    count_trips=('num_of_passengers', 'count')
).reset_index()

col_pass_fare, col_pass_tip = st.columns(2)
with col_pass_fare:
    fig_pass_fare = px.bar(avg_fare_tip_by_passengers, x='num_of_passengers', y='avg_total_fare',
                           title='Average Total Fare by Number of Passengers',
                           labels={'num_of_passengers': 'Number of Passengers', 'avg_total_fare': 'Average Total Fare ($)'},
                           template='plotly_white')
    st.plotly_chart(fig_pass_fare, use_container_width=True)
with col_pass_tip:
    fig_pass_tip = px.bar(avg_fare_tip_by_passengers, x='num_of_passengers', y='avg_tip',
                          title='Average Tip by Number of Passengers',
                          labels={'num_of_passengers': 'Number of Passengers', 'avg_tip': 'Average Tip ($)'},
                          template='plotly_white')
    st.plotly_chart(fig_pass_tip, use_container_width=True)

# Fare Rate Analysis
st.subheader("Fare Rate Analysis (Derived Metrics)")
col_fare_per_min, col_fare_per_dist = st.columns(2)
with col_fare_per_min:
    fig_fare_per_min = px.histogram(df, x='fare_per_minute', nbins=20,
                                    title='Distribution of Fare Per Minute (excluding 0s)',
                                    labels={'fare_per_minute': 'Fare Per Minute ($)'},
                                    template='plotly_white')
    st.plotly_chart(fig_fare_per_min, use_container_width=True) # Could filter out 0s if they are many
with col_fare_per_dist:
    fig_fare_per_dist = px.histogram(df, x='fare_per_distance', nbins=20,
                                     title='Distribution of Fare Per Distance (excluding 0s)',
                                     labels={'fare_per_distance': 'Fare Per Distance ($)'},
                                     template='plotly_white')
    st.plotly_chart(fig_fare_per_dist, use_container_width=True) # Could filter out 0s if they are many

st.markdown("---")
st.write("Analysis Complete. The dashboard provides an overview of key performance metrics and distributions within the provided data.")
