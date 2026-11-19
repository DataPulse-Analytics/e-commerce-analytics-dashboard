# E-Commerce Sales & Business Performance Analytics

[![Python Version](https://img.shields.io/badge/Python-3.13%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Analytics-Production--Ready-brightgreen.svg)]()

An enterprise-grade, end-to-end data analytics and business intelligence project built upon authentic Kaggle e-commerce transaction data. This repository features robust data cleaning pipelines, multi-dimensional exploratory analysis, publication-grade statistical visualizations, and complete Microsoft Power BI dashboard modeling assets.

---

## 1. Project Overview

In multi-category retail e-commerce, sustained profitability depends on data-driven decision-making across merchandising, customer retention, payment gateways, and return logistics. This project analyzes **24,999 transactions** across **4,212 unique customers** between **January 2020 and September 2023**, generating actionable intelligence on:
* **Gross & Net Revenue:** Evaluating top-line gross revenue ($67.97M) against refund-adjusted net retained revenue ($40.29M).
* **Category Merchandising:** Performance dynamics across **Clothing**, **Books**, **Home**, and **Electronics**.
* **Customer Lifecycle & Retention:** Lifetime value (CLV), purchasing frequency, repeat behavior (100% repeat buyers), and churn dynamics (20.49% churn rate).
* **Financial Risk & Return Volatility:** Quantification of return rates (~40.88%) accounting for $27.67M in refund liabilities.
* **Payment Channel Economics:** Comparative analysis across Credit Card, PayPal, Cash on Delivery, and Cryptocurrency.

---

## 2. Project Objectives

1. **Deterministic Data Hygiene:** Implement an automated, reproducible Python data pipeline using Pandas and NumPy to clean, validate, and enrich raw data without data loss or unjustified imputation.
2. **Comprehensive Exploratory Data Analysis:** Quantify sales trends, seasonality, customer order frequency tiers, and Pareto spend concentration.
3. **Statistical Visualization Suite:** Render 10 publication-quality charts using Matplotlib and Seaborn with consistent corporate styling.
4. **Power BI Enterprise Modeling:** Architect a Star Schema model with 20 production DAX measures and 4 executive dashboard pages.
5. **Transparency & Governance:** Explicitly document analytical boundaries (such as the absence of geographic tags and unit COGS in the Kaggle source) to prevent fabricated findings.

---

## 3. Project Folder Structure

```
final product/
│
├── 01_Project_Proposal/
│   └── Project_Proposal.docx               # Formal Microsoft Word project proposal
│
├── 02_Dataset/
│   ├── Original_Dataset/
│   │   └── raw_data.csv                    # Immutable copy of original Kaggle dataset
│   └── Cleaned_Dataset/
│       └── cleaned_data.csv                # Validated, enriched production dataset (24,999 rows)
│
├── 03_Data_Cleaning/
│   ├── data_cleaning.py                    # Automated cleaning, auditing, and feature engineering script
│   └── cleaning_report.txt                 # Detailed mathematical audit log of all transformations
│
├── 04_Data_Analysis/
│   ├── data_analysis.py                    # Quantitative business intelligence and cohort analysis script
│   └── analysis_report.txt                 # Complete executive findings and strategic recommendations
│
├── 05_Data_Visualisation/
│   ├── data_visualisation.ipynb            # Interactive Jupyter Notebook for live cell-by-cell plotting
│   ├── data_visualisation.py               # Automated chart generation script
│   └── charts/                             # High-resolution saved visualizations
│       ├── 01_monthly_sales_trend.png
│       ├── 02_category_wise_sales.png
│       ├── 03_payment_method_distribution.png
│       ├── 04_customer_spending_distribution.png
│       ├── 05_top_10_customers.png
│       ├── 06_revenue_by_age_and_gender.png
│       ├── 07_return_rate_by_category.png
│       ├── 08_customer_order_frequency_tiers.png
│       ├── 09_revenue_distribution_boxplots.png
│       └── 10_annual_performance.png
│
├── 06_PowerBI_Dashboard/
│   ├── DAX_Measures.dax                    # Enterprise DAX measures library
│   ├── PowerBI_Data_Model_and_Build_Guide.md # Step-by-step PBIX creation guide & Star Schema
│   ├── Dashboard_Specifications.json       # Visual coordinate layout schema
│   └── Dashboard_Screenshots/              # High-resolution 16:9 dashboard preview
│       └── Executive_Sales_Performance_Dashboard.png  # Master Executive Dashboard
│
├── 07_Documentation/
│   ├── Project_Report.pdf                  # Complete compiled academic & executive project report
│   ├── README.md                           # Master project documentation
│   └── requirements.txt                    # Pinned Python package dependencies
│
├── requirements.txt                        # Pinned Python package dependencies
└── final_data.csv                          # Original Kaggle source dataset (untouched)
```

---

## 4. Dataset Description

The analysis is based on the Kaggle E-Commerce Customer Behavior & Sales Dataset (`final_data.csv`):

| Attribute | Raw Type | Cleaned Type | Business Domain & Description |
| :--- | :--- | :--- | :--- |
| `customer_id` | `int64` | `int64` | Unique customer account identifier (4,212 unique accounts) |
| `purchase_date` | `object` | `datetime64[ns]` | Timestamp of purchase (standardized to ISO-8601 format) |
| `product_category` | `object` | `string` | Merchandise sector: Clothing, Books, Home, Electronics |
| `product_price` | `int64` | `int64` | Unit catalog price ranging from $10 to $500 |
| `quantity` | `int64` | `int64` | Number of items purchased per transaction (1 to 5 units) |
| `total_purchase_amount` | `int64` | `int64` | Gross transaction value ranging from $108 to $5,345 |
| `payment_method` | `object` | `string` | Checkout mechanism: Credit Card, PayPal, Cash, Crypto |
| `customer_age` | `int64` | `int64` | Customer age in completed years (18 to 70 years) |
| `returns` | `float64` | `int64` | Return indicator (0 = Kept, 1 = Returned; 4,716 NaNs imputed to 0) |
| `customer_name` | `object` | `string` | Customer full legal name |
| `Age` | `int64` | *Dropped* | 100% duplicate of `Customer Age`; removed during cleaning |
| `gender` | `object` | `string` | Customer gender: Male (50.4%), Female (49.6%) |
| `churn` | `int64` | `int64` | Binary churn status (0 = Retained/Active, 1 = Churned) |

### Engineered Features
* `purchase_year`, `purchase_month`, `purchase_month_name`, `purchase_year_month`, `purchase_day_name`, `purchase_hour`
* `line_item_total` (`product_price * quantity`)
* `net_purchase_amount` (Reflects returned orders as $0 retained revenue)
* `return_status` ('Returned' vs 'Not Returned')
* `churn_status` ('Churned' vs 'Active')
* `age_group` ('18-25', '26-35', '36-50', '51-70')

---

## 5. Installation & Setup Instructions

### Prerequisites
* Python 3.10+ (tested on Python 3.13)
* Microsoft Power BI Desktop (optional, for opening and editing PBIX models)

### Step 1: Clone or Navigate to Project
```bash
cd "c:\Users\Tharun\Desktop\3rd sem\DATA ANALYTICS AND VISUALIZATION\final product"
```

### Step 2: Create a Virtual Environment (Optional but Recommended)
```bash
python -m venv venv
# On Windows PowerShell:
.\venv\Scripts\Activate.ps1
```

### Step 3: Install Required Dependencies
```bash
python -m pip install -r requirements.txt
```

---

## 6. Execution Instructions

The project is structured with modular, independent Python scripts that can be executed from the root directory or from within their respective subfolders.

### Step 1: Run Data Cleaning
Executes missing value treatment, redundancy checks, standardization, and feature enrichment:
```bash
python 03_Data_Cleaning/data_cleaning.py
```
* **Output 1:** `02_Dataset/Cleaned_Dataset/cleaned_data.csv` (24,999 validated rows x 23 columns)
* **Output 2:** `03_Data_Cleaning/cleaning_report.txt` (Complete audit trail)

### Step 2: Run Exploratory Data Analysis
Executes quantitative sales, product, customer, and financial risk modeling:
```bash
python 04_Data_Analysis/data_analysis.py
```
* **Output:** `04_Data_Analysis/analysis_report.txt` (Comprehensive business diagnostic report)

### Step 3: Run Data Visualizations
Generates all 10 high-resolution statistical charts:
```bash
python 05_Data_Visualisation/data_visualisation.py
```
* **Output:** Saves charts to `05_Data_Visualisation/charts/`

---

## 7. Power BI Dashboard Build Instructions

> [!IMPORTANT]
> **Power BI Automation Note:**
> Power BI Desktop does not provide a command-line API for headless PBIX compilation. In accordance with strict guidelines ("Never create a fake file with a .pbix extension"), all necessary blueprints, DAX code, data model schemas, and visual mockups are provided in `06_PowerBI_Dashboard/`.

### Quick 4-Step Build in Power BI Desktop:
1. **Load Data:** Open Power BI Desktop, click **Get Data -> Text/CSV**, and select `02_Dataset/Cleaned_Dataset/cleaned_data.csv`.
2. **Create Date Dimension:** In Model View, add a new calculated table using the DAX code in `PowerBI_Data_Model_and_Build_Guide.md` and link `Dim_Date[Date]` 1-to-many to `cleaned_data[purchase_date]`.
3. **Add DAX Measures:** Copy and paste the 20 DAX measures from `06_PowerBI_Dashboard/DAX_Measures.dax`.
4. **Construct the Master Executive Dashboard:** Follow the visual layout blueprint in `PowerBI_Data_Model_and_Build_Guide.md` or refer to the high-resolution master mockup in `06_PowerBI_Dashboard/Dashboard_Screenshots/Executive_Sales_Performance_Dashboard.png`:
   * **Executive Slicer Ribbon:** Year, Category, and Payment Method filters
   * **Top KPI Cards:** Gross Revenue ($67.97M), Net Revenue ($40.29M), Returns ($27.67M), Customers (4,212), AOV ($2,718.76), Churn Rate (20.49%)
   * **Visual Panel 1:** Monthly Sales Velocity & Net Revenue Trend (2020 - 2023)
   * **Visual Panel 2:** Product Category Gross vs. Net Revenue Contribution
   * **Visual Panel 3:** Demographic Spend Breakdown across Age Cohorts & Gender
   * **Visual Panel 4:** Top 10 High-Value Spenders & Churn Risk Matrix

---

## 8. Summary of Analytical Findings

| Dimension | Core Metric | Business Finding & Insight |
| :--- | :--- | :--- |
| **Gross Sales** | **$67,966,223.00** | Sustained baseline averaging ~$18M annually (2020-2022). |
| **Net Retained Sales** | **$40,293,892.00** | Net revenue after deducting $27.67M in returned merchandise. |
| **Transaction Volume** | **24,999 Orders** | 75,075 total product units sold; 3.0 units average basket size. |
| **Average Order Value** | **$2,718.76** | Consistent AOV across weekdays ($2,719) and weekends ($2,718). |
| **Category Leaders** | **Clothing & Books** | Account for **60.6% ($41.19M)** of total sales revenue. |
| **Senior Demographic** | **Ages 51 - 70** | Generates **38.3% ($26.03M)** of revenue; lowest churn (18.9%) and highest AOV ($2,811). |
| **Customer Retention** | **79.51% Retained** | 3,349 retained customers vs 863 churned accounts (20.49% churn rate). |
| **Return Rate** | **40.88%** | 10,220 orders returned. Uniform across categories (~40-41%) and payment channels (~40.8%). |
| **Top Payment Method** | **Credit Card** | Dominant channel capturing **40.78% ($27.72M)** of gross volume. |

---

## 9. Data Governance & Limitations

1. **Geographic Distribution:** The Kaggle dataset contains no geographic features (City, State, Country, Zip Code). In compliance with data integrity protocols, no artificial geographic data was hallucinated.
2. **COGS & Profit Margins:** Transaction logs lack wholesale unit procurement costs. Profitability analysis focuses on Gross Revenue vs Return-Adjusted Net Revenue.

---

## 10. Contributors & License

* **Project:** E-Commerce Sales & Business Performance Analytics
* **Tools:** Python 3.13, Pandas, NumPy, Matplotlib, Seaborn, python-docx, Microsoft Power BI
* **License:** MIT License

