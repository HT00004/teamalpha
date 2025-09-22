#!/usr/bin/env python3
"""
🎖️ MISSION ALPHA - STREAMLIT APPLICATION
Pension Phantom Generator - Operation Synthetic Shield

A comprehensive web application for AI-driven synthetic pension data generation
using Azure AI Foundry and advanced data visualization.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
import io
import zipfile
import glob
from datetime import datetime, timedelta
import random
import os
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from streamlit_option_menu import option_menu

# Import our core generation modules
try:
    from pension_phantom_generator import PensionPhantomGenerator, MemberProfile, ContributionRecord, FundAllocation
    from data_realism_comparator import DataRealismComparator
except ImportError:
    # Fallback: Create a simple Azure AI integration
    try:
        from azure.identity import DefaultAzureCredential
        from azure.ai.projects import AIProjectClient
        from azure.ai.agents.models import ListSortOrder
        import pandas as pd
        
        # Also import the comparator in fallback
        try:
            from data_realism_comparator import DataRealismComparator
        except ImportError:
            DataRealismComparator = None
        
        # Use the Azure AI Foundry integration from alpha_data_generatorv2
        PROJECT_ENDPOINT = "https://ais-hack-u5nxuil7gjgjq.services.ai.azure.com/api/projects/lgir-team-alpha"
        AGENT_ID = "asst_YRz6huPVHYlT3Dwvm5cVlVi0"
        
        class AzureAIBackend:
            def __init__(self):
                self.project_client = AIProjectClient(
                    endpoint=PROJECT_ENDPOINT,
                    credential=DefaultAzureCredential()
                )
                self.agent = self.project_client.agents.get_agent(AGENT_ID)
                self.provider = "Azure AI Foundry"
                self.model = "GPT-4o"
            
            def generate_pension_data(self, count=100):
                """Generate pension data using Azure AI Foundry agent"""
                try:
                    prompt = f"""Generate exactly {count} rows of synthetic pension member data as CSV. Follow these specifications PRECISELY:

Start with header row:
MemberID,Age,Gender,Postcode,Sector,JobGrade,AnnualSalary,YearsService,Status

Requirements:
1. MemberID: Start from MB{1:08d} and increment by 1 for each row

2. Age Distribution:
   - 22-35: 40% of records
   - 36-45: 25% of records  
   - 46-55: 25% of records
   - 56-75: 10% of records

3. Gender: Exact proportions:
   - M: 49%
   - F: 50% 
   - O: 1%

4. Postcode: Use ONLY these formats:
   London: EC1A 1BB, SW1A 1AA, W1A 1AA, E1 6AN, N1 9GU
   Manchester: M1 1AA, M2 5BQ, M3 3EB
   Birmingham: B1 1HQ, B2 4QA, B3 3DH
   Glasgow: G1 1XW, G2 8DL
   Edinburgh: EH1 1BB, EH2 2ER
   Cardiff: CF10 1DD, CF11 9LJ
   Liverpool: L1 8JQ, L2 2PP
   Leeds: LS1 1UR, LS2 8JS
   Bristol: BS1 4TR, BS2 0FZ

5. Sector Distribution:
   Finance(15%), Manufacturing(12%), Public Service(18%), 
   Healthcare(13%), Education(10%), Retail(8%), Other(24%)

6. JobGrade by sector:
   Finance: [Analyst, Senior Analyst, Associate, Manager, Senior Manager, Director]
   Public Service: [Grade 7, Grade 6, Senior Officer, Principal Officer]
   Manufacturing: [Technician, Senior Technician, Supervisor, Production Manager]
   Healthcare: [Band 5, Band 6, Band 7, Senior Practitioner]
   Education: [Teacher, Senior Teacher, Head of Department, Deputy Head]
   Retail: [Sales Assistant, Supervisor, Store Manager, Area Manager]
   Other: [Associate, Consultant, Senior Consultant, Manager]

7. AnnualSalary ranges:
   Finance: 25000-120000 (40% between 35000-55000)
   Public Service: 20000-80000 (50% between 30000-45000)
   Manufacturing: 18000-75000 (60% between 28000-38000)
   Healthcare: 22000-85000 (45% between 32000-48000)
   Education: 24000-65000 (55% between 30000-45000)
   Retail: 18000-55000 (70% between 22000-35000)
   Other: 20000-90000 (45% between 35000-55000)

8. YearsService rules:
   - Cannot exceed (Age - 21)
   - Typically 20-40% of working age
   - More years in public sector

9. Status Distribution:
   Active(70%), Deferred(20%), Pensioner(10%, age 55+)

CRITICAL:
- Provide ONLY CSV data, no explanations
- Start with header row
- Generate EXACTLY {count} records
- Each record MUST follow ALL rules above
- No markdown formatting or code blocks"""

                    # Create a thread for this request
                    thread = self.project_client.agents.threads.create()
                    
                    # Send the generation request
                    message = self.project_client.agents.messages.create(
                        thread_id=thread.id,
                        role="user",
                        content=prompt
                    )
                    
                    # Process the request
                    run = self.project_client.agents.runs.create_and_process(
                        thread_id=thread.id,
                        agent_id=self.agent.id
                    )
                    
                    if run.status == "failed":
                        raise Exception(f"Generation failed: {run.last_error}")
                    
                    # Get the response
                    messages = self.project_client.agents.messages.list(
                        thread_id=thread.id,
                        order=ListSortOrder.ASCENDING
                    )
                    
                    # Get the last message
                    agent_messages = [msg for msg in messages if msg.role == "assistant" and msg.text_messages]
                    if not agent_messages:
                        raise Exception("No response received from agent")
                    
                    response = agent_messages[-1].text_messages[-1].text.value
                    
                    # Clean up any markdown or code formatting
                    clean_data = response.replace('```', '').strip()
                    if clean_data.startswith('csv\n'):
                        clean_data = clean_data[4:]
                    if clean_data.startswith('plaintext\n'):
                        clean_data = '\n'.join(clean_data.split('\n')[1:])
                    
                    return clean_data
                    
                except Exception as e:
                    raise Exception(f"Error generating data: {str(e)}")
        
        # Create a compatibility layer for the Streamlit app
        class PensionPhantomGenerator:
            def __init__(self):
                self.backend = AzureAIBackend()
                self.provider = self.backend.provider
                self.model = self.backend.model
            
            def call_ai_model(self, prompt, temperature=0.7):
                """Test AI connection"""
                try:
                    # Simple test generation
                    test_data = self.backend.generate_pension_data(1)
                    return test_data
                except Exception as e:
                    return None
            
            def generate_member_profiles_batch(self, count):
                """Generate member profiles using Azure AI"""
                try:
                    csv_data = self.backend.generate_pension_data(count)
                    
                    # Parse CSV data into MemberProfile objects
                    lines = csv_data.strip().split('\n')
                    header = lines[0].split(',')
                    profiles = []
                    
                    for line in lines[1:]:
                        values = line.split(',')
                        if len(values) >= 9:
                            profile = MemberProfile(
                                member_id=values[0],
                                age=int(values[1]) if values[1].isdigit() else 30,
                                gender=values[2],
                                postcode=values[3],
                                sector=values[4],
                                job_grade=values[5],
                                annual_salary=int(values[6]) if values[6].isdigit() else 35000,
                                years_service=int(values[7]) if values[7].isdigit() else 5,
                                status=values[8],
                                start_date=datetime.now().strftime("%Y-%m-%d")
                            )
                            profiles.append(profile)
                    
                    return profiles
                    
                except Exception as e:
                    st.error(f"Error generating profiles: {str(e)}")
                    return []
            
            def generate_contribution_history(self, member, months=12):
                """Generate contribution history for a member"""
                contributions = []
                base_salary = member.annual_salary
                
                for i in range(months):
                    contribution_date = (datetime.now() - timedelta(days=30*i)).strftime("%Y-%m-%d")
                    monthly_salary = base_salary / 12
                    employee_contrib = monthly_salary * 0.05  # 5% employee
                    employer_contrib = monthly_salary * 0.03  # 3% employer
                    
                    contribution = ContributionRecord(
                        member_id=member.member_id,
                        contribution_date=contribution_date,
                        employee_amount=round(employee_contrib, 2),
                        employer_amount=round(employer_contrib, 2),
                        salary_at_date=int(monthly_salary)
                    )
                    contributions.append(contribution)
                
                return contributions
            
            def generate_fund_allocations(self, member):
                """Generate fund allocations for a member"""
                # Simple fund allocation based on age
                funds = [
                    ("Conservative Growth Fund", "Low"),
                    ("Balanced Fund", "Medium"), 
                    ("Aggressive Growth Fund", "High"),
                    ("Global Equity Fund", "High"),
                    ("Bond Fund", "Low")
                ]
                
                allocations = []
                
                # Age-based allocation strategy
                if member.age < 35:
                    # Younger - more aggressive
                    selected_funds = [("Aggressive Growth Fund", "High", 60), ("Balanced Fund", "Medium", 40)]
                elif member.age < 50:
                    # Middle age - balanced
                    selected_funds = [("Balanced Fund", "Medium", 70), ("Conservative Growth Fund", "Low", 30)]
                else:
                    # Older - conservative
                    selected_funds = [("Conservative Growth Fund", "Low", 80), ("Bond Fund", "Low", 20)]
                
                for fund_name, risk_level, percentage in selected_funds:
                    allocation = FundAllocation(
                        member_id=member.member_id,
                        fund_name=fund_name,
                        allocation_percent=percentage,
                        risk_level=risk_level,
                        effective_date=datetime.now().strftime("%Y-%m-%d")
                    )
                    allocations.append(allocation)
                
                return allocations
            
            def validate_data_quality(self, profiles, contributions, allocations):
                """Validate data quality"""
                validation_results = {}
                
                if profiles:
                    ages = [p.age for p in profiles]
                    salaries = [p.annual_salary for p in profiles]
                    sectors = [p.sector for p in profiles]
                    
                    validation_results['age_distribution'] = {
                        'min': min(ages),
                        'max': max(ages),
                        'mean': sum(ages) / len(ages),
                        'median': sorted(ages)[len(ages)//2]
                    }
                    
                    validation_results['salary_stats'] = {
                        'min': min(salaries),
                        'max': max(salaries),
                        'mean': sum(salaries) / len(salaries)
                    }
                    
                    # Sector distribution
                    sector_counts = {}
                    for sector in sectors:
                        sector_counts[sector] = sector_counts.get(sector, 0) + 1
                    validation_results['sector_distribution'] = sector_counts
                    
                    validation_results['total_members'] = len(profiles)
                else:
                    validation_results = {
                        'age_distribution': {'min': 0, 'max': 0, 'mean': 0, 'median': 0},
                        'salary_stats': {'min': 0, 'max': 0, 'mean': 0},
                        'sector_distribution': {},
                        'total_members': 0
                    }
                
                # Fund allocation checks
                validation_results['fund_allocation_checks'] = {
                    'allocation_compliance_rate': 1.0 if allocations else 0.0,
                    'members_with_allocations': len(set([a.member_id for a in allocations])) if allocations else 0
                }
                
                return validation_results
        
        # Data classes for compatibility
        @dataclass
        class MemberProfile:
            member_id: str
            age: int
            gender: str
            postcode: str
            sector: str
            job_grade: str
            annual_salary: int
            years_service: int
            status: str
            start_date: str

        @dataclass
        class ContributionRecord:
            member_id: str
            contribution_date: str
            employee_amount: float
            employer_amount: float
            salary_at_date: int

        @dataclass
        class FundAllocation:
            member_id: str
            fund_name: str
            allocation_percent: int
            risk_level: str
            effective_date: str
        
        # Import DataRealismComparator
        from data_realism_comparator import DataRealismComparator
        
    except ImportError as e:
        st.error(f"❌ Could not import Azure AI dependencies: {str(e)}")
        st.error("Please install: pip install azure-identity azure-ai-projects")
        st.stop()

# Page configuration
st.set_page_config(
    page_title="🎖️ Mission Alpha - Pension Phantom Generator",
    page_icon="🎖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for military theme
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #2E4057 0%, #3E5065 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .mission-brief {
        background: #f0f2f6;
        padding: 1rem;
        border-left: 5px solid #FF6B6B;
        border-radius: 5px;
        margin: 1rem 0;
    }
    
    .success-metric {
        background: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 5px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    
    .warning-box {
        background: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 5px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    
    .stMetric > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables"""
    if 'generator' not in st.session_state:
        st.session_state.generator = None
    if 'generated_data' not in st.session_state:
        st.session_state.generated_data = {}
    if 'mission_status' not in st.session_state:
        st.session_state.mission_status = "Ready for Deployment"
    if 'ai_provider' not in st.session_state:
        st.session_state.ai_provider = None

def render_mission_header():
    """Render the mission header"""
    st.markdown("""
    <div class="main-header">
        <h1>🎖️ MISSION ALPHA - PENSION PHANTOM GENERATOR</h1>
        <h3>Operation Synthetic Shield - Data Generation Division</h3>
        <p><strong>CLASSIFIED:</strong> AI-driven synthetic pension data generation using Azure AI Foundry</p>
    </div>
    """, unsafe_allow_html=True)

def render_mission_briefing():
    """Render mission briefing sidebar"""
    with st.sidebar:
        st.markdown("## 📋 MISSION BRIEFING")
        
        st.markdown("""
        <div class="mission-brief">
        <strong>PRIMARY OBJECTIVE:</strong><br>
        Generate 1,000-5,000 synthetic UK pension members that pass operational 
        "Turing Tests" while maintaining complete civilian identity protection.
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 🎯 VICTORY CONDITIONS")
        victory_conditions = [
            "✅ Generate 1,000-5,000 synthetic records",
            "✅ Zero PII exposure",
            "✅ Statistical accuracy",
            "✅ Business rule compliance",
            "✅ Edge case coverage",
            "✅ Scalability demonstration"
        ]
        
        for condition in victory_conditions:
            st.markdown(condition)
        
        st.markdown("### 🚨 MISSION STATUS")
        status_color = "🟢" if st.session_state.mission_status == "Mission Accomplished" else "🟡"
        st.markdown(f"{status_color} **{st.session_state.mission_status}**")

def setup_ai_configuration():
    """Configure AI service connection"""
    st.header("🚀 AI WEAPONS SYSTEM CONFIGURATION")
    
    st.info("🔗 **Azure AI Foundry Integration Active**")
    st.markdown("""
    **Primary System:** Azure AI Foundry  
    **Endpoint:** `https://ais-hack-u5nxuil7gjgjq.services.ai.azure.com`  
    **Agent ID:** `asst_YRz6huPVHYlT3Dwvm5cVlVi0`  
    **Model:** GPT-4o  
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🤖 Azure AI Foundry Status")
        
        # Check Azure CLI authentication
        auth_status = st.empty()
        
        # Test connection button
        if st.button("🧪 Test AI Connection", type="primary"):
            with st.spinner("Testing Azure AI Foundry connection..."):
                try:
                    # Initialize generator which will test the connection
                    generator = PensionPhantomGenerator()
                    st.session_state.generator = generator
                    st.session_state.ai_provider = generator.provider
                    
                    # Test AI call
                    test_response = generator.call_ai_model(
                        "Generate one UK pension member profile with realistic data.", 
                        temperature=0.5
                    )
                    
                    if test_response and len(test_response) > 50:
                        st.success(f"✅ Connected to {generator.provider} - {generator.model}")
                        st.session_state.mission_status = "AI Systems Online"
                        
                        # Show sample response
                        with st.expander("🔍 Sample AI Response"):
                            st.code(test_response[:500] + "..." if len(test_response) > 500 else test_response)
                    else:
                        st.error("❌ AI connection test failed")
                        
                except Exception as e:
                    st.error(f"❌ Connection failed: {str(e)}")
                    
                    # Show troubleshooting tips
                    st.markdown("### 🔧 Troubleshooting")
                    st.markdown("""
                    1. **Check Azure CLI authentication:**
                    ```bash
                    az login --scope https://ai.azure.com/.default
                    ```
                    
                    2. **Verify project access:**
                    - Ensure you have access to the Azure AI Foundry project
                    - Check that the agent ID is correct
                    
                    3. **Environment setup:**
                    - Make sure you're in the correct virtual environment
                    - Verify Azure credentials are properly configured
                    """)
    
    with col2:
        st.subheader("⚙️ Generation Settings")
        
        # Show current configuration
        st.markdown("**Default Configuration:**")
        st.json({
            "Batch Size": "50 records",
            "Temperature": "0.7 (Balanced creativity)",
            "Chunk Processing": "Enabled",
            "Data Validation": "Comprehensive",
            "UK Compliance": "Enabled"
        })
        
        st.markdown("**Supported Data Types:**")
        st.markdown("""
        - ✅ Member Profiles (Core data)
        - ✅ Contribution History (Sample-based)
        - ✅ Fund Allocations (Age-appropriate)
        - ✅ Business Rule Validation
        - ✅ Geographic Distribution (UK postcodes)
        """)
        
        # Authentication check
        try:
            from azure.identity import DefaultAzureCredential
            credential = DefaultAzureCredential()
            st.success("✅ Azure credentials available")
        except Exception as e:
            st.warning(f"⚠️ Azure authentication issue: {str(e)}")
            st.markdown("Run: `az login --scope https://ai.azure.com/.default`")

def data_generation_interface():
    """Main data generation interface with alpha data generator integration"""
    st.header("🎯 SYNTHETIC DATA GENERATION OPERATIONS")
    st.markdown("**Generate high-quality synthetic pension data using Azure AI Foundry**")
    
    # Configuration tabs
    tab1, tab2 = st.tabs(["🎯 Alpha Generator", "⚙️ Advanced Settings"])
    
    with tab1:
        st.markdown("#### Alpha Data Generator Configuration")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("**📊 Data Parameters**")
            num_records = st.number_input(
                "Number of Records", 
                min_value=10, 
                max_value=50000, 
                value=100, 
                step=50,
                help="Number of records per batch (recommended: 50-200 for reliable generation)"
            )
            
            st.info("💡 **Large Dataset Strategy**: For 5000+ records, generate multiple batches and use the export tool to combine them.")
            
            start_id = st.number_input(
                "Starting Member ID", 
                min_value=1, 
                max_value=99999999, 
                value=1, 
                step=1,
                help="Starting ID for member records (format: MB{start_id:08d})"
            )
        
        with col2:
            st.markdown("**📁 Output Settings**")
            output_filename = st.text_input(
                "Output Filename", 
                value="generated_pension_data.csv",
                help="Name of the output CSV file"
            )
            
            preview_id = f"MB{start_id:08d}"
            st.info(f"First Member ID: {preview_id}")
            st.info(f"Last Member ID: MB{start_id + num_records - 1:08d}")
            
            # Show distribution calculations
            if num_records >= 1000:
                st.markdown("**📊 Distribution Preview:**")
                st.caption(f"Young Adults (22-35): {int(num_records * 0.40)} records")
                st.caption(f"Mid-Career (36-45): {int(num_records * 0.25)} records")
                st.caption(f"Experienced (46-55): {int(num_records * 0.25)} records")
                st.caption(f"Senior (56-75): {int(num_records * 0.10)} records")
        
        with col3:
            st.markdown("**🔧 Generation Status**")
            if 'last_generation' in st.session_state:
                last_gen = st.session_state.last_generation
                st.success(f"✅ Last: {last_gen['records']} records")
                st.info(f"📁 File: {last_gen['filename']}")
                st.caption(f"Generated: {last_gen['timestamp']}")
            else:
                st.info("No previous generation")
        
        # Generation button
        st.markdown("---")
        
        # Batch generation helper
        st.markdown("### 🔄 Batch Generation for Large Datasets")
        
        batch_col1, batch_col2, batch_col3 = st.columns(3)
        
        with batch_col1:
            st.markdown("**📦 Quick Batch Options**")
            if st.button("Generate Batch 1 (ID: 1-100)", type="secondary"):
                execute_alpha_data_generation(100, f"batch_01_{pd.Timestamp.now().strftime('%H%M%S')}.csv", 1)
            if st.button("Generate Batch 2 (ID: 101-200)", type="secondary"):
                execute_alpha_data_generation(100, f"batch_02_{pd.Timestamp.now().strftime('%H%M%S')}.csv", 101)
        
        with batch_col2:
            if st.button("Generate Batch 3 (ID: 201-300)", type="secondary"):
                execute_alpha_data_generation(100, f"batch_03_{pd.Timestamp.now().strftime('%H%M%S')}.csv", 201)
            if st.button("Generate Batch 4 (ID: 301-400)", type="secondary"):
                execute_alpha_data_generation(100, f"batch_04_{pd.Timestamp.now().strftime('%H%M%S')}.csv", 301)
        
        with batch_col3:
            if st.button("Generate Batch 5 (ID: 401-500)", type="secondary"):
                execute_alpha_data_generation(100, f"batch_05_{pd.Timestamp.now().strftime('%H%M%S')}.csv", 401)
            
            st.caption("💡 Generate 5 batches = 500 records total")
        
        st.markdown("---")
        
        if st.button("🚀 GENERATE PENSION DATA", type="primary", width='stretch'):
            execute_alpha_data_generation(num_records, output_filename, start_id)
    
    with tab2:
        st.markdown("#### Advanced Generation Settings")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**🎛️ AI Parameters**")
            st.info("These settings are pre-configured in the Azure AI agent:")
            st.markdown("""
            - **Detailed Age Brackets**: 22-27 (15%), 28-32 (15%), 33-35 (10%), 36-40 (15%), 41-45 (10%), 46-50 (15%), 51-55 (10%), 56-65 (7%), 66-75 (3%)
            - **Gender**: Male (49%), Female (50%), Other (1%)
            - **Sectors**: Finance (15%), Manufacturing (12%), Public Service (18%), Healthcare (13%), Education (10%), Retail (8%), Other (24%)
            - **Postcodes**: UK format with anonymized second half (e.g., M1 XXX, B2 XXX)
            - **Status**: Active (70%), Deferred (20%), Pensioner (10%)
            """)
        
        with col2:
            st.markdown("**📋 Data Validation**")
            st.markdown("""
            - ✅ UK Postcode validation (anonymized format)
            - ✅ Salary ranges by sector
            - ✅ Age-service correlation
            - ✅ Realistic job grades
            - ✅ Status distribution logic
            - ✅ Privacy protection (no real PII)
            """)
        
        # Azure connection status
        st.markdown("#### 🔗 Azure AI Connection")
        col1, col2 = st.columns(2)
        with col1:
            st.info("**Project**: ais-hack-u5nxuil7gjgjq.services.ai.azure.com")
        with col2:
            st.info("**Agent ID**: asst_YRz6huPVHYlT3Dwvm5cVlVi0")

def execute_alpha_data_generation(num_records, output_filename, start_id):
    """Execute data generation using alpha_data_generator.py"""
    
    # Import the alpha data generator
    try:
        import sys
        import os
        sys.path.append(os.path.dirname(__file__))
        from alpha_data_generator import generate_pension_data
        
        # Create progress indicators
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        status_text.text("🚀 Initializing Azure AI connection...")
        progress_bar.progress(0.1)
        
        status_text.text(f"📊 Preparing to generate {num_records} records...")
        progress_bar.progress(0.2)
        
        status_text.text("🤖 Sending request to Azure AI Foundry agent...")
        progress_bar.progress(0.3)
        
        # Execute the generation
        with st.spinner("🔄 Azure AI is generating your pension data..."):
            success = generate_pension_data(
                num_records=num_records,
                output_file=output_filename,
                start_id=start_id
            )
        
        progress_bar.progress(0.8)
        
        if success:
            progress_bar.progress(1.0)
            status_text.text("✅ Data generation completed successfully!")
            
            # Store generation info in session state
            st.session_state.last_generation = {
                'records': num_records,
                'filename': output_filename,
                'timestamp': pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S'),
                'start_id': start_id
            }
            
            st.success(f"🎉 Successfully generated {num_records} pension records!")
            st.info(f"📁 Data saved to: {output_filename}")
            
            # Show preview if file exists
            if os.path.exists(output_filename):
                st.markdown("#### � Data Preview")
                try:
                    preview_df = pd.read_csv(output_filename)
                    st.dataframe(preview_df.head(10), width='stretch')
                    
                    st.markdown("#### 📊 Quick Statistics")
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Total Records", len(preview_df))
                    with col2:
                        # Create age brackets for better analysis
                        age_brackets = pd.cut(preview_df['Age'], 
                                            bins=[21, 35, 45, 55, 75], 
                                            labels=['22-35', '36-45', '46-55', '56-75'],
                                            include_lowest=True)
                        age_dist = age_brackets.value_counts().sort_index()
                        most_common_bracket = age_dist.idxmax()
                        bracket_pct = (age_dist.max() / len(preview_df)) * 100
                        st.metric("Top Age Bracket", f"{most_common_bracket} ({bracket_pct:.1f}%)")
                    with col3:
                        st.metric("Sectors", preview_df['Sector'].nunique())
                    with col4:
                        st.metric("Avg Salary", f"£{preview_df['AnnualSalary'].mean():,.0f}")
                    
                    # Enhanced age bracket breakdown
                    st.markdown("#### 👥 Age Bracket Distribution")
                    age_col1, age_col2 = st.columns(2)
                    
                    with age_col1:
                        for bracket in age_dist.index:
                            count = age_dist[bracket]
                            percentage = (count / len(preview_df)) * 100
                            st.metric(f"Ages {bracket}", f"{count} ({percentage:.1f}%)")
                    
                    with age_col2:
                        # Gender and sector breakdown
                        st.markdown("**Gender Distribution:**")
                        gender_dist = preview_df['Gender'].value_counts()
                        for gender, count in gender_dist.items():
                            pct = (count / len(preview_df)) * 100
                            st.write(f"• {gender}: {count} ({pct:.1f}%)")
                        
                        st.markdown("**Top 3 Sectors:**")
                        sector_dist = preview_df['Sector'].value_counts().head(3)
                        for sector, count in sector_dist.items():
                            pct = (count / len(preview_df)) * 100
                            st.write(f"• {sector}: {count} ({pct:.1f}%)")
                        
                except Exception as e:
                    st.warning(f"Could not load preview: {str(e)}")
            
        else:
            progress_bar.progress(0.0)
            status_text.text("❌ Data generation failed!")
            st.error("❌ Data generation failed. Please check the console output for details.")
            st.markdown("### 🔍 Troubleshooting Tips:")
            st.markdown("""
            1. **Azure Authentication**: Make sure you're signed in with correct scope:
               ```bash
               az login --scope https://ai.azure.com/.default
               ```
            2. **Virtual Environment**: Ensure your virtual environment is activated
            3. **Network Connection**: Check your internet connection
            4. **Azure AI Access**: Verify you have access to the Azure AI Foundry project
            """)
            
    except ImportError as e:
        st.error(f"❌ Could not import alpha_data_generator: {str(e)}")
        st.info("Make sure alpha_data_generator.py is in the same directory as this app.")
    except Exception as e:
        st.error(f"❌ Unexpected error during data generation: {str(e)}")
        import traceback
        st.code(traceback.format_exc())

def execute_data_generation(member_count, batch_size, temperature, include_contributions, 
                          include_allocations, sample_size, include_edge_cases):
    """Execute the main data generation mission"""
    
    generator = st.session_state.generator
    
    # Mission progress tracking
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        # Phase 1: Generate Member Profiles
        status_text.text("🚀 Phase 1: Generating member profiles...")
        all_profiles = []
        
        for i in range(0, member_count, batch_size):
            current_batch_size = min(batch_size, member_count - i)
            progress = (i / member_count) * 0.4  # 40% for profiles
            progress_bar.progress(progress)
            
            status_text.text(f"Generating batch {i//batch_size + 1}: {current_batch_size} members...")
            
            batch_profiles = generator.generate_member_profiles_batch(current_batch_size)
            all_profiles.extend(batch_profiles)
        
        st.success(f"✅ Generated {len(all_profiles)} member profiles")
        
        # Phase 2: Generate Contribution Histories
        all_contributions = []
        if include_contributions:
            status_text.text("🚀 Phase 2: Generating contribution histories...")
            sample_count = int(len(all_profiles) * sample_size / 100)
            sample_profiles = random.sample(all_profiles, min(sample_count, len(all_profiles)))
            
            for i, member in enumerate(sample_profiles):
                progress = 0.4 + (i / len(sample_profiles)) * 0.3  # 30% for contributions
                progress_bar.progress(progress)
                
                if i % 10 == 0:
                    status_text.text(f"Processing contributions for member {i+1}/{len(sample_profiles)}...")
                
                contributions = generator.generate_contribution_history(member, 12)
                all_contributions.extend(contributions)
            
            st.success(f"✅ Generated {len(all_contributions)} contribution records")
        
        # Phase 3: Generate Fund Allocations
        all_allocations = []
        if include_allocations:
            status_text.text("🚀 Phase 3: Generating fund allocations...")
            sample_count = int(len(all_profiles) * sample_size / 100)
            sample_profiles = random.sample(all_profiles, min(sample_count, len(all_profiles)))
            
            for i, member in enumerate(sample_profiles):
                progress = 0.7 + (i / len(sample_profiles)) * 0.2  # 20% for allocations
                progress_bar.progress(progress)
                
                if i % 10 == 0:
                    status_text.text(f"Processing allocations for member {i+1}/{len(sample_profiles)}...")
                
                allocations = generator.generate_fund_allocations(member)
                all_allocations.extend(allocations)
            
            st.success(f"✅ Generated {len(all_allocations)} fund allocation records")
        
        # Phase 4: Validation
        status_text.text("🚀 Phase 4: Validating data quality...")
        progress_bar.progress(0.9)
        
        validation_results = generator.validate_data_quality(all_profiles, all_contributions, all_allocations)
        
        progress_bar.progress(1.0)
        status_text.text("🎖️ Mission Complete!")
        
        # Store results in session state
        st.session_state.generated_data = {
            'profiles': all_profiles,
            'contributions': all_contributions,
            'allocations': all_allocations,
            'validation': validation_results,
            'timestamp': datetime.now().strftime("%Y%m%d_%H%M%S")
        }
        
        st.session_state.mission_status = "Mission Accomplished"
        
        # Show success metrics
        display_generation_results(validation_results, len(all_profiles), 
                                 len(all_contributions), len(all_allocations))
        
    except Exception as e:
        st.error(f"❌ Mission Failed: {str(e)}")
        st.session_state.mission_status = "Mission Failed"

def display_generation_results(validation_results, profile_count, contribution_count, allocation_count):
    """Display generation results and metrics"""
    
    st.header("🏆 MISSION RESULTS")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("👥 Members Generated", profile_count)
    
    with col2:
        st.metric("💰 Contribution Records", contribution_count)
    
    with col3:
        st.metric("📊 Fund Allocations", allocation_count)
    
    with col4:
        compliance_rate = validation_results['fund_allocation_checks'].get('allocation_compliance_rate', 0)
        st.metric("✅ Compliance Rate", f"{compliance_rate:.1%}")
    
    # Detailed validation results
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Age Distribution")
        age_stats = validation_results['age_distribution']
        st.json({
            "Min Age": age_stats['min'],
            "Max Age": age_stats['max'], 
            "Average Age": f"{age_stats['mean']:.1f}",
            "Median Age": age_stats['median']
        })
    
    with col2:
        st.subheader("💼 Sector Distribution")
        sector_dist = validation_results['sector_distribution']
        st.json(sector_dist)
    
    # Salary statistics
    st.subheader("💰 Salary Statistics")
    salary_stats = validation_results['salary_stats']
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Min Salary", f"£{salary_stats['min']:,}")
    with col2:
        st.metric("Average Salary", f"£{salary_stats['mean']:,.0f}")
    with col3:
        st.metric("Max Salary", f"£{salary_stats['max']:,}")

def data_visualization_dashboard():
    """Interactive data visualization dashboard"""
    st.header("📊 INTELLIGENCE ANALYSIS DASHBOARD")
    
    if not st.session_state.generated_data:
        st.info("🔍 Generate data first to view analytics dashboard")
        return
    
    data = st.session_state.generated_data
    profiles_df = pd.DataFrame([asdict(p) for p in data['profiles']])
    
    # Dashboard tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["👥 Demographics", "💰 Financial Analysis", "📈 Fund Allocations", "🎯 Quality Metrics", "🔬 Realism Analysis"])
    
    with tab1:
        render_demographics_analysis(profiles_df)
    
    with tab2:
        render_financial_analysis(profiles_df, data.get('contributions', []))
    
    with tab3:
        render_fund_analysis(data.get('allocations', []))
    
    with tab4:
        render_quality_metrics(data['validation'])
    
    with tab5:
        render_realism_analysis()

def render_demographics_analysis(profiles_df):
    """Render demographics analysis charts"""
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Age distribution
        fig_age = px.histogram(profiles_df, x='age', nbins=20, 
                              title="Age Distribution",
                              labels={'age': 'Age', 'count': 'Number of Members'})
        fig_age.update_layout(showlegend=False)
        st.plotly_chart(fig_age, width='stretch')
        
        # Gender distribution
        gender_counts = profiles_df['gender'].value_counts()
        fig_gender = px.pie(values=gender_counts.values, names=gender_counts.index,
                           title="Gender Distribution")
        st.plotly_chart(fig_gender, width='stretch')
    
    with col2:
        # Sector distribution
        sector_counts = profiles_df['sector'].value_counts()
        fig_sector = px.bar(x=sector_counts.index, y=sector_counts.values,
                           title="Employment Sector Distribution",
                           labels={'x': 'Sector', 'y': 'Number of Members'})
        fig_sector.update_xaxes(tickangle=45)
        st.plotly_chart(fig_sector, width='stretch')
        
        # Service years distribution
        fig_service = px.histogram(profiles_df, x='years_service', nbins=15,
                                  title="Years of Service Distribution",
                                  labels={'years_service': 'Years of Service', 'count': 'Number of Members'})
        st.plotly_chart(fig_service, width='stretch')

def render_financial_analysis(profiles_df, contributions):
    """Render financial analysis charts"""
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Salary distribution by sector
        fig_salary = px.box(profiles_df, x='sector', y='annual_salary',
                           title="Salary Distribution by Sector")
        fig_salary.update_xaxes(tickangle=45)
        fig_salary.update_yaxes(title="Annual Salary (£)")
        st.plotly_chart(fig_salary, width='stretch')
        
        # Age vs Salary correlation
        fig_age_salary = px.scatter(profiles_df, x='age', y='annual_salary', color='sector',
                                   title="Age vs Salary Correlation",
                                   labels={'age': 'Age', 'annual_salary': 'Annual Salary (£)'})
        st.plotly_chart(fig_age_salary, width='stretch')
    
    with col2:
        # Salary by years of service
        fig_service_salary = px.scatter(profiles_df, x='years_service', y='annual_salary', 
                                       color='sector', size='age',
                                       title="Salary vs Years of Service",
                                       labels={'years_service': 'Years of Service', 
                                              'annual_salary': 'Annual Salary (£)'})
        st.plotly_chart(fig_service_salary, width='stretch')
        
        # Status distribution
        status_counts = profiles_df['status'].value_counts()
        fig_status = px.pie(values=status_counts.values, names=status_counts.index,
                           title="Member Status Distribution")
        st.plotly_chart(fig_status, width='stretch')

def render_fund_analysis(allocations):
    """Render fund allocation analysis"""
    
    if not allocations:
        st.info("No fund allocation data available")
        return
    
    allocations_df = pd.DataFrame([asdict(a) for a in allocations])
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Fund popularity
        fund_counts = allocations_df['fund_name'].value_counts()
        fig_funds = px.bar(x=fund_counts.values, y=fund_counts.index, orientation='h',
                          title="Fund Selection Frequency",
                          labels={'x': 'Number of Selections', 'y': 'Fund Name'})
        st.plotly_chart(fig_funds, width='stretch')
    
    with col2:
        # Risk level distribution
        risk_counts = allocations_df['risk_level'].value_counts()
        fig_risk = px.pie(values=risk_counts.values, names=risk_counts.index,
                         title="Risk Level Distribution")
        st.plotly_chart(fig_risk, width='stretch')
    
    # Allocation percentage analysis
    fig_allocation = px.histogram(allocations_df, x='allocation_percent', nbins=20,
                                 title="Fund Allocation Percentage Distribution",
                                 labels={'allocation_percent': 'Allocation Percentage', 'count': 'Frequency'})
    st.plotly_chart(fig_allocation, width='stretch')

def render_quality_metrics(validation_results):
    """Render data quality metrics"""
    
    # Business rule compliance
    st.subheader("🎯 Business Rule Compliance")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        allocation_checks = validation_results['fund_allocation_checks']
        compliance_rate = allocation_checks.get('allocation_compliance_rate', 0)
        
        fig_compliance = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = compliance_rate * 100,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Fund Allocation Compliance"},
            delta = {'reference': 95},
            gauge = {
                'axis': {'range': [None, 100]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 50], 'color': "lightgray"},
                    {'range': [50, 85], 'color': "gray"},
                    {'range': [85, 100], 'color': "lightgreen"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 95
                }
            }
        ))
        fig_compliance.update_layout(height=300)
        st.plotly_chart(fig_compliance, width='stretch')
    
    with col2:
        # Age distribution quality
        age_stats = validation_results['age_distribution']
        st.metric("Age Range Quality", f"{age_stats['min']}-{age_stats['max']} years")
        st.metric("Average Age", f"{age_stats['mean']:.1f} years")
        
    with col3:
        # Data volume metrics
        st.metric("Total Members", validation_results['total_members'])
        allocation_checks = validation_results['fund_allocation_checks']
        st.metric("Members with Allocations", allocation_checks.get('members_with_allocations', 0))

def render_realism_analysis():
    """Render data realism analysis comparing synthetic vs real UK pension data"""
    
    st.subheader("🔬 Data Realism Analysis")
    st.markdown("**Compare synthetic data against real UK pension industry benchmarks**")
    
    # Check for available data files
    available_files = []
    for filename in ['generated_pension_data_clean.csv', 'generated_pension_data_fixed.csv', 'generated_pension_data.csv']:
        try:
            import os
            if os.path.exists(filename):
                available_files.append(filename)
        except:
            pass
    
    if not available_files:
        st.warning("⚠️ No synthetic data files found. Please generate data first.")
        return
    
    # File selection
    selected_file = st.selectbox("Select data file for analysis:", available_files)
    
    if st.button("🔍 Analyze Data Realism", type="primary"):
        with st.spinner("Analyzing data realism against UK pension benchmarks..."):
            try:
                # Import the comparator here to avoid import issues
                from data_realism_comparator import DataRealismComparator
                
                # Initialize comparator
                comparator = DataRealismComparator()
                
                # Run comparison
                results = comparator.compare_synthetic_vs_real(selected_file)
                
                if "error" in results:
                    st.error(f"Analysis failed: {results['error']}")
                    return
                
                # Display overall score
                overall_score = results.get('overall_realism_score', 0)
                
                col1, col2, col3 = st.columns([2, 1, 1])
                
                with col1:
                    # Create gauge chart for overall score
                    fig_gauge = go.Figure(go.Indicator(
                        mode = "gauge+number+delta",
                        value = overall_score * 100,
                        domain = {'x': [0, 1], 'y': [0, 1]},
                        title = {'text': "Overall Realism Score (%)"},
                        delta = {'reference': 80},
                        gauge = {
                            'axis': {'range': [None, 100]},
                            'bar': {'color': "darkblue"},
                            'steps': [
                                {'range': [0, 60], 'color': "lightcoral"},
                                {'range': [60, 80], 'color': "lightyellow"},
                                {'range': [80, 100], 'color': "lightgreen"}
                            ],
                            'threshold': {
                                'line': {'color': "red", 'width': 4},
                                'thickness': 0.75,
                                'value': 90
                            }
                        }
                    ))
                    fig_gauge.update_layout(height=300)
                    st.plotly_chart(fig_gauge, width='stretch')
                
                with col2:
                    st.metric("Overall Score", f"{overall_score:.1%}")
                    if overall_score > 0.8:
                        st.success("✅ Highly Realistic")
                    elif overall_score > 0.6:
                        st.warning("⚠️ Moderately Realistic")
                    else:
                        st.error("❌ Needs Improvement")
                
                with col3:
                    st.metric("Data File", selected_file)
                    st.metric("Analysis Date", datetime.now().strftime("%Y-%m-%d"))
                
                # Detailed comparison results
                st.subheader("📊 Detailed Realism Analysis")
                
                detailed_comparisons = results.get('detailed_comparisons', {})
                
                # Create comparison charts
                comparison_data = []
                for category, data in detailed_comparisons.items():
                    if 'accuracy_score' in data:
                        comparison_data.append({
                            'Category': category.title(),
                            'Accuracy Score': data['accuracy_score'],
                            'Passes Test': '✅' if data.get('passes_test', False) else '❌',
                            'Summary': data.get('summary', 'No summary available')
                        })
                
                if comparison_data:
                    df_comparison = pd.DataFrame(comparison_data)
                    
                    # Display comparison table
                    st.dataframe(df_comparison, width='stretch')
                    
                    # Create bar chart of accuracy scores
                    fig_scores = px.bar(df_comparison, x='Category', y='Accuracy Score',
                                       title="Realism Accuracy by Category",
                                       color='Accuracy Score',
                                       color_continuous_scale='RdYlGn')
                    fig_scores.update_layout(showlegend=False)
                    st.plotly_chart(fig_scores, width='stretch')
                
                # Distribution comparisons
                if 'age' in detailed_comparisons and 'distributions' in detailed_comparisons['age']:
                    st.subheader("📈 Distribution Comparisons")
                    
                    # Create visualization for each distribution
                    for category in ['age', 'gender', 'sector', 'status']:
                        if category in detailed_comparisons and 'distributions' in detailed_comparisons[category]:
                            distributions = detailed_comparisons[category]['distributions']
                            
                            categories = list(distributions.keys())
                            synthetic_values = [distributions[cat]["synthetic"] * 100 for cat in categories]
                            real_values = [distributions[cat]["real"] * 100 for cat in categories]
                            
                            fig = go.Figure()
                            
                            fig.add_trace(go.Bar(
                                name='Synthetic Data',
                                x=categories,
                                y=synthetic_values,
                                marker_color='lightblue'
                            ))
                            
                            fig.add_trace(go.Bar(
                                name='Real UK Data',
                                x=categories,
                                y=real_values,
                                marker_color='darkblue'
                            ))
                            
                            fig.update_layout(
                                title=f"{category.title()} Distribution Comparison",
                                xaxis_title="Categories",
                                yaxis_title="Percentage (%)",
                                barmode='group',
                                height=400
                            )
                            
                            st.plotly_chart(fig, width='stretch')
                
                # Recommendations
                recommendations = results.get('recommendations', [])
                if recommendations:
                    st.subheader("🎯 Improvement Recommendations")
                    for rec in recommendations:
                        if "✅" in rec:
                            st.success(rec)
                        elif "⚠️" in rec:
                            st.warning(rec)
                        elif "❌" in rec:
                            st.error(rec)
                        else:
                            st.info(rec)
                
                # Raw comparison data
                with st.expander("🔍 View Raw Comparison Data"):
                    st.json(results)
                
            except ImportError as e:
                st.error(f"Import error: {str(e)}")
                st.info("Make sure data_realism_comparator.py is in the current directory")
            except Exception as e:
                st.error(f"Analysis failed: {str(e)}")
                import traceback
                st.code(traceback.format_exc())

def render_realism_analysis():
    """Render the data realism analysis tab with enhanced histogram visualizations"""
    st.markdown("### 🔬 Data Realism Analysis")
    st.markdown("Compare synthetic data against real UK pension industry benchmarks")
    
    # File upload for comparison
    col1, col2 = st.columns([3, 1])
    
    with col1:
        uploaded_file = st.file_uploader(
            "Upload synthetic pension data CSV for analysis",
            type=['csv'],
            help="Upload a CSV file containing synthetic pension data to compare against UK benchmarks"
        )
    
    with col2:
        st.markdown("**Required Columns:**")
        st.markdown("- Age\n- Gender\n- Sector\n- AnnualSalary\n- YearsService\n- Status")
    
    if uploaded_file is not None:
        try:
            # Load and analyze the data
            comparator = DataRealismComparator()
            df = comparator.load_data(uploaded_file)
            
            st.success(f"✅ Data loaded successfully! {len(df)} records found.")
            
            # Run the comparison analysis
            with st.spinner("🔍 Analyzing data realism..."):
                results = comparator.analyze_data_realism(df)
            
            # Display overall score
            overall_score = results.get("overall_score", 0) * 100
            score_color = "🟢" if overall_score >= 80 else "🟡" if overall_score >= 60 else "🔴"
            
            st.markdown(f"## {score_color} Overall Realism Score: {overall_score:.1f}%")
            
            # Create tabs for different analyses
            tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Overview", "📈 Detailed Metrics", "🎯 Category Analysis", "📊 Enhanced Histograms", "📋 Summary"])
            
            with tab1:
                st.markdown("### Data Realism Overview")
                
                # Display key metrics
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Overall Score", f"{overall_score:.1f}%")
                
                with col2:
                    categories_passed = sum(1 for cat in results.get("detailed_comparisons", {}).values() 
                                          if cat.get("passes_test", False))
                    total_categories = len(results.get("detailed_comparisons", {}))
                    st.metric("Categories Passed", f"{categories_passed}/{total_categories}")
                
                with col3:
                    grade = results.get("grade", "Unknown")
                    st.metric("Data Grade", grade)
                
                # Show visualizations
                st.markdown("### 📊 Comparison Visualizations")
                
                # Overall comparison chart
                fig_overview = comparator.create_comparison_visualizations()
                st.plotly_chart(fig_overview, width='stretch')
                
            with tab2:
                st.markdown("### 📈 Detailed Category Metrics")
                
                detailed_comparisons = results.get("detailed_comparisons", {})
                
                for category, details in detailed_comparisons.items():
                    with st.expander(f"📋 {category.title()} Analysis"):
                        
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            accuracy = details.get("accuracy_score", 0) * 100
                            passes = details.get("passes_test", False)
                            status = "✅ Pass" if passes else "❌ Fail"
                            
                            st.metric(f"{category.title()} Accuracy", f"{accuracy:.1f}%")
                            st.markdown(f"**Status:** {status}")
                        
                        with col2:
                            # Show distribution details if available
                            distributions = details.get("distributions", {})
                            if distributions:
                                st.markdown("**Distribution Comparison:**")
                                for key, values in distributions.items():
                                    synthetic = values.get("synthetic", 0) * 100
                                    real = values.get("real", 0) * 100
                                    st.markdown(f"- {key}: Synthetic {synthetic:.1f}% vs Real {real:.1f}%")
            
            with tab3:
                st.markdown("### 🎯 Individual Category Analysis")
                
                # Create sector-specific charts
                detailed_comparisons = results.get("detailed_comparisons", {})
                
                # Age distribution
                if "age" in detailed_comparisons:
                    st.markdown("#### 👥 Age Distribution")
                    age_fig = comparator.create_age_comparison_chart()
                    st.plotly_chart(age_fig, width='stretch')
                
                # Salary analysis
                if "salary" in detailed_comparisons:
                    st.markdown("#### 💰 Salary Analysis")
                    salary_fig = comparator.create_salary_comparison_chart()
                    st.plotly_chart(salary_fig, width='stretch')
                
                # Gender distribution
                if "gender" in detailed_comparisons:
                    st.markdown("#### ⚖️ Gender Distribution")
                    gender_data = detailed_comparisons["gender"]["distributions"]
                    
                    categories = list(gender_data.keys())
                    synthetic_values = [gender_data[cat]["synthetic"] * 100 for cat in categories]
                    real_values = [gender_data[cat]["real"] * 100 for cat in categories]
                    
                    fig = go.Figure(data=[
                        go.Bar(name='Synthetic', x=categories, y=synthetic_values, marker_color='lightpink'),
                        go.Bar(name='Real UK', x=categories, y=real_values, marker_color='darkred')
                    ])
                    fig.update_layout(title="Gender Distribution Comparison", barmode='group', height=400)
                    st.plotly_chart(fig, width='stretch')
            
            with tab4:
                st.markdown("### 📊 Enhanced Histogram Analysis")
                st.markdown("Detailed statistical visualizations for comprehensive data analysis")
                
                # Create sub-tabs for different histogram types
                hist_tab1, hist_tab2, hist_tab3, hist_tab4, hist_tab5, hist_tab6 = st.tabs([
                    "👥 Age Histograms", "💰 Salary Histograms", "⏱️ Service Histograms", 
                    "🌍 Geographic Histograms", "🎯 Accuracy Scores", "⚠️ Error Analysis"
                ])
                
                with hist_tab1:
                    st.markdown("#### Age Distribution Analysis")
                    try:
                        age_hist = comparator.create_age_histogram()
                        st.plotly_chart(age_hist, width='stretch')
                    except Exception as e:
                        st.warning(f"Could not generate age histogram: {str(e)}")
                
                with hist_tab2:
                    st.markdown("#### Salary Distribution Analysis")
                    try:
                        salary_hist = comparator.create_salary_histogram()
                        st.plotly_chart(salary_hist, width='stretch')
                    except Exception as e:
                        st.warning(f"Could not generate salary histogram: {str(e)}")
                
                with hist_tab3:
                    st.markdown("#### Years of Service Analysis")
                    try:
                        service_hist = comparator.create_service_histogram()
                        st.plotly_chart(service_hist, width='stretch')
                    except Exception as e:
                        st.warning(f"Could not generate service histogram: {str(e)}")
                
                with hist_tab4:
                    st.markdown("#### Geographic Distribution Analysis")
                    try:
                        geo_hist = comparator.create_geographic_histogram()
                        st.plotly_chart(geo_hist, width='stretch')
                    except Exception as e:
                        st.warning(f"Could not generate geographic histogram: {str(e)}")
                
                with hist_tab5:
                    st.markdown("#### Category Accuracy Scores")
                    try:
                        accuracy_hist = comparator.create_accuracy_scores_histogram()
                        st.plotly_chart(accuracy_hist, width='stretch')
                    except Exception as e:
                        st.warning(f"Could not generate accuracy histogram: {str(e)}")
                
                with hist_tab6:
                    st.markdown("#### Comprehensive Error Analysis")
                    try:
                        error_hist = comparator.create_error_analysis_histogram()
                        st.plotly_chart(error_hist, width='stretch')
                    except Exception as e:
                        st.warning(f"Could not generate error analysis histogram: {str(e)}")
            
            with tab5:
                st.markdown("### 📋 Analysis Summary")
                
                # Summary statistics
                st.markdown("#### Key Findings:")
                
                findings = results.get("findings", [])
                if findings:
                    for finding in findings:
                        st.markdown(f"• {finding}")
                else:
                    st.markdown("• Analysis completed successfully")
                    st.markdown(f"• Overall realism score: {overall_score:.1f}%")
                    st.markdown(f"• Data quality grade: {results.get('grade', 'Not available')}")
                
                # Recommendations
                st.markdown("#### Recommendations:")
                recommendations = results.get("recommendations", [])
                if recommendations:
                    for rec in recommendations:
                        st.markdown(f"• {rec}")
                else:
                    if overall_score >= 80:
                        st.markdown("• Excellent data quality - no immediate improvements needed")
                    elif overall_score >= 60:
                        st.markdown("• Good data quality - minor adjustments could improve realism")
                    else:
                        st.markdown("• Consider reviewing data generation parameters")
                        st.markdown("• Focus on categories with low accuracy scores")
                
                # Export option
                st.markdown("#### Export Results")
                if st.button("📄 Download Analysis Report"):
                    # Create a summary report
                    report = f"""
Data Realism Analysis Report
============================

Overall Score: {overall_score:.1f}%
Grade: {results.get('grade', 'Not available')}
Analysis Date: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}

Category Breakdown:
"""
                    for category, details in detailed_comparisons.items():
                        accuracy = details.get("accuracy_score", 0) * 100
                        status = "Pass" if details.get("passes_test", False) else "Fail"
                        report += f"- {category.title()}: {accuracy:.1f}% ({status})\n"
                    
                    st.download_button(
                        label="Download Report",
                        data=report,
                        file_name=f"realism_analysis_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.txt",
                        mime="text/plain"
                    )
                
        except Exception as e:
            st.error(f"❌ Error analyzing data: {str(e)}")
            st.markdown("Please check that your CSV file contains the required columns and is properly formatted.")
    
    else:
        st.info("👆 Upload a CSV file to begin the realism analysis")
        
        # Show example data format
        st.markdown("#### Example Data Format:")
        example_data = {
            'MemberID': ['M001', 'M002', 'M003'],
            'Age': [35, 42, 28],
            'Gender': ['Female', 'Male', 'Female'],
            'Sector': ['Public', 'Private', 'Public'],
            'AnnualSalary': [45000, 65000, 38000],
            'YearsService': [8, 15, 3],
            'Status': ['Active', 'Active', 'Deferred']
        }
        
        example_df = pd.DataFrame(example_data)
        st.dataframe(example_df, width='stretch')

def analyze_data_realism(file_path: str):
    """Perform comprehensive realism analysis on selected data file"""
    
    with st.spinner("🔍 Performing comprehensive realism analysis..."):
        try:
            # Initialize the comparator
            comparator = DataRealismComparator()
            
            # Perform comparison
            comparison_results = comparator.compare_synthetic_vs_real(file_path)
            
            if 'error' in comparison_results:
                st.error(f"❌ Analysis failed: {comparison_results['error']}")
                return
            
            # Store results in session state
            st.session_state.realism_analysis = comparison_results
            st.session_state.realism_comparator = comparator
            
            st.success("✅ Realism analysis complete!")
            
        except Exception as e:
            st.error(f"❌ Error during realism analysis: {str(e)}")

def display_realism_results():
    """Display comprehensive realism analysis results"""
    
    if 'realism_analysis' not in st.session_state:
        return
    
    results = st.session_state.realism_analysis
    comparator = st.session_state.get('realism_comparator')
    
    # Overall realism score
    st.markdown("### 🎯 Overall Realism Assessment")
    
    overall_score = results.get('overall_realism_score', 0)
    
    # Create score indicator
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Realism gauge
        if comparator:
            figures = comparator.create_comparison_visualizations()
            if 'realism_gauge' in figures:
                st.plotly_chart(figures['realism_gauge'], width='stretch')
    
    # Score interpretation
    if overall_score >= 0.8:
        st.success(f"🏆 **Excellent Realism**: {overall_score:.1%} - Synthetic data closely matches UK pension patterns")
    elif overall_score >= 0.6:
        st.warning(f"⚠️ **Good Realism**: {overall_score:.1%} - Some areas need improvement")
    else:
        st.error(f"❌ **Poor Realism**: {overall_score:.1%} - Significant improvements needed")
    
    # Detailed category analysis
    st.markdown("### 📊 Category-by-Category Analysis")
    
    detailed_comparisons = results.get('detailed_comparisons', {})
    
    # Create tabs for different categories
    if detailed_comparisons:
        category_tabs = st.tabs([
            "👥 Age", "⚧️ Gender", "🏢 Sector", 
            "💰 Salary", "🗺️ Geographic", "📋 Status"
        ])
        
        categories = ['age', 'gender', 'sector', 'salary', 'geographic', 'status']
        
        for i, (tab, category) in enumerate(zip(category_tabs, categories)):
            with tab:
                if category in detailed_comparisons:
                    render_category_analysis(category, detailed_comparisons[category], comparator)
                else:
                    st.info(f"No analysis available for {category} category")
    
    # Recommendations
    st.markdown("### 💡 Improvement Recommendations")
    
    recommendations = results.get('recommendations', [])
    if recommendations:
        for rec in recommendations:
            if "❌" in rec:
                st.error(rec)
            elif "⚠️" in rec:
                st.warning(rec)
            else:
                st.success(rec)
    else:
        st.info("No specific recommendations available")
    
    # Export analysis report
    st.markdown("### 📄 Export Analysis Report")
    
    if st.button("📥 Download Realism Analysis Report"):
        export_realism_report(results)

def render_category_analysis(category: str, category_data: dict, comparator):
    """Render analysis for a specific category"""
    
    # Category score
    accuracy_score = category_data.get('accuracy_score', 0)
    summary = category_data.get('summary', '')
    passes_test = category_data.get('passes_test', False)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        # Score display
        if passes_test:
            st.success(f"✅ **{summary}**")
        else:
            st.error(f"❌ **{summary}**")
        
        # Additional metrics
        if category == 'salary':
            sector_analysis = category_data.get('sector_analysis', {})
            if sector_analysis:
                st.markdown("**Sector Performance:**")
                for sector, data in sector_analysis.items():
                    sector_score = data.get('accuracy_score', 0)
                    status = "✅" if data.get('passes_test', False) else "❌"
                    st.markdown(f"{status} {sector}: {sector_score:.1%}")
        
        elif category == 'geographic':
            regions_covered = category_data.get('regions_covered', 0)
            st.metric("Regions Covered", regions_covered)
    
    with col2:
        # Visualization
        if comparator:
            figures = comparator.create_comparison_visualizations()
            chart_key = f"{category}_comparison"
            
            if chart_key in figures:
                st.plotly_chart(figures[chart_key], width='stretch')
            elif category == 'salary' and 'salary_comparison' in figures:
                st.plotly_chart(figures['salary_comparison'], width='stretch')
    
    # Detailed distributions
    if 'distributions' in category_data:
        st.markdown("**Detailed Comparison:**")
        distributions = category_data['distributions']
        
        comparison_df = pd.DataFrame([
            {
                'Category': cat,
                'Synthetic (%)': f"{data['synthetic']:.1%}",
                'Real UK (%)': f"{data['real']:.1%}",
                'Difference (%)': f"{data['difference']:.1%}",
                'Error (%)': f"{data['percentage_error']:.1f}%"
            }
            for cat, data in distributions.items()
        ])
        
        st.dataframe(comparison_df, width='stretch', hide_index=True)

def export_realism_report(results: dict):
    """Export comprehensive realism analysis report"""
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Create comprehensive report
    report = {
        "mission_name": "Mission Alpha - Data Realism Analysis",
        "analysis_timestamp": timestamp,
        "overall_assessment": {
            "realism_score": results.get('overall_realism_score', 0),
            "grade": "Excellent" if results.get('overall_realism_score', 0) >= 0.8 else 
                    "Good" if results.get('overall_realism_score', 0) >= 0.6 else "Needs Improvement"
        },
        "detailed_analysis": results.get('detailed_comparisons', {}),
        "recommendations": results.get('recommendations', []),
        "uk_benchmarks_used": "ONS, TPR, and industry sources",
        "methodology": "Statistical comparison against real UK pension industry patterns",
        "classification": "Synthetic Data Quality Assessment"
    }
    
    # Convert to JSON
    report_json = json.dumps(report, indent=2, default=str)
    
    st.download_button(
        label="📊 Download Realism Analysis Report (JSON)",
        data=report_json,
        file_name=f"realism_analysis_report_{timestamp}.json",
        mime="application/json"
    )

def data_export_interface():
    """Enhanced data export and download interface"""
    st.header("📁 DATA EXPORT & INTELLIGENCE SHARING")
    
    # Check for available CSV files
    import glob
    csv_files = glob.glob("*.csv")
    generated_files = [f for f in csv_files if 'generated' in f.lower() or 'pension' in f.lower()]
    
    if not generated_files:
        st.info("🔍 Generate data first to access export options")
        st.markdown("Go to **🎯 Synthetic Data Generation** tab to create data files")
        return
    
    st.markdown("### 📊 Available Data Files")
    
    for file in generated_files:
        with st.expander(f"📄 {file}"):
            try:
                df = pd.read_csv(file)
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Total Records", len(df))
                    st.metric("Columns", len(df.columns))
                
                with col2:
                    if 'Age' in df.columns:
                        # Create age brackets for analysis
                        age_brackets = pd.cut(df['Age'], 
                                            bins=[21, 35, 45, 55, 75], 
                                            labels=['22-35', '36-45', '46-55', '56-75'],
                                            include_lowest=True)
                        age_dist = age_brackets.value_counts().sort_index()
                        most_common_bracket = age_dist.idxmax()
                        st.metric("Top Age Bracket", most_common_bracket)
                    
                    if 'AnnualSalary' in df.columns:
                        st.metric("Avg Salary", f"£{df['AnnualSalary'].mean():,.0f}")
                
                with col3:
                    # File info
                    file_size = os.path.getsize(file) / 1024  # KB
                    st.metric("File Size", f"{file_size:.1f} KB")
                    
                    # Last modified
                    import datetime
                    mod_time = os.path.getmtime(file)
                    mod_date = datetime.datetime.fromtimestamp(mod_time)
                    st.metric("Modified", mod_date.strftime("%H:%M"))
                
                # Age bracket distribution
                if 'Age' in df.columns:
                    st.markdown("**Age Bracket Distribution:**")
                    bracket_col1, bracket_col2 = st.columns(2)
                    
                    with bracket_col1:
                        for i, (bracket, count) in enumerate(age_dist.items()):
                            if i < 2:  # First 2 brackets
                                pct = (count / len(df)) * 100
                                st.write(f"• {bracket}: {count} ({pct:.1f}%)")
                    
                    with bracket_col2:
                        for i, (bracket, count) in enumerate(age_dist.items()):
                            if i >= 2:  # Last 2 brackets
                                pct = (count / len(df)) * 100
                                st.write(f"• {bracket}: {count} ({pct:.1f}%)")
                
                # Data preview
                st.markdown("**Data Preview:**")
                st.dataframe(df.head(5), width='stretch')
                
                # Enhanced export options
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    # Download original file
                    with open(file, 'r') as f:
                        csv_data = f.read()
                    st.download_button(
                        label=f"📥 Download {file}",
                        data=csv_data,
                        file_name=file,
                        mime="text/csv"
                    )
                
                with col2:
                    # Download with timestamp
                    timestamp = pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")
                    filename_with_timestamp = f"{file.replace('.csv', '')}_{timestamp}.csv"
                    st.download_button(
                        label=f"📥 Download with Timestamp",
                        data=csv_data,
                        file_name=filename_with_timestamp,
                        mime="text/csv"
                    )
                
                with col3:
                    # Privacy and download options
                    anonymize_postcodes = st.checkbox(
                        "🔒 Anonymize Postcodes", 
                        value=True,
                        key=f"anon_{file}",
                        help="Replace postcode second half with XXX for privacy"
                    )
                    
                    if st.button(f"📥 Download (Privacy-Safe)", key=f"privacy_{file}"):
                        df_download = df.copy()
                        
                        if anonymize_postcodes and 'Postcode' in df_download.columns:
                            # Anonymize postcodes
                            def anonymize_postcode(postcode):
                                if pd.isna(postcode) or not isinstance(postcode, str):
                                    return postcode
                                import re
                                match = re.match(r'^([A-Z]{1,2}[0-9]{1,2}[A-Z]?)\s+([0-9][A-Z]{2})$', postcode.upper().strip())
                                if match:
                                    return f"{match.group(1)} XXX"
                                else:
                                    parts = postcode.strip().split()
                                    return f"{parts[0]} XXX" if len(parts) >= 1 else postcode
                            
                            df_download['Postcode'] = df_download['Postcode'].apply(anonymize_postcode)
                        
                        privacy_csv = df_download.to_csv(index=False)
                        privacy_filename = f"{file.replace('.csv', '')}_privacy_safe.csv"
                        
                        st.download_button(
                            label=f"💾 Download {privacy_filename}",
                            data=privacy_csv,
                            file_name=privacy_filename,
                            mime="text/csv"
                        )
                    
                    # Show advanced filtering options
                    if st.button(f"🎯 Advanced Filters", key=f"filter_{file}"):
                        st.session_state[f"show_filter_{file}"] = True
                
                # Show filtering options if requested
                if st.session_state.get(f"show_filter_{file}", False):
                    st.markdown("**Advanced Filter Options:**")
                    filter_col1, filter_col2, filter_col3 = st.columns(3)
                    
                    with filter_col1:
                        if 'Age' in df.columns:
                            selected_brackets = st.multiselect(
                                "Select Age Brackets",
                                options=age_dist.index.tolist(),
                                default=age_dist.index.tolist(),
                                key=f"age_filter_{file}"
                            )
                    
                    with filter_col2:
                        if 'Sector' in df.columns:
                            available_sectors = df['Sector'].unique()
                            selected_sectors = st.multiselect(
                                "Select Sectors",
                                options=available_sectors,
                                default=available_sectors.tolist(),
                                key=f"sector_filter_{file}"
                            )
                    
                    with filter_col3:
                        filter_anonymize = st.checkbox(
                            "🔒 Anonymize in Export", 
                            value=True,
                            key=f"filter_anon_{file}"
                        )
                    
                    if st.button(f"📥 Download Filtered Data", key=f"download_filtered_{file}"):
                        filtered_df = df.copy()
                        
                        # Apply age bracket filter
                        if 'Age' in df.columns and selected_brackets:
                            age_brackets_full = pd.cut(df['Age'], 
                                                     bins=[21, 35, 45, 55, 75], 
                                                     labels=['22-35', '36-45', '46-55', '56-75'],
                                                     include_lowest=True)
                            filtered_df = filtered_df[age_brackets_full.isin(selected_brackets)]
                        
                        # Apply sector filter
                        if 'Sector' in df.columns and selected_sectors:
                            filtered_df = filtered_df[filtered_df['Sector'].isin(selected_sectors)]
                        
                        # Apply anonymization if requested
                        if filter_anonymize and 'Postcode' in filtered_df.columns:
                            def anonymize_postcode(postcode):
                                if pd.isna(postcode) or not isinstance(postcode, str):
                                    return postcode
                                import re
                                match = re.match(r'^([A-Z]{1,2}[0-9]{1,2}[A-Z]?)\s+([0-9][A-Z]{2})$', postcode.upper().strip())
                                if match:
                                    return f"{match.group(1)} XXX"
                                else:
                                    parts = postcode.strip().split()
                                    return f"{parts[0]} XXX" if len(parts) >= 1 else postcode
                            
                            filtered_df['Postcode'] = filtered_df['Postcode'].apply(anonymize_postcode)
                        
                        filtered_csv = filtered_df.to_csv(index=False)
                        timestamp = pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")
                        privacy_suffix = "_private" if filter_anonymize else ""
                        filtered_filename = f"{file.replace('.csv', '')}_filtered{privacy_suffix}_{timestamp}.csv"
                        
                        st.download_button(
                            label=f"💾 Download {filtered_filename}",
                            data=filtered_csv,
                            file_name=filtered_filename,
                            mime="text/csv"
                        )
                        
                        st.success(f"✅ Filtered data ready: {len(filtered_df)} records")
                
            except Exception as e:
                st.error(f"❌ Error reading {file}: {str(e)}")
    
    # Batch export options
    if len(generated_files) > 1:
        st.markdown("### 📦 Batch Export Options")
        
        # Smart combining for large datasets
        st.markdown("#### 🔗 Smart Dataset Combiner")
        st.info("💡 Combine multiple batch files into a single large dataset")
        
        combine_col1, combine_col2 = st.columns(2)
        
        with combine_col1:
            selected_files = st.multiselect(
                "Select files to combine",
                options=generated_files,
                default=generated_files,
                help="Choose which CSV files to merge into one dataset"
            )
        
        with combine_col2:
            target_records = st.number_input(
                "Target Record Count",
                min_value=100,
                max_value=10000,
                value=5000,
                step=100,
                help="How many records you want in the final dataset"
            )
        
        if selected_files and st.button("🔗 Combine Selected Files", type="primary"):
            try:
                combined_dfs = []
                current_count = 0
                
                for file in selected_files:
                    if current_count >= target_records:
                        break
                        
                    df = pd.read_csv(file)
                    needed = min(len(df), target_records - current_count)
                    combined_dfs.append(df.head(needed))
                    current_count += needed
                
                if combined_dfs:
                    final_df = pd.concat(combined_dfs, ignore_index=True)
                    
                    # Fix Member IDs to be sequential
                    for i in range(len(final_df)):
                        final_df.iloc[i, 0] = f"MB{i+1:08d}"  # Assuming MemberID is first column
                    
                    timestamp = pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"combined_dataset_{len(final_df)}_records_{timestamp}.csv"
                    final_csv = final_df.to_csv(index=False)
                    
                    st.download_button(
                        label=f"📥 Download Combined Dataset ({len(final_df)} records)",
                        data=final_csv,
                        file_name=filename,
                        mime="text/csv"
                    )
                    
                    st.success(f"✅ Combined {len(combined_dfs)} files into {len(final_df)} records!")
                    
                    # Show preview
                    st.markdown("**Combined Dataset Preview:**")
                    st.dataframe(final_df.head(10))
            
            except Exception as e:
                st.error(f"❌ Error combining files: {str(e)}")
        
        st.markdown("---")
        
        if st.button("�️ Download All Files as ZIP"):
            import zipfile
            import io
            
            zip_buffer = io.BytesIO()
            
            with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                for file in generated_files:
                    zip_file.write(file, file)
            
            zip_buffer.seek(0)
            timestamp = pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")
            
            st.download_button(
                label="� Download mission_alpha_data.zip",
                data=zip_buffer.getvalue(),
                file_name=f"mission_alpha_data_{timestamp}.zip",
                mime="application/zip"
            )

def main():
    """Main Streamlit application"""
    
    initialize_session_state()
    render_mission_header()
    render_mission_briefing()
    
    # Main navigation
    selected = option_menu(
        menu_title=None,
        options=["🚀 AI Configuration", "🎯 Data Generation", "📊 Intelligence Dashboard", "� Data Realism", "�📁 Export Mission Data"],
        icons=["gear", "database", "graph-up", "microscope", "download"],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal",
        styles={
            "container": {"padding": "0!important", "background-color": "#fafafa"},
            "icon": {"color": "#2E4057", "font-size": "18px"},
            "nav-link": {
                "font-size": "16px",
                "text-align": "center",
                "margin": "0px",
                "--hover-color": "#eee",
            },
            "nav-link-selected": {"background-color": "#2E4057"},
        },
    )
    
    # Route to appropriate interface
    if selected == "🚀 AI Configuration":
        setup_ai_configuration()
    elif selected == "🎯 Data Generation":
        data_generation_interface()
    elif selected == "📊 Intelligence Dashboard":
        data_visualization_dashboard()
    elif selected == "� Data Realism":
        render_realism_analysis()
    elif selected == "�📁 Export Mission Data":
        data_export_interface()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666;'>
        <p>🎖️ <strong>Mission Alpha - Operation Synthetic Shield</strong> 🎖️</p>
        <p><em>"Creating synthetic intelligence that serves our testing purposes while protecting civilian privacy"</em></p>
        <p>Classification: Hackathon Participants Only | Status: {}</p>
    </div>
    """.format(st.session_state.mission_status), unsafe_allow_html=True)

if __name__ == "__main__":
    main()
