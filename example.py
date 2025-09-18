import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import numpy as np # For correlation matrix

st.set_page_config(layout="wide")
df = pd.read_csv("data/world_happiness_2024.csv",sep=None,engine='python')
# --- Data Preprocessing Function ---
# This function cleans and converts columns with comma decimals to numeric types.
def preprocess_dataframe(input_df):
    df_processed = input_df.copy()
    columns_to_convert = ['Ladder score', 'GDP per capita', 'Social support', 
                          'Freedom to make life choices', 'Generosity', 
                          'Perceptions of corruption']

    for col in columns_to_convert:
        if col in df_processed.columns:
            # Ensure the column is treated as string before replace to avoid AttributeError
            # Then replace comma with dot for decimal conversion and convert to numeric
            df_processed[col] = df_processed[col].astype(str).str.replace(',', '.', regex=False)
            df_processed[col] = pd.to_numeric(df_processed[col], errors='coerce')

    return df_processed

# --- Main Streamlit App Logic ---

# Assume 'df' is the DataFrame provided at runtime, as per instructions.
# Apply preprocessing to ensure correct data types for analysis.
df = preprocess_dataframe(df)

# Drop rows with NaN values in key numeric columns after conversion
# This ensures that calculations and visualizations are accurate.
initial_rows = len(df)
df.dropna(subset=['Ladder score', 'GDP per capita', 'Social support', 'Healthy life expectancy', 
                   'Freedom to make life choices', 'Generosity', 'Perceptions of corruption'], 
          inplace=True)
df.reset_index(drop=True, inplace=True)
rows_after_dropna = len(df)
if initial_rows > rows_after_dropna:
    st.warning(f"Removed {initial_rows - rows_after_dropna} rows with missing values for key metrics after data cleaning.")

# Markdown for the dashboard introduction
st.markdown("This dashboard provides an exploratory data analysis of the World Happiness Report data, focusing on key indicators influencing national happiness levels.")

# --- Overall Dashboard Section ---
st.header("Overall Happiness Dashboard")

# 1. Key Performance Indicators (KPIs)
st.subheader("Key Performance Indicators (KPIs)")

col1, col2, col3, col4 = st.columns(4)

with col1:
    avg_ladder_score = df['Ladder score'].mean()
    st.metric(label="Average Ladder Score", value=f"{avg_ladder_score:.2f}")

with col2:
    # Ensure there's data to find max/min; otherwise, handle gracefully
    if not df.empty:
        max_ladder_country = df.loc[df['Ladder score'].idxmax()]
        st.metric(label="Happiest Country", value=f"{max_ladder_country['Country']} ({max_ladder_country['Ladder score']:.2f})")
    else:
        st.metric(label="Happiest Country", value="N/A")


with col3:
    if not df.empty:
        min_ladder_country = df.loc[df['Ladder score'].idxmin()]
        st.metric(label="Least Happy Country", value=f"{min_ladder_country['Country']} ({min_ladder_country['Ladder score']:.2f})")
    else:
        st.metric(label="Least Happy Country", value="N/A")

with col4:
    avg_life_expectancy = df['Healthy life expectancy'].mean()
    st.metric(label="Avg. Healthy Life Expectancy", value=f"{avg_life_expectancy:.1f} years")

st.markdown("---")

# 2. Summary Statistics
st.subheader("Summary Statistics for Key Metrics")
numeric_cols = ['Ladder score', 'GDP per capita', 'Social support', 
                'Healthy life expectancy', 'Freedom to make life choices', 
                'Generosity', 'Perceptions of corruption']

st.dataframe(df[numeric_cols].describe().T.style.format("{:.2f}"))
st.caption("Descriptive statistics for the main numerical indicators, including mean, standard deviation, min, max, and quartile ranges.")

st.markdown("---")

# 3. EDA and Visualizations
st.header("Exploratory Data Analysis & Visualizations")

# 3.1. Distribution of Ladder Score
st.subheader("1. Distribution of Happiness Scores")
fig_hist = px.histogram(df, x='Ladder score', 
                        nbins=20, 
                        title='Distribution of Ladder Scores Across Countries',
                        color_discrete_sequence=px.colors.qualitative.Plotly, # A vibrant qualitative palette
                        template="plotly_white")
fig_hist.update_layout(bargap=0.1)
st.plotly_chart(fig_hist, use_container_width=True, key="ladder_score_dist_hist")
st.caption("This histogram displays the frequency distribution of 'Ladder score' across all countries, revealing the overall spread and central tendency of happiness levels.")

st.markdown("---")

# 3.2. Top 10 Happiest Countries
st.subheader("2. Top 10 Happiest Countries")
top_10_countries = df.nlargest(10, 'Ladder score')
fig_top10 = px.bar(top_10_countries, 
                   x='Ladder score', 
                   y='Country', 
                   orientation='h', 
                   title='Top 10 Happiest Countries by Ladder Score',
                   color='Ladder score', # Color by Ladder score
                   color_continuous_scale="Viridis", # Continuous scale for numerical values
                   template="plotly_white")
fig_top10.update_layout(yaxis={'categoryorder':'total ascending'}) # Ensure highest score is at the top
st.plotly_chart(fig_top10, use_container_width=True, key="top10_happiness_bar")
st.caption("Bar chart displaying the ten countries with the highest 'Ladder score', highlighting the nations perceived as most happy.")

st.markdown("---")

# 3.3. Bottom 10 Happiest Countries
st.subheader("3. Bottom 10 Happiest Countries")
bottom_10_countries = df.nsmallest(10, 'Ladder score')
fig_bottom10 = px.bar(bottom_10_countries, 
                      x='Ladder score', 
                      y='Country', 
                      orientation='h', 
                      title='Bottom 10 Happiest Countries by Ladder Score',
                      color='Ladder score', 
                      color_continuous_scale="Inferno_r", # Reversed scale for low values (darker for lower scores)
                      template="plotly_white")
fig_bottom10.update_layout(yaxis={'categoryorder':'total descending'}) # Ensure lowest score is at the bottom
st.plotly_chart(fig_bottom10, use_container_width=True, key="bottom10_happiness_bar")
st.caption("Bar chart illustrating the ten countries with the lowest 'Ladder score', indicating nations facing significant challenges in perceived happiness.")

st.markdown("---")

# 3.4. Average Ladder Score by Regional Indicator
st.subheader("4. Average Happiness Score by Region")
avg_score_by_region = df.groupby('Regional indicator')['Ladder score'].mean().sort_values(ascending=False).reset_index()
fig_region_bar = px.bar(avg_score_by_region, 
                        x='Regional indicator', 
                        y='Ladder score', 
                        title='Average Ladder Score by Regional Indicator',
                        color='Ladder score', # Color by Ladder score
                        color_continuous_scale="Tealrose", # Another continuous scale
                        template="plotly_white")
fig_region_bar.update_xaxes(tickangle=45)
st.plotly_chart(fig_region_bar, use_container_width=True, key="region_happiness_bar")
st.caption("This chart displays the average 'Ladder score' for each 'Regional indicator', providing insights into regional happiness disparities.")

st.markdown("---")

# 3.5. Scatter Plot: Ladder Score vs. GDP per capita
st.subheader("5. Happiness Score vs. GDP per capita")
fig_gdp = px.scatter(df, x='GDP per capita', y='Ladder score', 
                     hover_name='Country', 
                     size='GDP per capita', # Size of markers based on GDP
                     color='Ladder score', # Color based on Ladder Score
                     color_continuous_scale="Plasma", # Plasma continuous scale
                     title='Ladder Score vs. GDP per capita',
                     template="plotly_white")
st.plotly_chart(fig_gdp, use_container_width=True, key="gdp_ladder_scatter")
st.caption("Scatter plot showing the relationship between a country's 'GDP per capita' and its 'Ladder score'. Larger markers indicate higher GDP, and color intensity represents happiness.")

st.markdown("---")

# 3.6. Scatter Plot: Ladder Score vs. Healthy Life Expectancy
st.subheader("6. Happiness Score vs. Healthy Life Expectancy")
fig_life_exp = px.scatter(df, x='Healthy life expectancy', y='Ladder score', 
                          hover_name='Country', 
                          size='Healthy life expectancy', # Size of markers based on Life Expectancy
                          color='Ladder score', # Color based on Ladder Score
                          color_continuous_scale="Electric", # Electric continuous scale
                          title='Ladder Score vs. Healthy life expectancy',
                          template="plotly_white")
st.plotly_chart(fig_life_exp, use_container_width=True, key="life_exp_ladder_scatter")
st.caption("Scatter plot illustrating the relationship between 'Healthy life expectancy' and 'Ladder score'. Marker size reflects life expectancy, and color shows happiness level.")

st.markdown("---")

# 3.7. Correlation Heatmap of Numeric Factors
st.subheader("7. Correlation Matrix of Happiness Factors")
correlation_cols = ['Ladder score', 'GDP per capita', 'Social support', 
                    'Healthy life expectancy', 'Freedom to make life choices', 
                    'Generosity', 'Perceptions of corruption']
corr_matrix = df[correlation_cols].corr()

fig_corr = px.imshow(corr_matrix, 
                     text_auto=True, 
                     aspect="auto", # Auto aspect ratio
                     color_continuous_scale="RdBu_r", # Diverging scale for correlation (Red-Blue reversed)
                     title='Correlation Matrix of Happiness Factors',
                     template="plotly_white")
st.plotly_chart(fig_corr, use_container_width=True, key="correlation_heatmap")
st.caption("Heatmap showing the Pearson correlation coefficients between various factors and the 'Ladder score'. Values range from -1 (perfect negative correlation) to 1 (perfect positive correlation).")

st.markdown("---")

# 3.8. Box Plot for Freedom, Generosity, Corruption by Region
st.subheader("8. Regional Distribution of Key Factors")

selected_factor = st.selectbox(
    "Select a factor to visualize its regional distribution:",
    ['Freedom to make life choices', 'Generosity', 'Perceptions of corruption', 'Social support'],
    key="factor_selectbox"
)

fig_box = px.box(df, x='Regional indicator', y=selected_factor, 
                 color='Regional indicator', # Color by region
                 color_discrete_sequence=px.colors.qualitative.Vivid, # Use a qualitative palette for discrete regions
                 title=f'Distribution of {selected_factor} by Regional Indicator',
                 template="plotly_white")
fig_box.update_xaxes(tickangle=45)
st.plotly_chart(fig_box, use_container_width=True, key="regional_box_plot")
st.caption(f"Box plot showing the distribution of '{selected_factor}' within each 'Regional indicator'. The box represents the interquartile range (IQR), the line inside is the median, and whiskers extend to 1.5 times the IQR.")

st.markdown("---")

# --- Insights Writeup ---
st.header("Key Insights")
st.write("""
Based on the exploratory data analysis of the World Happiness Report dataset, several key insights emerge:

*   **Happiness Distribution:** The 'Ladder score' shows a relatively normal distribution, with most countries clustered around the average happiness score. There are distinct tails representing the happiest and least happy nations.
*   **Economic Prosperity and Happiness:** There is a strong positive correlation between 'GDP per capita' and 'Ladder score', suggesting that economic development plays a significant role in perceived national happiness. Countries with higher GDP tend to report higher happiness levels.
*   **Health and Well-being:** 'Healthy life expectancy' also shows a strong positive correlation with 'Ladder score', indicating that better health outcomes and longer healthy lives contribute significantly to overall happiness.
*   **Social Support is Crucial:** 'Social support' is another highly correlated factor, underscoring the importance of strong community and social networks for individual and national well-being.
*   **Freedom and Generosity:** 'Freedom to make life choices' and 'Generosity' generally correlate positively with happiness, implying that personal autonomy and altruism are valuable contributors to a country's happiness score.
*   **Perceptions of Corruption:** 'Perceptions of corruption' tends to have a negative correlation with 'Ladder score'. Higher perceived corruption is associated with lower happiness, highlighting the importance of good governance, transparency, and trust in public institutions.
*   **Regional Disparities:** Happiness levels and underlying factors vary significantly by region. Certain regions consistently show higher or lower average 'Ladder scores', along with varying distributions of factors like freedom, generosity, and corruption perceptions. This indicates socio-economic and political differences across the globe contribute to happiness variations.
*   **Interconnected Factors:** The correlation matrix reveals that many of the factors are inter-related. For instance, countries with higher GDP per capita often also have higher healthy life expectancy and social support, creating a complex web of influence on overall happiness.

Overall, the data suggests that a combination of economic prosperity, robust health systems, strong social support networks, personal freedom, and low perception of corruption are key drivers of national happiness. Addressing these areas could potentially contribute to improving a country's overall well-being.
""")