#!/usr/bin/env python3
"""
Hong Kong Transportation Dashboard Launcher
This script checks dependencies and launches the Streamlit application.
"""

import sys
import subprocess
import importlib.util

def check_dependency(package_name):
    """Check if a package is installed"""
    spec = importlib.util.find_spec(package_name)
    return spec is not None

def install_dependency(package_name):
    """Install a package using pip"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
        return True
    except subprocess.CalledProcessError:
        return False

def main():
    """Main launcher function"""
    print("🚇 Hong Kong Transportation Dashboard Launcher")
    print("=" * 50)
    
    # Required packages
    required_packages = [
        'streamlit',
        'folium',
        'pandas',
        'requests',
        'streamlit_folium',
        'plotly',
        'numpy'
    ]
    
    # Check and install missing packages
    missing_packages = []
    for package in required_packages:
        if not check_dependency(package):
            missing_packages.append(package)
    
    if missing_packages:
        print(f"Missing packages: {', '.join(missing_packages)}")
        print("Installing missing packages...")
        
        for package in missing_packages:
            print(f"Installing {package}...")
            if install_dependency(package):
                print(f"✅ {package} installed successfully")
            else:
                print(f"❌ Failed to install {package}")
                print("Please install manually: pip install -r requirements.txt")
                return
    
    print("✅ All dependencies are installed!")
    print("🚀 Launching Hong Kong Transportation Dashboard...")
    print("📱 The app will open in your default web browser")
    print("🔗 URL: http://localhost:8501")
    print("⏹️  Press Ctrl+C to stop the application")
    print("-" * 50)
    
    try:
        # Launch the Streamlit app
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "hk_transport_enhanced.py",
            "--server.port", "8501",
            "--server.address", "localhost"
        ])
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except Exception as e:
        print(f"❌ Error launching application: {e}")
        print("Try running manually: streamlit run hk_transport_enhanced.py")

if __name__ == "__main__":
    main() 