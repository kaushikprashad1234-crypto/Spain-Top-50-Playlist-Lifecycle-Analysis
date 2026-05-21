import pandas as pd
import numpy as np

# Load dataset
file_path = 'E:\\power bi\\Transactions\\raw\\Afficionado Coffee Roasters.xlsx - Transactions.csv'
df = pd.read_csv(file_path)

# Display basic information
print(df.head())
print(df.info())
print(df.isnull().sum())

# Remove duplicates
print("Duplicates:", df.duplicated().sum())
df = df.drop_duplicates()

# Convert time column
df['transaction_time'] = pd.to_datetime(df['transaction_time'])

# Create revenue column
df['revenue'] = df['transaction_qty'] * df['unit_price']

# Remove invalid quantities

df = df[df['transaction_qty'] > 0]

# Remove invalid prices

df = df[df['unit_price'] > 0]

# Save cleaned data
output_path = 'E:\\power bi\\Transactions\\processed\\cleaned_transactions.csv'
df.to_csv(output_path, index=False)

print('Data cleaned successfully')