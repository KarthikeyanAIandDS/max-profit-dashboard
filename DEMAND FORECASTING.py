import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

# Load historical demand data
demand_df = pd.read_csv('historical_demand.csv')

# Forecast demand for each customer
def forecast_demand(customer_id):
    # Filter data for the customer
    customer_data = demand_df[demand_df['Customer_ID'] == customer_id]
    X = customer_data[['Month']]  # Features (time)
    y = customer_data['Demand']  # Target (demand)

    # Train a linear regression model
    model = LinearRegression()
    model.fit(X, y)

    # Predict demand for the next 12 months
    future_months = pd.DataFrame(np.array(range(13, 25)), columns=['Month'])  # Convert to DataFrame
    forecast = model.predict(future_months)
    return forecast

# Example: Forecast demand for Customer 1
customer_id = 1
forecast = forecast_demand(customer_id)
print(f"Forecasted Demand for Customer {customer_id}: {forecast}")
