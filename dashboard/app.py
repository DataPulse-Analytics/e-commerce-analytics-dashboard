from pathlib import Path
import sys
import importlib.util
import pandas as pd
import plotly.express as px
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
CLEAN_FILE = ROOT / "clean_dataset" / "cleaned_data.csv"
RAW_FILE = ROOT / "Dataset" / "raw_data.csv"

st.set_page_config(page_title="E-Commerce Analytics", page_icon="🛍️", layout="wide")

@st.cache_data
def load_data():
    if CLEAN_FILE.exists():
        df = pd.read_csv(CLEAN_FILE)
    elif RAW_FILE.exists():
        cleaning_module_path = ROOT / "src" / "data_cleaning.py"
        if not cleaning_module_path.exists():
            raise FileNotFoundError(f"Could not find cleaning script at {cleaning_module_path}.")

        spec = importlib.util.spec_from_file_location("data_cleaning", cleaning_module_path)
        if spec is None or spec.loader is None:
            raise ImportError(f"Unable to load cleaning module from {cleaning_module_path}.")

        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)
        df = module.clean_data(pd.read_csv(RAW_FILE))
    else:
        raise FileNotFoundError("Place raw_data.csv inside the Dataset folder.")
    df["purchase_date"] = pd.to_datetime(df["purchase_date"], errors="coerce")
    return df.dropna(subset=["purchase_date"])

st.title("🛍️ E-Commerce Analytics Dashboard")
st.caption("Sales performance • Customer behaviour • Product insights")

try:
    df = load_data()
except Exception as exc:
    st.error(str(exc))
    st.stop()

with st.sidebar:
    st.header("Dashboard Filters")
    years = sorted(df["purchase_year"].dropna().unique().tolist())
    selected_years = st.multiselect("Purchase year", years, default=years)
    categories = sorted(df["product_category"].dropna().unique().tolist())
    selected_categories = st.multiselect("Product category", categories, default=categories)
    payments = sorted(df["payment_method"].dropna().unique().tolist())
    selected_payments = st.multiselect("Payment method", payments, default=payments)

filtered = df[
    df["purchase_year"].isin(selected_years)
    & df["product_category"].isin(selected_categories)
    & df["payment_method"].isin(selected_payments)
].copy()

if filtered.empty:
    st.warning("No records match these filters. Select at least one option in each filter.")
    st.stop()

gross = filtered["total_purchase_amount"].sum()
net = filtered["net_purchase_amount"].sum()
orders = len(filtered)
customers = filtered["customer_id"].nunique()
aov = filtered["total_purchase_amount"].mean()
return_rate = filtered["returns"].mean() * 100

k1, k2, k3, k4, k5, k6 = st.columns(6)
k1.metric("Gross Sales", f"${gross:,.0f}")
k2.metric("Net Revenue", f"${net:,.0f}")
k3.metric("Orders", f"{orders:,}")
k4.metric("Customers", f"{customers:,}")
k5.metric("Average Order", f"${aov:,.2f}")
k6.metric("Return Rate", f"{return_rate:.1f}%")

st.divider()
left, right = st.columns(2)
with left:
    monthly = filtered.groupby("purchase_year_month", as_index=False).agg(
        Gross_Sales=("total_purchase_amount", "sum"),
        Net_Revenue=("net_purchase_amount", "sum")
    )
    monthly_long = monthly.melt("purchase_year_month", var_name="Metric", value_name="Amount")
    fig = px.line(monthly_long, x="purchase_year_month", y="Amount", color="Metric",
                  markers=True, title="Monthly Sales: Gross vs Net")
    st.plotly_chart(fig, use_container_width=True)
with right:
    cat = filtered.groupby("product_category", as_index=False).agg(
        Revenue=("net_purchase_amount", "sum"), Orders=("customer_id", "count")
    ).sort_values("Revenue", ascending=False)
    fig = px.bar(cat, x="product_category", y="Revenue", color="Revenue",
                 title="Net Revenue by Product Category")
    st.plotly_chart(fig, use_container_width=True)

left, right = st.columns(2)
with left:
    pay = filtered.groupby("payment_method", as_index=False)["total_purchase_amount"].sum()
    fig = px.pie(pay, names="payment_method", values="total_purchase_amount",
                 hole=0.45, title="Revenue by Payment Method")
    st.plotly_chart(fig, use_container_width=True)
with right:
    age = filtered.dropna(subset=["age_group"]).groupby("age_group", observed=False,
            as_index=False)["net_purchase_amount"].sum()
    fig = px.bar(age, x="age_group", y="net_purchase_amount",
                 title="Net Revenue by Customer Age Group", labels={"net_purchase_amount":"Net Revenue"})
    st.plotly_chart(fig, use_container_width=True)

st.subheader("Customer Insights")
customer = filtered.groupby("customer_name", as_index=False).agg(
    Orders=("customer_id", "count"), Spend=("total_purchase_amount", "sum")
).sort_values("Spend", ascending=False).head(10)
st.plotly_chart(px.bar(customer, x="Spend", y="customer_name", orientation="h",
                       title="Top 10 Customers by Spend"), use_container_width=True)

st.subheader("Transaction Details")
st.dataframe(filtered, use_container_width=True, hide_index=True)
st.download_button("Download filtered data (CSV)", filtered.to_csv(index=False).encode("utf-8"),
                   file_name="ecommerce_filtered_data.csv", mime="text/csv")
