#!/usr/bin/env python3
"""
Warframe EDA App Updater
Fetches the latest Warframe items data, filters it using the engine rules,
and automatically rebuilds the standalone HTML application.
"""

import os
import sys
import shutil
import subprocess
from eda_engine import EDADatabase

def main():
    print("==================================================================")
    print("  🚀 WARFRAME EDA - STANDALONE APP UPDATER")
    print("==================================================================")
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    web_dir = os.path.join(base_dir, "web")
    cache_file = os.path.join(base_dir, "data", "warframe_items_cache.json")
    react_data_file = os.path.join(web_dir, "src", "data", "eda_data.json")
    final_app_path = os.path.join(base_dir, "Warframe Loadout Randomizer.html")

    # Step 1: Fetch and update the data
    print("\n[1/4] Fetching latest Warframe data from WFCD and applying EDA rules...")
    db = EDADatabase()
    # Force a fresh remote sync
    db.sync_remote_data()
    print("      Data successfully updated and filtered!")

    # Step 2: Copy updated data to the web app
    print("\n[2/4] Injecting updated data into the web application source...")
    if not os.path.exists(cache_file):
        print("      Error: Cache file was not generated.")
        sys.exit(1)
    
    os.makedirs(os.path.dirname(react_data_file), exist_ok=True)
    shutil.copy2(cache_file, react_data_file)
    print("      Data injection complete.")

    # Step 3: Build the standalone HTML file using Vite
    print("\n[3/4] Building the standalone HTML application (this may take a few seconds)...")
    try:
        # Run npm install just in case
        subprocess.run(["npm", "install"], cwd=web_dir, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        # Run npm build
        subprocess.run(["npm", "run", "build"], cwd=web_dir, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        print(f"      Error during build process: {e}")
        if e.stderr:
            print(f"      {e.stderr.decode('utf-8')}")
        sys.exit(1)
    except FileNotFoundError:
        print("      Error: 'npm' command not found. Please ensure Node.js and npm are installed.")
        sys.exit(1)
        
    print("      Build successful!")

    # Step 4: Move the compiled app to the root folder
    print("\n[4/4] Finalizing the standalone app...")
    dist_html = os.path.join(web_dir, "dist", "index.html")
    if not os.path.exists(dist_html):
        print("      Error: Built index.html not found.")
        sys.exit(1)
        
    shutil.copy2(dist_html, final_app_path)
    print(f"      App deployed to: {final_app_path}")

    print("\n✅ Update Complete! You can now open Warframe_EDA_App.html with the latest data.")

if __name__ == "__main__":
    main()
