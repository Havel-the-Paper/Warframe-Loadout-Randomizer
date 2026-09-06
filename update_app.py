#!/usr/bin/env python3
"""
Warframe Loadout Randomizer - App Updater
Fetches the latest Warframe items data, filters it using the engine rules,
and automatically rebuilds the standalone desktop application.
"""

import os
import sys
import shutil
import subprocess
from eda_engine import EDADatabase

def main():
    print("==================================================================")
    print("  🚀 WARFRAME LOADOUT RANDOMIZER - APP UPDATER")
    print("==================================================================")
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    web_dir = os.path.join(base_dir, "web")
    cache_file = os.path.join(base_dir, "data", "warframe_items_cache.json")
    react_data_file = os.path.join(web_dir, "src", "data", "eda_data.json")
    final_app_path = os.path.join(base_dir, "Warframe Loadout Randomizer.html")

    # Step 1: Fetch and update the data
    print("\n[1/4] Fetching latest Warframe data from WFCD and applying filter rules...")
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

    # Step 3: Build the standalone Desktop App using Electron
    print("\n[3/4] Packaging the standalone Electron desktop app (this may take a minute)...")
    try:
        # Run npm install just in case
        subprocess.run(["npm", "install"], cwd=web_dir, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        # Run npm run electron:build
        subprocess.run(["npm", "run", "electron:build"], cwd=web_dir, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        print(f"      Error during build process: {e}")
        if e.stderr:
            print(f"      {e.stderr.decode('utf-8')}")
        sys.exit(1)
    except FileNotFoundError:
        print("      Error: 'npm' command not found. Please ensure Node.js and npm are installed.")
        sys.exit(1)
        
    print("      Build successful!")

    # Step 4: Move the compiled apps to the root folder
    print("\n[4/4] Finalizing the desktop apps...")
    dist_dir = os.path.join(web_dir, "dist")
    deployed = []

    for file in os.listdir(dist_dir):
        src = os.path.join(dist_dir, file)

        if file.endswith(".AppImage"):
            dest = os.path.join(base_dir, "Warframe Loadout Randomizer.AppImage")
            shutil.copy2(src, dest)
            os.chmod(dest, 0o755)
            print(f"      🐧 Linux AppImage → {dest}")
            deployed.append(dest)

        elif file.endswith(".exe"):
            dest = os.path.join(base_dir, "Warframe Loadout Randomizer.exe")
            shutil.copy2(src, dest)
            print(f"      🪟 Windows Portable → {dest}")
            deployed.append(dest)

    if not deployed:
        print("      Error: No output files found. Did electron-builder succeed?")
        sys.exit(1)

    print(f"\n✅ Update Complete! {len(deployed)} file(s) built and ready to distribute.")

if __name__ == "__main__":
    main()
