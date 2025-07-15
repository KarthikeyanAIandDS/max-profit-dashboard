import pandas as pd

# Load your datasets
suppliers_df = pd.read_csv('suppliers.csv')
customers_df = pd.read_csv('customers.csv')

# Supplier-Customer Matching Function
def match_supplier_customer(suppliers_df, customers_df):
    matches = []
    for _, customer in customers_df.iterrows():
        best_supplier = None
        best_score = -1
        for _, supplier in suppliers_df.iterrows():
            # Check if supplier and customer are in the same location and capacity meets demand
            if supplier['Location'] == customer['Location'] and supplier['Capacity'] >= customer['Demand']:
                # Calculate a score based on reliability, sustainability, and carbon footprint
                score = (
                    (supplier['Reliability_Score'] * 10)  # Higher reliability is better
                    + (supplier['Sustainability_Score'] * 10)  # Higher sustainability is better
                    - (supplier['Carbon_Footprint'] * 5)  # Lower carbon footprint is better
                )
                # Update best supplier if the current score is higher
                if score > best_score:
                    best_score = score
                    best_supplier = supplier['Supplier_ID']
        # Add the match to the list
        matches.append({
            'Customer_ID': customer['Customer_ID'],
            'Supplier_ID': best_supplier,
            'Score': best_score
        })
    return pd.DataFrame(matches)

# Perform matching
matches_df = match_supplier_customer(suppliers_df, customers_df)

# Save matches to a CSV file
matches_df.to_csv('supplier_customer_matches.csv', index=False)

# Display the matches
print(matches_df.head())
