"""Clean the supplied e-commerce transaction dataset."""
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW_FILE = ROOT / "Dataset" / "raw_data.csv"
OUTPUT_FILE = ROOT / "clean_dataset" / "cleaned_data.csv"

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.drop_duplicates().copy()
    if "Age" in df.columns and "Customer Age" in df.columns:
        if df["Age"].equals(df["Customer Age"]):
            df = df.drop(columns=["Age"])

    mapping = {
        "Customer ID": "customer_id", "Purchase Date": "purchase_date",
        "Product Category": "product_category", "Product Price": "product_price",
        "Quantity": "quantity", "Total Purchase Amount": "total_purchase_amount",
        "Payment Method": "payment_method", "Customer Age": "customer_age",
        "Returns": "returns", "Customer Name": "customer_name",
        "Gender": "gender", "Churn": "churn"
    }
    df = df.rename(columns=mapping)
    required = set(mapping.values()) - {"customer_age"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    df["purchase_date"] = pd.to_datetime(
        df["purchase_date"], format="%d-%m-%Y %H:%M", errors="coerce"
    )
    df = df.dropna(subset=["purchase_date", "customer_id"])
    for col in ["product_price", "quantity", "total_purchase_amount",
                "customer_age", "returns", "churn"]:
        if col in df:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    df["returns"] = df["returns"].fillna(0).astype(int)
    df["churn"] = df["churn"].fillna(0).astype(int)

    for col in ["product_category", "payment_method", "customer_name", "gender"]:
        if col in df:
            df[col] = df[col].fillna("Unknown").astype(str).str.strip()
    df["product_category"] = df["product_category"].str.title()
    df["payment_method"] = df["payment_method"].str.title()
    df["gender"] = df["gender"].str.capitalize()

    dt = df["purchase_date"]
    df["purchase_year"] = dt.dt.year
    df["purchase_month"] = dt.dt.month
    df["purchase_month_name"] = dt.dt.month_name()
    df["purchase_year_month"] = dt.dt.to_period("M").astype(str)
    df["purchase_day_name"] = dt.dt.day_name()
    df["purchase_hour"] = dt.dt.hour
    df["line_item_total"] = df["product_price"] * df["quantity"]
    df["net_purchase_amount"] = np.where(
        df["returns"].eq(1), 0, df["total_purchase_amount"]
    )
    df["return_status"] = np.where(df["returns"].eq(1), "Returned", "Not Returned")
    df["churn_status"] = np.where(df["churn"].eq(1), "Churned", "Active")
    if "customer_age" in df:
        df["age_group"] = pd.cut(
            df["customer_age"], bins=[17, 25, 35, 50, 75],
            labels=["18-25", "26-35", "36-50", "51-75"]
        )
    df["purchase_date"] = dt.dt.strftime("%Y-%m-%d %H:%M:%S")
    return df

def main():
    if not RAW_FILE.exists():
        raise FileNotFoundError(f"Dataset not found: {RAW_FILE}")
    raw = pd.read_csv(RAW_FILE)
    cleaned = clean_data(raw)
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    cleaned.to_csv(OUTPUT_FILE, index=False)
    print(f"Cleaning complete: {len(cleaned):,} rows, {len(cleaned.columns)} columns")
    print(f"Saved to: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
