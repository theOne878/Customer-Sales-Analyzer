import pandas as pd
import numpy as np
import re
import random
from datetime import timedelta

# Load data
df = pd.read_csv('customer.csv')

# ---------------------- #
# 🧹 PHASE 1: DATA CLEANING
# ---------------------- #

# --- Normalize OrderDate ---
def normalize_dates(date_series):
    def parse_date(date_str):
        if pd.isna(date_str):
            return np.nan
        
        date_str = str(date_str).strip()

        # Handle formats like: "May 2nd 2023"
        match = re.match(r'([A-Za-z]+)\s+(\d+)(?:st|nd|rd|th)?,?\s*(\d{4})', date_str)
        if match:
            month, day, year = match.groups()
            try:
                return pd.to_datetime(f"{month} {day} {year}")
            except:
                return np.nan

        # Normalize format: replace '/' with '-'
        date_str = date_str.replace('/', '-')
        return pd.to_datetime(date_str, errors='coerce')

    parsed_dates = date_series.apply(parse_date)
    avg_date = parsed_dates.dropna().mean()

    # Add random time (00:00 to 23:59) to each date
    def add_random_time(dt):
        rand_seconds = random.randint(0, 86399)
        return dt + timedelta(seconds=rand_seconds)

    return parsed_dates.apply(lambda x: add_random_time(avg_date) if pd.isna(x) else x)

df['OrderDate'] = normalize_dates(df['OrderDate'])

# --- Clean Location ---
df['Location'] = df['Location'].replace(r'^\s*$', 'New York', regex=True)

# --- Clean Amount ---
df['Amount'] = (
    df['Amount']
    .replace(r'[^\d.]', '', regex=True)  # remove $, commas, etc.
    .astype(float)
    .fillna(df['Amount'].mode()[0])     # fill with mode
)

# --- Normalize Strings ---
df['PaymentMethod'] = df['PaymentMethod'].str.strip().str.lower().str.title()
df['CustomerName'] = df['CustomerName'].str.strip().str.title()

# --- Standardize Category Labels ---
correct_categories = {
    'Electronics': ['electronics', 'electrnics'],
    'Fashion': ['fashion'],
    'Home & Kitchen': ['home & kitchen', 'home kitchen', 'homeandkitchen']
}

# Reverse mapping
category_map = {v.lower(): k for k, vals in correct_categories.items() for v in vals}
df['Category'] = (
    df['Category']
    .str.strip().str.lower()
    .map(category_map)
    .fillna(df['Category'])
)

# ---------------------- #
# 📊 PHASE 2: ANALYSIS
# ---------------------- #

# --- Revenue Insights ---
pivot_insights = df.pivot_table(
    values='Amount',
    index='Location',
    columns='Category',
    aggfunc='sum',
    fill_value=0,
    margins=True,
    margins_name='Total'
).round(2)

avg_order_value_by_city = df.groupby('Location')['Amount'].mean().round(2)
top_customers = df.groupby('CustomerName')['Amount'].sum().sort_values(ascending=False)
top_payment_methods = df.groupby('PaymentMethod')['Amount'].sum().sort_values(ascending=False)
top_categories = df.groupby('Category')['Amount'].sum().sort_values(ascending=False)
orders_per_day = df.groupby(df['OrderDate'].dt.date).size()

# ---------------------- #
# 🔍 PHASE 3: ADVANCED INSIGHTS
# ---------------------- #

# --- Extract multiple coupon codes from Notes ---
df['Coupons'] = df['Notes'].apply(lambda x: re.findall(r'\b[A-Za-z]+\d+\b', str(x)))
df['HighValueOrder'] = df['Amount'] > 100
df['Weekday'] = df['OrderDate'].dt.day_name()
total_coupons_used = df['Coupons'].apply(len).sum()

print(f"Orders with coupons: {total_coupons_used}")

# ---------------------- #
# 📈 PHASE 4: GROWTH & STATISTICS
# ---------------------- #

# --- Correlation between Quantity and Revenue ---
correlation = df['Quantity'].corr(df['Amount'])
print(f"Correlation between Quantity and Revenue: {correlation:.2f}")

# --- Order Value Stats ---
order_stats = df['Amount'].describe(percentiles=[.25, .5, .75, .9])
print(order_stats)

# --- Quartile-based Customer Segmentation ---
customer_sales = df.groupby('CustomerID')['Amount'].sum()
quartiles = pd.qcut(customer_sales, 4, labels=['Q1 (Low)', 'Q2', 'Q3', 'Q4 (Top)'])

customer_segments = pd.DataFrame({
    'TotalSpent': customer_sales,
    'Segment': quartiles
})

print(customer_segments.head())
