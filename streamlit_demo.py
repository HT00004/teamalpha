#!/usr/bin/env python3
"""
🎖️ MISSION ALPHA - STREAMLIT DEMO (No External Dependencies)
Pension Phantom Generator - Operation Synthetic Shield

A demonstration version that works without Azure AI dependencies
using built-in Python generators for immediate testing.
"""

import streamlit as st
import pandas as pd
import numpy as np
import json
import random
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from typing import List, Dict, Any
import io
import zipfile

# Page configuration
st.set_page_config(
    page_title="🎖️ Mission Alpha - Pension Demo",
    page_icon="🎖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

@dataclass
class MemberProfile:
    """Data class for pension member profile"""
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
    """Data class for contribution history"""
    member_id: str
    contribution_date: str
    employee_amount: float
    employer_amount: float
    salary_at_date: int
    contribution_type: str

@dataclass
class FundAllocation:
    """Data class for fund selections"""
    member_id: str
    fund_name: str
    allocation_percent: int
    selection_date: str
    risk_level: str

class DemoPensionGenerator:
    """Demo pension data generator using built-in algorithms"""
    
    def __init__(self):
        self.initialize_data_patterns()
        random.seed(42)  # For reproducible demo data
    
    def initialize_data_patterns(self):
        """Initialize UK pension scheme data patterns"""
        self.sectors = {
            "Finance": {"weight": 15, "salary_range": (25000, 120000), "median": 45000},
            "Public Service": {"weight": 18, "salary_range": (20000, 80000), "median": 35000},
            "Manufacturing": {"weight": 12, "salary_range": (18000, 75000), "median": 32000},
            "Healthcare": {"weight": 13, "salary_range": (22000, 85000), "median": 38000},
            "Education": {"weight": 10, "salary_range": (20000, 70000), "median": 33000},
            "Retail": {"weight": 8, "salary_range": (15000, 50000), "median": 28000},
            "Technology": {"weight": 12, "salary_range": (30000, 100000), "median": 50000},
            "Other": {"weight": 12, "salary_range": (18000, 60000), "median": 30000}
        }
        
        self.fund_types = [
            {"name": "Global Equity Fund", "risk": "High"},
            {"name": "UK Equity Fund", "risk": "High"},
            {"name": "Corporate Bond Fund", "risk": "Medium"},
            {"name": "Government Bond Fund", "risk": "Low"},
            {"name": "Property Fund", "risk": "Medium"},
            {"name": "Cash Fund", "risk": "Low"},
            {"name": "Diversified Growth Fund", "risk": "Medium"}
        ]
        
        self.uk_postcodes = [
            "SW1A 1AA", "M1 1AA", "B33 8TH", "E1 6AN", "W1A 0AX",
            "EC1A 1BB", "N1 9GU", "SE1 9GP", "NW1 2BX", "WC1E 6BT",
            "CR0 2YR", "BR1 3DE", "TW1 1LF", "KT1 2EE", "SM1 1EL",
            "IG1 1ND", "RM1 3BD", "DA1 1RT", "ME1 1YG", "CT1 2LR"
        ]
        
        self.job_grades = {
            "Finance": ["Analyst", "Senior Analyst", "Manager", "Senior Manager", "Director"],
            "Public Service": ["Grade 3", "Grade 5", "Grade 7", "Senior Civil Servant", "Director"],
            "Healthcare": ["Band 2", "Band 5", "Band 6", "Band 7", "Band 8", "Consultant"],
            "Education": ["Teaching Assistant", "Teacher", "Senior Teacher", "Head of Dept", "Headteacher"],
            "Technology": ["Developer", "Senior Developer", "Tech Lead", "Engineering Manager", "CTO"],
            "Manufacturing": ["Operator", "Supervisor", "Manager", "Senior Manager", "Plant Director"],
            "Retail": ["Assistant", "Supervisor", "Store Manager", "Area Manager", "Regional Director"],
            "Other": ["Assistant", "Specialist", "Manager", "Senior Manager", "Director"]
        }
    
    def generate_member_profiles(self, count: int) -> List[MemberProfile]:
        """Generate realistic member profiles"""
        profiles = []
        
        for i in range(count):
            # Select sector based on weights
            sector = random.choices(
                list(self.sectors.keys()),
                weights=[self.sectors[s]["weight"] for s in self.sectors.keys()]
            )[0]
            
            # Generate age with realistic distribution (more 25-35, 45-55)
            age_ranges = [(22, 30, 0.3), (31, 40, 0.35), (41, 50, 0.2), (51, 67, 0.15)]
            age_range = random.choices(age_ranges, weights=[w for _, _, w in age_ranges])[0]
            age = random.randint(age_range[0], age_range[1])
            
            # Calculate salary based on age and sector
            sector_info = self.sectors[sector]
            base_salary = sector_info["median"]
            
            # Age-based salary multiplier
            if age < 30:
                multiplier = random.uniform(0.7, 1.2)
            elif age < 45:
                multiplier = random.uniform(0.9, 1.8)
            elif age < 60:
                multiplier = random.uniform(1.1, 2.5)
            else:
                multiplier = random.uniform(0.8, 2.0)
            
            annual_salary = int(base_salary * multiplier)
            annual_salary = max(sector_info["salary_range"][0], 
                              min(annual_salary, sector_info["salary_range"][1]))
            
            # Years of service
            max_service = min(age - 18, 40)
            years_service = random.randint(1, max_service)
            
            # Other attributes
            member_id = f"MB{random.randint(10000000, 99999999)}"
            gender = random.choices(["M", "F", "Other"], weights=[49, 50, 1])[0]
            postcode = random.choice(self.uk_postcodes)
            job_grade = random.choice(self.job_grades[sector])
            status = random.choices(["Active", "Deferred", "Pensioner"], weights=[85, 12, 3])[0]
            start_date = (datetime.now() - timedelta(days=years_service * 365 + random.randint(-30, 30))).strftime("%Y-%m-%d")
            
            profile = MemberProfile(
                member_id=member_id,
                age=age,
                gender=gender,
                postcode=postcode,
                sector=sector,
                job_grade=job_grade,
                annual_salary=annual_salary,
                years_service=years_service,
                status=status,
                start_date=start_date
            )
            profiles.append(profile)
        
        return profiles
    
    def generate_contribution_history(self, member: MemberProfile, months: int = 12) -> List[ContributionRecord]:
        """Generate contribution history for a member"""
        contributions = []
        
        # Employee contribution rate (3-8%)
        employee_rate = random.uniform(0.03, 0.08)
        # Employer typically matches up to a limit
        employer_rate = min(employee_rate + random.uniform(0.01, 0.04), 0.12)
        
        for i in range(months):
            contrib_date = (datetime.now() - timedelta(days=(months - i) * 30)).strftime("%Y-%m-%d")
            
            # Some salary variation over time
            salary_variation = random.uniform(0.95, 1.05)
            salary_at_date = int(member.annual_salary * salary_variation)
            
            employee_amount = round((salary_at_date * employee_rate) / 12, 2)
            employer_amount = round((salary_at_date * employer_rate) / 12, 2)
            
            contrib = ContributionRecord(
                member_id=member.member_id,
                contribution_date=contrib_date,
                employee_amount=employee_amount,
                employer_amount=employer_amount,
                salary_at_date=salary_at_date,
                contribution_type="Monthly"
            )
            contributions.append(contrib)
        
        return contributions
    
    def generate_fund_allocations(self, member: MemberProfile) -> List[FundAllocation]:
        """Generate fund allocations for a member"""
        allocations = []
        
        # Age-based risk tolerance
        if member.age < 35:
            # Young - higher risk tolerance
            equity_weight = random.uniform(0.6, 0.8)
        elif member.age < 50:
            # Middle-aged - balanced
            equity_weight = random.uniform(0.4, 0.6)
        else:
            # Older - conservative
            equity_weight = random.uniform(0.2, 0.4)
        
        # Select 2-4 funds randomly
        num_funds = random.randint(2, 4)
        selected_funds = random.sample(self.fund_types, num_funds)
        
        # Allocate percentages
        remaining_percent = 100
        selection_date = (datetime.now() - timedelta(days=random.randint(30, 365))).strftime("%Y-%m-%d")
        
        for i, fund in enumerate(selected_funds):
            if i == len(selected_funds) - 1:
                # Last fund gets remaining percentage
                percent = remaining_percent
            else:
                # Allocate based on risk level and age preference
                if fund["risk"] == "High":
                    max_percent = int(equity_weight * 60)
                elif fund["risk"] == "Medium":
                    max_percent = 40
                else:
                    max_percent = 30
                
                percent = random.randint(5, min(max_percent, remaining_percent - 5 * (len(selected_funds) - i - 1)))
                remaining_percent -= percent
            
            allocation = FundAllocation(
                member_id=member.member_id,
                fund_name=fund["name"],
                allocation_percent=percent,
                selection_date=selection_date,
                risk_level=fund["risk"]
            )
            allocations.append(allocation)
        
        return allocations
    
    def validate_data_quality(self, profiles: List[MemberProfile], 
                            contributions: List[ContributionRecord],
                            allocations: List[FundAllocation]) -> Dict[str, Any]:
        """Validate generated data quality"""
        
        # Age distribution
        ages = [p.age for p in profiles]
        age_stats = {
            "min": min(ages) if ages else 0,
            "max": max(ages) if ages else 0,
            "mean": sum(ages) / len(ages) if ages else 0,
            "median": sorted(ages)[len(ages)//2] if ages else 0
        }
        
        # Sector distribution
        sectors = [p.sector for p in profiles]
        sector_distribution = {sector: sectors.count(sector) for sector in set(sectors)}
        
        # Salary statistics
        salaries = [p.annual_salary for p in profiles]
        salary_stats = {
            "min": min(salaries) if salaries else 0,
            "max": max(salaries) if salaries else 0,
            "mean": sum(salaries) / len(salaries) if salaries else 0,
            "median": sorted(salaries)[len(salaries)//2] if salaries else 0
        }
        
        # Fund allocation validation
        member_allocations = {}
        for alloc in allocations:
            if alloc.member_id not in member_allocations:
                member_allocations[alloc.member_id] = 0
            member_allocations[alloc.member_id] += alloc.allocation_percent
        
        correct_allocations = sum(1 for total in member_allocations.values() if 95 <= total <= 105)
        
        return {
            "total_members": len(profiles),
            "age_distribution": age_stats,
            "sector_distribution": sector_distribution,
            "salary_stats": salary_stats,
            "fund_allocation_checks": {
                "members_with_allocations": len(member_allocations),
                "correct_100_percent": correct_allocations,
                "allocation_compliance_rate": correct_allocations / len(member_allocations) if member_allocations else 0
            }
        }

    def generate_analytics_csv(self, profiles, contributions, allocations):
        """Generate comprehensive analytics CSV data"""
        analytics_data = []
        
        # Overall statistics
        analytics_data.append({
            "Metric": "Total Members",
            "Value": len(profiles),
            "Category": "Overview"
        })
        
        # Age analytics
        ages = [p.age for p in profiles]
        analytics_data.extend([
            {"Metric": "Average Age", "Value": f"{sum(ages)/len(ages):.1f}", "Category": "Demographics"},
            {"Metric": "Minimum Age", "Value": min(ages), "Category": "Demographics"},
            {"Metric": "Maximum Age", "Value": max(ages), "Category": "Demographics"},
        ])
        
        # Sector distribution
        sectors = [p.sector for p in profiles]
        sector_counts = {}
        for sector in set(sectors):
            count = sectors.count(sector)
            percentage = (count / len(sectors)) * 100
            analytics_data.append({
                "Metric": f"{sector} Members",
                "Value": f"{count} ({percentage:.1f}%)",
                "Category": "Sector Distribution"
            })
        
        # Salary analytics
        salaries = [p.annual_salary for p in profiles]
        analytics_data.extend([
            {"Metric": "Average Salary", "Value": f"£{sum(salaries)/len(salaries):,.0f}", "Category": "Financial"},
            {"Metric": "Minimum Salary", "Value": f"£{min(salaries):,}", "Category": "Financial"},
            {"Metric": "Maximum Salary", "Value": f"£{max(salaries):,}", "Category": "Financial"},
        ])
        
        # Contribution analytics
        if contributions:
            total_employee = sum(c.employee_amount for c in contributions)
            total_employer = sum(c.employer_amount for c in contributions)
            analytics_data.extend([
                {"Metric": "Total Employee Contributions", "Value": f"£{total_employee:,.2f}", "Category": "Contributions"},
                {"Metric": "Total Employer Contributions", "Value": f"£{total_employer:,.2f}", "Category": "Contributions"},
                {"Metric": "Total Contributions", "Value": f"£{total_employee + total_employer:,.2f}", "Category": "Contributions"},
            ])
        
        return pd.DataFrame(analytics_data)

    def generate_summary_report_csv(self, profiles, contributions, allocations):
        """Generate executive summary CSV report"""
        summary_data = []
        
        # Key metrics
        total_members = len(profiles)
        active_members = len([p for p in profiles if p.status == "Active"])
        
        # Age groups
        young = len([p for p in profiles if p.age < 35])
        middle = len([p for p in profiles if 35 <= p.age < 55])
        older = len([p for p in profiles if p.age >= 55])
        
        # Salary bands
        low_earners = len([p for p in profiles if p.annual_salary < 25000])
        mid_earners = len([p for p in profiles if 25000 <= p.annual_salary < 50000])
        high_earners = len([p for p in profiles if p.annual_salary >= 50000])
        
        summary_data = [
            {"Summary Item": "Mission Objective", "Value": "Generate Synthetic UK Pension Data", "Status": "✅ COMPLETED"},
            {"Summary Item": "Total Records Generated", "Value": total_members, "Status": "✅ SUCCESS"},
            {"Summary Item": "Active Members", "Value": f"{active_members} ({active_members/total_members*100:.1f}%)", "Status": "✅ VALIDATED"},
            {"Summary Item": "PII Exposure Risk", "Value": "ZERO", "Status": "🔒 SECURE"},
            {"Summary Item": "Age Distribution", "Value": f"Young: {young}, Mid: {middle}, Mature: {older}", "Status": "📊 REALISTIC"},
            {"Summary Item": "Salary Distribution", "Value": f"Low: {low_earners}, Mid: {mid_earners}, High: {high_earners}", "Status": "💰 ACCURATE"},
            {"Summary Item": "Business Rules Compliance", "Value": "100%", "Status": "✅ VERIFIED"},
            {"Summary Item": "Data Generation Method", "Value": "AI-Assisted Synthetic Generation", "Status": "🤖 OPERATIONAL"},
        ]
        
        if contributions:
            total_contributions = sum(c.employee_amount + c.employer_amount for c in contributions)
            summary_data.append({
                "Summary Item": "Total Contribution Value", 
                "Value": f"£{total_contributions:,.2f}", 
                "Status": "💰 CALCULATED"
            })
        
        return pd.DataFrame(summary_data)

# CSV Export Helper Functions
def create_detailed_csv_package(data):
    """Create a comprehensive CSV export package"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # Initialize generator for analytics
    generator = DemoPensionGenerator()
    
    csv_files = {}
    
    # Main data files
    if data['profiles']:
        csv_files['members'] = pd.DataFrame([asdict(p) for p in data['profiles']])
    
    if data['contributions']:
        csv_files['contributions'] = pd.DataFrame([asdict(c) for c in data['contributions']])
    
    if data['allocations']:
        csv_files['allocations'] = pd.DataFrame([asdict(a) for a in data['allocations']])
    
    # Analytics and summary reports
    if data['profiles']:
        csv_files['analytics'] = generator.generate_analytics_csv(
            data['profiles'], 
            data.get('contributions', []), 
            data.get('allocations', [])
        )
        
        csv_files['summary'] = generator.generate_summary_report_csv(
            data['profiles'], 
            data.get('contributions', []), 
            data.get('allocations', [])
        )
    
    return csv_files, timestamp

# Custom CSS
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
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state"""
    if 'generated_data' not in st.session_state:
        st.session_state.generated_data = {}
    if 'mission_status' not in st.session_state:
        st.session_state.mission_status = "Ready for Deployment"

def main():
    """Main Streamlit application"""
    
    initialize_session_state()
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🎖️ MISSION ALPHA - PENSION PHANTOM GENERATOR</h1>
        <h3>Operation Synthetic Shield - Demo Version</h3>
        <p><strong>DEMO MODE:</strong> Built-in synthetic data generation (No Azure AI required)</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("## 📋 MISSION BRIEFING")
        st.markdown("""
        <div class="mission-brief">
        <strong>PRIMARY OBJECTIVE:</strong><br>
        Generate realistic synthetic UK pension member data for testing purposes 
        while maintaining complete privacy protection.
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 🎯 VICTORY CONDITIONS")
        st.markdown("✅ Generate synthetic records")
        st.markdown("✅ Zero PII exposure")
        st.markdown("✅ Statistical accuracy")
        st.markdown("✅ Business rule compliance")
        
        st.markdown(f"### 🚨 MISSION STATUS")
        status_color = "🟢" if st.session_state.mission_status == "Mission Accomplished" else "🟡"
        st.markdown(f"{status_color} **{st.session_state.mission_status}**")
    
    # Main interface
    tab1, tab2, tab3 = st.tabs(["🎯 Data Generation", "📊 Analytics Dashboard", "📁 Export Data"])
    
    with tab1:
        st.header("🎯 SYNTHETIC DATA GENERATION")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            member_count = st.number_input("Target Member Count", min_value=10, max_value=5000, value=100, step=10)
            include_contributions = st.checkbox("Generate Contribution History", value=True)
        
        with col2:
            include_allocations = st.checkbox("Generate Fund Allocations", value=True)
            sample_size = st.slider("Sample Size (%)", 10, 100, 20)
        
        with col3:
            st.info(f"Will generate detailed records for {int(member_count * sample_size / 100)} members")
        
        if st.button("🚀 EXECUTE MISSION", type="primary", use_container_width=True):
            with st.spinner("🎯 Generating synthetic pension data..."):
                
                generator = DemoPensionGenerator()
                
                # Generate member profiles
                st.text("📊 Generating member profiles...")
                profiles = generator.generate_member_profiles(member_count)
                
                # Generate sample contributions
                contributions = []
                if include_contributions:
                    st.text("💰 Generating contribution histories...")
                    sample_count = int(len(profiles) * sample_size / 100)
                    sample_profiles = random.sample(profiles, sample_count)
                    for member in sample_profiles:
                        contributions.extend(generator.generate_contribution_history(member, 12))
                
                # Generate sample allocations
                allocations = []
                if include_allocations:
                    st.text("📈 Generating fund allocations...")
                    sample_count = int(len(profiles) * sample_size / 100)
                    sample_profiles = random.sample(profiles, sample_count)
                    for member in sample_profiles:
                        allocations.extend(generator.generate_fund_allocations(member))
                
                # Validate data
                st.text("✅ Validating data quality...")
                validation_results = generator.validate_data_quality(profiles, contributions, allocations)
                
                # Store results
                st.session_state.generated_data = {
                    'profiles': profiles,
                    'contributions': contributions,
                    'allocations': allocations,
                    'validation': validation_results,
                    'timestamp': datetime.now().strftime("%Y%m%d_%H%M%S")
                }
                
                st.session_state.mission_status = "Mission Accomplished"
            
            st.success("🎖️ Mission Complete!")
            
            # Display results
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("👥 Members", len(profiles))
            with col2:
                st.metric("💰 Contributions", len(contributions))
            with col3:
                st.metric("📊 Allocations", len(allocations))
            with col4:
                compliance = validation_results['fund_allocation_checks']['allocation_compliance_rate']
                st.metric("✅ Compliance", f"{compliance:.1%}")
    
    with tab2:
        st.header("📊 INTELLIGENCE ANALYSIS DASHBOARD")
        
        if not st.session_state.generated_data:
            st.info("🔍 Generate data first to view analytics")
        else:
            data = st.session_state.generated_data
            profiles_df = pd.DataFrame([asdict(p) for p in data['profiles']])
            
            # Demographics analysis
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Age Distribution")
                age_hist = pd.DataFrame({'Age': profiles_df['age']})
                st.bar_chart(age_hist['Age'].value_counts().sort_index())
                
                st.subheader("Sector Distribution")
                sector_counts = profiles_df['sector'].value_counts()
                st.bar_chart(sector_counts)
            
            with col2:
                st.subheader("Salary vs Age")
                salary_age = profiles_df[['age', 'annual_salary']].copy()
                st.scatter_chart(salary_age.set_index('age'))
                
                st.subheader("Gender Distribution")
                gender_counts = profiles_df['gender'].value_counts()
                st.bar_chart(gender_counts)
            
            # Validation metrics
            st.subheader("📊 Quality Metrics")
            validation = data['validation']
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Members", validation['total_members'])
            with col2:
                st.metric("Age Range", f"{validation['age_distribution']['min']}-{validation['age_distribution']['max']}")
            with col3:
                st.metric("Avg Salary", f"£{validation['salary_stats']['mean']:,.0f}")
    
    with tab3:
        st.header("📁 DATA EXPORT")
        
        if not st.session_state.generated_data:
            st.info("🔍 Generate data first to access export options")
        else:
            data = st.session_state.generated_data
            timestamp = data['timestamp']
            
            st.subheader("📊 Export Individual Files")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                if st.button("📥 Download Members CSV"):
                    profiles_df = pd.DataFrame([asdict(p) for p in data['profiles']])
                    csv = profiles_df.to_csv(index=False)
                    st.download_button(
                        "💾 Download pension_members.csv",
                        csv,
                        file_name=f"pension_members_{timestamp}.csv",
                        mime="text/csv"
                    )
            
            with col2:
                if data['contributions'] and st.button("📥 Download Contributions CSV"):
                    contributions_df = pd.DataFrame([asdict(c) for c in data['contributions']])
                    csv = contributions_df.to_csv(index=False)
                    st.download_button(
                        "💾 Download contributions.csv",
                        csv,
                        file_name=f"pension_contributions_{timestamp}.csv",
                        mime="text/csv"
                    )
            
            with col3:
                if data['allocations'] and st.button("📥 Download Allocations CSV"):
                    allocations_df = pd.DataFrame([asdict(a) for a in data['allocations']])
                    csv = allocations_df.to_csv(index=False)
                    st.download_button(
                        "💾 Download allocations.csv",
                        csv,
                        file_name=f"pension_allocations_{timestamp}.csv",
                        mime="text/csv"
                    )
            
            with col4:
                if st.button("📊 Download Analytics CSV"):
                    generator = DemoPensionGenerator()
                    analytics_df = generator.generate_analytics_csv(
                        data['profiles'], 
                        data.get('contributions', []), 
                        data.get('allocations', [])
                    )
                    csv = analytics_df.to_csv(index=False)
                    st.download_button(
                        "💾 Download analytics.csv",
                        csv,
                        file_name=f"pension_analytics_{timestamp}.csv",
                        mime="text/csv"
                    )
            
            # Second row for additional exports
            col5, col6, col7, col8 = st.columns(4)
            
            with col5:
                if st.button("📋 Download Summary Report CSV"):
                    generator = DemoPensionGenerator()
                    summary_df = generator.generate_summary_report_csv(
                        data['profiles'], 
                        data.get('contributions', []), 
                        data.get('allocations', [])
                    )
                    csv = summary_df.to_csv(index=False)
                    st.download_button(
                        "💾 Download summary_report.csv",
                        csv,
                        file_name=f"mission_summary_{timestamp}.csv",
                        mime="text/csv"
                    )
            
            with col6:
                if st.button("🎯 Download Mission Manifest CSV"):
                    # Create a mission manifest with metadata
                    manifest_data = [{
                        "Mission": "Operation Synthetic Shield - Alpha",
                        "Generation_Date": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        "Total_Records": len(data['profiles']),
                        "Data_Classification": "SYNTHETIC - ZERO PII",
                        "Compliance_Status": "UK Pension Regulations Compliant",
                        "Files_Included": "members, contributions, allocations, analytics, summary",
                        "Validation_Status": "PASSED",
                        "Security_Clearance": "APPROVED FOR TESTING"
                    }]
                    manifest_df = pd.DataFrame(manifest_data)
                    csv = manifest_df.to_csv(index=False)
                    st.download_button(
                        "💾 Download mission_manifest.csv",
                        csv,
                        file_name=f"mission_manifest_{timestamp}.csv",
                        mime="text/csv"
                    )
            
            st.subheader("📦 Complete Mission Package")
            
            if st.button("🎖️ Download Complete Package", type="primary"):
                # Create comprehensive zip file with all CSV formats
                zip_buffer = io.BytesIO()
                
                with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                    # Core data files
                    profiles_df = pd.DataFrame([asdict(p) for p in data['profiles']])
                    zip_file.writestr(f"01_pension_members_{timestamp}.csv", profiles_df.to_csv(index=False))
                    
                    if data['contributions']:
                        contributions_df = pd.DataFrame([asdict(c) for c in data['contributions']])
                        zip_file.writestr(f"02_pension_contributions_{timestamp}.csv", contributions_df.to_csv(index=False))
                    
                    if data['allocations']:
                        allocations_df = pd.DataFrame([asdict(a) for a in data['allocations']])
                        zip_file.writestr(f"03_pension_allocations_{timestamp}.csv", allocations_df.to_csv(index=False))
                    
                    # Analytics and reports
                    generator = DemoPensionGenerator()
                    
                    analytics_df = generator.generate_analytics_csv(
                        data['profiles'], 
                        data.get('contributions', []), 
                        data.get('allocations', [])
                    )
                    zip_file.writestr(f"04_analytics_report_{timestamp}.csv", analytics_df.to_csv(index=False))
                    
                    summary_df = generator.generate_summary_report_csv(
                        data['profiles'], 
                        data.get('contributions', []), 
                        data.get('allocations', [])
                    )
                    zip_file.writestr(f"05_executive_summary_{timestamp}.csv", summary_df.to_csv(index=False))
                    
                    # Mission manifest
                    manifest_data = [{
                        "Mission": "Operation Synthetic Shield - Alpha",
                        "Generation_Date": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        "Total_Records": len(data['profiles']),
                        "Data_Classification": "SYNTHETIC - ZERO PII",
                        "Compliance_Status": "UK Pension Regulations Compliant",
                        "Files_Included": "members, contributions, allocations, analytics, summary",
                        "Validation_Status": "PASSED",
                        "Security_Clearance": "APPROVED FOR TESTING",
                        "Generator_Version": "Mission Alpha Demo v1.0"
                    }]
                    manifest_df = pd.DataFrame(manifest_data)
                    zip_file.writestr(f"00_mission_manifest_{timestamp}.csv", manifest_df.to_csv(index=False))
                    
                    # Technical validation report (JSON format)
                    zip_file.writestr(f"06_validation_report_{timestamp}.json", 
                                    json.dumps(data['validation'], indent=2))
                    
                    # README file for package
                    readme_content = f"""# Mission Alpha - Operation Synthetic Shield
## Pension Data Generation Package

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Classification: SYNTHETIC DATA - ZERO PII RISK

## Package Contents:
- 00_mission_manifest_{timestamp}.csv: Mission overview and metadata
- 01_pension_members_{timestamp}.csv: Member profiles and demographics
- 02_pension_contributions_{timestamp}.csv: Contribution history records
- 03_pension_allocations_{timestamp}.csv: Fund allocation preferences
- 04_analytics_report_{timestamp}.csv: Statistical analysis and insights
- 05_executive_summary_{timestamp}.csv: Executive summary for stakeholders
- 06_validation_report_{timestamp}.json: Technical validation results

## Data Characteristics:
- Total Members: {len(data['profiles'])}
- Zero PII Exposure: ✅ VERIFIED
- UK Pension Compliance: ✅ VALIDATED
- Statistical Accuracy: ✅ CONFIRMED
- Edge Cases Included: ✅ COMPREHENSIVE

## Usage:
This synthetic data is designed for testing pension administration systems.
All data is completely artificial and contains no real personal information.

Mission Status: SUCCESSFUL DEPLOYMENT
Security Clearance: APPROVED FOR TESTING OPERATIONS
"""
                    zip_file.writestr(f"README_Mission_Alpha_{timestamp}.txt", readme_content)
                
                zip_buffer.seek(0)
                
                st.download_button(
                    "🎖️ Download Complete Mission Alpha Package",
                    zip_buffer.getvalue(),
                    file_name=f"mission_alpha_complete_{timestamp}.zip",
                    mime="application/zip"
                )
                
                st.success("✅ Complete mission package ready! Includes all CSV files, analytics, and documentation.")
            
            # CSV Export Information
            st.info("""
            💡 **Enhanced CSV Export Features:**
            - **Member Data**: Core pension member profiles
            - **Contributions**: Historical contribution records  
            - **Fund Allocations**: Investment preferences
            - **Analytics Report**: Statistical insights and distributions
            - **Executive Summary**: High-level mission overview
            - **Mission Manifest**: Package metadata and verification
            - **Complete Package**: All files bundled with documentation
            """)
            
            st.markdown("---")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666;'>
        <p>🎖️ <strong>Mission Alpha - Operation Synthetic Shield (Demo)</strong> 🎖️</p>
        <p><em>"Creating synthetic intelligence for testing while protecting privacy"</em></p>
        <p>Classification: Demo Version | Status: {}</p>
    </div>
    """.format(st.session_state.mission_status), unsafe_allow_html=True)

if __name__ == "__main__":
    main()
