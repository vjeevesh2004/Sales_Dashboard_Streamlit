import streamlit as st
import pandas as pd
# import matplotlib.pyplot as plt
# import seaborn as sns 
import plotly.express as px 

st.set_page_config(page_title = "Sales Dashboard", layout = "wide")
@st.cache_data
def load_data():
    # Ensure 'Date' column is parsed correctly and handle potential errors
    df = pd.read_csv("product.csv")
    df['Date'] = pd.to_datetime(df['Date'], dayfirst=True, errors='coerce')
    # Drop rows where 'Date' could not be parsed
    df.dropna(subset=['Date'], inplace=True)
    return df

df = load_data()

st.sidebar.header("Filters")
region = st.sidebar.multiselect("Select Region", options=df['Region'].unique(), default=df['Region'].unique())
Category = st.sidebar.multiselect("Select Category", options=df['Category'].unique(), default=df['Category'].unique())

# Ensure date_range is a list of two dates
min_date = df['Date'].min().date() if not df['Date'].empty else pd.to_datetime('2020-01-01').date()
max_date = df['Date'].max().date() if not df['Date'].empty else pd.to_datetime('2023-12-31').date()

date_range_input = st.sidebar.date_input("Select Date", [min_date, max_date])

# Ensure date_range_input is a list of two dates before proceeding
if len(date_range_input) == 2:
    start_date = pd.to_datetime(date_range_input[0])
    end_date = pd.to_datetime(date_range_input[1])
else:
    # If only one date is selected (e.g., user is still picking), use default range
    start_date = pd.to_datetime(min_date)
    end_date = pd.to_datetime(max_date)

mask = (
    df['Region'].isin(region) &
    df['Category'].isin(Category) &
    (df['Date'] >= start_date) &
    (df['Date'] <= end_date)
)
df_filtered = df[mask]

# Display a warning if no data is available after filtering
if df_filtered.empty:
    st.warning("No data available for the selected filters. Please adjust your selections.")
    st.stop() # Stop execution if no data

st.title("Sales Dashboard")

# for KPIs
total_sales = df_filtered['Total_Sales'].sum()
total_quantity = df_filtered['Quantity'].sum()
total_transaction = df_filtered['Transaction_ID'].nunique()

st.markdown("### Key Performance Indicators")
col1, col2, col3 = st.columns(3)
col1.metric("💰 Total Sales", f"${total_sales:,.2f}")
col2.metric("📦 Total Quantity Sold", f"{total_quantity}")
col3.metric("🧾 Total Transactions", f"{total_transaction}")

st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    # Sales by Product
    st.subheader("Top 10 Products by Sales")
    top_products = df_filtered.groupby("Product")["Total_Sales"].sum().nlargest(10).reset_index()
    fig_top_products = px.bar(top_products, x='Total_Sales', y='Product',
                              orientation='h', title='Top 10 Products by Sales')
    fig_top_products.update_layout(yaxis={'categoryorder':'total ascending'}) # Sort bars
    st.plotly_chart(fig_top_products, use_container_width=True)
    st.info("""
    **Insight:** The top 3 products contribute a major share to overall revenue. Identifying these products helps prioritize inventory and marketing efforts for high performers.
    """)

with col2:
    # Sales by Category (Pie)
    st.subheader("Sales Distribution by Category")
    cat_sales = df_filtered.groupby("Category")["Total_Sales"].sum().reset_index()
    fig_cat_sales = px.pie(cat_sales, values='Total_Sales', names='Category',
                           title='Sales by Category', hole=0.3) # Added a hole for donut chart
    st.plotly_chart(fig_cat_sales, use_container_width=True)
    st.info("""
    **Insight:** One or two categories dominate sales contribution. This highlights which product types are most preferred by customers and could benefit from focused strategy.
    """)

col3, col4 = st.columns(2)

with col3:
    # Region vs Sales
    st.subheader("Sales by Region")
    region_sales = df_filtered.groupby("Region")["Total_Sales"].sum().reset_index()
    fig_region_sales = px.bar(region_sales, x='Region', y='Total_Sales',
                              title='Sales by Region')
    st.plotly_chart(fig_region_sales, use_container_width=True)
    st.info("""
    **Insight:** Some regions significantly outperform others in sales. These variations suggest potential for expanding in underperforming areas or strengthening supply chains in high-demand zones.
    """)

with col4:
    # Age Distribution
    st.subheader("Customer Age Distribution")
    fig_age_dist = px.histogram(df_filtered, x='Customer_Age', nbins=20,
                               title='Customer Age Distribution',
                               labels={'Customer_Age': 'Customer Age', 'count': 'Count'})
    st.plotly_chart(fig_age_dist, use_container_width=True)
    st.info("""
    **Insight:** Most customers belong to a specific age range (e.g., 25–45), showing the core demographic. Tailoring promotions and product designs to this age group can increase conversions.
    """)
