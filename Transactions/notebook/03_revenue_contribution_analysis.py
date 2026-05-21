import pandas as pd
import matplotlib.pyplot as plt

# Load data

df = pd.read_csv('E:\\power bi\\Transactions\\processed\\cleaned_transactions.csv')

# Revenue by product
revenue_summary = (
    df.groupby('product_detail')['revenue']
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)

# Revenue percentage

total_revenue = revenue_summary['revenue'].sum()
revenue_summary['revenue_share_pct'] = (
    revenue_summary['revenue'] / total_revenue
) * 100

print(revenue_summary.head())

# Save summary
revenue_summary.to_csv(
    'E:\\power bi\\Transactions\\processed\\product_revenue_summary.csv',
    index=False
)

# Plot top revenue products
plt.figure(figsize=(12,6))
plt.bar(
    revenue_summary['product_detail'][:10],
    revenue_summary['revenue'][:10]
)
plt.xticks(rotation=45)
plt.title('Top Revenue Generating Products')
plt.ylabel('Revenue')
plt.tight_layout()
plt.show()