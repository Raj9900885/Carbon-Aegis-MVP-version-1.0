import streamlit as st
import pandas as pd
from datetime import datetime
from utils.data_manager import init_session_state, get_saved_calculations, load_emission_data

# Page configuration
st.set_page_config(
    page_title="Carbon Aegis - Emission Calculator",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state variables
init_session_state()

# Add organization profile info to session state if not exists
if 'organization_name' not in st.session_state:
    st.session_state.organization_name = ""
if 'report_year' not in st.session_state:
    st.session_state.report_year = datetime.now().year

# Main page content
def main():
    # Header with simple styling
    col1, col2 = st.columns([1, 5])
    with col1:
        st.image("assets/logo.png", width=120)
    with col2:
        st.title("Carbon Aegis")
        st.markdown("<h3 style='color: #2E8B57; margin-top: -10px;'>Enterprise Carbon Management Platform</h3>", 
                   unsafe_allow_html=True)
    
    # Introduction section with native Streamlit components
    st.markdown("## Welcome to the Carbon Aegis Platform")
    st.write("""
    This advanced tool helps organizations accurately measure, track, and report 
    greenhouse gas emissions across all scopes according to the GHG Protocol standards.
    Our enterprise-grade solution provides detailed insights to support your sustainability goals.
    """)
    
    # Feature cards using native Streamlit components
    st.subheader("Key Features")
    
    # Create a 2x3 grid of feature cards using columns
    col1, col2, col3 = st.columns(3)
    
    with col1:
        with st.container():
            st.markdown("#### 📊 Input Data")
            st.markdown("Enter activity data by emission scope")
            
    with col2:
        with st.container():
            st.markdown("#### 📈 Dashboard")
            st.markdown("Analyze with interactive visualizations")
            
    with col3:
        with st.container():
            st.markdown("#### 📝 Reports")
            st.markdown("Generate comprehensive PDF/Excel reports")
            
    col4, col5, col6 = st.columns(3)
    
    with col4:
        with st.container():
            st.markdown("#### 🗄️ History")
            st.markdown("Access previously saved calculations")
            
    with col5:
        with st.container():
            st.markdown("#### 🤖 AI Assistant")
            st.markdown("Get ESG guidance from Terra AI")
            
    with col6:
        with st.container():
            st.markdown("#### 📡 IoT Integration")
            st.markdown("Connect devices for real-time monitoring")
    
    # Organization Profile with native Streamlit components
    st.markdown("### 🏢 Organization Profile")
    
    # Create a container with a light green background
    with st.container():
        # Add some space before content
        st.markdown("")
        
        col1, col2 = st.columns(2)
        with col1:
            organization_name = st.text_input("Organization Name", 
                                             value=st.session_state.organization_name,
                                             key="profile_org_name",
                                             help="Enter your organization's name for inclusion in reports")
            if organization_name != st.session_state.organization_name:
                st.session_state.organization_name = organization_name
        
        with col2:
            report_year = st.number_input("Reporting Year", 
                                         min_value=2000, max_value=2100,
                                         value=st.session_state.report_year,
                                         key="profile_report_year",
                                         help="Select the reporting year for your emissions data")
            if report_year != st.session_state.report_year:
                st.session_state.report_year = report_year
        
        # Add some space after content
        st.markdown("")
    
    # Load Saved Calculations with native Streamlit components
    st.markdown("### 📂 Load Saved Calculations")
    
    # Add simple container
    with st.container():
        # Add some space
        st.markdown("")
        
        st.write("Select a previously saved calculation to load:")
        
        # Get saved calculations from database
        saved_records = get_saved_calculations()
        
        if saved_records:
            # Format the data for display
            record_options = []
            for record in saved_records:
                org_name = record.get('organization_name', 'Unknown')
                year = record.get('report_year', 'N/A')
                
                # Handle different date formats
                created_at = record.get('created_at', datetime.now())
                if isinstance(created_at, str):
                    date = created_at
                else:
                    date = created_at.strftime('%Y-%m-%d %H:%M')
                    
                total = record.get('total_emissions', 0.0)
                
                display_text = f"{org_name} ({year}) - {date} - {total:.2f} tCO₂e"
                record_options.append({"id": record.get('id'), "display": display_text})
            
            # Create a selectbox for the records
            col1, col2 = st.columns([3, 1])
            
            with col1:
                selected_option = st.selectbox(
                    "Saved Records",
                    options=[{"id": 0, "display": "Select a record..."}] + record_options,
                    format_func=lambda x: x["display"],
                    key="saved_record_selector"
                )
            
            with col2:
                if selected_option["id"] != 0:
                    if st.button("📥 Load Record", key="load_record_btn", use_container_width=True):
                        record_id = selected_option["id"]
                        success = load_emission_data(record_id)
                        if success:
                            st.success(f"Successfully loaded record #{record_id}")
                            st.rerun()
            
            # Add navigation buttons for saved reports
            st.markdown("---")
            if st.button("📁 View All Saved Reports", use_container_width=True):
                st.switch_page("pages/4_Saved_Reports.py")
                
        else:
            st.info("No saved calculations found.")
            
            # Add buttons for key features
            col1, col2 = st.columns(2)
            with col1:
                if st.button("➕ Create New Calculation", use_container_width=True):
                    st.switch_page("pages/1_Data_Input.py")
            with col2:
                if st.button("📡 IoT Integration", use_container_width=True):
                    st.switch_page("pages/11_IoT_Integration.py")
        
        # Add some space
        st.markdown("")
    
    # Quick overview if data exists
    if 'has_data' in st.session_state and st.session_state.has_data:
        st.success("You have already entered some data. View your results in the Dashboard or continue adding data.")
        
        # Display organization info if available
        if st.session_state.organization_name:
            st.write(f"**Organization**: {st.session_state.organization_name}")
            st.write(f"**Reporting Year**: {st.session_state.report_year}")
        
        # Quick summary
        if 'total_emissions' in st.session_state:
            st.metric("Total Carbon Emissions (tCO₂e)", f"{st.session_state.total_emissions:.2f}")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                if 'scope1_total' in st.session_state:
                    st.metric("Direct Emissions (tCO₂e)", f"{st.session_state.scope1_total:.2f}")
            with col2:
                if 'scope2_total' in st.session_state:
                    st.metric("Energy Indirect (tCO₂e)", f"{st.session_state.scope2_total:.2f}")
            with col3:
                if 'scope3_total' in st.session_state:
                    st.metric("Other Indirect (tCO₂e)", f"{st.session_state.scope3_total:.2f}")

    else:
        st.info("No data has been entered yet. Please navigate to the Data Input page to begin.")
    
    # Add complete navigation section
    st.markdown("---")
    st.subheader("Navigation")
    
    # Core Features
    st.markdown("#### Core Features")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("📊 Data Input", key="nav_data_input", use_container_width=True):
            st.switch_page("pages/1_Data_Input.py")
    with col2:
        if st.button("📈 Dashboard", key="nav_dashboard", use_container_width=True):
            st.switch_page("pages/2_Dashboard.py")
    with col3:
        if st.button("📝 Reports", key="nav_reports", use_container_width=True):
            st.switch_page("pages/3_Report.py")
    with col4:
        if st.button("📁 Saved Reports", key="nav_saved", use_container_width=True):
            st.switch_page("pages/4_Saved_Reports.py")
    
    # ESG Tools
    st.markdown("#### ESG Tools")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("📏 Framework Finder", key="nav_frameworks", use_container_width=True):
            st.switch_page("pages/5_Framework_Finder.py")
    with col2:
        if st.button("🎯 ESG Dashboard", key="nav_esg", use_container_width=True):
            st.switch_page("pages/6_ESG_Dashboard.py")
    with col3:
        if st.button("📊 ESG Readiness", key="nav_readiness", use_container_width=True):
            st.switch_page("pages/7_ESG_Readiness.py")
    with col4:
        if st.button("👥 Team Workspace", key="nav_team", use_container_width=True):
            st.switch_page("pages/8_Team_Workspace.py")
    
    # Advanced Features
    st.markdown("#### Advanced Features")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🤖 AI Assistant", key="nav_ai", use_container_width=True):
            st.switch_page("pages/9_AI_Assistant.py")
    with col2:
        if st.button("📋 Survey Dispatch", key="nav_survey", use_container_width=True):
            st.switch_page("pages/10_Survey_Dispatch.py")
    with col3:
        if st.button("📡 IoT Integration", key="nav_iot", use_container_width=True):
            st.switch_page("pages/11_IoT_Integration.py")

if __name__ == "__main__":
    main()
