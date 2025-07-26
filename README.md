# 📊 Sales Dashboard with Streamlit

An interactive web dashboard built using **Streamlit** to analyze and visualize product sales data. It enables users to filter by **region**, **category**, and **date range**, and provides key insights using visualizations powered by **Seaborn** and **Matplotlib**.

---

## 🔍 Features

- 📅 Date, Region, and Category filtering from sidebar
- 💡 Key Performance Indicators (KPIs):
  - Total Sales
  - Quantity Sold
  - Total Transactions
- 📈 Visual Insights:
  - Top Products by Sales (Bar Chart)
  - Sales Distribution by Category (Pie Chart)
  - Sales by Region (Bar Chart)
  - Customer Age Distribution (Histogram)
  - Quantity by Category (Bar Chart)
  - Unit Price Distribution (Histogram)
  
---

## 📁 Dataset

The app uses a CSV file named `product.csv` with the following columns:

| Column Name       | Description                          |
|-------------------|--------------------------------------|
| Transaction_ID    | Unique ID per sale                   |
| Date              | Date of transaction                  |
| Product           | Product name                         |
| Category          | Product category                     |
| Customer_Age      | Age of the customer                  |
| Region            | Region where sale occurred           |
| Quantity          | Quantity sold                        |
| Unit_Price        | Price per unit                       |
| Total_Sales       | Quantity × Unit Price                |

---
## 🧠 Visual Insights

### ✅ Top 10 Products by Sales
> **Insight:** The top 3 products contribute a major share to overall revenue. Identifying these products helps prioritize inventory and marketing efforts for high performers.

### ✅ Sales Distribution by Category
> **Insight:** One or two categories dominate sales contribution. This highlights which product types are most preferred by customers and could benefit from focused strategy.

### ✅ Sales by Region
> **Insight:** Some regions significantly outperform others in sales. These variations suggest potential for expanding in underperforming areas or strengthening supply chains in high-demand zones.

### ✅ Customer Age Distribution
> **Insight:** Most customers belong to a specific age range (e.g., 25–45), showing the core demographic. Tailoring promotions and product designs to this age group can increase conversions.

### ✅ Quantity Sold by Category
> **Insight:** Most sales come from specific categories, indicating higher customer demand in those segments.

### ✅ Unit Price Distribution
> **Insight:** Majority of products are priced at the lower end, with a few premium-priced outliers.

---
