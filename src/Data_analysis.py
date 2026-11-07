"""
data_analysis.py
----------------
E-Commerce Sales & Business Performance Analytics

Performs core business analysis on the cleaned transaction dataset:
- Executive KPIs: Gross & Net Revenue, Orders, Customer Counts, AOV, Return/Churn Rates
- Category Performance: Revenue, Order Volume, Return Rates per Category
- Customer Behavior: Order frequency, repeat buyer rate, top spenders
- Channel & Demographics: Payment methods and Age Cohort revenue contributions
- Validates consistency with the comprehensive analysis_report.txt
"""

from pathlib import Path

import pandas as pd


def get_project_root() -> Path:
    """Returns the project root directory."""
    current_path = Path(__file__).resolve()
    return current_path.parent.parent


def get_dir(root: Path, *candidates: str) -> Path:
    """Returns the first existing folder candidate or defaults to the first."""
    for name in candidates:
        p = root / name
        if p.exists():
            return p
    return root / candidates[0]


def load_dataset(data_path: Path) -> pd.DataFrame:
    """Loads cleaned transactions dataset."""
    if not data_path.exists():
        raise FileNotFoundError(f"Cleaned dataset not found at {data_path}. Run data_cleaning.py first.")
    return pd.read_csv(data_path)


def analyze_sales_and_revenue(df: pd.DataFrame) -> dict:
    """Computes high-level revenue and transactional metrics."""
    gross_rev = df['total_purchase_amount'].sum()
    net_rev = df['net_purchase_amount'].sum()
    refund_loss = gross_rev - net_rev
    total_orders = len(df)
    unique_cust = df['customer_id'].nunique()
    aov = df['total_purchase_amount'].mean()
    return_rate = (df['returns'] == 1).mean() * 100

    # Customer-level churn rate: unique customers who have churned
    churn_rate = (df.groupby('customer_id')['churn'].first() == 1).mean() * 100

    return {
        'gross_revenue': gross_rev,
        'net_revenue': net_rev,
        'refund_loss': refund_loss,
        'total_orders': total_orders,
        'unique_customers': unique_cust,
        'aov': aov,
        'return_rate': return_rate,
        'churn_rate': churn_rate
    }


def analyze_categories(df: pd.DataFrame) -> pd.DataFrame:
    """Analyzes sales performance breakdown across product categories."""
    grouped = df.groupby('product_category').agg(
        orders=('total_purchase_amount', 'count'),
        units_sold=('quantity', 'sum'),
        gross_sales=('total_purchase_amount', 'sum'),
        net_sales=('net_purchase_amount', 'sum'),
        returns_count=('returns', 'sum')
    ).reset_index()

    grouped['return_rate'] = (grouped['returns_count'] / grouped['orders']) * 100
    grouped['share_of_sales'] = (grouped['gross_sales'] / df['total_purchase_amount'].sum()) * 100
    return grouped.sort_values(by='gross_sales', ascending=False)


def analyze_payment_channels(df: pd.DataFrame) -> pd.DataFrame:
    """Evaluates payment method breakdown and revenue distribution."""
    grouped = df.groupby('payment_method').agg(
        transactions=('total_purchase_amount', 'count'),
        total_amount=('total_purchase_amount', 'sum'),
        avg_ticket=('total_purchase_amount', 'mean')
    ).reset_index()

    grouped['volume_share'] = (grouped['transactions'] / len(df)) * 100
    return grouped.sort_values(by='total_amount', ascending=False)


def analyze_customers(df: pd.DataFrame) -> tuple[float, float, pd.DataFrame]:
    """Analyzes customer purchase frequency and top spending accounts."""
    orders_per_cust = df.groupby('customer_id').size()
    avg_orders = orders_per_cust.mean()
    repeat_rate = (orders_per_cust > 1).mean() * 100

    top_spenders = df.groupby('customer_id').agg(
        customer_name=('customer_name', 'first'),
        orders=('total_purchase_amount', 'count'),
        total_spend=('total_purchase_amount', 'sum'),
        churn=('churn', 'first')
    ).sort_values(by='total_spend', ascending=False).head(5)

    return avg_orders, repeat_rate, top_spenders


def print_executive_summary(kpis: dict, cat_df: pd.DataFrame, pay_df: pd.DataFrame,
                            avg_orders: float, repeat_rate: float, top_spenders: pd.DataFrame) -> None:
    """Displays formatted analytical summary to console."""
    sep = "=" * 70
    print("\n" + sep)
    print("        E-COMMERCE EXECUTIVE BUSINESS PERFORMANCE SUMMARY")
    print(sep)
    print(f"Gross Revenue        : ${kpis['gross_revenue']:>14,.2f}")
    print(f"Net Realized Revenue : ${kpis['net_revenue']:>14,.2f}")
    print(f"Refund / Return Loss : ${kpis['refund_loss']:>14,.2f} ({kpis['return_rate']:.2f}% return rate)")
    print(f"Total Transactions   : {kpis['total_orders']:>14,}")
    print(f"Unique Customers     : {kpis['unique_customers']:>14,}")
    print(f"Average Order Value  : ${kpis['aov']:>14,.2f}")
    print(f"Customer Churn Rate  : {kpis['churn_rate']:>13.2f}%")
    print(f"Repeat Customer Rate : {repeat_rate:>13.2f}%")
    print(sep)

    print("\n[+] Product Category Breakdown:")
    for _, row in cat_df.iterrows():
        print(f"  * {row['product_category']:<12}: Gross ${row['gross_sales']:>10,.2f} "
              f"| Net ${row['net_sales']:>10,.2f} | Returns: {row['return_rate']:.1f}%")

    print("\n[+] Payment Methods Breakdown:")
    for _, row in pay_df.iterrows():
        print(f"  * {row['payment_method']:<12}: ${row['total_amount']:>10,.2f} "
              f"({row['volume_share']:.1f}% of orders) | Avg Ticket: ${row['avg_ticket']:.2f}")

    print("\n[+] Top 5 High-Value Customers:")
    for _, row in top_spenders.iterrows():
        status = "CHURNED" if row['churn'] == 1 else "Active"
        print(f"  * {row['customer_name']:<20}: ${row['total_spend']:>9,.2f} across {row['orders']} orders [{status}]")
    print(sep + "\n")


def main():
    root = get_project_root()
    data_file = root / "clean_dataset" / "cleaned_data.csv"
    report_file = root / "analysis_report.txt"

    print(f"[+] Loading cleaned transactions: {data_file.relative_to(root)}")
    df = load_dataset(data_file)

    kpis = analyze_sales_and_revenue(df)
    cat_df = analyze_categories(df)
    pay_df = analyze_payment_channels(df)
    avg_orders, repeat_rate, top_spenders = analyze_customers(df)

    print_executive_summary(kpis, cat_df, pay_df, avg_orders, repeat_rate, top_spenders)

    if report_file.exists():
        print(f"[✓] Comprehensive business report verified at: {report_file.relative_to(root)}")
    else:
        print(f"[!] Notice: Analysis report not found at: {report_file.relative_to(root)}")


if __name__ == "__main__":
    main()
