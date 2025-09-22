#!/usr/bin/env python3
"""
🎖️ MISSION ALPHA - QUICK DEMO
Rapid demonstration of AI-driven pension data generation
"""

import os
import json
import random
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Azure AI Inference
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential

load_dotenv()

class QuickPensionDemo:
    """Quick demonstration of AI-driven pension data generation"""
    
    def __init__(self):
        self.setup_ai_client()
        
    def setup_ai_client(self):
        """Setup AI client - prioritize Azure AI Foundry, fallback to GitHub"""
        azure_endpoint = os.getenv("AZURE_ENDPOINT")
        azure_key = os.getenv("AZURE_API_KEY")
        
        if azure_endpoint and azure_key:
            self.client = ChatCompletionsClient(
                endpoint=azure_endpoint,
                credential=AzureKeyCredential(azure_key)
            )
            self.model = os.getenv("MODEL_DEPLOYMENT_NAME", "gpt-4o")
            self.provider = "Azure AI Foundry"
        else:
            github_token = os.getenv("GITHUB_TOKEN")
            if github_token:
                self.client = ChatCompletionsClient(
                    endpoint="https://models.github.ai/inference",
                    credential=AzureKeyCredential(github_token)
                )
                self.model = "openai/gpt-4.1"
                self.provider = "GitHub Models"
            else:
                raise ValueError("No AI credentials found")
        
        print(f"🚀 Connected to {self.provider} - {self.model}")
    
    def generate_sample_members(self, count=10):
        """Generate sample pension members"""
        
        prompt = f"""
        Generate {count} realistic UK pension scheme members in JSON format. 

        Requirements:
        - Ages 22-67 with realistic distribution
        - Valid UK postcodes (e.g. SW1A 1AA, M1 1AA, B33 8TH)
        - Employment sectors: Finance, Healthcare, Public Service, Manufacturing, Education, Retail, Technology
        - Age-appropriate salaries (£18,000-£120,000)
        - Realistic job titles/grades
        - Service years appropriate for age
        - Status: mostly Active, some Deferred

        Output as JSON array with exact fields:
        [
          {{
            "age": 34,
            "gender": "F", 
            "postcode": "M15 6JQ",
            "sector": "Finance",
            "job_grade": "Senior Analyst",
            "annual_salary": 47500,
            "years_service": 8,
            "status": "Active"
          }}
        ]
        """
        
        try:
            response = self.client.complete(
                messages=[
                    SystemMessage("You are a UK pension data expert. Generate realistic synthetic data with no real personal information."),
                    UserMessage(prompt)
                ],
                temperature=0.8,
                model=self.model
            )
            
            content = response.choices[0].message.content
            
            # Clean and parse JSON
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0]
            elif "```" in content:
                content = content.split("```")[1]
            
            members = json.loads(content.strip())
            
            # Add member IDs
            for i, member in enumerate(members):
                member['member_id'] = f"MB{random.randint(10000000, 99999999)}"
            
            return members
            
        except Exception as e:
            print(f"❌ Error generating members: {e}")
            return []
    
    def generate_fund_allocations(self, member):
        """Generate fund allocations for a member"""
        
        age = member['age']
        risk_profile = "Conservative" if age > 55 else "Moderate" if age > 40 else "Growth"
        
        prompt = f"""
        Generate realistic fund allocations for UK pension member:
        - Age: {age}
        - Risk Profile: {risk_profile}
        - Sector: {member['sector']}
        
        Available funds: Global Equity Fund, UK Equity Fund, Corporate Bond Fund, Government Bond Fund, Property Fund, Cash Fund, Diversified Growth Fund
        
        Rules:
        - Total allocation must equal exactly 100%
        - Age {age} should have {risk_profile} allocations
        - Younger members: more equity (60-80%)
        - Older members: more bonds/cash (50-70%)
        - Use 2-4 funds typically
        
        Output JSON array:
        [
          {{
            "fund_name": "Global Equity Fund",
            "allocation_percent": 60,
            "risk_level": "High"
          }}
        ]
        """
        
        try:
            response = self.client.complete(
                messages=[
                    SystemMessage("You are a UK pension fund allocation expert."),
                    UserMessage(prompt)
                ],
                temperature=0.6,
                model=self.model
            )
            
            content = response.choices[0].message.content
            
            # Clean and parse JSON
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0]
            elif "```" in content:
                content = content.split("```")[1]
            
            allocations = json.loads(content.strip())
            
            # Add member ID to each allocation
            for allocation in allocations:
                allocation['member_id'] = member['member_id']
                allocation['selection_date'] = (datetime.now() - timedelta(days=random.randint(30, 365))).strftime("%Y-%m-%d")
            
            return allocations
            
        except Exception as e:
            print(f"❌ Error generating allocations: {e}")
            return []
    
    def validate_allocations(self, allocations):
        """Validate fund allocations"""
        member_totals = {}
        
        for alloc in allocations:
            member_id = alloc['member_id']
            if member_id not in member_totals:
                member_totals[member_id] = 0
            member_totals[member_id] += alloc['allocation_percent']
        
        valid_count = sum(1 for total in member_totals.values() if 95 <= total <= 105)
        total_members = len(member_totals)
        
        return {
            'total_members': total_members,
            'valid_allocations': valid_count,
            'compliance_rate': valid_count / total_members if total_members > 0 else 0
        }
    
    def run_demo(self):
        """Run complete demonstration"""
        
        print("\n🎯 MISSION ALPHA - QUICK DEMO")
        print("=" * 40)
        
        # Generate members
        print(f"\n1️⃣ Generating sample pension members...")
        members = self.generate_sample_members(5)
        
        if not members:
            print("❌ Failed to generate members")
            return
        
        print(f"✅ Generated {len(members)} members")
        
        # Display sample member
        print(f"\n📋 Sample Member Profile:")
        sample = members[0]
        print(f"   ID: {sample['member_id']}")
        print(f"   Age: {sample['age']}, Gender: {sample['gender']}")
        print(f"   Location: {sample['postcode']}")
        print(f"   Sector: {sample['sector']} - {sample['job_grade']}")
        print(f"   Salary: £{sample['annual_salary']:,}")
        print(f"   Service: {sample['years_service']} years")
        print(f"   Status: {sample['status']}")
        
        # Generate fund allocations
        print(f"\n2️⃣ Generating fund allocations...")
        all_allocations = []
        
        for member in members:
            allocations = self.generate_fund_allocations(member)
            all_allocations.extend(allocations)
        
        print(f"✅ Generated allocations for {len(members)} members")
        
        # Display sample allocations
        sample_allocations = [a for a in all_allocations if a['member_id'] == sample['member_id']]
        print(f"\n💰 Fund Allocations for {sample['member_id']}:")
        total_percent = 0
        for alloc in sample_allocations:
            print(f"   {alloc['fund_name']}: {alloc['allocation_percent']}% ({alloc['risk_level']} risk)")
            total_percent += alloc['allocation_percent']
        print(f"   Total: {total_percent}%")
        
        # Validate data
        print(f"\n3️⃣ Validating data quality...")
        validation = self.validate_allocations(all_allocations)
        
        print(f"✅ Validation Results:")
        print(f"   Members with allocations: {validation['total_members']}")
        print(f"   Valid allocations (100%): {validation['valid_allocations']}")
        print(f"   Compliance rate: {validation['compliance_rate']:.1%}")
        
        # Statistics
        ages = [m['age'] for m in members]
        salaries = [m['annual_salary'] for m in members]
        sectors = [m['sector'] for m in members]
        
        print(f"\n📊 Statistics:")
        print(f"   Age range: {min(ages)}-{max(ages)} (avg: {sum(ages)/len(ages):.1f})")
        print(f"   Salary range: £{min(salaries):,}-£{max(salaries):,} (avg: £{sum(salaries)/len(salaries):,.0f})")
        print(f"   Sectors: {', '.join(set(sectors))}")
        
        print(f"\n🎖️ DEMO COMPLETE!")
        print(f"   Provider: {self.provider}")
        print(f"   AI Model: {self.model}")
        print("=" * 40)

def main():
    """Run the demo"""
    try:
        demo = QuickPensionDemo()
        demo.run_demo()
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        print("\nPlease ensure:")
        print("1. Environment variables are set (.env file)")
        print("2. Dependencies are installed (pip install -r requirements.txt)")
        print("3. AI service credentials are valid")

if __name__ == "__main__":
    main()
