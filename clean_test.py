import re

import re
import textwrap

def extract(code: str) -> str:
    """
    Extract pure Python code from an LLM response.
    - Removes ```python/``` fences
    - Handles multiple code blocks
    - Strips text before the first import/from
    """
    if not isinstance(code, str):
        return ""

    # Find all fenced code blocks
    blocks = re.findall(r"```(?:python)?\n(.*?)```", code, re.DOTALL | re.IGNORECASE)

    if blocks:
        # Join multiple blocks if present
        combined = "\n\n".join(blocks)
    else:
        # No fenced code, use raw response
        combined = code

    # Trim everything before the first import/from
    m = re.search(r"\b(import|from)\b", combined)
    if m:
        combined = combined[m.start():]

    # Dedent & clean
    return textwrap.dedent(combined).strip()




response = """As a data analyst, I've analyzed your dataset and created a comprehensive Streamlit dashboard. Here's what I found in the data:

The dataset contains vehicle sales information with various attributes including make, model, year, condition, and pricing data. Based on my analysis, I've identified several key insights and trends that will be valuable for your business intelligence needs.

Here's the complete Python code for your Streamlit application:

```python
import pandas as pd
import streamlit as st
import plotly.express as px
import numpy as np

# Configure Streamlit
st.set_page_config(page_title="Vehicle Sales Analysis", layout="wide")

# Title and header
st.title("🚗 Vehicle Sales Dashboard")
st.markdown("This dashboard provides insights into vehicle sales data")

# Sample data
data = {
    'make': ['Toyota', 'Honda', 'Ford', 'Chevrolet', 'Nissan'],
    'sales': [120, 95, 88, 76, 65],
    'avg_price': [25000, 23000, 22000, 21000, 20000]
}

df = pd.DataFrame(data)

# Create visualizations
col1, col2 = st.columns(2)

with col1:
    fig1 = px.bar(df, x='make', y='sales', title='Sales by Make')
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    fig2 = px.scatter(df, x='avg_price', y='sales', text='make', 
                      title='Price vs Sales Volume')
    st.plotly_chart(fig2, use_container_width=True)

# Display metrics
st.subheader("Key Metrics")
total_sales = df['sales'].sum()
avg_price = df['avg_price'].mean()


st.success("Dashboard loaded successfully!")
```

This dashboard includes interactive visualizations showing sales performance by vehicle make, pricing analysis, and key performance metrics. The code uses Plotly for interactive charts and implements a clean, professional layout.

The analysis reveals that Toyota leads in sales volume while maintaining competitive pricing. I recommend focusing on the top-performing brands for inventory decisions."""

cleaned=extract(response)
print(cleaned)