# %% [markdown]
# # E-Commerce Sales & Business Performance Analytics
# ## Interactive Visualizations
# Click **"▶ Run Cell"** above any block to generate and display that chart live.

# %% [1] Setup & Load Data
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

sns.set_theme(style="whitegrid")
plt.rcParams["figure.figsize"] = (10, 5)


def get_dataset_path() -> Path:
    root = Path(__file__).resolve().parents[1]
    return root / "clean_dataset" / "cleaned_data.csv"


data_path = get_dataset_path()
df = pd.read_csv(data_path)
print(f"[✓] Loaded {len(df):,} transactions from {data_path.name}")

# %% [2] Chart 1: Monthly Sales Trend (Gross vs Net)
monthly = df.groupby('purchase_year_month')[['total_purchase_amount', 'net_purchase_amount']].sum() / 1e6

plt.figure(figsize=(12, 5))
plt.plot(monthly.index, monthly['total_purchase_amount'], marker='o', label='Gross Sales ($M)', color='#1B365D')
plt.plot(monthly.index, monthly['net_purchase_amount'], marker='s', linestyle='--', label='Net Revenue ($M)', color='#10B981')
plt.title("Monthly Sales Trend: Gross vs Net Revenue (2020 - 2023)")
plt.xlabel("Year-Month")
plt.ylabel("Revenue ($ Millions)")
plt.xticks(range(0, len(monthly), 3), monthly.index[::3], rotation=45)
plt.legend()
plt.tight_layout()
plt.show()

# %% [3] Chart 2: Product Category Performance
cat = df.groupby('product_category')[['total_purchase_amount', 'net_purchase_amount']].sum() / 1e6
cat = cat.sort_values(by='total_purchase_amount', ascending=False)

cat.plot(kind='bar', color=['#1B365D', '#10B981'])
plt.title("Gross vs Net Revenue by Category")
plt.xlabel("Product Category")
plt.ylabel("Revenue ($ Millions)")
plt.xticks(rotation=0)
plt.legend(['Gross Sales', 'Net Revenue'])
plt.tight_layout()
plt.show()

# %% [4] Chart 3: Payment Method Distribution
payments = df.groupby('payment_method')['total_purchase_amount'].sum()

plt.figure(figsize=(7, 7))
plt.pie(
    payments,
    labels=payments.index,
    autopct='%1.1f%%',
    startangle=140,
    colors=['#1B365D', '#3B82F6', '#10B981', '#F59E0B'],
    wedgeprops={'edgecolor': 'white', 'linewidth': 2}
)
plt.title("Payment Method Share by Gross Revenue")
plt.tight_layout()
plt.show()

# %% [5] Chart 4: Customer Age Distribution
plt.figure(figsize=(9, 4.5))
sns.histplot(df['customer_age'], bins=25, kde=True, color='#1B365D', edgecolor='white')
plt.title("Customer Age Demographic Distribution")
plt.xlabel("Age")
plt.ylabel("Transaction Count")
plt.tight_layout()
plt.show()

# %% [6] Chart 5: Top 10 High-Value Customers
top10 = df.groupby('customer_name')['total_purchase_amount'].sum().sort_values(ascending=True).tail(10)

plt.figure(figsize=(10, 5.5))
top10.plot(kind='barh', color='#1B365D')
plt.title("Top 10 High-Value Customers by Total Spend")
plt.xlabel("Total Spend ($ USD)")
plt.ylabel("Customer Name")
plt.tight_layout()
plt.show()

# %% [7] Chart 6: Revenue by Age Cohort
age_rev = df.groupby('age_group', observed=False)['total_purchase_amount'].sum() / 1e6

plt.figure(figsize=(8, 4.5))
sns.barplot(
    x=age_rev.index,
    y=age_rev.values,
    hue=age_rev.index,
    palette=['#1B365D', '#3B82F6', '#60A5FA', '#93C5FD'],
    legend=False
)
plt.title("Gross Revenue Contribution by Age Cohort")
plt.xlabel("Age Cohort")
plt.ylabel("Gross Revenue ($ Millions)")
plt.tight_layout()
plt.show()

# %% [8] Chart 7: Return Rate by Product Category
ret = df.groupby('product_category')['returns'].mean() * 100
ret = ret.sort_values(ascending=False)

plt.figure(figsize=(8, 4.5))
bars = plt.bar(ret.index, ret.values, color='#EF4444', width=0.55)
plt.title("Return Rate (%) by Product Category")
plt.xlabel("Category")
plt.ylabel("Return Rate (%)")
plt.ylim(0, 50)
for bar in bars:
    y = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2, y + 1, f"{y:.1f}%", ha='center', fontsize=10)
plt.tight_layout()
plt.show()

# %% [9] Chart 8: Customer Churn Rate by Gender
churn = df.groupby('gender')['churn'].mean() * 100

plt.figure(figsize=(6, 4))
bars = plt.bar(churn.index, churn.values, color=['#3B82F6', '#EC4899'], width=0.5)
plt.title("Customer Churn Rate by Gender")
plt.ylabel("Churn Rate (%)")
plt.ylim(0, 30)
for bar in bars:
    y = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2, y + 0.8, f"{y:.1f}%", ha='center', fontsize=10)
plt.tight_layout()
plt.show()

# %% [10] Chart 9: Revenue by Day of Week
day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
day_rev = df.groupby('purchase_day_name')['total_purchase_amount'].sum().reindex(day_order) / 1e6

plt.figure(figsize=(9, 4.5))
sns.barplot(x=day_rev.index, y=day_rev.values, hue=day_rev.index, palette='Blues_r', legend=False)
plt.title("Weekly Purchasing Patterns: Gross Revenue by Day")
plt.xlabel("Day of Week")
plt.ylabel("Gross Revenue ($ Millions)")
plt.xticks(rotation=30)
plt.tight_layout()
plt.show()

# %% [11] Chart 10: Annual Sales and Orders
annual = df.groupby('purchase_year').agg(
    revenue=('total_purchase_amount', 'sum'),
    orders=('customer_id', 'count')
)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.5))
(annual['revenue'] / 1e6).plot.bar(ax=ax1, color='#1B365D')
ax1.set_title("Yearly Revenue ($M)")
ax1.set_xlabel("Year")
ax1.tick_params(axis='x', rotation=0)

annual['orders'].plot.bar(ax=ax2, color='#3B82F6')
ax2.set_title("Yearly Order Volume")
ax2.set_xlabel("Year")
ax2.tick_params(axis='x', rotation=0)

plt.tight_layout()
plt.show()
