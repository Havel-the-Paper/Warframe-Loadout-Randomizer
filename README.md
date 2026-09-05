# Warframe EDA/ETA Loadout Generator & Official Wiki Search

An **Elite Deep Archimedea (EDA)** and **Elite Temporal Archimedea (ETA)** style loadout randomizer (3 Warframes, 3 Primaries, 3 Secondaries, 3 Melee Weapons) with **Official Warframe Wiki (`wiki.warframe.com`)** integration.

---
## Features
- Randomly selects 3 of each warframe, primary weapon, secondary weapon, and melee weapon. They can be rerolled all at once or individually and display MR requirements
- Each option comes with a link to its page on the official Warframe wiki

---
## Installation & Running

Simply clone this repo wherever you'd like and run:
**`update_app.py`**

It will create the HTML app

### Building from Source

If you want to edit the React web source code and rebuild the standalone HTML file:

```bash
cd web
npm install
npm run build
```
This will generate a new `dist/index.html` containing the entire standalone application. You can copy it to the root folder and rename it to whatever you'd like.

(This is what the update script is doing)

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
