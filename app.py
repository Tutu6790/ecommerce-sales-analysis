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
# create month column
data['Month'] = data['Order_Date'].dt.month_name()

# set correct month order
month_order = [
    'January','February','March','April','May','June',
    'July','August','September','October','November','December'
]

# convert Month to ordered categorical
data['Month_Num'] = data['Order_Date'].dt.month
monthly_sales = data.groupby('Month_Num')['Sales'].sum().sort_index()

fig, ax = plt.subplots()

monthly_sales.plot(ax=ax)
plt.xticks(range(1,13), month_order, rotation=45)

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