"""
data_cleaning.py
----------------
E-Commerce Sales & Business Performance Analytics

Cleans and prepares the raw transaction dataset for analysis:
1. Loads raw Kaggle transaction data.
2. Removes duplicated records and standardizes headers to snake_case.
3. Imputes missing return values (unrecorded returns = kept purchases).
4. Normalizes categorical text (casing and whitespace).
5. Parses transaction timestamps and extracts temporal features.
6. Calculates net purchase amount (adjusting for returns) and customer age groups.
7. Exports the final cleaned dataset to Cleaned_Dataset/cleaned_data.csv.
"""

from pathlib import Path

import numpy as np
import pandas as pd


def get_project_root() -> Path:
    """Returns the project root directory based on standard folder layout."""
    current_path = Path(__file__).resolve()
    for parent in [current_path.parent, current_path.parent.parent]:
        if (parent / "02 Dataset").exists() or (parent / "02_Dataset").exists():
            return parent
    return Path.cwd()


def get_dir(root: Path, *candidates: str) -> Path:
    """Returns the first existing folder candidate or defaults to the first."""
    for name in candidates:
        p = root / name
        if p.exists():
            return p
    return root / candidates[0]


def load_raw_data(data_path: Path) -> pd.DataFrame:
    """Loads raw CSV data with fallback to root dataset if needed."""
    if not data_path.exists():
        alt_path = data_path.parents[2] / "final_data.csv"
        if alt_path.exists():
            data_path = alt_path
        else:
            raise FileNotFoundError(f"Could not locate raw dataset at {data_path}")

    print(f"[+] Loading raw data from: {data_path.name}")
    return pd.read_csv(data_path)


def clean_and_transform(df: pd.DataFrame) -> pd.DataFrame:
    """Performs all data cleaning and feature engineering operations."""
    print("[+] Cleaning and standardizing schema...")

    # Drop duplicate records if any exist
    df = df.drop_duplicates()

    # The dataset contains two identical age columns: 'Age' and 'Customer Age'
    # We drop the redundant 'Age' column to keep the schema clean
    if 'Age' in df.columns and 'Customer Age' in df.columns and (df['Age'] == df['Customer Age']).all():
        df = df.drop(columns=['Age'])

    # Standardize column names to lowercase snake_case for consistency
    column_mapping = {
        'Customer ID': 'customer_id',
        'Purchase Date': 'purchase_date',
        'Product Category': 'product_category',
        'Product Price': 'product_price',
        'Quantity': 'quantity',
        'Total Purchase Amount': 'total_purchase_amount',
        'Payment Method': 'payment_method',
        'Customer Age': 'customer_age',
        'Returns': 'returns',
        'Customer Name': 'customer_name',
        'Gender': 'gender',
        'Churn': 'churn'
    }
    df = df.rename(columns=column_mapping)

    # Impute missing values: unrecorded returns (NaN) represent completed, kept purchases
    # 0 = Item kept, 1 = Item returned
    df['returns'] = df['returns'].fillna(0).astype(int)

    # Clean and trim categorical string values
    for col in ['product_category', 'payment_method', 'customer_name', 'gender']:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()

    df['product_category'] = df['product_category'].str.title()
    df['payment_method'] = df['payment_method'].str.title()
    df['gender'] = df['gender'].str.capitalize()

    print("[+] Engineering temporal and financial dimensions...")

    # Parse timestamps (original format: DD-MM-YYYY HH:MM)
    parsed_dates = pd.to_datetime(df['purchase_date'], format='%d-%m-%Y %H:%M')

    # Temporal breakdown
    df['purchase_year'] = parsed_dates.dt.year
    df['purchase_month'] = parsed_dates.dt.month
    df['purchase_month_name'] = parsed_dates.dt.month_name()
    df['purchase_year_month'] = parsed_dates.dt.to_period('M').astype(str)
    df['purchase_day_name'] = parsed_dates.dt.day_name()
    df['purchase_hour'] = parsed_dates.dt.hour

    # Financial calculations:
    # line_item_total = price * quantity (base item cost before basket calculations)
    # net_purchase_amount = 0 if returned, full amount if retained
    df['line_item_total'] = df['product_price'] * df['quantity']
    df['net_purchase_amount'] = np.where(df['returns'] == 0, df['total_purchase_amount'], 0)

    # Human-readable status flags for reporting and dashboards
    df['return_status'] = np.where(df['returns'] == 1, 'Returned', 'Not Returned')
    df['churn_status'] = np.where(df['churn'] == 1, 'Churned', 'Active')

    # Demographic age bins (standard marketing cohorts)
    age_bins = [17, 25, 35, 50, 75]
    age_labels = ['18-25', '26-35', '36-50', '51-70']
    df['age_group'] = pd.cut(df['customer_age'], bins=age_bins, labels=age_labels)

    # Standardize purchase date into standard ISO format string
    df['purchase_date'] = parsed_dates.dt.strftime('%Y-%m-%d %H:%M:%S')

    return df


def main():
    root = get_project_root()
    dataset_dir = get_dir(root, "02 Dataset", "02_Dataset")
    cleaning_dir = get_dir(root, "03 Data Cleaning", "03_Data_Cleaning")

    input_file = dataset_dir / "Original_Dataset" / "raw_data.csv"
    output_file = dataset_dir / "Cleaned_Dataset" / "cleaned_data.csv"
    report_file = cleaning_dir / "cleaning_report.txt"

    output_file.parent.mkdir(parents=True, exist_ok=True)

    df_raw = load_raw_data(input_file)
    df_cleaned = clean_and_transform(df_raw)

    print(f"[+] Saving cleaned data to: {output_file.relative_to(root)}")
    df_cleaned.to_csv(output_file, index=False)

    if report_file.exists():
        print(f"[+] Verified cleaning audit report: {report_file.relative_to(root)}")

    print(f"[✓] Data cleaning complete: {len(df_cleaned):,} rows, {len(df_cleaned.columns)} columns.")


if __name__ == "__main__":
    main()
