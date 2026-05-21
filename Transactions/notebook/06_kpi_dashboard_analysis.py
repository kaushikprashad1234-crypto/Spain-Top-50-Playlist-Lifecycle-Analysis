import pandas as pd

# Load data

df = pd.read_csv('E:\\power bi\\Transactions\\processed\\cleaned_transactions.csv')

# KPI calculations

total_revenue = df['revenue'].sum()

total_transactions = df['transaction_id'].nunique()

average_order_value = total_revenue / total_transactions

best_product = (
    df.groupby('product_detail')['revenue']
    .sum()
    .idxmax()
)

best_category = (
    df.groupby('product_category')['revenue']
    .sum()
    .idxmax()
)

print('Total Revenue:', total_revenue)
print('Total Transactions:', total_transactions)
print('Average Order Value:', average_order_value)
print('Top Product:', best_product)
print('Top Category:', best_category)