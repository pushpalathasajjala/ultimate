import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Forecast Dashboard", layout="wide")

st.title("📈 Forecast Results 2024–2029 Dashboard")

# -------------------------
# Load Excel file directly
# -------------------------
df = pd.read_excel("forecast_results.xlsx")

# Sidebar Filters
st.sidebar.header("🔍 Filters")

area_list = df["Area"].unique()
area = st.sidebar.selectbox("Select Area", area_list)

filtered_df = df[df["Area"] == area]

category_list = filtered_df["Category"].unique()
category = st.sidebar.selectbox("Select Category", category_list)

filtered_df = filtered_df[filtered_df["Category"] == category]

subcat_list = filtered_df["Subcategory"].unique()
subcat = st.sidebar.selectbox("Select Subcategory", subcat_list)

filtered_df = filtered_df[filtered_df["Subcategory"] == subcat]

model_list = filtered_df["Model"].unique()
model = st.sidebar.selectbox("Select Model", model_list)

# Select the row for this model
row = filtered_df[filtered_df["Model"] == model].iloc[0]

# -------------------------
# Display Metrics
# -------------------------

st.subheader("📊 Model Performance Metrics")

col1, col2, col3 = st.columns(3)
col1.metric("MAE", round(row["MAE"], 4))
col2.metric("RMSE", round(row["RMSE"], 4))
col3.metric("MAPE", round(row["MAPE"], 4))


# -------------------------
# Forecast Extract
# -------------------------

forecast_years = ["pred_2024", "pred_2025", "pred_2026", "pred_2027", "pred_2028", "pred_2029"]

forecast_df = pd.DataFrame({
    "Year": [2024, 2025, 2026, 2027, 2028, 2029],
    "Forecast": [row[col] for col in forecast_years]
})

st.subheader(f"📉 Forecast Values ({area} → {category} → {subcat} → {model})")
st.dataframe(forecast_df, use_container_width=True)

# Line chart — Forecast
fig = px.line(
    forecast_df,
    x="Year",
    y="Forecast",
    markers=True,
    title=f"Forecast Trend ({model})"
)

st.plotly_chart(fig, use_container_width=True)


# -------------------------
# Model Comparison
# -------------------------

st.subheader("📊 Compare All Models (MAE / RMSE / MAPE)")

compare_df = df[(df["Area"] == area) &
                (df["Category"] == category) &
                (df["Subcategory"] == subcat)][["Model", "MAE", "RMSE", "MAPE"]]

fig2 = px.bar(
    compare_df,
    x="Model",
    y=["MAE", "RMSE", "MAPE"],
    barmode="group",
    title="Model Comparison"
)

st.plotly_chart(fig2, use_container_width=True)
