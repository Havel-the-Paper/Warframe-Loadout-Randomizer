# Warframe Loadout Randomizer

A loadout randomizer for Warframe that gives you 3 random Warframes, 3 Primaries, 3 Secondaries, and 3 Melee Weapons to choose from, with **Official Warframe Wiki (`wiki.warframe.com`)** integration.

---
## Features
- Randomly selects 3 of each warframe, primary weapon, secondary weapon, and melee weapon
- Choices can be rerolled all at once or individually per category
- Displays MR requirements for each item
- Each option links directly to its page on the official Warframe wiki

---
## Running the App

Simply double-click:
**`Warframe_EDA_Desktop.AppImage`** (Linux)
**`Warframe_EDA_Desktop.exe`** (Windows)

---

### Building from Source Manually

Clone this repo, then either run

```bash
update_app.py
```

OR

```bash
cd web
npm install
npm run electron:build
```

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
