import pandas as pd
import numpy as np

# Set random seed for reproducibility
np.random.seed(42)

# Generate historical production data for suppliers
suppliers = pd.read_csv('suppliers.csv')
historical_production = []
for _, supplier in suppliers.iterrows():
    for month in range(1, 13):  # 12 months of historical data
        historical_production.append({
            'Supplier_ID': supplier['Supplier_ID'],
            'Month': month,
            'Production': np.random.randint(supplier['Capacity'] * 0.8, supplier['Capacity'] * 1.2)  # Random production within 80-120% of capacity
        })

# Generate historical demand data for customers
customers = pd.read_csv('customers.csv')
historical_demand = []
for _, customer in customers.iterrows():
    for month in range(1, 13):  # 12 months of historical data
        historical_demand.append({
            'Customer_ID': customer['Customer_ID'],
            'Month': month,
            'Demand': np.random.randint(customer['Demand'] * 0.8, customer['Demand'] * 1.2)  # Random demand within 80-120% of average demand
        })

# Convert to DataFrames
production_df = pd.DataFrame(historical_production)
demand_df = pd.DataFrame(historical_demand)

# Save to CSV
production_df.to_csv('historical_production.csv', index=False)
demand_df.to_csv('historical_demand.csv', index=False)

# Display sample data
print("Historical Production Sample:")
print(production_df.head())
print("\nHistorical Demand Sample:")
print(demand_df.head())
