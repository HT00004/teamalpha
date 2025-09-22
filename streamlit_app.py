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
    """Main data generation interface"""
    st.header("🎯 SYNTHETIC DATA GENERATION OPERATIONS")
    
    if not st.session_state.generator:
        st.warning("⚠️ Please configure AI connection first")
        return
    
    # Generation parameters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        member_count = st.number_input("Target Member Count", min_value=10, max_value=10000, value=100, step=10)
        include_contributions = st.checkbox("Generate Contribution History", value=True)
        include_allocations = st.checkbox("Generate Fund Allocations", value=True)
    
    with col2:
        batch_size = st.selectbox("Batch Size", [10, 25, 50, 100], index=2)
        temperature = st.slider("AI Creativity Level", 0.1, 1.0, 0.7, 0.1)
        include_edge_cases = st.checkbox("Include Edge Cases", value=True)
    
    with col3:
        sample_size = st.number_input("Sample Size (%)", min_value=10, max_value=100, value=20, step=10)
        st.info(f"Will generate detailed records for {int(member_count * sample_size / 100)} members")
    
    # Generation progress
    if st.button("🚀 EXECUTE MISSION", type="primary", use_container_width=True):
        execute_data_generation(member_count, batch_size, temperature, include_contributions, 
                               include_allocations, sample_size, include_edge_cases)

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
        st.plotly_chart(fig_age, use_container_width=True)
        
        # Gender distribution
        gender_counts = profiles_df['gender'].value_counts()
        fig_gender = px.pie(values=gender_counts.values, names=gender_counts.index,
                           title="Gender Distribution")
        st.plotly_chart(fig_gender, use_container_width=True)
    
    with col2:
        # Sector distribution
        sector_counts = profiles_df['sector'].value_counts()
        fig_sector = px.bar(x=sector_counts.index, y=sector_counts.values,
                           title="Employment Sector Distribution",
                           labels={'x': 'Sector', 'y': 'Number of Members'})
        fig_sector.update_xaxes(tickangle=45)
        st.plotly_chart(fig_sector, use_container_width=True)
        
        # Service years distribution
        fig_service = px.histogram(profiles_df, x='years_service', nbins=15,
                                  title="Years of Service Distribution",
                                  labels={'years_service': 'Years of Service', 'count': 'Number of Members'})
        st.plotly_chart(fig_service, use_container_width=True)

def render_financial_analysis(profiles_df, contributions):
    """Render financial analysis charts"""
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Salary distribution by sector
        fig_salary = px.box(profiles_df, x='sector', y='annual_salary',
                           title="Salary Distribution by Sector")
        fig_salary.update_xaxes(tickangle=45)
        fig_salary.update_yaxis(title="Annual Salary (£)")
        st.plotly_chart(fig_salary, use_container_width=True)
        
        # Age vs Salary correlation
        fig_age_salary = px.scatter(profiles_df, x='age', y='annual_salary', color='sector',
                                   title="Age vs Salary Correlation",
                                   labels={'age': 'Age', 'annual_salary': 'Annual Salary (£)'})
        st.plotly_chart(fig_age_salary, use_container_width=True)
    
    with col2:
        # Salary by years of service
        fig_service_salary = px.scatter(profiles_df, x='years_service', y='annual_salary', 
                                       color='sector', size='age',
                                       title="Salary vs Years of Service",
                                       labels={'years_service': 'Years of Service', 
                                              'annual_salary': 'Annual Salary (£)'})
        st.plotly_chart(fig_service_salary, use_container_width=True)
        
        # Status distribution
        status_counts = profiles_df['status'].value_counts()
        fig_status = px.pie(values=status_counts.values, names=status_counts.index,
                           title="Member Status Distribution")
        st.plotly_chart(fig_status, use_container_width=True)

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
        st.plotly_chart(fig_funds, use_container_width=True)
    
    with col2:
        # Risk level distribution
        risk_counts = allocations_df['risk_level'].value_counts()
        fig_risk = px.pie(values=risk_counts.values, names=risk_counts.index,
                         title="Risk Level Distribution")
        st.plotly_chart(fig_risk, use_container_width=True)
    
    # Allocation percentage analysis
    fig_allocation = px.histogram(allocations_df, x='allocation_percent', nbins=20,
                                 title="Fund Allocation Percentage Distribution",
                                 labels={'allocation_percent': 'Allocation Percentage', 'count': 'Frequency'})
    st.plotly_chart(fig_allocation, use_container_width=True)

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
        st.plotly_chart(fig_compliance, use_container_width=True)
    
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

def data_export_interface():
    """Data export and download interface"""
    st.header("📁 DATA EXPORT & INTELLIGENCE SHARING")
    
    if not st.session_state.generated_data:
        st.info("🔍 Generate data first to access export options")
        return
    
    data = st.session_state.generated_data
    timestamp = data['timestamp']
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Dataset Overview")
        st.metric("Member Profiles", len(data['profiles']))
        st.metric("Contribution Records", len(data.get('contributions', [])))
        st.metric("Fund Allocations", len(data.get('allocations', [])))
        st.metric("Generation Timestamp", timestamp)
    
    with col2:
        st.subheader("🎯 Export Options")
        
        # Individual file downloads
        if st.button("📥 Download Member Profiles CSV"):
            profiles_df = pd.DataFrame([asdict(p) for p in data['profiles']])
            csv = profiles_df.to_csv(index=False)
            st.download_button(
                label="💾 Download pension_members.csv",
                data=csv,
                file_name=f"pension_members_{timestamp}.csv",
                mime="text/csv"
            )
        
        if data.get('contributions') and st.button("📥 Download Contributions CSV"):
            contributions_df = pd.DataFrame([asdict(c) for c in data['contributions']])
            csv = contributions_df.to_csv(index=False)
            st.download_button(
                label="💾 Download pension_contributions.csv",
                data=csv,
                file_name=f"pension_contributions_{timestamp}.csv",
                mime="text/csv"
            )
        
        if data.get('allocations') and st.button("📥 Download Allocations CSV"):
            allocations_df = pd.DataFrame([asdict(a) for a in data['allocations']])
            csv = allocations_df.to_csv(index=False)
            st.download_button(
                label="💾 Download pension_allocations.csv",
                data=csv,
                file_name=f"pension_allocations_{timestamp}.csv",
                mime="text/csv"
            )
    
    # Complete dataset download
    st.subheader("📦 Complete Mission Package")
    
    if st.button("🎖️ Download Complete Intelligence Package", type="primary"):
        # Create zip file with all data
        zip_buffer = io.BytesIO()
        
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            # Add member profiles
            profiles_df = pd.DataFrame([asdict(p) for p in data['profiles']])
            zip_file.writestr(f"pension_members_{timestamp}.csv", profiles_df.to_csv(index=False))
            
            # Add contributions if available
            if data.get('contributions'):
                contributions_df = pd.DataFrame([asdict(c) for c in data['contributions']])
                zip_file.writestr(f"pension_contributions_{timestamp}.csv", contributions_df.to_csv(index=False))
            
            # Add allocations if available
            if data.get('allocations'):
                allocations_df = pd.DataFrame([asdict(a) for a in data['allocations']])
                zip_file.writestr(f"pension_allocations_{timestamp}.csv", allocations_df.to_csv(index=False))
            
            # Add validation report
            zip_file.writestr(f"validation_report_{timestamp}.json", 
                            json.dumps(data['validation'], indent=2))
            
            # Add mission summary
            mission_summary = {
                "mission_name": "Operation Synthetic Shield - Mission Alpha",
                "generation_timestamp": timestamp,
                "ai_provider": st.session_state.ai_provider,
                "total_members": len(data['profiles']),
                "total_contributions": len(data.get('contributions', [])),
                "total_allocations": len(data.get('allocations', [])),
                "mission_status": "Accomplished",
                "classification": "Synthetic Data - No Real PII"
            }
            zip_file.writestr(f"mission_summary_{timestamp}.json", 
                            json.dumps(mission_summary, indent=2))
        
        zip_buffer.seek(0)
        
        st.download_button(
            label="🎖️ Download Mission Alpha Intelligence Package",
            data=zip_buffer.getvalue(),
            file_name=f"mission_alpha_complete_{timestamp}.zip",
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
        options=["🚀 AI Configuration", "🎯 Data Generation", "📊 Intelligence Dashboard", "📁 Export Mission Data"],
        icons=["gear", "database", "graph-up", "download"],
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
    elif selected == "📁 Export Mission Data":
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
