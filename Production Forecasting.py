import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

# Load historical production data
production_df = pd.read_csv('historical_production.csv')

# Forecast production for each supplier
def forecast_production(supplier_id):
    # Filter data for the supplier
    supplier_data = production_df[production_df['Supplier_ID'] == supplier_id]
    X = supplier_data[['Month']]  # Features (time)
    y = supplier_data['Production']  # Target (production)

    # Train a linear regression model
    model = LinearRegression()
    model.fit(X, y)

    # Predict production for the next 12 months
    future_months = pd.DataFrame(np.array(range(13, 25)), columns=['Month'])  # Convert to DataFrame
    forecast = model.predict(future_months)
    return forecast

# Example: Forecast production for Supplier 1
supplier_id = 1
forecast = forecast_production(supplier_id)
print(f"Forecasted Production for Supplier {supplier_id}: {forecast}")
