import streamlit as st
import pandas as pd
import plotly.express as px

# Load dataset
df = pd.read_excel("forecast_results_2024_2029.xlsx")

st.set_page_config(page_title="Forecast Dashboard", layout="wide")

st.title("📊 Forecast Dashboard (2024-2029)")

# --- SIDEBAR FILTERS ---
categories = st.sidebar.multiselect("Select Category", df['Category'].unique())
countries = st.sidebar.multiselect("Select Country", df['Area'].unique())

# Apply Filters
filtered = df[
    (df['Category'].isin(categories) if categories else True) &
    (df['Area'].isin(countries) if countries else True) &
   

st.subheader("📈 Forecasted Trend")
fig1 = px.line(filtered, x="Year", y="Forecast", color="Category", markers=True)
st.plotly_chart(fig1, use_container_width=True)

st.subheader("📊 Growth/Market Share")
fig2 = px.bar(filtered, x="Year", y="Growth%", color="Country", barmode="group")
st.plotly_chart(fig2, use_container_width=True)

# Show Data Table
st.dataframe(filtered)

# Download Button
st.download_button("⬇ Download Filtered Data", data=filtered.to_csv(index=False), file_name="filtered_data.csv")
