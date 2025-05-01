import streamlit as st
import pandas as pd
import numpy as np
from utils.data_manager import init_session_state
from utils.visualization import (
    create_emissions_summary_chart,
    create_scope_breakdown_chart,
    create_emissions_by_category_chart,
    create_scope3_breakdown_chart
)

# Initialize session state if needed
init_session_state()

st.title("Carbon Emissions Dashboard")

# Check if user has entered data
if not st.session_state.get('has_data', False):
    st.warning("No data has been entered yet. Please go to the Data Input page first.")
    st.stop()

# Get organization information and settings
organization_name = st.session_state.get('organization_name', '')
report_year = st.session_state.get('report_year', '')
time_period = st.session_state.get('time_period', 'Annually')
calculation_method = st.session_state.get('calculation_method', 'Exact (measured data)')

# Display organization information if available
if organization_name:
    st.markdown(f"### Organization: {organization_name}")
    if report_year:
        st.markdown(f"### Reporting Year: {report_year}")
    st.markdown("---")

# Show total emissions with time period
st.markdown(f"## Total Carbon Emissions ({time_period})")
st.metric("Total Carbon Footprint", f"{st.session_state.total_emissions:.2f} tCO₂e")
st.caption(f"Calculation method: {calculation_method}")

# Key metrics in columns
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Direct Emissions", 
             f"{st.session_state.scope1_total:.2f} tCO₂e", 
             f"{(st.session_state.scope1_total / st.session_state.total_emissions * 100):.1f}% of total")
with col2:
    st.metric("Energy Indirect", 
             f"{st.session_state.scope2_total:.2f} tCO₂e", 
             f"{(st.session_state.scope2_total / st.session_state.total_emissions * 100):.1f}% of total")
with col3:
    st.metric("Other Indirect", 
             f"{st.session_state.scope3_total:.2f} tCO₂e", 
             f"{(st.session_state.scope3_total / st.session_state.total_emissions * 100):.1f}% of total")

# Visual Overview
st.markdown("## Visual Overview")

# Display emissions summary chart (pie chart of scopes)
st.plotly_chart(create_emissions_summary_chart(), use_container_width=True)

# Transportation Emissions Section
st.markdown("## Transportation Emissions")

# Display transportation-related metrics
transportation_sources = [
    ('fuel_type', 'fuel_amount', 'fuel_unit'),
    ('vehicle_type', 'vehicle_distance', 'distance_unit_vehicle'),
    ('flight_type', 'flight_distance', 'distance_unit'),
    ('transport_type', 'transport_distance', 'transport_distance_unit')
]

# Create a container for transportation metrics
transport_container = st.container()
with transport_container:
    col1, col2 = st.columns(2)
    
    # Display each transportation source as a metric if it has a value
    for i, (type_key, amount_key, unit_key) in enumerate(transportation_sources):
        if type_key in st.session_state and amount_key in st.session_state and st.session_state.get(amount_key, 0) > 0:
            with col1 if i % 2 == 0 else col2:
                type_value = st.session_state.get(type_key, "")
                amount_value = st.session_state.get(amount_key, 0)
                unit_value = st.session_state.get(unit_key, "")
                
                # Get corresponding emissions if available
                emission_value = 0
                emission_found = False
                
                # Map to legacy variables for emissions lookup
                if type_key == 'fuel_type' and amount_key == 'fuel_amount':
                    if type_value == 'Petrol/Gasoline' and 'gasoline' in st.session_state.emissions_data.get('scope1', {}):
                        emission_value = st.session_state.emissions_data['scope1']['gasoline']
                        emission_found = True
                    elif type_value == 'Diesel' and 'diesel_mobile' in st.session_state.emissions_data.get('scope1', {}):
                        emission_value = st.session_state.emissions_data['scope1']['diesel_mobile']
                        emission_found = True
                elif type_key == 'flight_type' and amount_key == 'flight_distance':
                    if type_value == 'Short-haul (<1,500 km)' and 'air_travel_short' in st.session_state.emissions_data.get('scope3', {}):
                        emission_value = st.session_state.emissions_data['scope3']['air_travel_short']
                        emission_found = True
                    elif type_value == 'Long-haul (>3,700 km)' and 'air_travel_long' in st.session_state.emissions_data.get('scope3', {}):
                        emission_value = st.session_state.emissions_data['scope3']['air_travel_long']
                        emission_found = True
                
                # Display the metric with emission value if found
                metric_label = f"{type_value}: {amount_value} {unit_value}"
                if emission_found:
                    st.metric(metric_label, f"{emission_value:.2f} tCO₂e")
                else:
                    st.metric(metric_label, "N/A")

# Energy Emissions Section
st.markdown("## Energy Emissions")

# Display energy-related metrics
energy_sources = [
    ('electricity', 'electricity_unit', 'grid_region'),
    ('heating_type', 'heating_amount', 'heating_unit')
]

# Create a container for energy metrics
energy_container = st.container()
with energy_container:
    col1, col2 = st.columns(2)
    
    # Display each energy source as a metric if it has a value
    for i, (source_key, amount_key, unit_key) in enumerate(energy_sources):
        if source_key in st.session_state and amount_key in st.session_state and st.session_state.get(amount_key, 0) > 0:
            with col1 if i % 2 == 0 else col2:
                source_value = st.session_state.get(source_key, "")
                amount_value = st.session_state.get(amount_key, 0)
                unit_value = st.session_state.get(unit_key, "")
                
                # Get corresponding emissions if available
                emission_value = 0
                emission_found = False
                
                # Map to legacy variables for emissions lookup
                if source_key == 'electricity' and 'electricity' in st.session_state.emissions_data.get('scope2', {}):
                    emission_value = st.session_state.emissions_data['scope2']['electricity']
                    emission_found = True
                elif source_key == 'heating_type' and source_value == 'Natural Gas' and 'natural_gas' in st.session_state.emissions_data.get('scope1', {}):
                    emission_value = st.session_state.emissions_data['scope1']['natural_gas']
                    emission_found = True
                
                # Display the metric with emission value if found
                metric_label = f"{source_value}: {amount_value} {unit_value}"
                if emission_found:
                    st.metric(metric_label, f"{emission_value:.2f} tCO₂e")
                else:
                    st.metric(metric_label, "N/A")

# Detailed Breakdowns (using the original scopes for compatibility)
st.markdown("## Detailed Breakdown")

tab1, tab2, tab3 = st.tabs(["Direct (Scope 1)", "Energy Indirect (Scope 2)", "Other Indirect (Scope 3)"])

with tab1:
    st.subheader("Direct Emissions (Scope 1)")
    
    # Metrics for Scope 1 categories
    if hasattr(st.session_state, 'emissions_data') and 'scope1' in st.session_state.emissions_data:
        scope1_data = st.session_state.emissions_data['scope1']
        
        # Create columns for metrics
        cols = st.columns(3)
        
        for i, (source, value) in enumerate(scope1_data.items()):
            with cols[i % 3]:
                # Map technical names to more user-friendly names
                display_name = source.replace('_', ' ').title()
                if source == 'natural_gas':
                    display_name = "Natural Gas"
                elif source == 'diesel_stationary':
                    display_name = "Heating Oil"
                elif source == 'gasoline':
                    display_name = "Petrol/Gasoline"
                elif source == 'diesel_mobile':
                    display_name = "Diesel (Vehicles)"
                
                st.metric(display_name, f"{value:.2f} tCO₂e")
        
        # Scope 1 breakdown chart
        st.plotly_chart(create_scope_breakdown_chart('scope1'), use_container_width=True)
    else:
        st.info("No direct emissions data available.")

with tab2:
    st.subheader("Energy Indirect Emissions (Scope 2)")
    
    # Metrics for Scope 2 categories
    if hasattr(st.session_state, 'emissions_data') and 'scope2' in st.session_state.emissions_data:
        scope2_data = st.session_state.emissions_data['scope2']
        
        # Create columns for metrics
        cols = st.columns(3)
        
        for i, (source, value) in enumerate(scope2_data.items()):
            with cols[i % 3]:
                # Map technical names to more user-friendly names
                display_name = source.replace('_', ' ').title()
                if source == 'purchased_steam':
                    display_name = "District Heating (Steam)"
                elif source == 'purchased_heat':
                    display_name = "District Heating (Heat)"
                
                st.metric(display_name, f"{value:.2f} tCO₂e")
        
        # Scope 2 breakdown chart
        st.plotly_chart(create_scope_breakdown_chart('scope2'), use_container_width=True)
    else:
        st.info("No energy indirect emissions data available.")

with tab3:
    st.subheader("Other Indirect Emissions (Scope 3)")
    
    # Metrics for Scope 3 categories
    if hasattr(st.session_state, 'emissions_data') and 'scope3' in st.session_state.emissions_data:
        scope3_data = st.session_state.emissions_data['scope3']
        
        # Group Scope 3 emissions by category
        categories = {
            'Transportation': ['air_travel_short', 'air_travel_long', 'rental_car', 'car_commute', 'public_transit'],
            'Accommodation': ['hotel_stays'],
            'Waste': ['landfill_waste', 'recycled_waste'],
            'Materials & Services': ['paper_consumption', 'water_consumption']
        }
        
        # Display category totals
        for category, sources in categories.items():
            category_total = sum(scope3_data.get(source, 0) for source in sources)
            if category_total > 0:
                st.metric(f"{category}", f"{category_total:.2f} tCO₂e")
                
                # Show details for each category
                with st.expander(f"{category} Details"):
                    for source in sources:
                        if source in scope3_data and scope3_data[source] > 0:
                            # Map technical names to more user-friendly names
                            display_name = source.replace('_', ' ').title()
                            if source == 'air_travel_short':
                                display_name = "Short-haul Flights"
                            elif source == 'air_travel_long':
                                display_name = "Long-haul Flights"
                            elif source == 'car_commute':
                                display_name = "Car Travel"
                            
                            st.metric(display_name, f"{scope3_data[source]:.2f} tCO₂e")
        
        # Scope 3 category breakdown chart
        st.plotly_chart(create_scope3_breakdown_chart(), use_container_width=True)
    else:
        st.info("No other indirect emissions data available.")

# Overall emissions by category
st.markdown("## Emissions by Category")
st.plotly_chart(create_emissions_by_category_chart(), use_container_width=True)

# Zero Emissions Tracking
if 'zero_emission_distance' in st.session_state and st.session_state.zero_emission_distance > 0:
    st.markdown("## Zero Emission Transportation")
    zero_type = st.session_state.get('zero_emission_type', 'Walking')
    zero_distance = st.session_state.get('zero_emission_distance', 0)
    distance_unit = st.session_state.get('distance_unit', 'Kilometers')
    
    st.success(f"You traveled {zero_distance} {distance_unit} by {zero_type}, which produced zero carbon emissions. Great job! 👏")

# Recommendations section
st.markdown("## Reduction Recommendations")
st.markdown("""
Based on your carbon emissions profile, consider these reduction strategies:

1. **Transportation**: 
   - Use public transport or carpooling to reduce individual vehicle emissions
   - Consider electric or hybrid vehicles for your next purchase
   - Try walking or cycling for short distances

2. **Energy Efficiency**: 
   - Switch to LED lighting and energy-efficient appliances
   - Improve insulation to reduce heating/cooling needs
   - Consider renewable energy sources for your electricity

3. **Consumption**: 
   - Reduce waste by recycling and composting
   - Choose products with minimal packaging
   - Opt for locally produced goods to reduce transportation emissions

For detailed recommendations tailored to your specific emissions profile, please download the full Carbon Emissions Report.
""")

# Navigation buttons
st.markdown("## Next Steps")
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("⬅️ Return to Data Input"):
        st.switch_page("pages/1_Data_Input.py")
with col2:
    if st.button("📊 View Saved Reports"):
        st.switch_page("pages/4_Saved_Reports.py")
with col3:
    if st.button("➡️ Go to Report Generation"):
        st.switch_page("pages/3_Report.py")
