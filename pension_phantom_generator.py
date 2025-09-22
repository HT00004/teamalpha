#!/usr/bin/env python3
"""
🎖️ MISSION ALPHA - PENSION PHANTOM GENERATOR
Operation Synthetic Shield - Data Generation Division

This module implements AI-driven synthetic pension data generation using Azure AI Foundry.
"""

import os
import json
import csv
import random
import uuid
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from dotenv import load_dotenv

# Azure AI Inference
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential

# Load environment variables
load_dotenv()

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

class PensionPhantomGenerator:
    """
    🎯 Main AI-driven pension data generator
    
    Uses Azure AI Foundry GPT-4o for realistic synthetic data generation
    following UK pension scheme patterns and regulations.
    """
    
    def __init__(self):
        """Initialize the generator with Azure AI configuration"""
        self.setup_ai_client()
        self.load_config()
        self.initialize_data_patterns()
        
    def setup_ai_client(self):
        """Configure Azure AI Foundry or GitHub Models client"""
        # Try Azure AI Foundry first
        azure_endpoint = os.getenv("AZURE_ENDPOINT")
        azure_key = os.getenv("AZURE_API_KEY")
        
        if azure_endpoint and azure_key:
            self.client = ChatCompletionsClient(
                endpoint=azure_endpoint,
                credential=AzureKeyCredential(azure_key)
            )
            self.model = os.getenv("MODEL_DEPLOYMENT_NAME", "gpt-4o")
            self.provider = "Azure AI Foundry"
            print(f"🚀 Connected to Azure AI Foundry - Model: {self.model}")
        else:
            # Fallback to GitHub Models
            github_token = os.getenv("GITHUB_TOKEN")
            if github_token:
                self.client = ChatCompletionsClient(
                    endpoint="https://models.github.ai/inference",
                    credential=AzureKeyCredential(github_token)
                )
                self.model = "openai/gpt-4.1"
                self.provider = "GitHub Models"
                print(f"🚀 Connected to GitHub Models - Model: {self.model}")
            else:
                raise ValueError("❌ No AI credentials found. Set AZURE_API_KEY or GITHUB_TOKEN")
    
    def load_config(self):
        """Load generation configuration"""
        self.member_count = int(os.getenv("MEMBER_COUNT", 2500))
        self.output_format = os.getenv("OUTPUT_FORMAT", "csv")
        self.include_edge_cases = os.getenv("INCLUDE_EDGE_CASES", "true").lower() == "true"
        
        print(f"📊 Configuration: {self.member_count} members, format: {self.output_format}")
        
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
            {"name": "Global Equity Fund", "risk": "High", "typical_allocation": "40-70%"},
            {"name": "UK Equity Fund", "risk": "High", "typical_allocation": "10-30%"},
            {"name": "Corporate Bond Fund", "risk": "Medium", "typical_allocation": "20-40%"},
            {"name": "Government Bond Fund", "risk": "Low", "typical_allocation": "5-20%"},
            {"name": "Property Fund", "risk": "Medium", "typical_allocation": "5-15%"},
            {"name": "Cash Fund", "risk": "Low", "typical_allocation": "0-20%"},
            {"name": "Diversified Growth Fund", "risk": "Medium", "typical_allocation": "20-60%"},
            {"name": "Ethical Fund", "risk": "Medium", "typical_allocation": "0-30%"}
        ]
        
        print("✅ Data patterns initialized")

    def generate_ai_prompt(self, prompt_type: str, context: Dict[str, Any] = None) -> str:
        """Generate AI prompts for different data generation tasks"""
        
        base_context = """
        You are a UK pension scheme data expert. Generate realistic synthetic data that:
        - Follows UK pension regulations and typical patterns
        - Reflects realistic demographics and employment patterns
        - Maintains statistical accuracy for business validation
        - Contains zero real personal information
        - Includes realistic edge cases and variations
        """
        
        prompts = {
            "member_profiles": f"""
            {base_context}
            
            Generate {context.get('count', 10)} realistic UK pension scheme member profiles in JSON format.
            
            Requirements:
            - Age: 22-67 (realistic UK workforce distribution)
            - Gender: Balanced distribution (M/F/Other)
            - Postcodes: Valid UK format, clustered by employment patterns
            - Employment sectors: {list(self.sectors.keys())}
            - Salaries: Age and sector appropriate (career progression patterns)
            - Service years: Realistic for age and sector
            - Status: Mostly 'Active', some 'Deferred', few 'Pensioner'
            
            Output as JSON array with fields: age, gender, postcode, sector, job_grade, annual_salary, years_service, status.
            Ensure realistic correlations (older members = higher salaries, longer service).
            """,
            
            "contribution_patterns": f"""
            {base_context}
            
            Generate monthly contribution patterns for member: {context.get('member_info', 'sample member')}
            
            Requirements:
            - Employee contributions: 3-8% of salary (auto-enrollment minimum 3%)
            - Employer contributions: 3-12% of salary (often match employee up to limit)
            - Realistic variations: salary changes, contribution rate changes, career breaks
            - UK pension annual allowance compliance
            
            Generate {context.get('months', 12)} months of contribution history in JSON format.
            Fields: contribution_date, employee_amount, employer_amount, salary_at_date, contribution_type.
            """,
            
            "fund_allocations": f"""
            {base_context}
            
            Generate realistic fund allocations for member: {context.get('member_info', 'sample member')}
            
            Available funds: {[f["name"] for f in self.fund_types]}
            
            Requirements:
            - Total allocation must equal exactly 100%
            - Age-appropriate risk tolerance:
              * 22-35: Higher equity (60-80%)
              * 36-50: Balanced (40-60% equity)
              * 51-67: Conservative (20-40% equity)
            - Realistic fund combinations (most members use 2-4 funds)
            
            Output JSON array with fields: fund_name, allocation_percent, selection_date, risk_level.
            """
        }
        
        return prompts.get(prompt_type, "Invalid prompt type")

    def call_ai_model(self, prompt: str, temperature: float = 0.7) -> str:
        """Make API call to AI model"""
        try:
            response = self.client.complete(
                messages=[
                    SystemMessage("You are a UK pension data expert generating realistic synthetic data."),
                    UserMessage(prompt)
                ],
                temperature=temperature,
                top_p=0.9,
                model=self.model
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"❌ AI API Error: {e}")
            return None

    def parse_ai_response(self, response: str) -> List[Dict]:
        """Parse JSON response from AI model"""
        if not response:
            return []
            
        try:
            # Clean response and extract JSON
            response = response.strip()
            if response.startswith("```json"):
                response = response[7:]
            if response.endswith("```"):
                response = response[:-3]
            
            # Parse JSON
            data = json.loads(response)
            if isinstance(data, dict):
                return [data]
            return data
        except json.JSONDecodeError as e:
            print(f"❌ JSON Parse Error: {e}")
            print(f"Response: {response[:200]}...")
            return []

    def generate_member_profiles_batch(self, batch_size: int = 50) -> List[MemberProfile]:
        """Generate a batch of member profiles using AI"""
        prompt = self.generate_ai_prompt("member_profiles", {"count": batch_size})
        response = self.call_ai_model(prompt)
        
        profiles = []
        ai_data = self.parse_ai_response(response)
        
        for data in ai_data:
            try:
                # Generate unique member ID
                member_id = f"MB{random.randint(10000000, 99999999)}"
                
                # Calculate start date based on service years
                years_service = data.get('years_service', random.randint(1, 20))
                start_date = (datetime.now() - timedelta(days=years_service * 365)).strftime("%Y-%m-%d")
                
                profile = MemberProfile(
                    member_id=member_id,
                    age=data.get('age', random.randint(22, 67)),
                    gender=data.get('gender', random.choice(['M', 'F'])),
                    postcode=data.get('postcode', 'SW1A 1AA'),
                    sector=data.get('sector', 'Other'),
                    job_grade=data.get('job_grade', 'Grade 1'),
                    annual_salary=data.get('annual_salary', 30000),
                    years_service=years_service,
                    status=data.get('status', 'Active'),
                    start_date=start_date
                )
                profiles.append(profile)
                
            except Exception as e:
                print(f"⚠️ Error creating profile: {e}")
                continue
                
        return profiles

    def generate_contribution_history(self, member: MemberProfile, months: int = 12) -> List[ContributionRecord]:
        """Generate contribution history for a member"""
        context = {
            "member_info": f"Age: {member.age}, Sector: {member.sector}, Salary: £{member.annual_salary:,}, Service: {member.years_service} years",
            "months": months
        }
        
        prompt = self.generate_ai_prompt("contribution_patterns", context)
        response = self.call_ai_model(prompt)
        
        contributions = []
        ai_data = self.parse_ai_response(response)
        
        for i, data in enumerate(ai_data):
            try:
                # Calculate date
                contrib_date = (datetime.now() - timedelta(days=(months - i) * 30)).strftime("%Y-%m-%d")
                
                contrib = ContributionRecord(
                    member_id=member.member_id,
                    contribution_date=contrib_date,
                    employee_amount=data.get('employee_amount', member.annual_salary * 0.05 / 12),
                    employer_amount=data.get('employer_amount', member.annual_salary * 0.05 / 12),
                    salary_at_date=data.get('salary_at_date', member.annual_salary),
                    contribution_type=data.get('contribution_type', 'Monthly')
                )
                contributions.append(contrib)
                
            except Exception as e:
                print(f"⚠️ Error creating contribution: {e}")
                continue
                
        return contributions

    def generate_fund_allocations(self, member: MemberProfile) -> List[FundAllocation]:
        """Generate fund allocations for a member"""
        context = {
            "member_info": f"Age: {member.age}, Risk Profile: {'Conservative' if member.age > 55 else 'Moderate' if member.age > 40 else 'Growth'}"
        }
        
        prompt = self.generate_ai_prompt("fund_allocations", context)
        response = self.call_ai_model(prompt)
        
        allocations = []
        ai_data = self.parse_ai_response(response)
        
        selection_date = (datetime.now() - timedelta(days=random.randint(30, 365))).strftime("%Y-%m-%d")
        
        for data in ai_data:
            try:
                # Find risk level for fund
                risk_level = "Medium"
                for fund in self.fund_types:
                    if fund["name"] == data.get('fund_name'):
                        risk_level = fund["risk"]
                        break
                
                allocation = FundAllocation(
                    member_id=member.member_id,
                    fund_name=data.get('fund_name', 'Diversified Growth Fund'),
                    allocation_percent=data.get('allocation_percent', 50),
                    selection_date=selection_date,
                    risk_level=risk_level
                )
                allocations.append(allocation)
                
            except Exception as e:
                print(f"⚠️ Error creating allocation: {e}")
                continue
                
        return allocations

    def validate_data_quality(self, profiles: List[MemberProfile], 
                            contributions: List[ContributionRecord],
                            allocations: List[FundAllocation]) -> Dict[str, Any]:
        """Validate generated data quality and business rules"""
        
        validation_results = {
            "total_members": len(profiles),
            "age_distribution": {},
            "sector_distribution": {},
            "salary_stats": {},
            "fund_allocation_checks": {},
            "business_rule_compliance": {}
        }
        
        # Age distribution
        ages = [p.age for p in profiles]
        validation_results["age_distribution"] = {
            "min": min(ages) if ages else 0,
            "max": max(ages) if ages else 0,
            "mean": sum(ages) / len(ages) if ages else 0,
            "median": sorted(ages)[len(ages)//2] if ages else 0
        }
        
        # Sector distribution
        sectors = [p.sector for p in profiles]
        for sector in set(sectors):
            validation_results["sector_distribution"][sector] = sectors.count(sector)
        
        # Salary statistics
        salaries = [p.annual_salary for p in profiles]
        validation_results["salary_stats"] = {
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
        
        # Check 100% allocations
        correct_allocations = sum(1 for total in member_allocations.values() if 95 <= total <= 105)
        validation_results["fund_allocation_checks"] = {
            "members_with_allocations": len(member_allocations),
            "correct_100_percent": correct_allocations,
            "allocation_compliance_rate": correct_allocations / len(member_allocations) if member_allocations else 0
        }
        
        return validation_results

    def export_data(self, profiles: List[MemberProfile], 
                   contributions: List[ContributionRecord],
                   allocations: List[FundAllocation],
                   validation_results: Dict[str, Any]):
        """Export generated data to files"""
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Export member profiles
        profiles_df = pd.DataFrame([asdict(p) for p in profiles])
        profiles_df.to_csv(f"pension_members_{timestamp}.csv", index=False)
        print(f"💾 Exported {len(profiles)} member profiles")
        
        # Export contributions
        if contributions:
            contributions_df = pd.DataFrame([asdict(c) for c in contributions])
            contributions_df.to_csv(f"pension_contributions_{timestamp}.csv", index=False)
            print(f"💾 Exported {len(contributions)} contribution records")
        
        # Export fund allocations
        if allocations:
            allocations_df = pd.DataFrame([asdict(a) for a in allocations])
            allocations_df.to_csv(f"pension_fund_allocations_{timestamp}.csv", index=False)
            print(f"💾 Exported {len(allocations)} fund allocation records")
        
        # Export validation report
        with open(f"validation_report_{timestamp}.json", "w") as f:
            json.dump(validation_results, f, indent=2)
        print(f"📊 Exported validation report")
        
        return timestamp

def main():
    """🎖️ Main mission execution"""
    print("=" * 60)
    print("🎖️ MISSION ALPHA - PENSION PHANTOM GENERATOR")
    print("Operation Synthetic Shield - Data Generation Division")
    print("=" * 60)
    
    try:
        # Initialize generator
        generator = PensionPhantomGenerator()
        
        # Phase 1: Generate member profiles
        print(f"\n🚀 Phase 1: Generating {generator.member_count} member profiles...")
        all_profiles = []
        batch_size = 50
        
        for i in range(0, generator.member_count, batch_size):
            current_batch_size = min(batch_size, generator.member_count - i)
            print(f"   Generating batch {i//batch_size + 1}: {current_batch_size} members...")
            
            batch_profiles = generator.generate_member_profiles_batch(current_batch_size)
            all_profiles.extend(batch_profiles)
            
            if len(batch_profiles) < current_batch_size:
                print(f"   ⚠️ Generated {len(batch_profiles)} of {current_batch_size} requested")
        
        print(f"✅ Generated {len(all_profiles)} member profiles")
        
        # Phase 2: Generate contribution histories (sample)
        print(f"\n🚀 Phase 2: Generating contribution histories for sample members...")
        sample_size = min(100, len(all_profiles))
        sample_profiles = random.sample(all_profiles, sample_size)
        
        all_contributions = []
        for i, member in enumerate(sample_profiles):
            if i % 10 == 0:
                print(f"   Processing member {i+1}/{sample_size}...")
            
            contributions = generator.generate_contribution_history(member, 12)
            all_contributions.extend(contributions)
        
        print(f"✅ Generated {len(all_contributions)} contribution records")
        
        # Phase 3: Generate fund allocations (sample)
        print(f"\n🚀 Phase 3: Generating fund allocations for sample members...")
        
        all_allocations = []
        for i, member in enumerate(sample_profiles):
            if i % 10 == 0:
                print(f"   Processing member {i+1}/{sample_size}...")
            
            allocations = generator.generate_fund_allocations(member)
            all_allocations.extend(allocations)
        
        print(f"✅ Generated {len(all_allocations)} fund allocation records")
        
        # Phase 4: Validate and export
        print(f"\n🚀 Phase 4: Validating data quality...")
        validation_results = generator.validate_data_quality(
            all_profiles, all_contributions, all_allocations
        )
        
        print(f"\n📊 Validation Results:")
        print(f"   Total Members: {validation_results['total_members']}")
        print(f"   Age Range: {validation_results['age_distribution']['min']}-{validation_results['age_distribution']['max']}")
        print(f"   Average Age: {validation_results['age_distribution']['mean']:.1f}")
        print(f"   Average Salary: £{validation_results['salary_stats']['mean']:,.0f}")
        print(f"   Fund Allocation Compliance: {validation_results['fund_allocation_checks']['allocation_compliance_rate']:.1%}")
        
        # Export data
        print(f"\n🚀 Phase 5: Exporting data...")
        timestamp = generator.export_data(
            all_profiles, all_contributions, all_allocations, validation_results
        )
        
        print(f"\n🎖️ MISSION ALPHA COMPLETED SUCCESSFULLY!")
        print(f"   Generated: {len(all_profiles)} members, {len(all_contributions)} contributions, {len(all_allocations)} allocations")
        print(f"   Files exported with timestamp: {timestamp}")
        print(f"   Provider: {generator.provider}")
        print("=" * 60)
        
    except Exception as e:
        print(f"❌ MISSION FAILED: {e}")
        raise

if __name__ == "__main__":
    main()
