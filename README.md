# Warframe EDA/ETA Loadout Generator & Official Wiki Search

An **Elite Deep Archimedea (EDA)** and **Elite Temporal Archimedea (ETA)** loadout randomizer (3 Warframes, 3 Primaries, 3 Secondaries, 3 Melee Weapons) with **Official Warframe Wiki (`wiki.warframe.com`)** integration.

---
## Features
- Randomly selects 3 of each warframe, primary weapon, secondary weapon, and melee weapon. They can be rerolled all at once or individually and display MR requirements
- Each option comes with a link to its page on the official Warframe wiki

---
## Installation

Clone the repository. Then run

```bash
cd web
npm install
npm run build
cd ..
./run_web.py
```

## 🚀 1-Click Launchers (Web UI + Default Browser)

### 🐧 Linux / macOS
Simply execute the "start_web.sh" script in your terminal or double-click it:
*Starts the local web server and automatically opens `http://localhost:5173` in your default browser.*

---

### 🪟 Windows
Double-click:
- **`start_web.bat`** (Batch file) or run **`start_web.ps1`** in PowerShell.

*Starts the local server and automatically launches `http://localhost:5173` in your default browser.*

---

## 💻 Terminal CLI Tool (`eda_cli.py`)

If you prefer using the terminal:
```bash
# Roll 3 of each equipment category
python3 eda_cli.py roll

# Search wiki.warframe.com for any item
python3 eda_cli.py search "nikana"
python3 eda_cli.py search "saryn"

# Interactive terminal dashboard
python3 eda_cli.py interactive

# Export Discord / Markdown summary
python3 eda_cli.py export
```

---


```
