#!/usr/bin/env python3
"""
🎖️ MISSION ALPHA - LAUNCHER
Quick launcher for the Streamlit application
"""

import subprocess
import sys
import os

def check_streamlit():
    """Check if Streamlit is installed"""
    try:
        import streamlit
        return True
    except ImportError:
        return False

def install_streamlit():
    """Install Streamlit"""
    print("📦 Installing Streamlit...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "streamlit", "pandas", "numpy"])
    print("✅ Streamlit installed successfully!")

def launch_demo():
    """Launch the demo application"""
    print("🚀 Launching Mission Alpha Demo...")
    
    # Check if demo file exists
    demo_file = "streamlit_demo.py"
    if not os.path.exists(demo_file):
        print(f"❌ Demo file {demo_file} not found!")
        return
    
    # Launch Streamlit
    subprocess.run([sys.executable, "-m", "streamlit", "run", demo_file])

def launch_full_app():
    """Launch the full application"""
    print("🚀 Launching Mission Alpha Full Application...")
    
    # Check if app file exists
    app_file = "streamlit_app.py"
    if not os.path.exists(app_file):
        print(f"❌ App file {app_file} not found!")
        return
    
    # Launch Streamlit
    subprocess.run([sys.executable, "-m", "streamlit", "run", app_file])

def main():
    """Main launcher"""
    print("=" * 60)
    print("🎖️ MISSION ALPHA - PENSION PHANTOM GENERATOR")
    print("Operation Synthetic Shield - Data Generation Division")
    print("=" * 60)
    
    if not check_streamlit():
        print("⚠️ Streamlit not found. Installing...")
        try:
            install_streamlit()
        except subprocess.CalledProcessError:
            print("❌ Failed to install Streamlit. Please install manually:")
            print("   pip install streamlit pandas numpy")
            return
    
    print("\n📋 Available Launch Options:")
    print("1. 🎯 Demo Version (No dependencies - immediate start)")
    print("2. 🚀 Full Application (Requires Azure AI configuration)")
    print("3. ❌ Exit")
    
    while True:
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == "1":
            launch_demo()
            break
        elif choice == "2":
            launch_full_app()
            break
        elif choice == "3":
            print("🎖️ Mission Aborted. Good luck, Squadron!")
            break
        else:
            print("❌ Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()
