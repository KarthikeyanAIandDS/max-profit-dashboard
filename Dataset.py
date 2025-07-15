import pandas as pd
import numpy as np

# List of real cities in Tamil Nadu and Kerala with their latitude and longitude
cities = [
    {"City": "Chennai", "Latitude": 13.0827, "Longitude": 80.2707},
    {"City": "Coimbatore", "Latitude": 11.0168, "Longitude": 76.9558},
    {"City": "Madurai", "Latitude": 9.9252, "Longitude": 78.1198},
    {"City": "Tiruchirappalli", "Latitude": 10.7905, "Longitude": 78.7047},
    {"City": "Salem", "Latitude": 11.6643, "Longitude": 78.1460},
    {"City": "Thiruvananthapuram", "Latitude": 8.5241, "Longitude": 76.9366},
    {"City": "Kochi", "Latitude": 9.9312, "Longitude": 76.2673},
    {"City": "Kozhikode", "Latitude": 11.2588, "Longitude": 75.7804},
    {"City": "Kollam", "Latitude": 8.8932, "Longitude": 76.6141},
    {"City": "Thrissur", "Latitude": 10.5276, "Longitude": 76.2144},
    {"City": "Tirunelveli", "Latitude": 8.7139, "Longitude": 77.7567},
    {"City": "Tiruppur", "Latitude": 11.1075, "Longitude": 77.3398},
    {"City": "Erode", "Latitude": 11.3410, "Longitude": 77.7172},
    {"City": "Vellore", "Latitude": 12.9165, "Longitude": 79.1325},
    {"City": "Thoothukudi", "Latitude": 8.7642, "Longitude": 78.1348},
    {"City": "Kannur", "Latitude": 11.8745, "Longitude": 75.3704},
    {"City": "Alappuzha", "Latitude": 9.4981, "Longitude": 76.3388},
    {"City": "Palakkad", "Latitude": 10.7867, "Longitude": 76.6548},
    {"City": "Kottayam", "Latitude": 9.5916, "Longitude": 76.5222},
    {"City": "Malappuram", "Latitude": 11.0732, "Longitude": 76.0740},
]

# Function to generate synthetic data
def generate_data(num_rows, data_type):
    data = []
    for i in range(1, num_rows + 1):
        city = np.random.choice(cities)
        if data_type == "supplier":
            row = {
                "Supplier_ID": i,
                "Location": city["City"],
                "Capacity": np.random.randint(500, 1000),
                "Reliability_Score": np.random.randint(5, 10),
                "Sustainability_Score": np.random.randint(5, 10),
                "Carbon_Footprint": np.random.randint(1, 5),
                "Latitude": city["Latitude"],
                "Longitude": city["Longitude"],
            }
        elif data_type == "customer":
            row = {
                "Customer_ID": i,
                "Location": city["City"],
                "Demand": np.random.randint(100, 500),
                "Reliability_Score": np.random.randint(5, 10),
                "Latitude": city["Latitude"],
                "Longitude": city["Longitude"],
            }
        data.append(row)
    return pd.DataFrame(data)

# Generate 1000 rows of data for suppliers and customers
suppliers_df = generate_data(1000, "supplier")
customers_df = generate_data(1000, "customer")

# Save the data to CSV files
suppliers_df.to_csv("suppliers.csv", index=False)
customers_df.to_csv("customers.csv", index=False)

print("Suppliers and Customers CSV files have been updated with 1000 rows of data.")
