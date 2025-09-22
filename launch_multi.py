#!/usr/bin/env python3
"""
🎖️ Mission Alpha Multi-App Launcher
Enhanced launcher with dashboard integration and advanced mission control
"""

import subprocess
import sys
import os
import time
from pathlib import Path

def print_banner():
    """Print Mission Alpha banner"""
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║                  🎖️  MISSION ALPHA  🎖️                      ║
    ║              Operation Synthetic Shield                       ║
    ║         Advanced Multi-Application Command Center             ║
    ╚══════════════════════════════════════════════════════════════╝
    """)

def check_dependencies():
    """Check if required dependencies are installed"""
    required = ['streamlit', 'pandas', 'numpy', 'plotly']
    missing = []
    
    for package in required:
        try:
            __import__(package)
        except ImportError:
            missing.append(package)
    
    if missing:
        print(f"❌ Missing dependencies: {', '.join(missing)}")
        print("Install with: pip install streamlit pandas numpy plotly")
        return False
    
    return True

def check_optional_dependencies():
    """Check optional Azure AI dependencies"""
    optional = ['azure-ai-inference', 'python-dotenv']
    available = []
    
    for package in optional:
        try:
            __import__(package.replace('-', '.'))
            available.append(package)
        except ImportError:
            pass
    
    return available

def get_python_command():
    """Get the correct Python command for this system"""
    # Try common Python commands
    for cmd in ['py', 'python', 'python3']:
        try:
            result = subprocess.run([cmd, '--version'], capture_output=True, text=True)
            if result.returncode == 0 and 'Python' in result.stdout:
                return cmd
        except FileNotFoundError:
            continue
    
    return 'python'  # fallback

def run_streamlit_app(app_file, port=8501):
    """Run a Streamlit application"""
    python_cmd = get_python_command()
    
    print(f"🚀 Launching {app_file}...")
    print(f"📡 Running on http://localhost:{port}")
    print("🛑 Press Ctrl+C to stop")
    print("=" * 60)
    
    try:
        subprocess.run([python_cmd, '-m', 'streamlit', 'run', app_file, '--server.port', str(port)])
    except KeyboardInterrupt:
        print("\n🛑 Application stopped by user")
    except Exception as e:
        print(f"❌ Error running application: {e}")

def check_azure_configuration():
    """Check Azure AI configuration status"""
    env_file = Path(".env")
    
    if not env_file.exists():
        return False, "No .env file found"
    
    try:
        with open(env_file, 'r') as f:
            content = f.read()
            
        required_vars = ['AZURE_AI_ENDPOINT', 'AZURE_AI_KEY', 'AZURE_AI_MODEL']
        missing = []
        
        for var in required_vars:
            if var not in content or f"{var}=" not in content:
                missing.append(var)
        
        if missing:
            return False, f"Missing variables: {', '.join(missing)}"
        
        return True, "Azure AI configuration appears complete"
        
    except Exception as e:
        return False, f"Error reading .env file: {e}"

def create_env_template():
    """Create environment template file"""
    template_content = """# Mission Alpha - Azure AI Configuration
# Copy this file to .env and fill in your actual values

# Azure AI Foundry Configuration
AZURE_AI_ENDPOINT=https://your-foundry-endpoint.region.inference.ml.azure.com
AZURE_AI_KEY=your-actual-api-key-here
AZURE_AI_MODEL=gpt-4o

# Application Settings
ENABLE_AZURE_AI=true
FALLBACK_TO_DEMO=true
DEFAULT_MEMBER_COUNT=1000
MAX_MEMBER_COUNT=5000

# Dashboard Settings
DASHBOARD_AUTO_REFRESH=false
DASHBOARD_REFRESH_INTERVAL=30
"""
    
    with open('.env.template', 'w') as f:
        f.write(template_content)
    
    print("✅ Created .env.template file")
    print("📝 Copy this to .env and add your Azure AI credentials")

def interactive_azure_setup():
    """Interactive Azure AI setup"""
    print("\n🔧 Azure AI Foundry Setup Assistant")
    print("=" * 40)
    
    endpoint = input("Enter your Azure AI endpoint URL: ").strip()
    api_key = input("Enter your Azure AI API key: ").strip()
    model = input("Enter your model name (default: gpt-4o): ").strip() or "gpt-4o"
    
    env_content = f"""# Mission Alpha - Azure AI Configuration
AZURE_AI_ENDPOINT={endpoint}
AZURE_AI_KEY={api_key}
AZURE_AI_MODEL={model}

# Application Settings
ENABLE_AZURE_AI=true
FALLBACK_TO_DEMO=true
DEFAULT_MEMBER_COUNT=1000
MAX_MEMBER_COUNT=5000

# Dashboard Settings
DASHBOARD_AUTO_REFRESH=false
DASHBOARD_REFRESH_INTERVAL=30
"""
    
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("✅ Configuration saved to .env file")
    return True

def show_system_info():
    """Show system information"""
    print("\n📊 System Information")
    print("=" * 30)
    
    # Python version
    python_cmd = get_python_command()
    try:
        result = subprocess.run([python_cmd, '--version'], capture_output=True, text=True)
        print(f"🐍 Python: {result.stdout.strip()}")
    except:
        print("🐍 Python: Unknown version")
    
    # Dependencies
    print(f"📦 Core Dependencies: {'✅ Available' if check_dependencies() else '❌ Missing'}")
    
    optional_deps = check_optional_dependencies()
    print(f"🔧 Azure AI Dependencies: {', '.join(optional_deps) if optional_deps else 'None installed'}")
    
    # Azure configuration
    azure_ok, azure_msg = check_azure_configuration()
    print(f"🤖 Azure AI Config: {'✅' if azure_ok else '❌'} {azure_msg}")
    
    # Available apps
    apps = [
        ("streamlit_demo.py", "Demo Version"),
        ("streamlit_azure_ai.py", "Azure AI Version"), 
        ("dashboard.py", "Command Dashboard")
    ]
    
    print("\n📱 Available Applications:")
    for app_file, description in apps:
        if Path(app_file).exists():
            print(f"  ✅ {description} ({app_file})")
        else:
            print(f"  ❌ {description} ({app_file}) - Not found")

def main():
    """Main launcher interface"""
    print_banner()
    
    while True:
        print("\n🎯 Mission Alpha Command Center")
        print("=" * 35)
        print("1. 🎲 Demo Version (Instant Start)")
        print("2. 🤖 Azure AI Version (Full AI Power)")
        print("3. 📊 Command Dashboard (Analytics & Control)")
        print("4. ⚙️  Setup Azure AI Configuration")
        print("5. 📋 System Information")
        print("6. 🚪 Exit")
        
        choice = input("\n🎖️ Select your mission: ").strip()
        
        if choice == '1':
            # Demo Version
            if not check_dependencies():
                print("Install required dependencies first!")
                continue
                
            if Path("streamlit_demo.py").exists():
                run_streamlit_app("streamlit_demo.py", 8501)
            else:
                print("❌ streamlit_demo.py not found!")
        
        elif choice == '2':
            # Azure AI Version
            if not check_dependencies():
                print("Install required dependencies first!")
                continue
                
            optional_deps = check_optional_dependencies()
            if 'azure-ai-inference' not in optional_deps:
                print("❌ Azure AI dependencies not installed!")
                print("Install with: pip install azure-ai-inference python-dotenv")
                continue
            
            azure_ok, azure_msg = check_azure_configuration()
            if not azure_ok:
                print(f"❌ Azure AI Configuration Issue: {azure_msg}")
                print("Use option 4 to set up Azure AI configuration")
                continue
            
            if Path("streamlit_azure_ai.py").exists():
                run_streamlit_app("streamlit_azure_ai.py", 8502)
            else:
                print("❌ streamlit_azure_ai.py not found!")
        
        elif choice == '3':
            # Command Dashboard
            if not check_dependencies():
                print("Install required dependencies first!")
                continue
                
            # Install plotly if not available
            try:
                import plotly
            except ImportError:
                print("📦 Installing dashboard dependencies...")
                python_cmd = get_python_command()
                subprocess.run([python_cmd, '-m', 'pip', 'install', 'plotly'])
            
            if Path("dashboard.py").exists():
                run_streamlit_app("dashboard.py", 8503)
            else:
                print("❌ dashboard.py not found!")
        
        elif choice == '4':
            # Setup Azure AI
            print("\n⚙️ Azure AI Configuration Setup")
            print("1. Create template file (.env.template)")
            print("2. Interactive setup (creates .env)")
            
            setup_choice = input("Choose setup method (1 or 2): ").strip()
            
            if setup_choice == '1':
                create_env_template()
            elif setup_choice == '2':
                interactive_azure_setup()
            else:
                print("Invalid choice")
        
        elif choice == '5':
            # System Information
            show_system_info()
        
        elif choice == '6':
            # Exit
            print("\n🎖️ Mission complete. Returning to base.")
            break
        
        else:
            print("❌ Invalid choice. Please select 1-6.")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n🛑 Mission aborted by user")
    except Exception as e:
        print(f"\n❌ Critical error: {e}")
        sys.exit(1)
