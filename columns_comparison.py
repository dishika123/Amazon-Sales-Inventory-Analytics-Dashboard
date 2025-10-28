import pandas as pd

# Read all CSV files
new_2022 = pd.read_csv('new_2022_product_info.csv')
new_2021 = pd.read_csv('new_2021_product_info.csv')
int_sales = pd.read_csv('new_international_sales_report.csv') 
sales_report = pd.read_csv('new_stock_report.csv')
amazon_sales = pd.read_csv('new_amazon_national_sales.csv')  # Note: Changed filename to match actual file

# Create dictionary with table names and their columns
tables = {
    'Product_Info_2022': new_2022.columns,
    'Product_Info_2021': new_2021.columns,
    'International_Sales': int_sales.columns,
    'Stock_Report': sales_report.columns,
    'Amazon_Sales': amazon_sales.columns
}

# Find maximum number of columns
max_cols = max(len(cols) for cols in tables.values())

# Create DataFrame with padded columns
comparison_df = pd.DataFrame()
for table_name, columns in tables.items():
    # Pad with NaN if needed
    padded_cols = list(columns) + [pd.NA] * (max_cols - len(columns))
    comparison_df[table_name] = padded_cols

# Export to CSV
comparison_df.to_csv('new_columns_comparison.csv', index=False)
