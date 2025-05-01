import streamlit as st
import pandas as pd
import time
from datetime import datetime
from utils.data_manager import init_session_state

# Initialize session state
init_session_state()

# Add Carbon Aegis branding
col1, col2 = st.columns([1, 5])
with col1:
    st.image("assets/logo.png", width=100)
with col2:
    st.title("Carbon Aegis - Terra: ESG AI Assistant")

st.markdown("""
Meet Terra, your AI assistant for ESG and sustainability guidance. Terra can help answer your questions about
emissions reduction strategies, sustainability reporting, and ESG best practices tailored to your organization's profile.
""")

# Initialize chat session variables
if 'terra_chat_initialized' not in st.session_state:
    st.session_state.terra_chat_initialized = False
if 'terra_messages' not in st.session_state:
    st.session_state.terra_messages = []
if 'terra_onboarding_complete' not in st.session_state:
    st.session_state.terra_onboarding_complete = False
if 'terra_context' not in st.session_state:
    # Store user context for personalized responses
    st.session_state.terra_context = {
        'industry': '',
        'size': '',
        'goals': [],
        'challenges': [],
        'priorities': ''
    }

# Onboarding process
if not st.session_state.terra_onboarding_complete:
    st.subheader("First, let's get to know your organization")
    st.markdown("This helps Terra provide more relevant and tailored guidance to your specific needs.")
    
    with st.form("terra_onboarding_form"):
        # Get organization profile
        if not st.session_state.terra_context['industry']:
            industry = st.selectbox(
                "What industry is your organization in?",
                options=[
                    "Manufacturing", "Retail", "Financial Services", "Technology", 
                    "Healthcare", "Energy", "Transportation", "Construction", 
                    "Agriculture", "Education", "Hospitality", "Professional Services",
                    "Public Sector", "Other"
                ],
                index=0
            )
        else:
            industry = st.session_state.terra_context['industry']
        
        size = st.radio(
            "What is the size of your organization?",
            options=["Small (< 50 employees)", "Medium (50-250 employees)", "Large (250+ employees)"],
            index=1
        )
        
        goals = st.multiselect(
            "What are your primary sustainability goals? (Select up to 3)",
            options=[
                "Reduce carbon emissions", "Comply with regulations", 
                "Improve ESG ratings", "Attract sustainable investment",
                "Enhance brand reputation", "Reduce costs", 
                "Prepare for climate risks", "Support sustainable development goals"
            ],
            default=["Reduce carbon emissions", "Comply with regulations"]
        )
        
        challenges = st.multiselect(
            "What are your biggest ESG challenges? (Select up to 3)",
            options=[
                "Data collection and management", "Budget constraints", 
                "Lack of expertise", "Measuring ROI of sustainability initiatives",
                "Engaging employees", "Supply chain transparency", 
                "Setting appropriate targets", "Reporting and disclosure requirements"
            ],
            default=["Data collection and management"]
        )
        
        priorities = st.select_slider(
            "What's your current priority?",
            options=["Understanding basics", "Planning initiatives", "Implementing programs", "Advanced optimization"],
            value="Planning initiatives"
        )
        
        submit_onboarding = st.form_submit_button("Start Chatting with Terra", use_container_width=True)
        
        if submit_onboarding:
            # Save context
            st.session_state.terra_context['industry'] = industry
            st.session_state.terra_context['size'] = size
            st.session_state.terra_context['goals'] = goals
            st.session_state.terra_context['challenges'] = challenges
            st.session_state.terra_context['priorities'] = priorities
            
            # Mark onboarding complete
            st.session_state.terra_onboarding_complete = True
            
            # Add welcome message
            welcome_message = f"""
            Thanks for sharing your profile! I'm Terra, your ESG AI assistant.
            
            Based on your information:
            * You're in the **{industry}** industry
            * You're a **{size}** organization
            * Your main goals are **{', '.join(goals)}**
            * Your biggest challenges are **{', '.join(challenges)}**
            * Your current priority is **{priorities}**
            
            I'll tailor my guidance accordingly. What ESG or sustainability question can I help you with today?
            """
            
            st.session_state.terra_messages.append({"role": "assistant", "content": welcome_message, "time": datetime.now().strftime("%H:%M")})
            st.rerun()

# Display chat interface once onboarding is complete
if st.session_state.terra_onboarding_complete:
    # Display chat history
    chat_container = st.container(height=400, border=False)
    with chat_container:
        for message in st.session_state.terra_messages:
            if message["role"] == "user":
                with st.chat_message("user"):
                    st.write(f"{message['content']}")
                    st.caption(f"{message['time']}")
            else:
                with st.chat_message("assistant", avatar="🌍"):
                    st.write(f"{message['content']}")
                    st.caption(f"{message['time']}")
    
    # Chat input
    user_input = st.chat_input("Ask Terra about ESG and sustainability...")
    
    if user_input:
        # Add user message to chat history
        st.session_state.terra_messages.append({"role": "user", "content": user_input, "time": datetime.now().strftime("%H:%M")})
        
        # For demo purposes, create predefined responses based on keywords
        # In a real implementation, this would call an actual AI model
        
        # Simulate typing indicator
        with st.chat_message("assistant", avatar="🌍"):
            message_placeholder = st.empty()
            message_placeholder.markdown("⏳ Thinking...")
            
            # Generate response based on user query
            response = generate_terra_response(user_input, st.session_state.terra_context)
            
            # Simulate typing
            full_response = ""
            for chunk in response.split():
                full_response += chunk + " "
                time.sleep(0.05)
                message_placeholder.markdown(full_response + "▌")
            
            message_placeholder.markdown(response)
            st.caption(f"{datetime.now().strftime('%H:%M')}")
        
        # Add assistant response to chat history
        st.session_state.terra_messages.append({"role": "assistant", "content": response, "time": datetime.now().strftime("%H:%M")})
        
        # Rerun to update UI
        st.rerun()

# Function to generate Terra's responses
def generate_terra_response(query, context):
    """
    Generate response based on user query and context.
    In a real implementation, this would call an external AI API.
    """
    query_lower = query.lower()
    industry = context['industry']
    size = context['size']
    
    # Check for emission reduction questions
    if any(keyword in query_lower for keyword in ["reduce emissions", "reduce carbon", "lower emissions", "scope 1", "scope 2", "scope 3"]):
        if "scope 1" in query_lower:
            return f"""
            ### Scope 1 Emission Reduction Strategies for {industry}
            
            Based on your organization profile as a {size} {industry} company, here are tailored recommendations for reducing Scope 1 (direct) emissions:
            
            1. **Energy Efficiency Upgrades**: Implement energy-efficient equipment and processes in your facilities
            2. **Fuel Switching**: Transition from high-carbon fuels to lower-carbon alternatives where possible
            3. **Renewable Energy**: Consider on-site renewable energy generation like solar panels
            4. **Fleet Optimization**: If you operate vehicles, consider electric or hybrid alternatives
            5. **Refrigerant Management**: Implement leak detection and prevention systems
            
            Would you like me to elaborate on any of these strategies or calculate potential emission reductions?
            """
        
        elif "scope 2" in query_lower:
            return f"""
            ### Scope 2 Emission Reduction Strategies for {industry}
            
            Based on your organization profile as a {size} {industry} company, here are tailored recommendations for reducing Scope 2 (indirect energy) emissions:
            
            1. **Renewable Energy Procurement**: Purchase renewable energy through Power Purchase Agreements (PPAs)
            2. **Green Tariffs**: Opt for green electricity tariffs from your utility provider
            3. **Renewable Energy Certificates (RECs)**: Purchase RECs to offset your electricity consumption
            4. **Energy Efficiency**: Implement building management systems and energy-efficient lighting
            5. **Load Shifting**: Shift energy-intensive activities to times when grid electricity is cleaner
            
            Would you like specific guidance on implementing any of these strategies given your current priorities?
            """
        
        elif "scope 3" in query_lower:
            return f"""
            ### Scope 3 Emission Reduction Strategies for {industry}
            
            Based on your organization profile as a {size} {industry} company, here are tailored recommendations for reducing Scope 3 (value chain) emissions:
            
            1. **Supplier Engagement**: Work with suppliers to reduce their emissions
            2. **Sustainable Procurement**: Update procurement policies to favor low-carbon products and services
            3. **Product Design**: Design products for circularity and reduced lifecycle emissions
            4. **Logistics Optimization**: Optimize shipping routes and modes of transportation
            5. **Employee Commuting**: Implement work-from-home policies or encourage public transportation
            
            Scope 3 emissions often represent the largest portion of an organization's carbon footprint but also the most challenging to address. Would you like a more detailed strategy for a specific Scope 3 category?
            """
        
        else:
            return f"""
            ### Comprehensive Emission Reduction Strategy for {industry}
            
            Based on your organization profile as a {size} {industry} company, here's a tailored approach to reduce your overall emissions:
            
            **Quick Wins (0-6 months):**
            * Conduct an energy audit to identify efficiency opportunities
            * Implement LED lighting and smart thermostats
            * Optimize equipment operating schedules
            
            **Medium-Term Actions (6-18 months):**
            * Develop a renewable energy procurement strategy
            * Engage top suppliers on their emission reduction plans
            * Set science-based reduction targets
            
            **Long-Term Initiatives (18+ months):**
            * Invest in on-site renewable energy generation
            * Electrify your vehicle fleet and heating systems
            * Develop low-carbon products and services
            
            I recommend starting with a comprehensive carbon footprint assessment using the Carbon Aegis emissions calculator to identify your highest impact areas. Would you like help with that?
            """
    
    # Check for reporting framework questions
    elif any(keyword in query_lower for keyword in ["reporting", "framework", "disclosure", "gri", "tcfd", "csrd", "esrs"]):
        return f"""
        ### ESG Reporting Guidance for {industry}
        
        Based on your organization profile as a {size} {industry} company, these reporting frameworks are most relevant:
        
        1. **Primary Frameworks to Consider:**
            * {'CSRD and ESRS' if 'Large' in size else 'GRI Standards'} - Comprehensive sustainability reporting
            * {'TCFD' if industry in ['Financial Services', 'Energy', 'Manufacturing'] else 'CDP'} - Climate-specific disclosures
        
        2. **Reporting Best Practices:**
            * Start with a materiality assessment to identify key topics
            * Focus on quality over quantity in your first reports
            * Ensure data reliability through proper documentation
            * Align reporting cycles with financial reporting when possible
        
        You can use Carbon Aegis's Framework Finder for a more detailed assessment of which frameworks apply to your specific situation. Would you like me to explain any particular framework in more detail?
        """
    
    # Check for sustainable finance questions
    elif any(keyword in query_lower for keyword in ["finance", "investment", "fund", "capital", "green bond", "sustainable finance", "esg investment"]):
        return f"""
        ### Sustainable Finance Opportunities for {industry}
        
        Based on your organization profile as a {size} {industry} company, here are relevant sustainable finance options:
        
        1. **Funding Mechanisms:**
            * {'Green Bonds or Sustainability-Linked Loans' if 'Large' in size else 'Green Loans and Sustainability-Linked Credit Lines'} 
            * Carbon Credits from emission reduction projects
            * {'ESG-linked Supply Chain Finance' if industry in ['Manufacturing', 'Retail'] else 'Energy Efficiency Incentives and Rebates'}
        
        2. **Investor Considerations:**
            * ESG performance increasingly impacts cost of capital
            * Strong sustainability governance attracts long-term investors
            * Climate risk disclosure becoming standard due diligence
        
        3. **Next Steps:**
            * Develop robust ESG data for investor communications
            * Identify specific green/sustainable projects for targeted funding
            * Engage with financial partners about sustainability-linked products
        
        Would you like me to elaborate on any specific financial instrument or how to prepare for ESG-focused investor engagement?
        """
    
    # Check for employee engagement questions
    elif any(keyword in query_lower for keyword in ["employee", "engagement", "staff", "culture", "awareness", "training"]):
        return f"""
        ### Employee Engagement Strategies for Sustainability
        
        Based on your organization profile as a {size} {industry} company, here are effective approaches to engage employees in sustainability:
        
        1. **Engagement Programs:**
            * Green Teams: Cross-functional groups focused on sustainability initiatives
            * Sustainability Challenges: Friendly competitions to reduce impacts
            * Volunteer Days: Community environmental service opportunities
        
        2. **Communication Approaches:**
            * Regular sustainability newsletters with metrics and achievements
            * Executive messaging connecting sustainability to business strategy
            * Recognition programs for sustainability innovations and contributions
        
        3. **Training Opportunities:**
            * Role-specific sustainability training (how each function contributes)
            * Carbon literacy training for all employees
            * Green skills development in relevant areas
        
        Remember that employee engagement is crucial for embedding sustainability across operations. Would you like specific suggestions for launching any of these programs?
        """
    
    # Check for data collection questions
    elif any(keyword in query_lower for keyword in ["data", "collection", "measurement", "tracking", "monitor", "metric"]):
        return f"""
        ### ESG Data Collection Best Practices for {industry}
        
        Based on your organization profile as a {size} {industry} company, here's guidance on effective ESG data management:
        
        1. **Data Collection Strategy:**
            * Start with high-impact, high-confidence metrics (energy, water, waste)
            * Define clear boundaries and calculation methodologies
            * Establish regular collection frequencies aligned with business cycles
        
        2. **Technology Solutions:**
            * {'Enterprise ESG software platforms' if 'Large' in size else 'Carbon Aegis and similar dedicated tools'}
            * {'Automated data collection from utility providers and IoT devices' if industry in ['Manufacturing', 'Energy'] else 'Structured spreadsheet templates for consistent tracking'}
            * Carbon calculator tools for emissions conversion factors
        
        3. **Data Governance:**
            * Clear roles and responsibilities for data owners
            * Documented methodology and assumptions
            * Internal verification processes before disclosure
        
        4. **Common Challenges and Solutions:**
            * Data gaps: Use industry benchmarks as interim estimates
            * Quality concerns: Implement validation checks
            * Supplier data: Start with largest suppliers and phase in requirements
        
        Would you like specific guidance on collecting data for any particular ESG metric?
        """
    
    # Default response if no specific topic is matched
    else:
        return f"""
        Thanks for your question about "{query}". 
        
        As your ESG assistant, I can help with various sustainability topics including:
        
        * Carbon emissions reduction strategies
        * ESG reporting frameworks and requirements
        * Sustainable finance opportunities
        * Employee engagement for sustainability
        * ESG data collection and management
        * Industry-specific sustainability practices
        * Regulatory compliance guidance
        
        Could you provide a bit more detail about what specific aspect of {query} you'd like to know about? For example, are you looking for implementation steps, best practices, or case studies?
        """

# Add additional features in the sidebar
with st.sidebar:
    st.subheader("Terra Settings")
    
    # Allow modifying organization context
    if st.button("Update Organization Profile"):
        st.session_state.terra_onboarding_complete = False
        st.rerun()
    
    # Clear chat history
    if st.button("Clear Chat History"):
        st.session_state.terra_messages = []
        # Add welcome message back
        welcome_message = f"""
        Hi there! I'm Terra, your ESG AI assistant. How can I help you with your sustainability initiatives today?
        """
        st.session_state.terra_messages.append({"role": "assistant", "content": welcome_message, "time": datetime.now().strftime("%H:%M")})
        st.rerun()
    
    # Example queries
    st.subheader("Example Questions")
    example_queries = [
        "How can we reduce our Scope 1 emissions?",
        "Which reporting frameworks apply to our company?",
        "What are the best strategies for employee sustainability engagement?",
        "How should we approach ESG data collection?",
        "What sustainable finance options are available to us?"
    ]
    
    for query in example_queries:
        if st.button(query, key=f"example_{query}"):
            # Clear input and add example as user message
            st.session_state.terra_messages.append({"role": "user", "content": query, "time": datetime.now().strftime("%H:%M")})
            
            # Generate and add response
            response = generate_terra_response(query, st.session_state.terra_context)
            st.session_state.terra_messages.append({"role": "assistant", "content": response, "time": datetime.now().strftime("%H:%M")})
            
            st.rerun()

# Add navigation
st.markdown("---")
col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    if st.button("📊 ESG Dashboard", use_container_width=True):
        st.switch_page("pages/6_ESG_Dashboard.py")
with col2:
    if st.button("👥 Team Workspace", use_container_width=True):
        st.switch_page("pages/8_Team_Workspace.py")
with col3:
    if st.button("🏠 Home", use_container_width=True):
        st.switch_page("app.py")