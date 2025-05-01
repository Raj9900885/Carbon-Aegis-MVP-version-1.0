import streamlit as st
import pandas as pd
import numpy as np
from utils.data_manager import init_session_state, save_input_data, clear_data
from utils.calculation import calculate_emissions

# Initialize session state if needed
init_session_state()

# Add Carbon Aegis branding
col1, col2 = st.columns([1, 5])
with col1:
    st.image("assets/logo.png", width=100)
with col2:
    st.title("Carbon Aegis - Data Input")

st.markdown("""
Enter your activity data categorized by emission scope. All calculations follow the GHG Protocol Corporate Standard.

* **Scope 1**: Direct emissions from owned or controlled sources
* **Scope 2**: Indirect emissions from purchased electricity, steam, heating, and cooling
* **Scope 3**: All other indirect emissions in a company's value chain
""")

# Create tabs for different scopes
tab1, tab2, tab3, tab4 = st.tabs(["Scope 1: Direct", "Scope 2: Energy Indirect", "Scope 3: Other Indirect", "Settings"])

# Time Period Selection (in Settings tab)
with tab4:
    st.header("Settings")
    
    st.subheader("Reporting Period")
    col1, col2 = st.columns(2)
    with col1:
        time_period = st.selectbox(
            "Time Period", 
            ["Daily", "Weekly", "Monthly", "Quarterly", "Annually"],
            index=4 if 'time_period' not in st.session_state else 
                  ["Daily", "Weekly", "Monthly", "Quarterly", "Annually"].index(st.session_state.time_period),
            key="time_period_select"
        )
    
    st.subheader("Calculation Method")
    calculation_method = st.selectbox(
        "Accuracy Level", 
        ["Exact (measured data)", "Average (based on typical values)", "Estimate (approximated)"],
        index=0 if 'calculation_method' not in st.session_state else 
              ["Exact (measured data)", "Average (based on typical values)", "Estimate (approximated)"].index(st.session_state.calculation_method),
        key="calculation_method_select"
    )
    
    st.subheader("Preferred Units")
    col1, col2 = st.columns(2)
    with col1:
        distance_unit = st.selectbox(
            "Distance Unit", 
            ["Kilometers", "Miles"],
            index=0 if 'distance_unit' not in st.session_state else 
                  ["Kilometers", "Miles"].index(st.session_state.distance_unit),
            key="distance_unit_select"
        )
    with col2:
        volume_unit = st.selectbox(
            "Volume Unit", 
            ["Liters", "Gallons"],
            index=0 if 'volume_unit' not in st.session_state else 
                  ["Liters", "Gallons"].index(st.session_state.volume_unit),
            key="volume_unit_select"
        )
        
    st.info("These settings affect how your emissions are calculated and displayed across the application.")

# SCOPE 1 - Direct emissions
with tab1:
    st.header("Scope 1: Direct Emissions")
    st.markdown("""
    Direct GHG emissions from sources owned or controlled by your organization, such as:
    - Stationary combustion (boilers, furnaces)
    - Mobile combustion (company vehicles)
    - Refrigerant leakage
    - Process emissions
    """)
    
    # Fuel Consumption 
    st.subheader("Fuel Consumption")
    with st.expander("Vehicle Fuel Usage", expanded=True):
        st.markdown("Enter details about your vehicle fuel consumption:")
        
        # First row - Fuel Type and Amount
        col1, col2, col3 = st.columns(3)
        with col1:
            fuel_type = st.selectbox(
                "Fuel Type", 
                ["Petrol/Gasoline", "Diesel", "LPG/Propane", "Biodiesel", "E85 (Ethanol)", "CNG", "Other"],
                index=0 if 'fuel_type' not in st.session_state else 
                      ["Petrol/Gasoline", "Diesel", "LPG/Propane", "Biodiesel", "E85 (Ethanol)", "CNG", "Other"].index(st.session_state.fuel_type),
                key="fuel_type_select"
            )
        
        with col2:
            fuel_unit = st.selectbox(
                "Unit", 
                ["Liters", "Gallons", "kg"],
                index=0 if 'fuel_unit' not in st.session_state else 
                      ["Liters", "Gallons", "kg"].index(st.session_state.fuel_unit),
                key="fuel_unit_select"
            )
        
        with col3:
            fuel_amount = st.number_input(
                f"Amount ({fuel_unit})", 
                min_value=0.0, 
                value=st.session_state.get('fuel_amount', 0.0),
                help=f"Enter the amount of {fuel_type} consumed"
            )
    
    # Vehicle Types
    st.subheader("Vehicle Transportation")
    with st.expander("Vehicle Travel", expanded=True):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            vehicle_type = st.selectbox(
                "Vehicle Type", 
                ["Car (Petrol/Gasoline)", "Car (Diesel)", "Car (Hybrid)", "Car (Electric)", 
                 "Motorcycle", "Bus", "Truck (Light)", "Truck (Heavy)", "Other"],
                index=0 if 'vehicle_type' not in st.session_state else 
                      ["Car (Petrol/Gasoline)", "Car (Diesel)", "Car (Hybrid)", "Car (Electric)", 
                       "Motorcycle", "Bus", "Truck (Light)", "Truck (Heavy)", "Other"].index(st.session_state.vehicle_type),
                key="vehicle_type_select"
            )
        
        with col2:
            distance_unit_vehicle = st.selectbox(
                "Distance Unit", 
                ["Kilometers", "Miles"],
                index=0 if 'distance_unit_vehicle' not in st.session_state else 
                      ["Kilometers", "Miles"].index(st.session_state.distance_unit_vehicle),
                key="distance_unit_vehicle_select"
            )
        
        with col3:
            vehicle_distance = st.number_input(
                f"Distance ({distance_unit_vehicle})", 
                min_value=0.0, 
                value=st.session_state.get('vehicle_distance', 0.0),
                help=f"Enter the distance traveled by {vehicle_type}"
            )
    
    # Air Travel
    st.subheader("Air Travel")
    with st.expander("Flight Information", expanded=True):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            flight_type = st.selectbox(
                "Flight Type", 
                ["Short-haul (<1,500 km)", "Medium-haul (1,500-3,700 km)", "Long-haul (>3,700 km)"],
                index=0 if 'flight_type' not in st.session_state else 
                      ["Short-haul (<1,500 km)", "Medium-haul (1,500-3,700 km)", "Long-haul (>3,700 km)"].index(st.session_state.flight_type),
                key="flight_type_select"
            )
        
        with col2:
            flight_class = st.selectbox(
                "Travel Class", 
                ["Economy", "Premium Economy", "Business", "First"],
                index=0 if 'flight_class' not in st.session_state else 
                      ["Economy", "Premium Economy", "Business", "First"].index(st.session_state.flight_class),
                key="flight_class_select"
            )
        
        with col3:
            flight_distance = st.number_input(
                f"Distance ({distance_unit})", 
                min_value=0.0, 
                value=st.session_state.get('flight_distance', 0.0),
                help=f"Enter the total flight distance"
            )
        
        # Number of passengers option
        col1, col2 = st.columns(2)
        with col1:
            num_passengers = st.number_input(
                "Number of Passengers", 
                min_value=1, 
                value=st.session_state.get('num_passengers', 1),
                help="Enter the number of passengers for this trip"
            )
    
    # Public Transport
    st.subheader("Public Transport")
    with st.expander("Public Transportation", expanded=True):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            transport_type = st.selectbox(
                "Transport Type", 
                ["Bus", "Train (Local/Regional)", "Train (Intercity)", "Train (High-speed)", 
                 "Tram/Light Rail", "Subway/Metro", "Ferry", "Other"],
                index=0 if 'transport_type' not in st.session_state else 
                      ["Bus", "Train (Local/Regional)", "Train (Intercity)", "Train (High-speed)", 
                       "Tram/Light Rail", "Subway/Metro", "Ferry", "Other"].index(st.session_state.transport_type),
                key="transport_type_select"
            )
        
        with col2:
            transport_distance_unit = st.selectbox(
                "Distance Unit", 
                ["Kilometers", "Miles"],
                index=0 if 'transport_distance_unit' not in st.session_state else 
                      ["Kilometers", "Miles"].index(st.session_state.transport_distance_unit),
                key="transport_distance_unit_select"
            )
        
        with col3:
            transport_distance = st.number_input(
                f"Distance ({transport_distance_unit})", 
                min_value=0.0, 
                value=st.session_state.get('transport_distance', 0.0),
                help=f"Enter the distance traveled by {transport_type}"
            )
    
    # Zero Emission Transport
    st.subheader("Zero Emission Transport")
    with st.expander("Walking, Cycling, etc.", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            zero_emission_type = st.selectbox(
                "Transport Type", 
                ["Walking", "Cycling", "E-Bike (Renewable Charged)", "Other Zero Emission"],
                index=0 if 'zero_emission_type' not in st.session_state else 
                      ["Walking", "Cycling", "E-Bike (Renewable Charged)", "Other Zero Emission"].index(st.session_state.zero_emission_type),
                key="zero_emission_type_select"
            )
        
        with col2:
            zero_emission_distance = st.number_input(
                f"Distance ({distance_unit})", 
                min_value=0.0, 
                value=st.session_state.get('zero_emission_distance', 0.0),
                help=f"Enter the distance traveled by {zero_emission_type} (no emissions calculated)"
            )

# SCOPE 2 - Energy Indirect Emissions
with tab2:
    st.header("Scope 2: Energy Indirect Emissions")
    st.markdown("""
    Indirect GHG emissions from purchased electricity, steam, heating and cooling consumed by your organization:
    - Purchased electricity
    - Purchased steam
    - Purchased heating or cooling
    - District energy systems
    """)
    
    # Electricity
    st.subheader("Electricity Consumption")
    with st.expander("Electricity", expanded=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            electricity = st.number_input(
                "Electricity Consumption", 
                min_value=0.0, 
                value=st.session_state.get('electricity', 0.0),
                help="Enter the total electricity consumption"
            )
        
        with col2:
            electricity_unit = st.selectbox(
                "Unit", 
                ["kWh", "MWh"],
                index=0 if 'electricity_unit' not in st.session_state else 
                      ["kWh", "MWh"].index(st.session_state.electricity_unit),
                key="electricity_unit_select"
            )
        
        with col3:
            grid_region = st.selectbox(
                "Electricity Grid Region", 
                ["Northeast", "Southeast", "Midwest", "Southwest", "West", "Other"],
                index=0 if 'grid_region' not in st.session_state else 
                      ["Northeast", "Southeast", "Midwest", "Southwest", "West", "Other"].index(st.session_state.grid_region),
                key="grid_region_select"
            )
        
        # Renewable energy percentage
        col1, col2 = st.columns(2)
        with col1:
            renewable_percentage = st.slider(
                "Renewable Energy Percentage", 
                min_value=0, 
                max_value=100,
                value=st.session_state.get('renewable_percentage', 0),
                help="Percentage of electricity from renewable sources"
            )
    
    # Heating and Cooling
    st.subheader("Heating and Cooling")
    with st.expander("Heating and Cooling Systems", expanded=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            heating_type = st.selectbox(
                "Heating Type", 
                ["Natural Gas", "Heating Oil", "Propane", "Electric Heating", "District Heating", "Biomass", "Other"],
                index=0 if 'heating_type' not in st.session_state else 
                      ["Natural Gas", "Heating Oil", "Propane", "Electric Heating", "District Heating", "Biomass", "Other"].index(st.session_state.heating_type),
                key="heating_type_select"
            )
        
        with col2:
            heating_unit = st.selectbox(
                "Unit", 
                ["kWh", "MJ", "BTU", "m³", "liters", "gallons"],
                index=0 if 'heating_unit' not in st.session_state else 
                      ["kWh", "MJ", "BTU", "m³", "liters", "gallons"].index(st.session_state.heating_unit),
                key="heating_unit_select"
            )
        
        with col3:
            heating_amount = st.number_input(
                f"Amount ({heating_unit})", 
                min_value=0.0, 
                value=st.session_state.get('heating_amount', 0.0),
                help=f"Enter the amount of {heating_type} consumed for heating"
            )

# SCOPE 3 - Other Indirect Emissions
with tab3:
    st.header("Scope 3: Other Indirect Emissions")
    st.markdown("""
    All other indirect emissions from your value chain, including:
    - Business travel
    - Employee commuting
    - Purchased goods and services
    - Transportation and distribution
    - Waste disposal
    - Use of sold products
    - End-of-life treatment
    """)
    
    # Waste
    st.subheader("Waste Generation")
    with st.expander("Waste Disposal", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            waste_type = st.selectbox(
                "Waste Type", 
                ["Landfill (Mixed)", "Recycled Paper", "Recycled Plastic", "Recycled Glass", 
                 "Recycled Metal", "Organic/Compost", "Electronic Waste", "Other"],
                index=0 if 'waste_type' not in st.session_state else 
                      ["Landfill (Mixed)", "Recycled Paper", "Recycled Plastic", "Recycled Glass", 
                       "Recycled Metal", "Organic/Compost", "Electronic Waste", "Other"].index(st.session_state.waste_type),
                key="waste_type_select"
            )
        
        with col2:
            waste_amount = st.number_input(
                "Amount (kg)", 
                min_value=0.0, 
                value=st.session_state.get('waste_amount', 0.0),
                help=f"Enter the weight of {waste_type}"
            )
    
    # Water
    st.subheader("Water Consumption")
    with st.expander("Water Usage", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            water_type = st.selectbox(
                "Water Source", 
                ["Municipal Supply", "Well Water", "Harvested Rainwater", "Recycled Water", "Other"],
                index=0 if 'water_type' not in st.session_state else 
                      ["Municipal Supply", "Well Water", "Harvested Rainwater", "Recycled Water", "Other"].index(st.session_state.water_type),
                key="water_type_select"
            )
        
        with col2:
            water_amount = st.number_input(
                "Amount (m³)", 
                min_value=0.0, 
                value=st.session_state.get('water_amount', 0.0),
                help=f"Enter the volume of {water_type} consumed"
            )
    
    # Other emissions (e.g., paper, refrigerants)
    st.subheader("Other Materials")
    with st.expander("Other Consumables", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            material_type = st.selectbox(
                "Material Type", 
                ["Paper", "Plastic", "Metal", "Glass", "Electronics", "Textiles", "Other"],
                index=0 if 'material_type' not in st.session_state else 
                      ["Paper", "Plastic", "Metal", "Glass", "Electronics", "Textiles", "Other"].index(st.session_state.material_type),
                key="material_type_select"
            )
        
        with col2:
            material_amount = st.number_input(
                "Amount (kg)", 
                min_value=0.0, 
                value=st.session_state.get('material_amount', 0.0),
                help=f"Enter the weight of {material_type} consumed"
            )
    
    # Refrigerants
    st.subheader("Refrigerants")
    with st.expander("Refrigerant Leakage", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            refrigerant_type = st.selectbox(
                "Refrigerant Type", 
                ["R-410A", "R-134a", "R-404A", "R-32", "R-22", "R-407C", "Other"],
                index=0 if 'refrigerant_type' not in st.session_state else 
                      ["R-410A", "R-134a", "R-404A", "R-32", "R-22", "R-407C", "Other"].index(st.session_state.refrigerant_type),
                key="refrigerant_type_select"
            )
        
        with col2:
            refrigerant_amount = st.number_input(
                "Amount (kg)", 
                min_value=0.0, 
                value=st.session_state.get('refrigerant_amount', 0.0),
                help="Enter the amount of refrigerant leaked"
            )

# Actions section with improved UI
st.markdown("---")
st.subheader("📋 Actions")

# Add a container with a background color
with st.container():
    st.markdown("""
    <style>
    .action-container {
        background-color: #f0f8f4;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #2E8B57;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="action-container">', unsafe_allow_html=True)
    
    # Create three columns for the buttons
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        save_button = st.button("💾 Save and Calculate", use_container_width=True)
    with col2:
        save_db_button = st.button("🌐 Save to Database", use_container_width=True)
    with col3:
        clear_button = st.button("🗑️ Clear All Data", use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Handle button clicks
if save_button or save_db_button:
    # Gather all the input data
    input_data = {
        # Settings
        'time_period': time_period,
        'calculation_method': calculation_method,
        'distance_unit': distance_unit,
        'volume_unit': volume_unit,
        
        # Transportation
        'fuel_type': fuel_type,
        'fuel_unit': fuel_unit,
        'fuel_amount': fuel_amount,
        'vehicle_type': vehicle_type,
        'distance_unit_vehicle': distance_unit_vehicle,
        'vehicle_distance': vehicle_distance,
        'flight_type': flight_type,
        'flight_class': flight_class,
        'flight_distance': flight_distance,
        'num_passengers': num_passengers,
        'transport_type': transport_type,
        'transport_distance_unit': transport_distance_unit,
        'transport_distance': transport_distance,
        'zero_emission_type': zero_emission_type,
        'zero_emission_distance': zero_emission_distance,
        
        # Energy
        'electricity': electricity,
        'electricity_unit': electricity_unit,
        'grid_region': grid_region,
        'renewable_percentage': renewable_percentage,
        'heating_type': heating_type,
        'heating_unit': heating_unit,
        'heating_amount': heating_amount,
        
        # Other Sources
        'waste_type': waste_type,
        'waste_amount': waste_amount,
        'water_type': water_type,
        'water_amount': water_amount,
        'material_type': material_type,
        'material_amount': material_amount,
        'refrigerant_type': refrigerant_type,
        'refrigerant_amount': refrigerant_amount,
        
        # Legacy variables to maintain compatibility with calculation module
        'natural_gas': heating_amount if heating_type == "Natural Gas" and heating_unit == "m³" else 0.0,
        'diesel_stationary': heating_amount if heating_type == "Heating Oil" and heating_unit == "liters" else 0.0,
        'gasoline': fuel_amount if fuel_type == "Petrol/Gasoline" and fuel_unit == "Liters" else 0.0,
        'diesel_mobile': fuel_amount if fuel_type == "Diesel" and fuel_unit == "Liters" else 0.0,
        'purchased_steam': heating_amount if heating_type == "District Heating" and heating_unit == "MJ" else 0.0,
        'purchased_heat': heating_amount if heating_type == "District Heating" and heating_unit == "MJ" else 0.0,
        'air_travel_short': flight_distance if flight_type == "Short-haul (<1,500 km)" else 0.0,
        'air_travel_long': flight_distance if flight_type == "Long-haul (>3,700 km)" else 0.0,
        'car_commute': vehicle_distance if vehicle_type.startswith("Car") else 0.0,
        'public_transit': transport_distance if transport_type in ["Bus", "Train (Local/Regional)", "Tram/Light Rail", "Subway/Metro"] else 0.0,
        'landfill_waste': waste_amount if waste_type == "Landfill (Mixed)" else 0.0,
        'recycled_waste': waste_amount if waste_type.startswith("Recycled") else 0.0,
        'paper_consumption': material_amount if material_type == "Paper" else 0.0,
        'water_consumption': water_amount 
    }
    
    # Save to session state (always do this)
    save_to_db = save_db_button  # Only save to DB if the save_db_button was clicked
    
    # For database operations, use organization info from session state
    organization_name = st.session_state.get('organization_name', '')
    report_year = st.session_state.get('report_year', 2025)
    
    # Save data
    save_input_data(input_data, save_to_db=save_to_db, 
                   organization_name=organization_name, 
                   report_year=report_year)
    
    # Calculate emissions
    calculate_emissions()
    
    # Display different messages based on which button was clicked
    if save_db_button:
        record_id = st.session_state.get('current_record_id')
        if record_id:
            st.success(f"Data saved to database (Record #{record_id}) and emissions calculated successfully! Navigate to the Dashboard to view your results.")
        else:
            st.warning("Data saved to session but database save may have failed. Check database connection.")
    else:
        st.success("Data saved and emissions calculated successfully! Navigate to the Dashboard to view your results.")
    
    st.session_state.has_data = True

# Handle clear button
if clear_button:
    clear_data()
    st.success("All data has been cleared!")
    st.rerun()  # Rerun the app to reflect the cleared state

# Navigation section
st.markdown("---")
st.subheader("📍 Navigation")

# Create a navigation container with styled buttons
with st.container():
    st.markdown("""
    <style>
    .nav-container {
        background-color: #f0f8f4;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #2E8B57;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="nav-container">', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button("📊 View Dashboard", use_container_width=True):
            st.switch_page("pages/2_Dashboard.py")
    
    with col2:
        if st.button("📑 Generate Report", use_container_width=True):
            st.switch_page("pages/3_Report.py")
            
    with col3:
        if st.button("📁 View Saved Reports", use_container_width=True):
            st.switch_page("pages/4_Saved_Reports.py")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Help section with improved styling
st.markdown("### ❓ Help & Resources")
with st.container():
    st.markdown("""
    <style>
    .help-container {
        background-color: #f5f7fa;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #3498db;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="help-container">', unsafe_allow_html=True)
    
    st.markdown("""
    ### Carbon Aegis Data Input Guide
    
    **Scope Classification Tips:**
    * **Scope 1**: Enter direct emissions from sources you own or control
    * **Scope 2**: Record purchased electricity, steam, heating, and cooling  
    * **Scope 3**: Track all other indirect emissions from your value chain
    
    **For Best Results:**
    * Use data from utility bills, fuel receipts, and accurate records
    * Select the appropriate time period and units in Settings tab
    * Be consistent with your measurement approach across reporting periods
    * Consider using the Carbon Aegis verification service for external validation
    
    **Need Additional Help?**
    Hover over any input field for specific guidance, or contact Carbon Aegis support for comprehensive assistance.
    """)
    
    st.markdown('</div>', unsafe_allow_html=True)
