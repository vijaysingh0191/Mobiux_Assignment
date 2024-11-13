from collections import defaultdict
from datetime import datetime

# Helper function to parse CSV line into a dictionary
def parse_line(line):
    date_str, sku, unit_price, quantity, total_price = line.strip().split(',')
    date = datetime.strptime(date_str, '%Y-%m-%d')
    return {
        'date': date,
        'month': date.strftime('%Y-%m'),  # extract month as "YYYY-MM"
        'sku': sku,
        'unit_price': float(unit_price),
        'quantity': int(quantity),
        'total_price': float(total_price)
    }

# Load data
sales_data = []
with open("ice_cream_salesdata.txt") as file:
    for line in file:
        if line.startswith("Date"):
            continue  # skip header
        sales_data.append(parse_line(line))

# Initialize dictionaries for analysis
total_sales = 0
month_sales_totals = defaultdict(float)
monthly_quantity = defaultdict(lambda: defaultdict(int))
monthly_revenue = defaultdict(lambda: defaultdict(float))
popular_item_stats = defaultdict(lambda: defaultdict(list))

# Process each sale record
for sale in sales_data:
    total_sales += sale['total_price']
    month_sales_totals[sale['month']] += sale['total_price']
    
    # Track quantities and revenue by item in each month
    monthly_quantity[sale['month']][sale['sku']] += sale['quantity']
    monthly_revenue[sale['month']][sale['sku']] += sale['total_price']
    
    # Collect data for min, max, and average calculations for the most popular item
    popular_item_stats[sale['month']][sale['sku']].append(sale['quantity'])

# Output the results
print("Total Sales of the Store:", total_sales)

# Monthly sales totals
print("\nMonth-wise Sales Totals:")
for month, sales in month_sales_totals.items():
    print(f"{month}: {sales}")

# Most popular item (by quantity) and highest revenue item in each month
print("\nMost Popular and Highest Revenue Items by Month:")
for month in monthly_quantity:
    # Find the most popular item by quantity
    popular_item = max(monthly_quantity[month], key=monthly_quantity[month].get)
    popular_qty = monthly_quantity[month][popular_item]
    
    # Find the highest revenue item
    top_revenue_item = max(monthly_revenue[month], key=monthly_revenue[month].get)
    top_revenue = monthly_revenue[month][top_revenue_item]
    
    print(f"{month}:")
    print(f"  Most Popular Item: {popular_item} with {popular_qty} units sold")
    print(f"  Highest Revenue Item: {top_revenue_item} with ${top_revenue}")

# Min, max, and average for the most popular item
print("\nStatistics for Most Popular Items:")
for month, items in popular_item_stats.items():
    # Determine the most popular item
    popular_item = max(monthly_quantity[month], key=monthly_quantity[month].get)
    quantities = items[popular_item]
    
    min_orders = min(quantities)
    max_orders = max(quantities)
    avg_orders = sum(quantities) / len(quantities)
    
    print(f"{month} - {popular_item}:")
    print(f"  Min Orders: {min_orders}")
    print(f"  Max Orders: {max_orders}")
    print(f"  Avg Orders: {avg_orders:.2f}")
