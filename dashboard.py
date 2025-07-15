import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import folium
from streamlit_folium import folium_static
from sklearn.linear_model import LinearRegression
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Set page configuration
st.set_page_config(page_title="Tapioca Thippi Flour Dashboard", page_icon="🌾", layout="wide")

# Load datasets
@st.cache_data
def load_data():
    suppliers = pd.read_csv('suppliers.csv')
    customers = pd.read_csv('customers.csv')
    matches = pd.read_csv('supplier_customer_matches.csv')
    production = pd.read_csv('historical_production.csv')
    demand = pd.read_csv('historical_demand.csv')
    return suppliers, customers, matches, production, demand

suppliers_df, customers_df, matches_df, production_df, demand_df = load_data()

# Forecasting
def forecast(data, column, months_ahead=24):
    if data.empty:
        return [], []
    X = data[['Month']]
    y = data[column]
    model = LinearRegression().fit(X, y)
    future_months = pd.DataFrame({'Month': range(X.max().values[0] + 1, X.max().values[0] + months_ahead + 1)})
    forecast_values = model.predict(future_months)
    return future_months['Month'], forecast_values

# Map Visualization
def display_map(map_type, selected_id):
    # Changed tiles to default OpenStreetMap
    m = folium.Map(location=[10.8505, 76.2711], zoom_start=7)
    
    if map_type == "Supplier to Customers" and selected_id:
        supplier = suppliers_df[suppliers_df['Supplier_ID'] == selected_id].iloc[0]
        for _, customer in customers_df.iterrows():
            folium.PolyLine(
                [(supplier['Latitude'], supplier['Longitude']), (customer['Latitude'], customer['Longitude'])], 
                color='red', weight=2.5, opacity=0.8  # Changed back to red
            ).add_to(m)
    
    elif map_type == "Customer to Supplier" and selected_id:
        customer = customers_df[customers_df['Customer_ID'] == selected_id].iloc[0]
        for _, supplier in suppliers_df.iterrows():
            folium.PolyLine(
                [(customer['Latitude'], customer['Longitude']), (supplier['Latitude'], supplier['Longitude'])], 
                color='blue', weight=2.5, opacity=0.8  # Changed back to blue
            ).add_to(m)
    
    folium_static(m)
def send_email_notification(subject, message):
    sender_email = "narainkarthikeyan05@gmail.com"
    receiver_email = "karthikeyann.aids2023@citchennai.net"
    password = "nqdz bzga xouu jtkz"

    email_message = MIMEMultipart()
    email_message["From"] = sender_email
    email_message["To"] = receiver_email
    email_message["Subject"] = subject
    email_message.attach(MIMEText(message, "plain"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, email_message.as_string())
        st.success("Notification sent successfully!")
    except Exception as e:
        st.error(f"An error occurred: {e}")

# Main Dashboard
st.title("🌾 Tapioca Thippi Flour Dashboard")
st.sidebar.title("Navigation")

# Define the 'page' variable
page = st.sidebar.radio("Go to", ["Home", "Forecasting", "Inventory Management", "Dynamic Pricing", "Map View", "Best Match Predictor", "Additional Insights"])

# Custom CSS for dark theme
st.markdown(
    """
    <style>
    /* Main background */
    .stApp {
        background-color: #000000;
        color: #FFFFFF;
    }

    /* Sidebar */
    .css-1d391kg {
        background-color: #1A1A1A !important;
        color: #FFFFFF !important;
    }

    /* Buttons */
    .stButton button {
        background-color: #2E86C1;
        color: #FFFFFF;
        border-radius: 8px;
        padding: 10px 24px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    .stButton button:hover {
        background-color: #1A5276;
        transform: scale(1.05);
    }

    /* Headers */
    h1, h2, h3, h4, h5, h6 {
        color: #2E86C1 !important;
    }

    /* Dataframes */
    .stDataFrame {
        background-color: #1A1A1A !important;
        border: 1px solid #2E86C1 !important;
        border-radius: 8px !important;
    }

    /* Input fields */
    .stTextInput input, .stNumberInput input {
        background-color: #1A1A1A !important;
        color: #FFFFFF !important;
        border: 1px solid #2E86C1 !important;
    }

    /* Select boxes */
    .stSelectbox select {
        background-color: #1A1A1A !important;
        color: #FFFFFF !important;
    }

    /* Charts */
    .plotly-graph-div {
        background-color: #1A1A1A !important;
        border-radius: 10px;
        padding: 15px;
    }

    /* Alert boxes */
    .stAlert {
        background-color: #1A1A1A !important;
        border: 1px solid #2E86C1 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Page Navigation
if page == "Home":
    st.header("📊 Overview")
    st.write("Welcome to the Tapioca Thippi Flour Dashboard! Navigate using the sidebar.")
    
    # Custom dataframe styling
    st.dataframe(
        matches_df.style
            .apply(lambda x: ['background-color: #1A1A1A; color: #FFFFFF' for _ in x], axis=1)
            .set_properties(**{'border': '1px solid #2E86C1', 'border-radius': '8px'})
    )

elif page == "Forecasting":
    st.header("📈 Forecasting")
    forecast_type = st.selectbox("Select Forecasting Type", ["Production Forecast", "Demand Forecast"])
    
    if forecast_type == "Production Forecast":
        supplier_id = st.selectbox("Select Supplier ID", suppliers_df['Supplier_ID'].unique())
        months, forecast_values = forecast(production_df[production_df['Supplier_ID'] == supplier_id], 'Production')
        
        fig = px.line(
            pd.DataFrame({'Month': months, 'Production': forecast_values}),
            x='Month',
            y='Production',
            title="Production Forecast",
            color_discrete_sequence=['#2E86C1']
        )
        fig.update_layout(
            plot_bgcolor='#1A1A1A',
            paper_bgcolor='#1A1A1A',
            font=dict(color='#FFFFFF'),
            xaxis=dict(linecolor='#FFFFFF', gridcolor='#333333'),
            yaxis=dict(linecolor='#FFFFFF', gridcolor='#333333')
        )
        st.plotly_chart(fig, use_container_width=True)
    
    else:
        customer_id = st.selectbox("Select Customer ID", customers_df['Customer_ID'].unique())
        months, forecast_values = forecast(demand_df[demand_df['Customer_ID'] == customer_id], 'Demand')
        
        fig = px.line(
            pd.DataFrame({'Month': months, 'Demand': forecast_values}),
            x='Month',
            y='Demand',
            title="Demand Forecast",
            color_discrete_sequence=['#E74C3C']
        )
        fig.update_layout(
            plot_bgcolor='#1A1A1A',
            paper_bgcolor='#1A1A1A',
            font=dict(color='#FFFFFF'),
            xaxis=dict(linecolor='#FFFFFF', gridcolor='#333333'),
            yaxis=dict(linecolor='#FFFFFF', gridcolor='#333333')
        )
        st.plotly_chart(fig, use_container_width=True)

elif page == "Inventory Management":
    st.header("📦 Inventory Management")
    INVENTORY_FILE = "inventory.txt"
    
    def load_inventory():
        try:
            with open(INVENTORY_FILE, "r") as f:
                return int(f.read())
        except FileNotFoundError:
            return 1000  # Default inventory
    
    def save_inventory(inventory):
        with open(INVENTORY_FILE, "w") as f:
            f.write(str(inventory))

    # Initialize session state
    if 'inventory' not in st.session_state:
        st.session_state.inventory = load_inventory()

    current_inventory = st.session_state.inventory
    st.write(f"Current Inventory: {current_inventory} tons")

    inventory_update = st.number_input("Update Inventory (Tons)", value=0)
    if st.button("Update Inventory"):
        new_inventory = current_inventory + inventory_update
        if new_inventory < 0:
            st.error("❌ Inventory cannot be negative!")
        else:
            save_inventory(new_inventory)
            st.session_state.inventory = new_inventory  # Update session state
            st.success(f"Inventory updated to {new_inventory} tons")

    # Low inventory notification
    if st.session_state.inventory < 500:  # Now properly initialized
        st.warning("⚠️ Low Inventory Alert!")
        if st.button("Send Notification", key="send_notification"):
            inventory_details = {
                'current_inventory': st.session_state.inventory,
                'threshold': 500,
                'location': 'Warehouse A',
                'product': 'Tapioca Thippi Flour',
                'unit': 'tons'
            }

            subject = "Low Inventory Alert - Action Required"
            message = f"""Dear Mill Owner,

This is to inform you that the inventory level for {inventory_details['product']} at {inventory_details['location']} is currently at {inventory_details['current_inventory']} {inventory_details['unit']}, which is below the threshold of {inventory_details['threshold']} {inventory_details['unit']}.

Please take necessary action to replenish the inventory.

Best regards,
{inventory_details['location']} Management Team
            """

            send_email_notification(subject, message)  

elif page == "Dynamic Pricing":
    st.header("💰 Dynamic Pricing")
    base_price = st.number_input("Base Price (INR per Ton)", min_value=1, value=500)
    demand = st.number_input("Demand (Tons)", min_value=1, value=1000)
    supply = st.number_input("Supply (Tons)", min_value=1, value=800)
    price = base_price * (1.2 if demand > supply else 0.8)
    st.metric("Dynamic Price", f"₹{price:.2f} per ton")

elif page == "Map View":
    st.header("🗺 Map View")
    map_type = st.selectbox("Select Map View", ["Supplier to Customers", "Customer to Supplier"])
    selected_id = st.selectbox("Select ID", suppliers_df['Supplier_ID'].unique() if map_type == "Supplier to Customers" else customers_df['Customer_ID'].unique())
    display_map(map_type, selected_id)

elif page == "Best Match Predictor":
    st.header("🔮 Best Match Predictor")
    entity_type = st.selectbox("Select Entity Type", ["Customer", "Supplier"])
    location = st.selectbox("Location", suppliers_df['Location'].unique())
    demand_capacity = st.number_input("Capacity/Demand (Tons)", min_value=1, value=100)
    
    if entity_type == "Customer":
        best_supplier = suppliers_df[(suppliers_df['Location'] == location) & (suppliers_df['Capacity'] >= demand_capacity)].nlargest(1, 'Reliability_Score')
        result = best_supplier.iloc[0]['Supplier_ID'] if not best_supplier.empty else "No match found"
        st.success(f"Best Supplier: {result}")
    else:
        best_customer = customers_df[(customers_df['Location'] == location) & (customers_df['Demand'] <= demand_capacity)].nlargest(1, 'Reliability_Score')
        result = best_customer.iloc[0]['Customer_ID'] if not best_customer.empty else "No match found"
        st.success(f"Best Customer: {result}")

elif page == "Additional Insights":
    st.header("📊 Additional Insights")
    insight_option = st.selectbox("Select Insight", ["Supplier Capacity Overview", "Demand by Location"])
    
    if insight_option == "Supplier Capacity Overview":
        fig = px.bar(suppliers_df, x='Supplier_ID', y='Capacity', title="Supplier Capacity Overview", 
                    color='Supplier_ID', color_discrete_sequence=px.colors.qualitative.Dark24)
        fig.update_layout(
            plot_bgcolor='#1A1A1A',
            paper_bgcolor='#1A1A1A',
            font=dict(color='#FFFFFF')
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        if 'Customer_ID' in demand_df.columns and 'Customer_ID' in customers_df.columns:
            demand_with_location = demand_df.merge(customers_df[['Customer_ID', 'Location']], on='Customer_ID')
            demand_by_location = demand_with_location.groupby('Location')['Demand'].sum().reset_index()
            fig = px.pie(demand_by_location, values='Demand', names='Location', title="Demand by Location",
                        color_discrete_sequence=px.colors.qualitative.Dark24)
            fig.update_layout(
                plot_bgcolor='#1A1A1A',
                paper_bgcolor='#1A1A1A',
                font=dict(color='#FFFFFF')
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.error("Missing required columns in dataset")

# Footer
st.markdown(
    """
    <div style="background: #1A1A1A; padding: 20px; border-top: 2px solid #2E86C1; margin-top: 50px;">
        <p style="color: #FFFFFF; text-align: center;">© 2023 Tapioca Thippi Flour Dashboard</p>
    </div>
    """,
    unsafe_allow_html=True
)
