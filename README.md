# E-Commerce Analytics Dashboard

A Python-based analytics project for exploring e-commerce transactions, sales performance,
product categories, payment methods, customer behaviour, returns, and churn.

## Project workflow

1. **Project Proposal** — project scope and objectives.
2. **Data Collection** — source transaction data in `Dataset/raw_data.csv`.
3. **Data Cleaning** — duplicate handling, data type normalization, date features,
   return status, and customer cohorts.
4. **Data Analytics** — business KPIs, category performance, payment channels,
   and customer metrics.
5. **Data Visualization** — static analytical charts.
6. **Interactive Dashboard** — filterable Streamlit dashboard with Plotly charts.

## Folder structure

```text
Project Proposal/       Project proposal document
Dataset/                Original transaction CSV
clean_dataset/          Cleaned transaction CSV
src/                    Cleaning, analysis, and visualization scripts
dashboard/              Interactive Streamlit application
requirements.txt        Python dependencies
```

## Setup (Windows PowerShell)

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python src/data_cleaning.py
streamlit run dashboard/app.py
```

If PowerShell blocks activation, run the app using `.venv\Scripts\python.exe -m streamlit run dashboard/app.py`.

## Notes

- The dashboard reads `clean_dataset/cleaned_data.csv`; if it is missing, it attempts
  to clean `Dataset/raw_data.csv` in memory.
- Currency is displayed as USD because the source transaction data is represented
  in dollar amounts. Confirm the dataset's original currency before presenting results.
- Do not upload private customer data. Review dataset licensing and attribution before
  publishing the raw CSV publicly.\n