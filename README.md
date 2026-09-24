# 🏦 Bank Customer Churn & Retention Analytics Dashboard

An end-to-end interactive executive dashboard analyzing bank customer churn drivers across demographic segments, credit score tiers, account balances, and product usage. Built with **Python**, **Streamlit**, **SQL Server**, and **Seaborn/Matplotlib**.

---

## 📌 Executive Summary & Key Insights

Analyzing $10,000$ bank customer records revealed an overall churn rate of **20.4%**, placing **$185.59M in account balances at risk**. Key behavioral and demographic patterns identified include:

* **Product Over-Saturation (Critical Indicator):** Customers holding **4 products** exhibit a **100.0% churn rate**, and those with **3 products** churn at **82.7%**. Optimal customer retention occurs at **2 products** (churn drops to **7.6%**).
* **Age Demographic Vulnerability:** Churn peaks significantly in the **50–59 age bracket at 56.0%**, followed by **40–49 at 30.8%**. Younger demographics (<30) maintain low churn rates of **7.6%**.
* **High-Balance Capital Flight:** Churned customers display a strong density concentration around **$100,000 – $150,000** in account balances, indicating that capital loss is heavily skewed toward middle-to-high net worth accounts.
* **Credit Score Tiers:** Churn remains relatively consistent across credit tiers, confirming that financial risk profiles do not drive customer departure as much as product strain and demographic age brackets.

---

## 🛠️ Tech Stack & Architecture

* **Database:** Microsoft SQL Server (Relational storage, indexed churn tables)
* **Data Ingestion & Connection:** Python, `SQLAlchemy`, `pyodbc`
* **Data Manipulation & Analytics:** `pandas`
* **Visualization Engine:** `Seaborn`, `Matplotlib` (Custom centered layout & constrained density curves)
* **Frontend Framework:** `Streamlit`

---

## 📊 Dashboard Visualizations & Features

1. **KPI Metrics Panel:** Real-time summary displaying *Total Customers*, *Churn Rate (%)*, *Total Balance at Risk ($)*, and *Average Credit Score*.
2. **Dynamic Sidebar Filtering:** Multi-select filtering by *Geography* (France, Germany, Spain), *Gender*, and *Member Status* (Active vs. Inactive).
3. **Churn Rate by Age Group:** Custom ordered categorical bar chart highlighting vulnerable age demographics.
4. **Churn Rate by Product Count:** Bar chart showing churn rate behavior as product adoption scales from 1 to 4 products.
5. **Credit Tier Breakdown:** Grouped counts comparing retained vs. churned members across standard credit bands (Poor to Excellent).
6. **Account Balance Kernel Density Estimate (KDE):** Comparative probability density curve illustrating balance distributions for retained vs. churned clients.
7. **Interactive Data Inspector:** Expandable raw dataset viewer driven by active filter selections.

---

## 📁 Repository Structure

```text
├── app.py                   # Main Streamlit dashboard application code
├── requirements.txt         # Required Python dependencies
├── data\Churn_Modelling.csv # dataset csv file
├── src\db_ingestion.ipynb   # Data cleaning & push data to SQL  file
└── README.md                # Project documentation
