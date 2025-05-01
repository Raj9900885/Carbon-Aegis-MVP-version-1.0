import streamlit as st
import pandas as pd
from datetime import datetime
import os

# --- Page Config ---
st.set_page_config(
    page_title="Carbon Aegis",
    page_icon="🌍",
    layout="wide"
)

# --- Header ---
col1, col2 = st.columns([1, 10])
with col1:
    st.image("assets/logo.png", width=60)
with col2:
    st.markdown("## **Carbon Aegis**")
    st.markdown("### _Enterprise Carbon Management Platform_")

st.markdown("---")

# --- Welcome Message ---
st.markdown("""
Welcome to the Carbon Aegis Platform — a powerful tool designed to help your organization track, report, and reduce greenhouse gas emissions in alignment with GHG Protocol and EU standards like CSRD and VSME.

Use the navigation sidebar to get started or select a key module below:
""")

# --- Feature Cards ---
st.markdown("### 🔧 Key Features")

fcol1, fcol2 = st.columns(2)

with fcol1:
    st.markdown("#### 📊 **Input Data**")
    st.markdown("Enter activity data by emission scope")
    st.markdown("#### 📈 **Dashboard**")
    st.markdown("Visualize emissions breakdown")

with fcol2:
    st.markdown("#### 📝 **Reports**")
    st.markdown("Download emissions summaries as PDF or Excel")
    st.markdown("#### 🤖 **AI Assistant**")
    st.markdown("Ask Terra ESG questions or get reporting help")

st.markdown("---")

# --- Org Info (Optional Collapse) ---
with st.expander("📁 Organization Profile", expanded=False):
    org_name = st.text_input("Organization Name", placeholder="e.g., Carbon Aegis GmbH")
    report_year = st.number_input("Reporting Year", value=datetime.now().year)

# --- Simulated Save Button (CSV fallback) ---
if st.button("💾 Save Session Data"):
    data = {
        "organization_name": org_name,
        "report_year": report_year,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    df = pd.DataFrame([data])
    df.to_csv("session_data.csv", mode='a', index=False, header=not Path("session_data.csv").exists())
    st.success("✅ Data saved locally to session_data.csv")