#!/usr/bin/env python3
"""
🎖️ Mission Alpha Enhanced Launcher
Operation Synthetic Shield - Pension Data Generation

Launch options:
1. Demo Version - Standalone demo with built-in algorithms
2. Azure AI Version - Full Azure AI Foundry integration
3. Setup Assistant - Configure Azure AI credentials
"""

import subprocess
import sys
import os
from pathlib import Path

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = {
        'streamlit': 'streamlit',
        'pandas': 'pandas', 
        'numpy': 'numpy'
    }
    
    missing = []
    for package, import_name in required_packages.items():
        try:
            __import__(import_name)
        except ImportError:
            missing.append(package)
    
    return missing

def check_azure_dependencies():
    """Check if Azure AI packages are installed"""
    try:
        import azure.ai.inference
        import dotenv
        return True
    except ImportError:
        return False

def install_dependencies(packages):
    """Install missing packages"""
    print(f"📦 Installing missing packages: {', '.join(packages)}")
    
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install"] + packages)
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def check_azure_config():
    """Check if Azure AI is configured"""
    env_file = Path(".env")
    
    if not env_file.exists():
        return False, "No .env file found"
    
    try:
        # Simple check - read the file and look for required keys
        with open(env_file, 'r') as f:
            content = f.read()
        
        has_endpoint = "AZURE_AI_ENDPOINT=" in content and "your-foundry-endpoint" not in content
        has_key = "AZURE_AI_KEY=" in content and "your-azure-ai-key" not in content
        
        if not has_endpoint or not has_key:
            return False, "Azure AI credentials not configured in .env"
        
        return True, "Azure AI configured"
    except Exception as e:
        return False, f"Configuration error: {e}"

def setup_azure_config():
    """Interactive setup for Azure AI configuration"""
    print("\n🎖️ AZURE AI FOUNDRY SETUP ASSISTANT")
    print("=" * 50)
    
    template_file = Path(".env.template")
    env_file = Path(".env")
    
    if not template_file.exists():
        print("❌ .env.template file not found!")
        return False
    
    print("\nTo configure Azure AI Foundry, you need:")
    print("1. 🔗 Azure AI Foundry model deployment endpoint")
    print("2. 🔑 API key for your deployment") 
    print("3. 🤖 Model deployment name")
    print("\n💡 You can find these in your Azure AI Foundry deployment details.")
    
    if env_file.exists():
        overwrite = input(f"\n.env file already exists. Overwrite? (y/N): ").strip().lower()
        if overwrite != 'y':
            print("Setup cancelled.")
            return False
    
    print(f"\nCopying {template_file} to {env_file}...")
    
    try:
        with open(template_file, 'r') as src:
            content = src.read()
        
        with open(env_file, 'w') as dst:
            dst.write(content)
        
        print(f"✅ Created {env_file}")
        print(f"\n📝 NEXT STEPS:")
        print(f"1. Edit {env_file} with your Azure AI Foundry details:")
        print(f"   🔗 AZURE_AI_ENDPOINT=https://your-foundry-endpoint...")
        print(f"   🔑 AZURE_AI_KEY=your-api-key")
        print(f"   🤖 AZURE_AI_MODEL=your-model-deployment-name")
        print(f"2. Save the file")
        print(f"3. Run this launcher again and select option 2")
        print(f"\n💡 Tip: You can also enable fallback mode to use demo generation")
        print(f"    when Azure AI is unavailable by setting FALLBACK_TO_DEMO=true")
        
        return True
    except Exception as e:
        print(f"❌ Failed to create .env file: {e}")
        return False

def launch_demo():
    """Launch the demo version"""
    print("🚀 Launching Mission Alpha Demo Version...")
    print("   🎲 Using built-in synthetic data generation algorithms")
    print("   🔒 Zero external dependencies")
    print("   ⚡ Immediate start")
    
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "streamlit_demo.py"])
    except KeyboardInterrupt:
        print("\n🎖️ Mission Demo terminated by user")
    except Exception as e:
        print(f"❌ Failed to launch demo: {e}")

def launch_azure_ai():
    """Launch the Azure AI version"""
    print("🚀 Launching Mission Alpha Azure AI Version...")
    print("   🤖 AI-powered pension data generation")
    print("   🔗 Azure AI Foundry integration")
    print("   🎯 Realistic, compliant synthetic data")
    
    # Check Azure dependencies
    if not check_azure_dependencies():
        print("\n⚠️ Azure AI dependencies not installed.")
        install = input("Install Azure AI packages now? (y/N): ").strip().lower()
        if install == 'y':
            azure_packages = ['azure-ai-inference', 'python-dotenv']
            if not install_dependencies(azure_packages):
                print("❌ Cannot launch Azure AI version without dependencies")
                return
        else:
            print("❌ Cannot launch Azure AI version without dependencies")
            return
    
    # Check configuration
    configured, message = check_azure_config()
    if not configured:
        print(f"\n⚠️ Azure AI configuration issue: {message}")
        print("The app will start with demo mode fallback.")
        print("💡 Configure Azure AI using option 3 for full AI functionality.")
    else:
        print(f"✅ {message}")
    
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "streamlit_azure_ai.py"])
    except KeyboardInterrupt:
        print("\n🎖️ Mission Azure AI terminated by user")
    except Exception as e:
        print(f"❌ Failed to launch Azure AI version: {e}")

def show_system_info():
    """Display system information"""
    print("\n📋 MISSION ALPHA SYSTEM STATUS")
    print("=" * 40)
    
    # Check basic dependencies
    missing = check_dependencies()
    azure_deps = check_azure_dependencies()
    azure_configured, config_message = check_azure_config()
    
    print(f"🐍 Python: {sys.version.split()[0]}")
    print(f"📁 Working Directory: {os.getcwd()}")
    print(f"🎲 Demo Mode: ✅ Ready")
    print(f"📦 Basic Dependencies: {'✅ Installed' if not missing else '❌ Missing: ' + ', '.join(missing)}")
    print(f"🤖 Azure AI Dependencies: {'✅ Installed' if azure_deps else '❌ Not Installed'}")
    print(f"⚙️ Azure AI Configuration: {'✅ Configured' if azure_configured else '❌ ' + config_message}")
    
    # Check for files
    demo_exists = os.path.exists("streamlit_demo.py")
    azure_exists = os.path.exists("streamlit_azure_ai.py")
    template_exists = os.path.exists(".env.template")
    env_exists = os.path.exists(".env")
    
    print(f"\n📄 Files:")
    print(f"   streamlit_demo.py: {'✅' if demo_exists else '❌'}")
    print(f"   streamlit_azure_ai.py: {'✅' if azure_exists else '❌'}")
    print(f"   .env.template: {'✅' if template_exists else '❌'}")
    print(f"   .env: {'✅' if env_exists else '❌'}")
    
    if azure_configured:
        try:
            # Try to read some config info safely
            with open(".env", 'r') as f:
                lines = f.readlines()
            
            for line in lines:
                if line.startswith("AZURE_AI_ENDPOINT=") and "your-foundry-endpoint" not in line:
                    endpoint = line.split("=", 1)[1].strip()
                    print(f"🔗 Azure Endpoint: {endpoint[:50]}...")
                elif line.startswith("AZURE_AI_MODEL=") and "your-model" not in line:
                    model = line.split("=", 1)[1].strip()
                    print(f"🤖 Azure Model: {model}")
        except:
            pass

def main():
    """Main launcher interface"""
    print("🎖️ MISSION ALPHA ENHANCED LAUNCHER")
    print("Operation Synthetic Shield - Pension Data Generation")
    print("=" * 55)
    print("🎯 Advanced AI-Powered Synthetic Data Generation")
    print("🔒 Zero PII Risk - Completely Synthetic Data")
    print("🇬🇧 UK Pension Regulations Compliant")
    
    # Check basic dependencies first
    missing = check_dependencies()
    if missing:
        print(f"\n⚠️ Missing required packages: {', '.join(missing)}")
        install = input("Install missing packages? (y/N): ").strip().lower()
        if install == 'y':
            if not install_dependencies(missing):
                print("❌ Cannot continue without required packages")
                return
        else:
            print("❌ Cannot continue without required packages")
            return
    
    while True:
        print("\n" + "=" * 55)
        print("🎯 MISSION DEPLOYMENT OPTIONS")
        print("=" * 55)
        print("1. 🎲 Demo Version")
        print("   └── Built-in algorithms, no external dependencies")
        print("2. 🤖 Azure AI Version") 
        print("   └── Full AI-powered generation with Azure AI Foundry")
        print("3. ⚙️ Setup Azure AI Configuration")
        print("   └── Configure your Azure AI Foundry credentials")
        print("4. 📋 System Information")
        print("   └── View current system status and configuration")
        print("5. ❌ Exit Launcher")
        
        choice = input("\n🎖️ Select mission deployment (1-5): ").strip()
        
        if choice == "1":
            launch_demo()
            break
        elif choice == "2":
            launch_azure_ai()
            break
        elif choice == "3":
            if setup_azure_config():
                print("\n✅ Configuration setup complete!")
                print("💡 You can now use option 2 to launch the Azure AI version")
            else:
                print("\n❌ Configuration setup failed")
        elif choice == "4":
            show_system_info()
            input("\nPress Enter to continue...")
        elif choice == "5":
            print("\n🎖️ Mission launcher terminated.")
            print("📋 Status: Standing by for future operations")
            print("🔒 Security: All systems secure")
            break
        else:
            print("❌ Invalid choice. Please select 1-5.")

if __name__ == "__main__":
    main()
