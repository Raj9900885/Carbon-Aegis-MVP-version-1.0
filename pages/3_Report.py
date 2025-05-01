import streamlit as st
import pandas as pd
import numpy as np
import base64
from datetime import datetime
from utils.data_manager import init_session_state
from utils.report_generator import generate_pdf_report, generate_excel_report
from utils.database import save_report

# Initialize session state if needed
init_session_state()

st.title("Emission Baseline Report")

# Check if user has entered data
if not st.session_state.get('has_data', False):
    st.warning("No data has been entered yet. Please go to the Data Input page first.")
    st.stop()

# Report configuration section
st.header("Report Configuration")

# Get organization info from session state (if available)
org_name_default = st.session_state.get('organization_name', 'Your Company')
report_year_default = st.session_state.get('report_year', datetime.now().year)

col1, col2 = st.columns(2)

with col1:
    organization_name = st.text_input("Organization Name", org_name_default)
    report_year = st.selectbox("Reporting Year", 
                              options=list(range(datetime.now().year, datetime.now().year-10, -1)),
                              index=list(range(datetime.now().year, datetime.now().year-10, -1)).index(report_year_default)
                                  if report_year_default in range(datetime.now().year, datetime.now().year-10, -1) else 0)

with col2:
    prepared_by = st.text_input("Prepared By", "")
    report_date = st.date_input("Report Date", datetime.now())

# Report preview section
st.header("Report Preview")

# Summary tab
with st.expander("Summary", expanded=True):
    st.markdown(f"""
    ## Emission Baseline Report - {organization_name}
    
    **Reporting Period:** January 1, {report_year} - December 31, {report_year}  
    **Prepared By:** {prepared_by}  
    **Date:** {report_date.strftime('%B %d, %Y')}
    
    ### Executive Summary
    
    This report provides a comprehensive overview of greenhouse gas (GHG) emissions for {organization_name} during the {report_year} reporting period. 
    All calculations follow the GHG Protocol Corporate Standard methodology.
    
    ### Key Findings
    
    Total GHG Emissions: **{st.session_state.total_emissions:.2f} tCO₂e**
    
    Emissions by Scope:
    - Scope 1 (Direct): **{st.session_state.scope1_total:.2f} tCO₂e** ({(st.session_state.scope1_total / st.session_state.total_emissions * 100):.1f}%)
    - Scope 2 (Indirect Energy): **{st.session_state.scope2_total:.2f} tCO₂e** ({(st.session_state.scope2_total / st.session_state.total_emissions * 100):.1f}%)
    - Scope 3 (Other Indirect): **{st.session_state.scope3_total:.2f} tCO₂e** ({(st.session_state.scope3_total / st.session_state.total_emissions * 100):.1f}%)
    """)

# Input data tab
with st.expander("Input Data"):
    st.markdown("### Activity Data Used in Calculations")
    
    # Scope 1 input data
    st.markdown("#### Scope 1: Direct Emissions")
    scope1_inputs = {
        "Natural Gas (m³)": st.session_state.get('natural_gas', 0),
        "Stationary Diesel (liters)": st.session_state.get('diesel_stationary', 0),
        "Gasoline (liters)": st.session_state.get('gasoline', 0),
        "Mobile Diesel (liters)": st.session_state.get('diesel_mobile', 0),
        f"Refrigerant - {st.session_state.get('refrigerant_type', 'N/A')} (kg)": st.session_state.get('refrigerant_amount', 0)
    }
    
    scope1_df = pd.DataFrame(list(scope1_inputs.items()), columns=["Source", "Activity Data"])
    st.table(scope1_df)
    
    # Scope 2 input data
    st.markdown("#### Scope 2: Indirect Emissions from Purchased Energy")
    scope2_inputs = {
        "Electricity (kWh)": st.session_state.get('electricity', 0),
        "Grid Region": st.session_state.get('grid_region', 'N/A'),
        "Purchased Steam (MJ)": st.session_state.get('purchased_steam', 0),
        "Purchased Heat (MJ)": st.session_state.get('purchased_heat', 0)
    }
    
    scope2_df = pd.DataFrame(list(scope2_inputs.items()), columns=["Source", "Activity Data"])
    st.table(scope2_df)
    
    # Scope 3 input data
    st.markdown("#### Scope 3: Other Indirect Emissions")
    scope3_inputs = {
        "Short-haul Air Travel (passenger-km)": st.session_state.get('air_travel_short', 0),
        "Long-haul Air Travel (passenger-km)": st.session_state.get('air_travel_long', 0),
        "Hotel Stays (room-nights)": st.session_state.get('hotel_stays', 0),
        "Rental Car (km)": st.session_state.get('rental_car', 0),
        "Car Commuting (passenger-km)": st.session_state.get('car_commute', 0),
        "Public Transit (passenger-km)": st.session_state.get('public_transit', 0),
        "Landfill Waste (kg)": st.session_state.get('landfill_waste', 0),
        "Recycled Waste (kg)": st.session_state.get('recycled_waste', 0),
        "Paper Consumption (kg)": st.session_state.get('paper_consumption', 0),
        "Water Consumption (m³)": st.session_state.get('water_consumption', 0)
    }
    
    scope3_df = pd.DataFrame(list(scope3_inputs.items()), columns=["Source", "Activity Data"])
    st.table(scope3_df)

# Results tab
with st.expander("Detailed Results"):
    st.markdown("### Detailed Emissions Results")
    
    # Emissions by scope and source
    emissions_data = {
        "Scope": [],
        "Emission Source": [],
        "Emissions (tCO₂e)": [],
        "Percentage of Total": []
    }
    
    # Add Scope 1 emissions
    if hasattr(st.session_state, 'emissions_data') and 'scope1' in st.session_state.emissions_data:
        for source, value in st.session_state.emissions_data['scope1'].items():
            emissions_data["Scope"].append("Scope 1")
            emissions_data["Emission Source"].append(source.replace("_", " ").title())
            emissions_data["Emissions (tCO₂e)"].append(round(value, 2))
            emissions_data["Percentage of Total"].append(f"{(value / st.session_state.total_emissions * 100):.1f}%")
    
    # Add Scope 2 emissions
    if hasattr(st.session_state, 'emissions_data') and 'scope2' in st.session_state.emissions_data:
        for source, value in st.session_state.emissions_data['scope2'].items():
            emissions_data["Scope"].append("Scope 2")
            emissions_data["Emission Source"].append(source.replace("_", " ").title())
            emissions_data["Emissions (tCO₂e)"].append(round(value, 2))
            emissions_data["Percentage of Total"].append(f"{(value / st.session_state.total_emissions * 100):.1f}%")
    
    # Add Scope 3 emissions
    if hasattr(st.session_state, 'emissions_data') and 'scope3' in st.session_state.emissions_data:
        for source, value in st.session_state.emissions_data['scope3'].items():
            emissions_data["Scope"].append("Scope 3")
            emissions_data["Emission Source"].append(source.replace("_", " ").title())
            emissions_data["Emissions (tCO₂e)"].append(round(value, 2))
            emissions_data["Percentage of Total"].append(f"{(value / st.session_state.total_emissions * 100):.1f}%")
    
    # Create DataFrame and display
    emissions_df = pd.DataFrame(emissions_data)
    st.dataframe(emissions_df)
    
    # Scope totals
    st.markdown("### Emissions by Scope")
    scope_totals = {
        "Scope": ["Scope 1", "Scope 2", "Scope 3", "Total"],
        "Emissions (tCO₂e)": [
            round(st.session_state.scope1_total, 2),
            round(st.session_state.scope2_total, 2),
            round(st.session_state.scope3_total, 2),
            round(st.session_state.total_emissions, 2)
        ],
        "Percentage": [
            f"{(st.session_state.scope1_total / st.session_state.total_emissions * 100):.1f}%",
            f"{(st.session_state.scope2_total / st.session_state.total_emissions * 100):.1f}%",
            f"{(st.session_state.scope3_total / st.session_state.total_emissions * 100):.1f}%",
            "100.0%"
        ]
    }
    
    scope_totals_df = pd.DataFrame(scope_totals)
    st.table(scope_totals_df)

# Methodology tab
with st.expander("Methodology"):
    st.markdown("""
    ### Calculation Methodology
    
    This GHG emissions inventory follows the Greenhouse Gas Protocol Corporate Standard, which provides requirements and guidance for companies and organizations preparing a GHG emissions inventory.
    
    #### Emission Factors
    
    The following emission factors were used in the calculations:
    
    **Scope 1**
    - Natural Gas: 0.00205 tCO₂e/m³
    - Diesel (stationary): 0.00270 tCO₂e/liter
    - Gasoline: 0.00233 tCO₂e/liter
    - Diesel (mobile): 0.00267 tCO₂e/liter
    - Refrigerants: Varies by type (R-410A: 2088 GWP, R-134a: 1430 GWP)
    
    **Scope 2**
    - Electricity: Varies by grid region (US average: 0.000416 tCO₂e/kWh)
    - Steam: 0.00009 tCO₂e/MJ
    - Heat: 0.00007 tCO₂e/MJ
    
    **Scope 3**
    - Air Travel (short haul): 0.000156 tCO₂e/passenger-km
    - Air Travel (long haul): 0.000139 tCO₂e/passenger-km
    - Hotel Stays: 0.0218 tCO₂e/room-night
    - Rental Car: 0.000175 tCO₂e/km
    - Car Commuting: 0.000175 tCO₂e/passenger-km
    - Public Transit: 0.000067 tCO₂e/passenger-km
    - Landfill Waste: 0.000458 tCO₂e/kg
    - Recycled Waste: 0.000021 tCO₂e/kg
    - Paper: 0.00139 tCO₂e/kg
    - Water: 0.000344 tCO₂e/m³
    
    All calculations were performed using the activity data provided and the appropriate emission factors.
    """)

# Recommendations tab
with st.expander("Recommendations"):
    st.markdown("""
    ### Emission Reduction Recommendations
    
    Based on the emissions profile, the following recommendations are provided to reduce GHG emissions:
    
    #### Scope 1 Reduction Strategies
    
    1. **Energy Efficiency in Facilities**
       - Optimize heating systems to reduce natural gas consumption
       - Regular maintenance of equipment to ensure optimal performance
       - Implement building automation systems for better energy management
    
    2. **Fleet Management**
       - Consider transitioning to electric or hybrid vehicles
       - Implement a vehicle maintenance program to improve fuel efficiency
       - Optimize routes to reduce fuel consumption
    
    3. **Refrigerant Management**
       - Regular leak detection and repair
       - Consider transitioning to refrigerants with lower global warming potential
    
    #### Scope 2 Reduction Strategies
    
    1. **Energy Conservation**
       - Energy-efficient lighting (LED)
       - Optimized HVAC systems
       - Energy-efficient office equipment
    
    2. **Renewable Energy**
       - On-site renewable energy generation (solar panels)
       - Purchase of renewable energy credits (RECs)
       - Green power purchasing agreements
    
    #### Scope 3 Reduction Strategies
    
    1. **Business Travel**
       - Implement a sustainable travel policy
       - Utilize virtual meeting technologies
       - Consider carbon offsetting for necessary travel
    
    2. **Employee Commuting**
       - Encourage carpooling and public transportation
       - Implement a work-from-home policy where possible
       - Provide incentives for low-carbon commuting
    
    3. **Waste Management**
       - Implement a comprehensive recycling program
       - Reduce paper usage through digitalization
       - Composting organic waste
    
    4. **Supply Chain**
       - Engage with suppliers on emissions reduction
       - Prioritize suppliers with strong environmental commitments
       - Consider local sourcing to reduce transportation emissions
    """)

# Download options
st.header("Download Report")

report_format = st.radio("Select Report Format", ["PDF", "Excel"])

# Additional report configuration for PDF
# Default values
include_charts = True
include_methodology = True
include_recommendations = True

if report_format == "PDF":
    include_charts = st.checkbox("Include Charts", value=True)
    include_methodology = st.checkbox("Include Methodology Section", value=True)
    include_recommendations = st.checkbox("Include Recommendations Section", value=True)

# Generate and download report
if st.button("Generate and Download Report"):
    try:
        with st.spinner("Generating report..."):
            if report_format == "PDF":
                # Generate PDF report
                pdf_bytes = generate_pdf_report(
                    organization_name=organization_name,
                    report_year=report_year,
                    prepared_by=prepared_by,
                    report_date=report_date,
                    include_charts=include_charts,
                    include_methodology=include_methodology,
                    include_recommendations=include_recommendations
                )
                
                # Create download link
                b64_pdf = base64.b64encode(pdf_bytes).decode()
                href = f'<a href="data:application/pdf;base64,{b64_pdf}" download="Emission_Baseline_Report_{organization_name}_{report_year}.pdf">Download PDF Report</a>'
                st.markdown(href, unsafe_allow_html=True)
                
                # Save report metadata to database
                if 'current_record_id' in st.session_state:
                    emission_data_id = st.session_state.current_record_id
                    report_name = f"Emission_Baseline_Report_{organization_name}_{report_year}.pdf"
                    report_type = "pdf"
                    report_content = f"PDF report generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}. Includes: {'charts' if include_charts else 'no charts'}, {'methodology' if include_methodology else 'no methodology'}, {'recommendations' if include_recommendations else 'no recommendations'}"
                    
                    # Save report metadata to database
                    try:
                        report_id = save_report(
                            emission_data_id=emission_data_id,
                            report_name=report_name,
                            report_type=report_type,
                            organization_name=organization_name,
                            report_year=report_year,
                            prepared_by=prepared_by,
                            report_date=report_date,
                            report_content=report_content
                        )
                        st.success(f"Report metadata saved to database (ID: {report_id})")
                    except Exception as e:
                        st.warning(f"Report generated but metadata could not be saved to database: {str(e)}")
                
            else:  # Excel
                # Generate Excel report
                excel_bytes = generate_excel_report(
                    organization_name=organization_name,
                    report_year=report_year,
                    prepared_by=prepared_by,
                    report_date=report_date
                )
                
                # Create download link
                b64_excel = base64.b64encode(excel_bytes).decode()
                href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64_excel}" download="Emission_Baseline_Report_{organization_name}_{report_year}.xlsx">Download Excel Report</a>'
                st.markdown(href, unsafe_allow_html=True)
                
                # Save report metadata to database
                if 'current_record_id' in st.session_state:
                    emission_data_id = st.session_state.current_record_id
                    report_name = f"Emission_Baseline_Report_{organization_name}_{report_year}.xlsx"
                    report_type = "excel"
                    report_content = f"Excel report generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                    
                    # Save report metadata to database
                    try:
                        report_id = save_report(
                            emission_data_id=emission_data_id,
                            report_name=report_name,
                            report_type=report_type,
                            organization_name=organization_name,
                            report_year=report_year,
                            prepared_by=prepared_by,
                            report_date=report_date,
                            report_content=report_content
                        )
                        st.success(f"Report metadata saved to database (ID: {report_id})")
                    except Exception as e:
                        st.warning(f"Report generated but metadata could not be saved to database: {str(e)}")
            
            st.success("Report generated successfully!")
    except Exception as e:
        st.error(f"An error occurred while generating the report: {str(e)}")

# Navigation buttons
st.markdown("## Navigation")
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("⬅️ Return to Dashboard"):
        st.switch_page("pages/2_Dashboard.py")
with col2:
    if st.button("📊 View Saved Reports"):
        st.switch_page("pages/4_Saved_Reports.py")
with col3:
    if st.button("🏠 Go to Home"):
        st.switch_page("app.py")

# Help section
with st.expander("Need Help?"):
    st.markdown("""
    ### Report Download Instructions
    
    1. Fill in the report configuration details (Organization Name, Reporting Year, etc.)
    2. Select your preferred report format (PDF or Excel)
    3. If you selected PDF, choose which sections to include
    4. Click the "Generate and Download Report" button
    5. Click the download link that appears after the report is generated
    
    The report will contain all the emissions data you entered, along with calculations, charts, and recommendations based on your emissions profile.
    """)
