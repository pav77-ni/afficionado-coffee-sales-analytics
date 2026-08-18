# Afficionado Coffee Roasters – Sales & Demand Analytics

## Project Overview

This project analyzes transaction-level sales data from Afficionado Coffee Roasters to identify revenue patterns, product performance, store performance, transaction activity, and hourly demand patterns.

The project was completed as part of a Data Analyst Internship.

## Objectives

- Analyze overall sales and revenue performance
- Identify high-performing stores
- Identify high-performing product categories
- Identify top-performing products
- Analyze hourly revenue and demand patterns
- Calculate important business KPIs
- Develop an interactive Streamlit dashboard

## Dataset

The dataset contains 149,116 transaction records with information including:

- Transaction ID
- Transaction Time
- Transaction Quantity
- Store ID
- Store Location
- Product ID
- Unit Price
- Product Category
- Product Type
- Product Detail

## Key Results

| KPI | Result |
|---|---:|
| Total Revenue | ₹698,812.33 |
| Total Transactions | 149,116 |
| Total Quantity Sold | 214,470 |
| Average Transaction Value | ₹4.69 |
| Best Store | Hell's Kitchen |
| Best Category | Coffee |
| Best Product | Sustainably Grown Organic Lg |
| Peak Revenue Hour | 10:00 AM |

## Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib
- Plotly
- Streamlit
- Google Colab
- Visual Studio Code

## Dashboard

The project includes an interactive Streamlit dashboard for exploring sales performance, revenue, product performance, store performance, and hourly demand.

## Project Structure

```text
afficionado-coffee-sales-analytics/
│
├── app.py
├── Coffee_Final_Analysis.csv
├── Coffee_Hourly_Analysis.csv
├── Coffee_Feature_Engineered.csv
├── Coffee_cleaned.csv
│
├── revenue_by_category.png
├── revenue_by_store.png
├── revenue_top10_products.png
│
├── Research_Report.pdf
└── README.md
