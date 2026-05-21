import pandas as pd
import matplotlib.pyplot as plt

# Load data

df = pd.read_csv('E:\\power bi\\Transactions\\processed\\cleaned_transactions.csv')

# Category analysis
category_revenue = (
    df.groupby('product_category')['revenue']
    .sum()
    .sort_values(ascending=False)
)

print(category_revenue)

# Revenue share
category_share = (
    category_revenue / category_revenue.sum()
) * 100

# Visualization
plt.figure(figsize=(8,8))
plt.pie(
    category_share,
    labels=category_share.index,
    autopct='%1.1f%%'
)
plt.title('Revenue Share by Category')
plt.show()

# Save output
category_share.to_csv(
    'E:\\power bi\\Transactions\\processed\\category_revenue_summary.csv'
)