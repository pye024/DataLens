import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# --- 1. Data Loading and Initial Preprocessing ---
# Provided sample data
data = {'date': {1562: '2024-09-15', 279: '2024-04-13', 109: '2024-03-14', 302: '2024-04-16', 1287: '2024-08-15', 2914: '2025-02-03', 2933: '2025-02-03', 3066: '2025-02-12', 600: '2024-05-26', 888: '2024-06-29', 1006: '2024-07-22', 1219: '2024-08-10', 1355: '2024-08-23', 3353: '2025-03-04', 921: '2024-07-05', 3387: '2025-03-05', 2283: '2024-11-11', 2246: '2024-11-08', 2014: '2024-10-20', 3216: '2025-02-21', 3288: '2025-02-27', 558: '2024-05-22', 2771: '2025-01-13', 2473: '2024-12-04', 1600: '2024-09-18', 2807: '2025-01-17', 985: '2024-07-18', 2609: '2024-12-22', 907: '2024-07-03', 3526: '2025-03-16'}, 'datetime': {1562: '2024-09-15 14:53:18.708', 279: '2024-04-13 16:18:03.938', 109: '2024-03-14 13:28:24.527', 302: '2024-04-16 10:46:25.706', 1287: '2024-08-15 14:17:48.183', 2914: '2025-02-03 08:04:03.627', 2933: '2025-02-03 17:15:40.901', 3066: '2025-02-12 17:05:31.989', 600: '2024-05-26 17:19:15.521', 888: '2024-06-29 12:31:42.582', 1006: '2024-07-22 08:13:23.147', 1219: '2024-08-10 11:52:33.836', 1355: '2024-08-23 08:21:48.054', 3353: '2025-03-04 07:19:21.939', 921: '2024-07-05 22:11:56.471', 3387: '2025-03-05 19:02:56.818', 2283: '2024-11-11 17:33:32.053', 2246: '2024-11-08 11:47:11.390', 2014: '2024-10-20 14:29:43.545', 3216: '2025-02-21 19:09:09.551', 3288: '2025-02-27 14:43:19.325', 558: '2024-05-22 12:29:50.841', 2771: '2025-01-13 20:51:18.275', 2473: '2024-12-04 09:04:14.145', 1600: '2024-09-18 21:18:21.554', 2807: '2025-01-17 17:39:10.610', 985: '2024-07-18 21:21:59.855', 2609: '2024-12-22 19:36:29.863', 907: '2024-07-03 16:50:25.223', 3526: '2025-03-16 14:22:42.633'}, 'cash_type': {1562: 'card', 279: 'card', 109: 'card', 302: 'card', 1287: 'card', 2914: 'card', 2933: 'card', 3066: 'card', 600: 'card', 888: 'card', 1006: 'card', 1219: 'card', 1355: 'card', 3353: 'card', 921: 'card', 3387: 'card', 2283: 'card', 2246: 'card', 2014: 'card', 3216: 'card', 3288: 'card', 558: 'card', 2771: 'card', 2473: 'card', 1600: 'card', 2807: 'card', 985: 'card', 2609: 'card', 907: 'card', 3526: 'card'}, 'card': {1562: 'ANON-0000-0000-0543', 279: 'ANON-0000-0000-0111', 109: 'ANON-0000-0000-0012', 302: 'ANON-0000-0000-0116', 1287: 'ANON-0000-0000-0012', 2914: 'ANON-0000-0000-1152', 2933: 'ANON-0000-0000-1165', 3066: 'ANON-0000-0000-1200', 600: 'ANON-0000-0000-0217', 888: 'ANON-0000-0000-0334', 1006: 'ANON-0000-0000-0375', 1219: 'ANON-0000-0000-0012', 1355: 'ANON-0000-0000-0141', 3353: 'ANON-0000-0000-1161', 921: 'ANON-0000-0000-0349', 3387: 'ANON-0000-0000-1264', 2283: 'ANON-0000-0000-0885', 2246: 'ANON-0000-0000-0494', 2014: 'ANON-0000-0000-0650', 3216: 'ANON-0000-0000-1178', 3288: 'ANON-0000-0000-1253', 558: 'ANON-0000-0000-0012', 2771: 'ANON-0000-0000-0050', 2473: 'ANON-0000-0000-0979', 1600: 'ANON-0000-0000-0040', 2807: 'ANON-0000-0000-0906', 985: 'ANON-0000-0000-0383', 2609: 'ANON-0000-0000-1032', 907: 'ANON-0000-0000-0343', 3526: 'ANON-0000-0000-1170'}, 'money': {1562: 32.82, 279: 38.7, 109: 28.9, 302: 33.8, 1287: 23.02, 2914: 21.06, 2933: 35.76, 3066: 35.76, 600: 37.72, 888: 37.72, 1006: 23.02, 1219: 23.02, 1355: 23.02, 3353: 35.76, 921: 23.02, 3387: 35.76, 2283: 35.76, 2246: 35.76, 2014: 25.96, 3216: 35.76, 3288: 35.76, 558: 27.92, 2771: 21.06, 2473: 25.96, 1600: 27.92, 2807: 35.76, 985: 32.82, 2609: 35.76, 907: 37.72, 3526: 25.96}, 'coffee_name': {1562: 'Cappuccino', 279: 'Cappuccino', 109: 'Americano', 302: 'Americano with Milk', 1287: 'Americano', 2914: 'Espresso', 2933: 'Hot Chocolate', 3066: 'Cappuccino', 600: 'Cappuccino', 888: 'Cappuccino', 1006: 'Americano', 1219: 'Cortado', 1355: 'Cortado', 3353: 'Cappuccino', 921: 'Espresso', 3387: 'Cocoa', 2283: 'Cappuccino', 2246: 'Cappuccino', 2014: 'Cortado', 3216: 'Cocoa', 3288: 'Latte', 558: 'Americano', 2771: 'Espresso', 2473: 'Americano', 1600: 'Americano with Milk', 2807: 'Hot Chocolate', 985: 'Latte', 2609: 'Hot Chocolate', 907: 'Cappuccino', 3526: 'Americano'}}
df = pd.DataFrame(data)

# Convert 'date' and 'datetime' columns to datetime objects
df['date'] = pd.to_datetime(df['date'], errors='coerce', utc=True)
df['datetime'] = pd.to_datetime(df['datetime'], errors='coerce', utc=True)

# Drop rows where datetime conversion failed, if any
df.dropna(subset=['date', 'datetime'], inplace=True)

# Feature Engineering for EDA
df['year'] = df['datetime'].dt.year
df['month'] = df['datetime'].dt.month
df['day'] = df['datetime'].dt.day
df['hour_of_day'] = df['datetime'].dt.hour
df['day_of_week'] = df['datetime'].dt.day_name()
df['month_year'] = df['datetime'].dt.to_period('M').astype(str) # For monthly trend

# Set Streamlit page configuration
st.set_page_config(layout="wide", page_title="Coffee Shop Sales Dashboard")

st.title("☕ Coffee Shop Sales Dashboard")

# --- 2. Generate KPIs ---
total_revenue = df['money'].sum()
num_transactions = df.shape[0]
average_transaction_value = df['money'].mean()
unique_customers = df['card'].nunique()

st.subheader("Key Performance Indicators")
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(label="Total Revenue", value=f"${total_revenue:,.2f}")
with col2:
    st.metric(label="Number of Transactions", value=f"{num_transactions:,}")
with col3:
    st.metric(label="Average Transaction Value", value=f"${average_transaction_value:,.2f}")
with col4:
    st.metric(label="Unique Customers", value=f"{unique_customers:,}")

# --- 3. Compute Summary Statistics ---
st.subheader("Summary Statistics")
st.write("#### Transaction Value (`money`) Statistics")
st.write(df['money'].describe())

st.write("#### Payment Type (`cash_type`) Distribution")
# To ensure there are enough colors for all categories if it expands
cash_type_counts = df['cash_type'].value_counts().reset_index()
cash_type_counts.columns = ['cash_type', 'count']
st.dataframe(cash_type_counts, use_container_width=True)

st.write("#### Top Selling Coffee (`coffee_name`) Counts")
coffee_counts = df['coffee_name'].value_counts().reset_index()
coffee_counts.columns = ['coffee_name', 'count']
st.dataframe(coffee_counts.head(10), use_container_width=True) # Display top 10

# --- 4. Conduct EDA and Plot Charts ---
st.subheader("Exploratory Data Analysis")

# Use st.columns for better layout of charts
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.write("#### 1. Monthly Revenue Trend")
    monthly_revenue = df.groupby('month_year')['money'].sum().reset_index()
    fig_monthly_revenue = px.line(
        monthly_revenue,
        x='month_year',
        y='money',
        title='Monthly Revenue Over Time',
        markers=True,
        color_discrete_sequence=px.colors.sequential.Aggrnyl, # Using a green sequence
        template="plotly_white",
    )
    fig_monthly_revenue.update_layout(
        xaxis_title="Month",
        yaxis_title="Revenue ($)",
        hovermode="x unified",
        title_x=0.5
    )
    st.plotly_chart(fig_monthly_revenue, use_container_width=True, key="monthly_revenue_chart")

with chart_col2:
    st.write("#### 2. Revenue Distribution by Payment Type")
    revenue_by_cash_type = df.groupby('cash_type')['money'].sum().reset_index()
    # Using a diverging color scale for distinct categories
    fig_cash_type = px.pie(
        revenue_by_cash_type,
        values='money',
        names='cash_type',
        title='Revenue by Payment Type',
        hole=0.4,
        color_discrete_sequence=px.colors.qualitative.Pastel # Using a pastel qualitative scale
    )
    fig_cash_type.update_traces(textposition='inside', textinfo='percent+label')
    fig_cash_type.update_layout(title_x=0.5)
    st.plotly_chart(fig_cash_type, use_container_width=True, key="cash_type_pie_chart")


chart_col3, chart_col4 = st.columns(2)

with chart_col3:
    st.write("#### 3. Top 10 Coffee Products by Revenue")
    top_coffees = df.groupby('coffee_name')['money'].sum().nlargest(10).reset_index()
    fig_top_coffees = px.bar(
        top_coffees,
        x='money',
        y='coffee_name',
        orientation='h',
        title='Top 10 Coffee Products by Revenue',
        color='money',
        color_continuous_scale="PuBuGn", # Using a blue-green continuous scale
        template="plotly_white",
    )
    fig_top_coffees.update_layout(
        yaxis={'categoryorder':'total ascending'}, # Sort bars by revenue
        xaxis_title="Revenue ($)",
        yaxis_title="Coffee Name",
        title_x=0.5
    )
    st.plotly_chart(fig_top_coffees, use_container_width=True, key="top_coffees_chart")

with chart_col4:
    st.write("#### 4. Transaction Value Distribution")
    fig_hist_money = px.histogram(
        df,
        x='money',
        nbins=15, # Adjust as needed for data spread
        title='Distribution of Transaction Values',
        color_discrete_sequence=px.colors.qualitative.Plotly, # Using Plotly's default qualitative
        template="plotly_white",
    )
    fig_hist_money.update_layout(
        xaxis_title="Transaction Value ($)",
        yaxis_title="Number of Transactions",
        title_x=0.5
    )
    st.plotly_chart(fig_hist_money, use_container_width=True, key="money_histogram_chart")


chart_col5, chart_col6 = st.columns(2)

with chart_col5:
    st.write("#### 5. Sales by Day of Week")
    # Order days of week for chronological display
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    sales_by_day = df.groupby('day_of_week')['money'].sum().reindex(day_order).reset_index()
    fig_day_of_week = px.bar(
        sales_by_day,
        x='day_of_week',
        y='money',
        title='Total Revenue by Day of Week',
        color='money',
        color_continuous_scale="Darkmint", # Using a dark mint continuous scale
        template="plotly_white",
    )
    fig_day_of_week.update_layout(
        xaxis_title="Day of Week",
        yaxis_title="Revenue ($)",
        title_x=0.5
    )
    st.plotly_chart(fig_day_of_week, use_container_width=True, key="day_of_week_chart")

with chart_col6:
    st.write("#### 6. Sales by Hour of Day")
    sales_by_hour = df.groupby('hour_of_day')['money'].sum().reset_index()
    fig_hour_of_day = px.bar(
        sales_by_hour,
        x='hour_of_day',
        y='money',
        title='Total Revenue by Hour of Day',
        color='money',
        color_continuous_scale="Sunsetdark", # Using a sunset dark continuous scale
        template="plotly_white",
    )
    fig_hour_of_day.update_layout(
        xaxis_title="Hour of Day",
        yaxis_title="Revenue ($)",
        xaxis=dict(tickmode='linear'), # Ensure all hours are shown if data spans
        title_x=0.5
    )
    st.plotly_chart(fig_hour_of_day, use_container_width=True, key="hour_of_day_chart")

# --- 5. Insights Writeup ---
st.subheader("Insights from the Data")
st.markdown("""
Based on the provided sample data, here are some initial insights:

*   **Overall Sales Performance**: The coffee shop has generated a total revenue of **\\${:,.2f}** across **{:,.0f}** transactions, serving **{:,.0f}** unique customers. The average transaction value is approximately **\\${:,.2f}**.
*   **Payment Method Dominance**: From the 'Revenue by Payment Type' chart, it's clear that **'card'** is the overwhelmingly dominant payment method. This suggests a modern customer base and efficient card processing.
*   **Top Products**: The 'Top 10 Coffee Products by Revenue' chart identifies the best-selling items. This is crucial for inventory management, promotional activities, and menu optimization. (Specific top products would be identified here if the sample was larger and more varied). For this sample, 'Cappuccino' and 'Hot Chocolate' appear frequently.
*   **Transaction Value**: The 'Distribution of Transaction Values' shows the typical price points customers spend. Most transactions fall within a certain range, indicating common purchase amounts.
*   **Temporal Trends**:
    *   **Monthly Revenue**: The 'Monthly Revenue Over Time' chart shows revenue fluctuations across months. This can reveal seasonality or growth trends.
    *   **Day of Week Sales**: The 'Total Revenue by Day of Week' chart helps identify which days are busiest (e.g., weekends vs. weekdays).
    *   **Hour of Day Sales**: The 'Total Revenue by Hour of Day' chart pinpoints peak operating hours, which is vital for staffing and marketing efforts. (e.g., often lunch or late afternoon/evening rush for coffee shops).

This initial analysis provides a strong foundation for understanding sales patterns and customer behavior. Further deep dives into specific products, customer segments, or promotional impacts would yield more granular actionable insights.
""".format(total_revenue, num_transactions, unique_customers, average_transaction_value))