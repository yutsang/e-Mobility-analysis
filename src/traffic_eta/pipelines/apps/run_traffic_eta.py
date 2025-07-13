#!/usr/bin/env python3
"""
Traffic ETA - Production Launcher
Launches the production-ready Traffic ETA application with all enhancements
"""

import sys
import subprocess
import os
import glob
import shutil
from kedro.config import OmegaConfigLoader

def clear_cache():
    """Clear streamlit cache and temporary files"""
    print("🧹 Clearing cache and temporary files...")
    
    # Cache patterns to clear
    cache_patterns = [
        ".streamlit",
        "__pycache__",
        "*.pyc",
        "*.pyo",
        ".cache",
        "*.cache.json"
    ]
    
    for pattern in cache_patterns:
        if "*" in pattern:
            # Handle wildcard patterns
            for file in glob.glob(f"**/{pattern}", recursive=True):
                try:
                    os.remove(file)
                    print(f"   ✅ Removed {os.path.basename(file)}")
                except OSError:
                    pass
        else:
            # Handle directories
            if os.path.exists(pattern):
                try:
                    if os.path.isdir(pattern):
                        shutil.rmtree(pattern)
                        print(f"   ✅ Removed directory {pattern}")
                    else:
                        os.remove(pattern)
                        print(f"   ✅ Removed file {pattern}")
                except OSError as e:
                    print(f"   ⚠️  Could not remove {pattern}: {e}")

def load_configuration():
    """Load application configuration"""
    try:
        conf_path = os.path.join(os.path.dirname(__file__), "..", "..", "conf")
        conf_loader = OmegaConfigLoader(conf_source=conf_path)
        return conf_loader["parameters"]
    except Exception as e:
        print(f"⚠️ Could not load configuration: {e}")
        # Return default config
        return {
            "app": {"port": 8508, "host": "localhost"},
            "database": {"path": "data/01_raw/kmb_data.db"}
        }

def check_database(params):
    """Check if database exists and is accessible"""
    db_path = params["database"]["path"]
    
    if os.path.exists(db_path):
        size_mb = os.path.getsize(db_path) / (1024 * 1024)
        print(f"✅ Database found: {size_mb:.1f} MB")
        return True
    else:
        print(f"❌ Database not found at: {db_path}")
        return False

def check_first_run():
    """Check if this is the first run"""
    first_run_file = "data/.first_run_complete"
    if not os.path.exists(first_run_file):
        print("🚀 First run detected - will perform initial setup")
        return True
    return False

def setup_data_update(params):
    """Setup data update process if needed"""
    from pipelines.web_app.nodes import should_update_data
    
    if should_update_data():
        print("📊 Data update required...")
        try:
            # Import and run data update
            from data_updater import KMBDataUpdater
            from database_manager import KMBDatabaseManager
            
            updater = KMBDataUpdater()
            db_manager = KMBDatabaseManager()
            
            print("   • Updating routes...")
            routes = updater.fetch_routes()
            if routes:
                db_manager.insert_routes(routes)
            
            print("   • Updating stops...")
            stops = updater.fetch_stops()
            if stops:
                db_manager.insert_stops(stops)
            
            print("✅ Data update completed")
            return True
        except Exception as e:
            print(f"⚠️ Data update failed: {e}")
            return False
    else:
        print("📊 Data is up to date")
        return True

def main():
    """Main launcher function"""
    print("🚌 Traffic ETA - Production Launcher")
    print("=" * 70)
    print("🌟 Enhanced Hong Kong Public Transport Explorer")
    print("🎯 Complete route coverage with dual directions")
    print("🗺️ OSM routing with auto-zoom and center controls")
    print("🏷️ Route type classification (Express, Night, Circular)")
    print("🔍 Enhanced search with depot names")
    print("-" * 70)
    
    # Load configuration
    params = load_configuration()
    
    # Clear cache
    clear_cache()
    
    # Check if first run
    is_first_run = check_first_run()
    
    # Check database
    print("\n📊 Checking database...")
    if not check_database(params):
        print("Please ensure the database is properly set up.")
        print("Run: python src/traffic_eta/data_updater.py --all")
        return
    
    # Setup data update if configured
    if params.get("schedule", {}).get("daily_update", {}).get("enabled", True):
        print("\n🔄 Checking data updates...")
        setup_data_update(params)
    
    print("\n🚀 Launching Traffic ETA application...")
    print("📱 Opening in your default web browser")
    print(f"🔗 URL: http://{params['app']['host']}:{params['app']['port']}")
    print("⏹️  Press Ctrl+C to stop the application")
    print("🔧 Enhanced features:")
    print("   • Dual direction search with depot names")
    print("   • Route type classification and badges")
    print("   • Auto-zoom maps with center button")
    print("   • Enhanced search and filtering")
    print("   • First-run setup and daily updates")
    print("   • Complete route coverage (788 routes)")
    print("-" * 70)
    
    try:
        # Launch the Traffic ETA Streamlit app
        app_path = "src/traffic_eta/traffic_eta_app.py"
        port = params["app"]["port"]
        host = params["app"]["host"]
        
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", app_path,
            "--server.port", str(port),
            "--server.address", host,
            "--server.headless", "true",
            "--server.runOnSave", "true",
            "--browser.gatherUsageStats", "false"
        ])
    except KeyboardInterrupt:
        print("\n👋 Traffic ETA stopped by user")
        print("🧹 Cleaning up...")
        clear_cache()
    except Exception as e:
        print(f"❌ Error launching application: {e}")
        print("Try running manually:")
        print(f"  streamlit run {app_path} --server.port {port}")

if __name__ == "__main__":
    main() 