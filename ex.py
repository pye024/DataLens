import pandas as pd
import streamlit as st
import plotly.express as px

# --- Configuration ---
st.set_page_config(layout="wide", page_title="Trip Data Analysis")

# --- Data Loading and Initial Inspection ---
# Provided sample data
data_sample = {
    'trip_duration': {143408: 606.0, 165249: 2161.0, 36642: 85606.0, 46156: 832.0, 135464: 389.0, 86654: 784.0, 78786: 451.0, 116594: 532.0, 140733: 569.0, 193225: 136.0, 39383: 692.0, 9395: 285.0, 58593: 205.0, 21005: 1042.0, 42650: 2085.0, 157105: 314.0, 101960: 1562.0, 40966: 1066.0, 116293: 709.0, 68425: 91.0, 183596: 531.0, 36202: 626.0, 82511: 394.0, 85318: 639.0, 139834: 626.0, 134794: 799.0, 174167: 1327.0, 54448: 1065.0, 149182: 264.0, 155894: 704.0},
    'distance_traveled': {143408: 2.25, 165249: 11.65, 36642: 2.69, 46156: 4.35, 135464: 1.29, 86654: 3.22, 78786: 2.72, 116594: 2.04, 140733: 1.8, 193225: 1.06, 39383: 2.72, 9395: 0.97, 58593: 1.13, 21005: 2.9, 42650: 12.49, 157105: 2.11, 101960: 5.21, 40966: 6.26, 116293: 2.74, 68425: 0.48, 183596: 3.04, 36202: 4.68, 82511: 1.5, 85318: 3.27, 139834: 0.97, 134794: 3.78, 174167: 5.28, 54448: 3.3, 149182: 1.14, 155894: 1.95},
    'num_of_passengers': {143408: 1.0, 165249: 1.0, 36642: 1.0, 46156: 1.0, 135464: 1.0, 86654: 1.0, 78786: 1.0, 116594: 1.0, 140733: 1.0, 193225: 1.0, 39383: 6.0, 9395: 2.0, 58593: 1.0, 21005: 1.0, 42650: 1.0, 157105: 1.0, 101960: 1.0, 40966: 1.0, 116293: 1.0, 68425: 1.0, 183596: 1.0, 36202: 1.0, 82511: 1.0, 85318: 1.0, 139834: 1.0, 134794: 2.0, 174167: 5.0, 54448: 1.0, 149182: 1.0, 155894: 6.0},
    'fare': {143408: 63.75, 165249: 202.5, 36642: 82.5, 46156: 86.25, 135464: 45.0, 86654: 75.0, 78786: 60.0, 116594: 60.0, 140733: 60.0, 193225: 30.0, 39383: 67.5, 9395: 37.5, 58593: 33.75, 21005: 90.0, 42650: 217.5, 157105: 45.0, 101960: 131.25, 40966: 112.5, 116293: 71.25, 68425: 26.25, 183596: 63.75, 36202: 86.25, 82511: 45.0, 85318: 71.25, 139834: 56.25, 134794: 86.25, 174167: 123.75, 54448: 90.0, 149182: 37.5, 155894: 67.5},
    'tip': {143408: 0, 165249: 59, 36642: 0, 46156: 22, 135464: 11, 86654: 0, 78786: 0, 116594: 0, 140733: 16, 193225: 0, 39383: 0, 9395: 0, 58593: 0, 21005: 23, 42650: 0, 157105: 10, 101960: 33, 40966: 0, 116293: 25, 68425: 12, 183596: 18, 36202: 18, 82511: 15, 85318: 15, 139834: 12, 134794: 18, 174167: 0, 54448: 0, 149182: 7, 155894: 11},
    'miscellaneous_fees': {143408: 6.0, 165249: 34.299999999999955, 36642: 6.0, 46156: 27.125, 135464: 9.700000000000005, 86654: 13.5, 78786: 30.375, 116594: 6.0, 140733: 6.5, 193225: 13.5, 39383: 13.5, 9395: 6.0, 58593: 13.5, 21005: 26.94999999999999, 42650: 26.625, 157105: 6.200000000000003, 101960: 34.19999999999999, 40966: 6.0, 116293: 13.625, 68425: 13.424999999999995, 183596: 10.125, 36202: 6.450000000000003, 82511: 6.0, 85318: 6.0, 139834: 6.375, 134794: 6.450000000000003, 174167: 6.0, 54448: 13.5, 149182: 5.524999999999999, 155894: 26.875},
    'total_fare': {143408: 69.75, 165249: 295.79999999999995, 36642: 88.5, 46156: 135.375, 135464: 65.7, 86654: 88.5, 78786: 90.375, 116594: 66.0, 140733: 82.5, 193225: 43.5, 39383: 81.0, 9395: 43.5, 58593: 47.25, 21005: 139.95, 42650: 244.125, 157105: 61.2, 101960: 198.45, 40966: 118.5, 116293: 109.875, 68425: 51.675, 183596: 91.875, 36202: 110.7, 82511: 66.0, 85318: 92.25, 139834: 74.625, 134794: 110.7, 174167: 129.75, 54448: 103.5, 149182: 50.025, 155894: 105.375},
    'surge_applied': {143408: 0, 165249: 1, 36642: 0, 46156: 1, 135464: 0, 86654: 0, 78786: 1, 116594: 0, 140733: 0, 193225: 0, 39383: 0, 9395: 0, 58593: 0, 21005: 1, 42650: 1, 157105: 0, 101960: 1, 40966: 0, 116293: 0, 68425: 0, 183596: 0, 36202: 0, 82511: 0, 85318: 0, 139834: 0, 134794: 0, 174167: 0, 54448: 0, 149182: 0, 155894: 1}
}
df = pd.DataFrame(data_sample)

# --- Data Type Conversion and Feature Engineering ---
# 'num_of_passengers' and 'surge_applied' are typically integers/categorical
df['num_of_passengers'] = df['num_of_passengers'].astype(int)
df['surge_applied'] = df['surge_applied'].astype(bool) # Convert to boolean for better representation

# Create derived metrics
df['tip_percentage'] = (df['tip'] / df['fare'] * 100).round(2).fillna(0)
df['fare_per_mile'] = (df['fare'] / df['distance_traveled']).round(2).fillna(0) # Handling division by zero
df.loc[df['distance_traveled'] == 0, 'fare_per_mile'] = 0 # Set to 0 if distance is 0

# Convert trip_duration to minutes for better readability in some contexts
df['trip_duration_minutes'] = (df['trip_duration'] / 60).round(2)

# --- Overall Dashboard ---
st.title("📊 Ride-Sharing Trip Data Dashboard")

# --- Section 1: Key Performance Indicators (KPIs) ---
st.header("Key Performance Indicators (KPIs)")

total_trips = len(df)
total_revenue = df['total_fare'].sum()
avg_trip_duration_minutes = df['trip_duration_minutes'].mean()
avg_distance_traveled = df['distance_traveled'].mean()
avg_fare = df['fare'].mean()
total_tips = df['tip'].sum()
avg_tip_percentage = df['tip_percentage'].mean()
surge_trips_percentage = (df['surge_applied'].sum() / total_trips * 100) if total_trips > 0 else 0

kpi_cols = st.columns(4)

with kpi_cols[0]:
    st.metric("Total Trips", f"{total_trips}")
    st.metric("Total Revenue", f"${total_revenue:,.2f}")
with kpi_cols[1]:
    st.metric("Avg. Trip Duration", f"{avg_trip_duration_minutes:,.2f} mins")
    st.metric("Avg. Distance Traveled", f"{avg_distance_traveled:,.2f} miles")
with kpi_cols[2]:
    st.metric("Avg. Base Fare", f"${avg_fare:,.2f}")
    st.metric("Total Tips Collected", f"${total_tips:,.2f}")
with kpi_cols[3]:
    st.metric("Avg. Tip Percentage", f"{avg_tip_percentage:,.2f}%")
    st.metric("Trips with Surge", f"{surge_trips_percentage:,.2f}%")

st.markdown("---")

# --- Section 2: Summary Statistics ---
st.header("Summary Statistics for Numeric Data")
summary_stats_df = df[['trip_duration_minutes', 'distance_traveled', 'num_of_passengers', 'fare', 'tip', 'miscellaneous_fees', 'total_fare', 'tip_percentage', 'fare_per_mile']].describe().transpose()
summary_stats_df['sum'] = df[['trip_duration_minutes', 'distance_traveled', 'num_of_passengers', 'fare', 'tip', 'miscellaneous_fees', 'total_fare', 'tip_percentage', 'fare_per_mile']].sum()
summary_stats_df['median'] = df[['trip_duration_minutes', 'distance_traveled', 'num_of_passengers', 'fare', 'tip', 'miscellaneous_fees', 'total_fare', 'tip_percentage', 'fare_per_mile']].median()

# Reorder columns for better readability (min, max, mean, median, sum, std, count)
summary_stats_df = summary_stats_df[['count', 'min', 'max', 'mean', 'median', 'sum', 'std']]

st.dataframe(summary_stats_df.style.format("{:,.2f}"), use_container_width=True, key="summary_stats_table")

st.markdown("---")

# --- Section 3: Exploratory Data Analysis (EDA) and Visualizations ---
st.header("Exploratory Data Analysis")

# Visualization 1: Distribution of Total Fare
st.subheader("Distribution of Total Fare")
fig_total_fare_dist = px.histogram(
    df,
    x='total_fare',
    nbins=15,
    title='Distribution of Total Fare per Trip',
    labels={'total_fare': 'Total Fare ($)'},
    color_discrete_sequence=px.colors.sequential.Tealgrn, # Using a vibrant sequential color
    template='plotly_white'
)
fig_total_fare_dist.update_layout(showlegend=False)
st.plotly_chart(fig_total_fare_dist, use_container_width=True, key="total_fare_dist_chart")

# Visualization 2: Relationship between Distance Traveled and Total Fare
st.subheader("Distance Traveled vs. Total Fare")
fig_dist_fare = px.scatter(
    df,
    x='distance_traveled',
    y='total_fare',
    size='num_of_passengers', # Size points by number of passengers
    color='trip_duration_minutes', # Color by trip duration
    hover_name=df.index.astype(str), # Use index as hover name for unique identification
    title='Total Fare vs. Distance Traveled (Colored by Trip Duration)',
    labels={'distance_traveled': 'Distance Traveled (miles)', 'total_fare': 'Total Fare ($)', 'trip_duration_minutes': 'Trip Duration (minutes)'},
    color_continuous_scale=px.colors.sequential.Plasma, # Using a continuous color scale
    template='plotly_white'
)
st.plotly_chart(fig_dist_fare, use_container_width=True, key="dist_fare_scatter_chart")

# Visualization 3: Passenger Count Distribution
st.subheader("Distribution of Number of Passengers")
# Group by num_of_passengers and count occurrences
passenger_counts = df['num_of_passengers'].value_counts().sort_index().reset_index()
passenger_counts.columns = ['num_of_passengers', 'count']

fig_passengers = px.bar(
    passenger_counts,
    x='num_of_passengers',
    y='count',
    title='Distribution of Number of Passengers per Trip',
    labels={'num_of_passengers': 'Number of Passengers', 'count': 'Number of Trips'},
    color='num_of_passengers', # Color bars by passenger count
    color_continuous_scale=px.colors.sequential.Viridis, # Using a continuous color scale for passenger count
    template='plotly_white',
    hover_data={'count': ':.0f'}
)
fig_passengers.update_layout(xaxis=dict(tickmode='linear', dtick=1)) # Ensure integer ticks
st.plotly_chart(fig_passengers, use_container_width=True, key="passengers_dist_chart")

# Visualization 4: Impact of Surge Pricing on Total Fare
st.subheader("Impact of Surge Pricing on Total Fare")
fig_surge = px.box(
    df,
    x='surge_applied',
    y='total_fare',
    title='Total Fare Distribution with and Without Surge Pricing',
    labels={'surge_applied': 'Surge Applied', 'total_fare': 'Total Fare ($)'},
    color='surge_applied', # Color boxes based on surge applied
    color_discrete_map={True: px.colors.qualitative.Plotly[1], False: px.colors.qualitative.Plotly[0]}, # Custom colors
    template='plotly_white',
    category_orders={'surge_applied': [False, True]}
)
fig_surge.update_layout(xaxis_title="Surge Applied (False/True)")
st.plotly_chart(fig_surge, use_container_width=True, key="surge_impact_chart")

# Visualization 5: Trip Duration Distribution
st.subheader("Distribution of Trip Duration")
fig_duration = px.histogram(
    df,
    x='trip_duration_minutes',
    nbins=20,
    title='Distribution of Trip Duration (Minutes)',
    labels={'trip_duration_minutes': 'Trip Duration (Minutes)'},
    color_discrete_sequence=px.colors.sequential.Bluyl, # Another color palette
    template='plotly_white'
)
st.plotly_chart(fig_duration, use_container_width=True, key="trip_duration_chart")

# Visualization 6: Fare Breakdown (Average)
st.subheader("Average Fare Component Breakdown")
fare_components = df[['fare', 'tip', 'miscellaneous_fees']].mean().reset_index()
fare_components.columns = ['Component', 'Average Amount']

fig_fare_breakdown = px.pie(
    fare_components,
    values='Average Amount',
    names='Component',
    title='Average Breakdown of Total Fare Components',
    color_discrete_sequence=px.colors.qualitative.Pastel, # Pastel color palette for pie chart
    template='plotly_white'
)
st.plotly_chart(fig_fare_breakdown, use_container_width=True, key="fare_breakdown_chart")

# Visualization 7: Tip Percentage vs. Total Fare
st.subheader("Tip Percentage vs. Total Fare")
fig_tip_pct_fare = px.scatter(
    df,
    x='total_fare',
    y='tip_percentage',
    color='surge_applied', # See if surge impacts tip percentage behavior
    size='tip', # Size points by tip amount
    title='Tip Percentage vs. Total Fare (Colored by Surge Applied)',
    labels={'total_fare': 'Total Fare ($)', 'tip_percentage': 'Tip Percentage (%)', 'surge_applied': 'Surge Applied'},
    color_discrete_map={True: px.colors.qualitative.Set1[0], False: px.colors.qualitative.Set1[1]}, # Distinct colors
    template='plotly_white'
)
st.plotly_chart(fig_tip_pct_fare, use_container_width=True, key="tip_pct_fare_scatter_chart")
