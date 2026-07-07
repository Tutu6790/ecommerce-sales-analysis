import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("📊 E-Commerce Sales Dashboard")

data = pd.read_csv("data/cleaned_data.csv")
# Convert Order_Date to datetime
data["Order_Date"] = pd.to_datetime(
    data["Order_Date"],
    format="mixed"
)

st.subheader("Dataset Preview")
st.dataframe(data.head())  

#show key metrics
st.subheader("Key Metrics")

st.metric("Total Sales", f"${data['Sales'].sum():,.2f}")
st.metric("Total Orders", len(data))
st.metric("Average Order Value", f"${data['Sales'].mean():.2f}")

#sales by region
sales_region = data.groupby("Region")["Sales"].sum()

fig, ax = plt.subplots()
sales_region.plot(kind="bar", ax=ax)

st.pyplot(fig)

#monthly sales
data["Month"] = data["Order_Date"].dt.month_name()

monthly_sales = (
    data.groupby("Month")["Sales"]
    .sum()
)

fig, ax = plt.subplots()

monthly_sales.plot(ax=ax)

st.pyplot(fig)

#Top products
top_products = (
    data.groupby("Product")["Sales"]
    .sum()
    .sort_values(ascending=False)
)

st.bar_chart(top_products)

#add filter
region = st.selectbox(
    "Choose Region",
    data["Region"].unique()
)

filtered = data[data["Region"] == region]

st.dataframe(filtered)