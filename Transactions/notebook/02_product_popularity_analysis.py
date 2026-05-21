import pandas as pd
import matplotlib.pyplot as plt

# Load cleaned data

df = pd.read_csv('E:\\power bi\\Transactions\\processed\\cleaned_transactions.csv')

# Product popularity
product_popularity = (
    df.groupby('product_detail')['transaction_qty']
    .sum()
    .sort_values(ascending=False)
)

print(product_popularity.head(10))

# Plot top 10 products
plt.figure(figsize=(12,6))
product_popularity.head(10).plot(kind='bar')
plt.title('Top 10 Selling Products')
plt.xlabel('Product')
plt.ylabel('Units Sold')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Bottom 10 products
print(product_popularity.tail(10))