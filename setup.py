#!/usr/bin/env python3
"""
🎖️ MISSION ALPHA - SETUP AND CONFIGURATION
Azure AI Foundry Setup Assistant
"""

import os
import shutil
from dotenv import load_dotenv

def check_dependencies():
    """Check if required packages are installed"""
    print("🔍 Checking dependencies...")
    
    missing_packages = []
    required_packages = [
        'azure.ai.inference',
        'pandas', 
        'numpy',
        'dotenv'
    ]
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"   ✅ {package}")
        except ImportError:
            missing_packages.append(package)
            print(f"   ❌ {package}")
    
    if missing_packages:
        print(f"\n⚠️ Missing packages: {', '.join(missing_packages)}")
        print("Install with: pip install -r requirements.txt")
        return False
    
    print("✅ All dependencies satisfied")
    return True

def setup_environment():
    """Setup environment configuration"""
    print("\n🔧 Setting up environment configuration...")
    
    # Copy example env file if .env doesn't exist
    if not os.path.exists('.env'):
        if os.path.exists('.env.example'):
            shutil.copy('.env.example', '.env')
            print("✅ Created .env file from template")
        else:
            print("❌ No .env.example file found")
            return False
    else:
        print("✅ .env file already exists")
    
    return True

def validate_ai_configuration():
    """Validate AI model configuration"""
    print("\n🤖 Validating AI configuration...")
    
    load_dotenv()
    
    # Check Azure AI Foundry
    azure_endpoint = os.getenv("AZURE_ENDPOINT")
    azure_key = os.getenv("AZURE_API_KEY")
    
    # Check GitHub Models
    github_token = os.getenv("GITHUB_TOKEN")
    
    if azure_endpoint and azure_key:
        print("✅ Azure AI Foundry configuration found")
        return True
    elif github_token:
        print("✅ GitHub Models configuration found")
        return True
    else:
        print("❌ No AI configuration found")
        print("\nConfiguration options:")
        print("1. Azure AI Foundry: Set AZURE_ENDPOINT and AZURE_API_KEY")
        print("2. GitHub Models: Set GITHUB_TOKEN")
        return False

def run_quick_test():
    """Run a quick test of the system"""
    print("\n🧪 Running quick test...")
    
    try:
        from pension_phantom_generator import PensionPhantomGenerator
        
        # Test initialization
        generator = PensionPhantomGenerator()
        print(f"✅ Connected to {generator.provider}")
        
        # Test AI call with simple prompt
        test_prompt = "Generate one sample UK pension member profile with realistic data in JSON format."
        response = generator.call_ai_model(test_prompt, temperature=0.5)
        
        if response and len(response) > 50:
            print("✅ AI model responding correctly")
            return True
        else:
            print("❌ AI model test failed")
            return False
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def print_usage_instructions():
    """Print usage instructions"""
    print(f"\n{'='*60}")
    print("🎖️ MISSION ALPHA - READY FOR DEPLOYMENT")
    print(f"{'='*60}")
    print()
    print("📋 MISSION COMMANDS:")
    print("   python pension_phantom_generator.py    # Run full mission")
    print("   python setup.py                       # Run this setup again")
    print()
    print("🔧 CONFIGURATION:")
    print("   Edit .env file to configure:")
    print("   - AZURE_ENDPOINT and AZURE_API_KEY (for Azure AI Foundry)")
    print("   - GITHUB_TOKEN (for GitHub Models)")
    print("   - MEMBER_COUNT (number of records to generate)")
    print()
    print("📊 OUTPUTS:")
    print("   - pension_members_TIMESTAMP.csv")
    print("   - pension_contributions_TIMESTAMP.csv") 
    print("   - pension_fund_allocations_TIMESTAMP.csv")
    print("   - validation_report_TIMESTAMP.json")
    print()
    print("🎯 SUCCESS CRITERIA:")
    print("   ✅ Generate 1,000-5,000 synthetic members")
    print("   ✅ Zero PII exposure")
    print("   ✅ Statistical accuracy")
    print("   ✅ Business rule compliance")
    print("   ✅ Edge case coverage")
    print(f"{'='*60}")

def main():
    """Main setup routine"""
    print("🎖️ MISSION ALPHA - SETUP AND CONFIGURATION")
    print("=" * 50)
    
    success = True
    
    # Check dependencies
    if not check_dependencies():
        success = False
    
    # Setup environment
    if not setup_environment():
        success = False
    
    # Validate AI config
    if not validate_ai_configuration():
        success = False
        
    # Run test if everything looks good
    if success:
        if run_quick_test():
            print_usage_instructions()
        else:
            success = False
    
    if not success:
        print(f"\n❌ Setup incomplete. Please fix the issues above.")
        return False
    
    print(f"\n🎖️ SETUP COMPLETE - MISSION READY!")
    return True

if __name__ == "__main__":
    main()
