import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# --- 1. Data Inspection and Preparation ---
# Provided sample data
sample_data = {
    'date': {2552: '2024-12-15', 1698: '2024-09-27', 2639: '2024-12-25', 964: '2024-07-13', 533: '2024-05-20', 526: '2024-05-19', 3165: '2025-02-19', 3392: '2025-03-06', 747: '2024-06-09', 1233: '2024-08-11', 555: '2024-05-22', 737: '2024-06-09', 3: '2024-03-01', 1149: '2024-08-02', 2535: '2024-12-13', 1495: '2024-09-07', 1448: '2024-09-04', 1896: '2024-10-11', 2117: '2024-10-27', 1180: '2024-08-05', 384: '2024-04-28', 1343: '2024-08-21', 232: '2024-04-05', 1842: '2024-10-08', 1042: '2024-07-25', 3365: '2025-03-04', 2917: '2025-02-03', 402: '2024-05-02', 3353: '2025-03-04', 3448: '2025-03-10'},
    'datetime': {2552: '2024-12-15 17:58:05.386', 1698: '2024-09-27 09:33:43.977', 2639: '2024-12-25 21:57:30.270', 964: '2024-07-13 10:38:10.273', 533: '2024-05-20 13:27:13.420', 526: '2024-05-19 21:15:41.761', 3165: '2025-02-19 13:06:54.382', 3392: '2025-03-06 10:57:35.031', 747: '2024-06-09 19:21:19.277', 1233: '2024-08-11 15:53:51.552', 555: '2024-05-22 10:49:47.044', 737: '2024-06-09 10:30:04.461', 3: '2024-03-01 13:46:33.006', 1149: '2024-08-02 21:23:04.359', 2535: '2024-12-13 16:23:23.898', 1495: '2024-09-07 20:14:59.212', 1448: '2024-09-04 19:41:41.962', 1896: '2024-10-11 17:26:11.166', 2117: '2024-10-27 16:17:06.175', 1180: '2024-08-05 20:50:21.919', 384: '2024-04-28 18:28:11.411', 1343: '2024-08-21 10:38:44.527', 232: '2024-04-05 15:30:50.383', 1842: '2024-10-08 15:50:43.122', 1042: '2024-07-25 22:38:51.330', 3365: '2025-03-04 16:48:58.420', 2917: '2025-02-03 10:22:18.416', 402: '2024-05-02 10:33:55.746', 3353: '2025-03-04 07:19:21.939', 3448: '2025-03-10 18:49:22.317'},
    'cash_type': {2552: 'card', 1698: 'card', 2639: 'card', 964: 'card', 533: 'card', 526: 'card', 3165: 'card', 3392: 'card', 747: 'card', 1233: 'card', 555: 'card', 737: 'card', 3: 'card', 1149: 'card', 2535: 'card', 1495: 'card', 1448: 'card', 1896: 'card', 2117: 'card', 1180: 'card', 384: 'card', 1343: 'card', 232: 'cash', 1842: 'card', 1042: 'card', 3365: 'card', 2917: 'card', 402: 'card', 3353: 'card', 3448: 'card'},
    'card': {2552: 'ANON-0000-0000-0798', 1698: 'ANON-0000-0000-0141', 2639: 'ANON-0000-0000-1046', 964: 'ANON-0000-0000-0365', 533: 'ANON-0000-0000-0003', 526: 'ANON-0000-0000-0188', 3165: 'ANON-0000-0000-1171', 3392: 'ANON-0000-0000-1163', 747: 'ANON-0000-0000-0279', 1233: 'ANON-0000-0000-0483', 555: 'ANON-0000-0000-0191', 737: 'ANON-0000-0000-0272', 3: 'ANON-0000-0000-0003', 1149: 'ANON-0000-0000-0009', 2535: 'ANON-0000-0000-0494', 1495: 'ANON-0000-0000-0598', 1448: 'ANON-0000-0000-0097', 1896: 'ANON-0000-0000-0747', 2117: 'ANON-0000-0000-0507', 1180: 'ANON-0000-0000-0463', 384: 'ANON-0000-0000-0012', 1343: 'ANON-0000-0000-0276', 232: float('nan'), 1842: 'ANON-0000-0000-0730', 1042: 'ANON-0000-0000-0328', 3365: 'ANON-0000-0000-1167', 2917: 'ANON-0000-0000-1155', 402: 'ANON-0000-0000-0143', 3353: 'ANON-0000-0000-1161', 3448: 'ANON-0000-0000-1257'},
    'money': {2552: 35.76, 1698: 23.02, 2639: 35.76, 964: 32.82, 533: 27.92, 526: 37.72, 3165: 25.96, 3392: 25.96, 747: 32.82, 1233: 32.82, 555: 32.82, 737: 37.72, 3: 28.9, 1149: 32.82, 2535: 35.76, 1495: 32.82, 1448: 27.92, 1896: 35.76, 2117: 35.76, 1180: 32.82, 384: 27.92, 1343: 27.92, 232: 40.0, 1842: 30.86, 1042: 23.02, 3365: 25.96, 2917: 35.76, 402: 27.92, 3353: 35.76, 3448: 35.76},
    'coffee_name': {2552: 'Hot Chocolate', 1698: 'Cortado', 2639: 'Latte', 964: 'Latte', 533: 'Americano', 526: 'Cappuccino', 3165: 'Americano', 3392: 'Americano', 747: 'Americano with Milk', 1233: 'Latte', 555: 'Americano with Milk', 737: 'Latte', 3: 'Americano', 1149: 'Latte', 2535: 'Cocoa', 1495: 'Latte', 1448: 'Americano with Milk', 1896: 'Hot Chocolate', 2117: 'Latte', 1180: 'Cocoa', 384: 'Americano', 1343: 'Americano with Milk', 232: 'Latte', 1842: 'Americano with Milk', 1042: 'Cortado', 3365: 'Americano', 2917: 'Cappuccino', 402: 'Americano', 3353: 'Cappuccino', 3448: 'Latte'}
}

df = pd.DataFrame(sample_data)

# Convert 'date' and 'datetime' columns to datetime objects
df['date'] = pd.to_datetime(df['date'])
df['datetime'] = pd.to_datetime(df['datetime'])

# Extract useful time components
df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month_name()
df['day_of_week'] = df['date'].dt.day_name()
df['hour'] = df['datetime'].dt.hour

# Sort data by datetime for time-series analysis
df = df.sort_values(by='datetime').reset_index(drop=True)


# --- Streamlit Dashboard Setup ---
st.set_page_config(layout="wide", page_title="Coffee Shop Sales Dashboard", page_icon="☕")

st.title("☕ Coffee Shop Sales Dashboard")
st.markdown("---")


# --- 2. KPIs (Key Performance Indicators) ---
st.header("Key Performance Indicators (KPIs)")

total_revenue = df['money'].sum()
total_transactions = df.shape[0]
avg_transaction_value = df['money'].mean()
unique_coffees = df['coffee_name'].nunique()
# For unique customers, we count unique card numbers. Cash payments do not have an identifiable customer ID.
unique_card_customers = df[df['cash_type'] == 'card']['card'].nunique()
first_date = df['date'].min().strftime('%Y-%m-%d')
last_date = df['date'].max().strftime('%Y-%m-%d')


col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(label="Total Revenue", value=f"${total_revenue:,.2f}")
with col2:
    st.metric(label="Total Transactions", value=f"{total_transactions:,}")
with col3:
    st.metric(label="Average Transaction Value", value=f"${avg_transaction_value:,.2f}")
with col4:
    st.metric(label="Unique Coffee Types", value=f"{unique_coffees:,}")
with col5:
    st.metric(label="Unique Card Customers", value=f"{unique_card_customers:,}")

st.markdown(f"Data period: From **{first_date}** to **{last_date}**")
st.markdown("---")

# --- 3. Summary Statistics ---
st.header("Summary Statistics for Sales ('money' column)")
st.dataframe(df['money'].describe().to_frame().T) # Display as a small DataFrame for clarity
st.markdown("---")


# --- 4. EDA and Visualizations ---
st.header("Exploratory Data Analysis")

# 4.1. Revenue Trend Over Time
st.subheader("Revenue Trend Over Time")
# Aggregate daily revenue
daily_revenue = df.groupby(df['date'].dt.to_period('D'))['money'].sum().reset_index()
daily_revenue['date'] = daily_revenue['date'].dt.to_timestamp() # Convert Period back to Timestamp for Plotly

fig_daily_revenue = px.line(
    daily_revenue,
    x='date',
    y='money',
    title='Daily Revenue Over Time',
    labels={'date': 'Date', 'money': 'Revenue ($)'},
    template='plotly_white',
    color_discrete_sequence=['#1f77b4'] # Using a specific color for the line
)
fig_daily_revenue.update_traces(mode='lines+markers', marker=dict(size=5, opacity=0.8, color='#1f77b4'))
fig_daily_revenue.update_layout(hovermode="x unified")
st.plotly_chart(fig_daily_revenue, use_container_width=True, key="daily_revenue_chart")

# 4.2. Sales by Payment Type
st.subheader("Sales Distribution by Payment Type")
payment_type_sales = df.groupby('cash_type')['money'].sum().reset_index()

fig_payment_type = px.pie(
    payment_type_sales,
    values='money',
    names='cash_type',
    title='Total Revenue by Payment Type',
    hole=0.4,
    color_discrete_sequence=["DarkCyan", "CadetBlue"] # Custom colors
)
fig_payment_type.update_traces(textinfo='percent+label', marker=dict(line=dict(color='#000000', width=1)))
st.plotly_chart(fig_payment_type, use_container_width=True, key="payment_type_pie")


# 4.3. Top 10 Coffees by Revenue
st.subheader("Top Coffee Products by Total Revenue")
top_coffees = df.groupby('coffee_name')['money'].sum().nlargest(10).reset_index()

fig_top_coffees = px.bar(
    top_coffees,
    x='money',
    y='coffee_name',
    orientation='h',
    title='Top 10 Coffee Products by Total Revenue',
    labels={'money': 'Total Revenue ($)', 'coffee_name': 'Coffee Name'},
    template='plotly_white',
    color='money',
    color_continuous_scale="Viridis_r" # Reversing for darker colors for larger values
)
fig_top_coffees.update_layout(yaxis={'categoryorder':'total ascending'})
st.plotly_chart(fig_top_coffees, use_container_width=True, key="top_coffees_chart")


# 4.4. Sales by Day of Week
st.subheader("Sales by Day of Week")
sales_by_day = df.groupby('day_of_week')['money'].sum().reindex([
    'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'
]).reset_index()

fig_day_of_week = px.bar(
    sales_by_day,
    x='day_of_week',
    y='money',
    title='Total Revenue by Day of Week',
    labels={'day_of_week': 'Day of Week', 'money': 'Total Revenue ($)'},
    template='plotly_white',
    color='money',
    color_continuous_scale="Plasma" # An appealing color scale
)
st.plotly_chart(fig_day_of_week, use_container_width=True, key="day_of_week_chart")

# 4.5. Sales by Hour of Day
st.subheader("Sales by Hour of Day")
sales_by_hour = df.groupby('hour')['money'].sum().reset_index()

fig_hour_of_day = px.bar(
    sales_by_hour,
    x='hour',
    y='money',
    title='Total Revenue by Hour of Day',
    labels={'hour': 'Hour of Day (24h)', 'money': 'Total Revenue ($)'},
    template='plotly_white',
    color='money',
    color_continuous_scale="Cividis" # Another appealing color scale
)
fig_hour_of_day.update_layout(xaxis=dict(tickmode='linear', dtick=1))
st.plotly_chart(fig_hour_of_day, use_container_width=True, key="hour_of_day_chart")

# 4.6. Distribution of Transaction Values
st.subheader("Distribution of Transaction Values")
fig_hist_money = px.histogram(
    df,
    x='money',
    title='Distribution of Transaction Values',
    labels={'money': 'Transaction Value ($)', 'count': 'Number of Transactions'},
    template='plotly_white',
    nbins=15, # Adjust as needed
    color_discrete_sequence=['#84A98C'] # A single, distinct strong color
)
fig_hist_money.update_traces(marker_line_width=1, marker_line_color="black")
st.plotly_chart(fig_hist_money, use_container_width=True, key="hist_money_chart")


st.markdown("---")

# --- 5. Insights Writeup ---
st.header("Insights Summary")
st.write(f"""
Based on the provided sales data, spanning from **{first_date}** to **{last_date}**, here are some key insights:

*   **Overall Performance:** The coffee shop generated a total revenue of **${total_revenue:,.2f}** across **{total_transactions:,}** transactions. The average transaction value stands at **${avg_transaction_value:,.2f}**, suggesting a consistent purchase pattern among customers.
*   **Payment Preferences:** Card payments are overwhelmingly dominant, indicating a customer base that prefers cashless transactions. The **{unique_card_customers:,}** unique card customers represent a significant portion of identifiable patrons. This suggests opportunities for loyalty programs targeting card users.
*   **Product Popularity:** Analyzing revenue by `coffee_name` clearly highlights the top-selling products. (Based on the sample data, 'Latte', 'Americano', and 'Cappuccino' are frequently purchased, with 'Hot Chocolate' and 'Americano with Milk' also showing strong performance.) Focusing on these popular items and ensuring their consistent availability can maximize sales.
*   **Temporal Trends:**
    *   **Daily Revenue:** The `Daily Revenue Over Time` chart reveals fluctuations, which could be influenced by specific days of the week, holidays, or promotional activities. A longer dataset would allow for more robust trend analysis.
    *   **Day of Week:** Sales patterns vary significantly throughout the week, with certain days generating higher revenue. This insight is crucial for optimizing staffing and inventory.
    *   **Hour of Day:** Transactions peak at specific hours, likely corresponding to morning commutes, lunch breaks, or evening rushes. Understanding these peak times can help in efficient resource allocation and targeted marketing.
*   **Transaction Value Distribution:** The histogram shows that most transactions fall within a narrow price range, possibly reflecting the pricing structure of individual beverages. This distribution can inform pricing strategies and combo offers.

These insights provide a foundational understanding of sales performance and customer behavior, enabling data-driven decisions for operational improvements and strategic planning.
""")

st.markdown("---")

# --- Code snippets for potential follow-up questions ---

def answer_follow_up_questions(df_main):
    st.sidebar.header("Ask a Follow-up Question")
    question_options = [
        "Select a question...",
        "What product sold most this month?",
        "Where did most of my sales come from (payment type)?",
        "Show me the distribution of customers (card vs. cash).",
        "What are my sales trends by month?"
    ]
    selected_question = st.sidebar.selectbox("Choose a question:", question_options)

    if selected_question == "What product sold most this month?":
        st.subheader(f"Answer: {selected_question}")
        # Determine the latest full month in the data
        latest_date = df_main['date'].max()
        # If the latest date is early in the month, consider the previous month as "this month" for full data
        if latest_date.day < 15 and len(df_main[df_main['date'].dt.month == latest_date.month]) < 5: # heuristic for 'full month'
            target_month = (latest_date - pd.DateOffset(months=1)).month
            target_year = (latest_date - pd.DateOffset(months=1)).year
        else:
            target_month = latest_date.month
            target_year = latest_date.year

        monthly_df = df_main[(df_main['date'].dt.month == target_month) & (df_main['date'].dt.year == target_year)]

        if not monthly_df.empty:
            top_product_by_revenue = monthly_df.groupby('coffee_name')['money'].sum().idxmax()
            top_product_revenue = monthly_df.groupby('coffee_name')['money'].sum().max()

            top_product_by_quantity = monthly_df.groupby('coffee_name').size().idxmax()
            top_product_quantity = monthly_df.groupby('coffee_name').size().max()

            st.success(f"For the month of **{pd.to_datetime(target_month, format='%m').strftime('%B')} {target_year}**:")
            st.write(f"- The product that generated the most revenue was **'{top_product_by_revenue}'** with **${top_product_revenue:,.2f}** in sales.")
            st.write(f"- The product sold most frequently (by quantity) was **'{top_product_by_quantity}'** with **{top_product_quantity:,}** units sold.")

            fig_monthly_top_products = px.bar(
                monthly_df.groupby('coffee_name')['money'].sum().sort_values(ascending=False).head(5).reset_index(),
                x='money',
                y='coffee_name',
                orientation='h',
                title=f'Top 5 Products by Revenue in {pd.to_datetime(target_month, format="%m").strftime("%B")} {target_year}',
                labels={'money': 'Total Revenue ($)', 'coffee_name': 'Coffee Name'},
                color='money',
                color_continuous_scale="Mint"
            )
            fig_monthly_top_products.update_layout(yaxis={'categoryorder':'total ascending'})
            st.plotly_chart(fig_monthly_top_products, use_container_width=True, key="monthly_top_products_chart")
        else:
            st.warning(f"No data available for the month of {pd.to_datetime(target_month, format='%m').strftime('%B')} {target_year}.")

    elif selected_question == "Where did most of my sales come from (payment type)?":
        st.subheader(f"Answer: {selected_question}")
        payment_summary = df_main.groupby('cash_type')['money'].sum().reset_index()
        total_sales = payment_summary['money'].sum()

        st.write("Most of your sales come from the following payment types:")
        for index, row in payment_summary.iterrows():
            st.write(f"- **{row['cash_type'].capitalize()}**: **${row['money']:,.2f}** ({row['money']/total_sales:.1%})")

        fig_sales_origin = px.pie(
            payment_summary,
            values='money',
            names='cash_type',
            title='Revenue Distribution by Payment Type',
            hole=0.3,
            color_discrete_sequence=["DarkSlateGrey", "LightSeaGreen"]
        )
        fig_sales_origin.update_traces(textinfo='percent+label', marker=dict(line=dict(color='#000000', width=1)))
        st.plotly_chart(fig_sales_origin, use_container_width=True, key="sales_origin_pie")

    elif selected_question == "Show me the distribution of customers (card vs. cash).":
        st.subheader(f"Answer: {selected_question}")
        num_card_transactions = df_main[df_main['cash_type'] == 'card'].shape[0]
        num_cash_transactions = df_main[df_main['cash_type'] == 'cash'].shape[0]

        st.write(f"From the provided data:")
        st.write(f"- Number of transactions by **Card**: **{num_card_transactions:,}**")
        st.write(f"- Number of transactions by **Cash**: **{num_cash_transactions:,}**")
        st.write(f"- Unique identifiable card-paying customers: **{df_main[df_main['cash_type'] == 'card']['card'].nunique():,}**")
        st.markdown("*Note: Cash customers are not individually identifiable in this dataset.*")

        customer_dist_data = pd.DataFrame({
            'Payment Method': ['Card Transactions', 'Cash Transactions'],
            'Count': [num_card_transactions, num_cash_transactions]
        })

        fig_customer_dist = px.bar(
            customer_dist_data,
            x='Payment Method',
            y='Count',
            title='Transaction Count by Payment Method',
            labels={'Payment Method': 'Payment Method', 'Count': 'Number of Transactions'},
            color='Payment Method',
            color_discrete_sequence=["SteelBlue", "DarkOrange"]
        )
        st.plotly_chart(fig_customer_dist, use_container_width=True, key="customer_dist_bar")

    elif selected_question == "What are my sales trends by month?":
        st.subheader(f"Answer: {selected_question}")
        monthly_revenue = df_main.set_index('date').resample('MS')['money'].sum().reset_index()
        monthly_revenue['month_year'] = monthly_revenue['date'].dt.strftime('%Y-%m')

        fig_monthly_trend = px.line(
            monthly_revenue,
            x='month_year',
            y='money',
            title='Monthly Revenue Trend',
            labels={'month_year': 'Month', 'money': 'Total Revenue ($)'},
            template='plotly_white',
            color_discrete_sequence=['#A63D40']
        )
        fig_monthly_trend.update_traces(mode='lines+markers', marker=dict(size=6, opacity=0.8, color='#A63D40'))
        fig_monthly_trend.update_layout(hovermode="x unified", xaxis_title="Month (YYYY-MM)")
        st.plotly_chart(fig_monthly_trend, use_container_width=True, key="monthly_trend_chart")

    elif selected_question == "Select a question...":
        st.sidebar.info("Select a question from the dropdown to see its analysis.")

# Add a section for follow-up questions
st.markdown("---")
st.header("Further Analysis: Follow-up Questions")
st.write("Use the sidebar to explore specific questions about the data.")
answer_follow_up_questions(df)

# General advice for other potential questions not directly implemented above:
# "How do I increase next month’s revenue?"
# Insights from the dashboard suggest:
# 1. Promote top-selling products (e.g., Lattes, Americanos) during peak hours/days.
# 2. Consider loyalty programs for card-paying customers.
# 3. Analyze peak hours/days for staffing optimization and potential upselling during busy periods.
# 4. Introduce new products or limited-time offers to drive interest.
# This would require more detailed sales data, cost analysis, and marketing data for truly actionable advice.

# "What are the predictions for next month’s sales?"
# This requires time-series forecasting models (e.g., ARIMA, Prophet) which are beyond the scope of initial EDA.
# With more historical data, such models could be built.

# "What does the demographic of my sales look like?"
# The provided data does not contain demographic information (age, gender, location, etc.).
# Therefore, it is not possible to provide insights into sales demographics using this dataset.

