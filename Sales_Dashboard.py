import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns 

st.set_page_config(page_title = "Sales Dashboard", layout = "wide")

@st.cache_data
def load_data():
    df=pd.read_csv("product.csv", parse_dates = ['Date'], dayfirst = True)
    return df

df = load_data()

st.sidebar.header("Filters")
region = st.sidebar.multiselect("Select Region", options = df['Region'].unique(), default = df['Region'].unique())
Category = st.sidebar.multiselect("Select Category", options = df['Category'].unique(), default = df['Category'].unique())
date_range = st.sidebar.date_input("Select Date", [df['Date'].min(), df['Date'].max()])

mask = (
    df['Region'].isin(region) & 
    df['Category'].isin(Category) & 
    (df['Date'] >= pd.to_datetime(date_range[0])) & 
    (df['Date'] <= pd.to_datetime(date_range[1]))
)
df_filtered = df[mask]



st.title("Sales Dashboard")
# # Sales Over Time
# st.subheader("Sales Over Time")
# sales_over_time = df_filtered.groupby("Date")["Total_Sales"].sum().reset_index()
# fig, ax = plt.subplots()
# ax.plot(sales_over_time['Date'], sales_over_time['Total_Sales'], marker='o')
# ax.set_title("Sales Over Time")
# ax.set_xlabel("Date")
# ax.set_ylabel("Total Sales")
# st.pyplot(fig)
# st.info("""
# **Insight:** Sales show noticeable trends over time, with visible peaks that may correspond to promotions or high-demand periods. Continuous growth or sudden drops can help identify seasonality or anomalies.
# """)

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
    fig, ax = plt.subplots()
    sns.barplot(x='Total_Sales', y='Product', data=top_products, ax=ax)
    ax.set_title("Top 10 Products by Sales")
    st.pyplot(fig)
    st.info("""
    **Insight:** The top 3 products contribute a major share to overall revenue. Identifying these products helps prioritize inventory and marketing efforts for high performers.
    """)

with col2:
    # Sales by Category (Pie)
    st.subheader("Sales Distribution by Category")
    cat_sales = df_filtered.groupby("Category")["Total_Sales"].sum().reset_index()
    fig, ax = plt.subplots()
    ax.pie(cat_sales['Total_Sales'], labels=cat_sales['Category'], autopct='%1.1f%%', startangle=90)
    ax.set_title("Sales by Category")
    st.pyplot(fig)
    st.info("""
    **Insight:** One or two categories dominate sales contribution. This highlights which product types are most preferred by customers and could benefit from focused strategy.
    """)

col3, col4 = st.columns(2)

with col3:
# Region vs Sales
    st.subheader("Sales by Region")
    region_sales = df_filtered.groupby("Region")["Total_Sales"].sum().reset_index()
    fig, ax = plt.subplots()
    sns.barplot(x='Region', y='Total_Sales', data=region_sales, ax=ax)
    ax.set_title("Sales by Region")
    st.pyplot(fig)
    st.info("""
    **Insight:** Some regions significantly outperform others in sales. These variations suggest potential for expanding in underperforming areas or strengthening supply chains in high-demand zones.
    """)

with col4: 
# Age Distribution
    st.subheader("Customer Age Distribution")
    fig, ax = plt.subplots()
    sns.histplot(df_filtered['Customer_Age'], bins=20, kde=True, ax=ax)
    ax.set_title("Customer Age Distribution")
    ax.set_xlabel("Customer Age")
    ax.set_ylabel("Count")
    st.pyplot(fig)
    st.info("""
    **Insight:** Most customers belong to a specific age range (e.g., 25–45), showing the core demographic. Tailoring promotions and product designs to this age group can increase conversions.
    """)

# # Scatter: Price vs Quantity
# st.subheader("Unit Price vs Quantity")
# fig, ax = plt.subplots()
# sns.scatterplot(data=df_filtered, x='Unit_Price', y='Quantity', hue='Category', size='Total_Sales', ax=ax)
# ax.set_title("Unit Price vs Quantity")
# ax.set_xlabel("Unit Price")
# ax.set_ylabel("Quantity")
# st.pyplot(fig)
# st.info("""
# **Insight:** Products with lower unit prices tend to be sold in higher quantities, indicating price sensitivity among customers. Premium products sell fewer units but can still contribute significantly due to higher prices.
# """)
# col5, col6 = st.columns(2)

# # with col5:
# #     st.markdown("### Monthly Sales Trend")
# #     df_filtered['Month'] = df_filtered['Date'].dt.to_period('M').astype(str)
# #     monthly_sales = df_filtered.groupby('Month')['Total_Sales'].sum().reset_index()

# #     fig5, ax5 = plt.subplots(figsize=(6, 3))
# #     sns.lineplot(x='Month', y='Total_Sales', data=monthly_sales, marker='o', ax=ax5)
# #     ax5.set_xticklabels(monthly_sales['Month'], rotation=45)
# #     st.pyplot(fig5)

# with col5: 
#     st.markdown("### Quantity Sold by Category")
#     qty_category = df_filtered.groupby("Category")["Quantity"].sum().reset_index()

#     fig6, ax6 = plt.subplots(figsize=(6, 3))
#     sns.barplot(x="Quantity", y="Category", data=qty_category, ax=ax6)
#     st.pyplot(fig)
#     st.info(""" **Insight:** Most sales come from specific categories, indicating higher customer demand in those segments.""")

# # col7, col8 = st.columns(2)

# with col6:
#     st.markdown("### Unit Price Distribution")
#     fig7, ax7 = plt.subplots(figsize=(6, 3))
#     sns.histplot(df_filtered['Unit_Price'], bins=30, kde=True, ax=ax7)
#     st.pyplot(fig)
#     st.info(""" **Insight:** Majority of products are priced at the lower end, with a few premium-priced outliers.""")


# # with col8:
# #     st.markdown("### Customer Age vs Total Sales")
#     fig8, ax8 = plt.subplots(figsize=(6, 3))
#     sns.regplot(x='Customer_Age', y='Total_Sales', data=df_filtered, ax=ax8)
#     st.pyplot(fig8) 


# # Footer
# st.caption("Dashboard built using Streamlit ✨")
