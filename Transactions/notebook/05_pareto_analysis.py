import pandas as pd
import matplotlib.pyplot as plt

# Load data

df = pd.read_csv('E:\\power bi\\Transactions\\processed\\cleaned_transactions.csv')

# Revenue per product
pareto_df = (
    df.groupby('product_detail')['revenue']
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)

# Cumulative revenue
pareto_df['cumulative_revenue'] = pareto_df['revenue'].cumsum()
pareto_df['cumulative_pct'] = (
    pareto_df['cumulative_revenue'] /
    pareto_df['revenue'].sum()
) * 100

# Save output
pareto_df.to_csv('E:\\power bi\\Transactions\\processed\\pareto_analysis.csv', index=False)

# Plot Pareto chart
fig, ax1 = plt.subplots(figsize=(12,6))

ax1.bar(
    pareto_df['product_detail'],
    pareto_df['revenue']
)

ax2 = ax1.twinx()
ax2.plot(
    pareto_df['product_detail'],
    pareto_df['cumulative_pct'],
    color='red'
)

ax2.axhline(80, color='green', linestyle='--')

plt.xticks(rotation=90)
plt.title('Pareto Analysis of Product Revenue')
plt.tight_layout()
plt.show()