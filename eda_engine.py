#!/usr/bin/env python3
"""
Warframe EDA/ETA Loadout Engine
Exclusively uses pure base variants of Warframes and Weapons (no Primes / Kuva / Tenet / Vandals / Prismas).
Links directly to official wiki.warframe.com.
"""

import json
import os
import random
import urllib.parse
import urllib.request
from typing import Dict, List, Any, Optional

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
CACHE_FILE = os.path.join(DATA_DIR, "warframe_items_cache.json")

WFCD_URLS = {
    "warframes": "https://raw.githubusercontent.com/WFCD/warframe-items/master/data/json/Warframes.json",
    "primary": "https://raw.githubusercontent.com/WFCD/warframe-items/master/data/json/Primary.json",
    "secondary": "https://raw.githubusercontent.com/WFCD/warframe-items/master/data/json/Secondary.json",
    "melee": "https://raw.githubusercontent.com/WFCD/warframe-items/master/data/json/Melee.json"
}

DISALLOWED_PREFIXES = (
    "Kuva ", "Tenet ", "Prisma ", "Vandal ", "Wraith ", "Dex ", 
    "Sancti ", "Synoid ", "Telos ", "Secura ", "Rakta ", "Ceti ", 
    "Carmine ", "MK1-", "Mk1-", "Mutalist ", "Dragon ", "Mara ", "Coda "
)

DISALLOWED_SUFFIXES = (
    " Prime", " Vandal", " Wraith", " Prisma", " Dex", " Mara", " (Dual)"
)

EXCLUDED_NAMES = {
    "Bonewidow", "Voidrig", "Suit", "Iron Staff", "Artemis Bow", "Exalted Blade",
    "Desert Wind", "Regulators", "Dex Pixia", "Balefire", "Diwata", "Garuda Talons",
    "Shadow Claws", "Sevagoth's Shadow", "Venari", "Venari Prime", "Hildryn's Balefire Charger",
    "Mesa's Peacemaker", "Ivara's Artemis Bow", "Titania's Dex Pixia", "Titania's Diwata",
    "Wukong's Iron Staff", "Baruuk's Desert Wind", "Excalibur's Exalted Blade", "Valkyr's Talons",
    "Follie", "Excalibur Umbra", "Sirocco"
}


def make_official_wiki_url(item_name: str) -> str:
    """Generate the official wiki.warframe.com link."""
    formatted_name = item_name.replace(" ", "_")
    encoded = urllib.parse.quote(formatted_name, safe=":/_")
    return f"https://wiki.warframe.com/w/{encoded}"


def extract_base_family(name: str) -> str:
    """Extracts base family name (e.g., 'Saryn Prime' -> 'Saryn', 'Kuva Bramma' -> 'Bramma')."""
    cleaned = name
    for p in DISALLOWED_PREFIXES:
        if cleaned.startswith(p):
            cleaned = cleaned[len(p):]
    for s in DISALLOWED_SUFFIXES:
        if cleaned.endswith(s):
            cleaned = cleaned[:-len(s)]
    return cleaned.strip()


def is_pure_base_item(item: Dict[str, Any]) -> bool:
    name = item.get("name", "")
    if name in EXCLUDED_NAMES:
        return False
    if item.get("isPrime") or name.endswith(" Prime"):
        return False
    if item.get("isKuva") or item.get("isTenet"):
        return False
    if any(name.startswith(p) for p in DISALLOWED_PREFIXES):
        return False
    if any(name.endswith(s) for s in DISALLOWED_SUFFIXES):
        return False
    return True


class EDADatabase:
    def __init__(self):
        self.warframes: List[Dict[str, Any]] = []
        self.primary: List[Dict[str, Any]] = []
        self.secondary: List[Dict[str, Any]] = []
        self.melee: List[Dict[str, Any]] = []
        self.all_items: List[Dict[str, Any]] = []
        self.load_or_sync_data()

    def load_or_sync_data(self, force_refresh: bool = False):
        """Loads cached data or fetches from remote repository."""
        os.makedirs(DATA_DIR, exist_ok=True)
        if not force_refresh and os.path.exists(CACHE_FILE):
            try:
                with open(CACHE_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.warframes = data.get("warframes", [])
                    self.primary = data.get("primary", [])
                    self.secondary = data.get("secondary", [])
                    self.melee = data.get("melee", [])
                    self.all_items = self.warframes + self.primary + self.secondary + self.melee
                    if len(self.warframes) > 0 and all(is_pure_base_item(it) for it in self.all_items):
                        return
            except Exception as e:
                print(f"[Warning] Cache read failed: {e}. Fetching fresh data...")

        self.sync_remote_data()

    def sync_remote_data(self):
        """Fetches and extracts strictly pure BASE variants from WFCD official datasets."""
        raw_datasets = {}
        for category, url in WFCD_URLS.items():
            try:
                req = urllib.request.Request(url, headers={"User-Agent": "WarframeEDATool/1.0"})
                with urllib.request.urlopen(req, timeout=10) as resp:
                    raw_datasets[category] = json.loads(resp.read().decode("utf-8"))
            except Exception as e:
                print(f"[Error] Failed to fetch {category}: {e}")
                raw_datasets[category] = []

        raw_frames = self._clean_raw_items(raw_datasets.get("warframes", []), "Warframe")
        raw_primary = self._clean_raw_items(raw_datasets.get("primary", []), "Primary")
        raw_secondary = self._clean_raw_items(raw_datasets.get("secondary", []), "Secondary")
        raw_melee = self._clean_raw_items(raw_datasets.get("melee", []), "Melee")

        # Filter strictly to pure base items
        self.warframes = [it for it in raw_frames if is_pure_base_item(it)]
        self.primary = [it for it in raw_primary if is_pure_base_item(it)]
        self.secondary = [it for it in raw_secondary if is_pure_base_item(it)]
        self.melee = [it for it in raw_melee if is_pure_base_item(it)]
        self.all_items = self.warframes + self.primary + self.secondary + self.melee

        # Save to cache
        cache_data = {
            "warframes": self.warframes,
            "primary": self.primary,
            "secondary": self.secondary,
            "melee": self.melee,
            "updated_at": "2026-08-25",
            "pure_base_only": True
        }
        with open(CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(cache_data, f, indent=2)

    def _clean_raw_items(self, raw_list: List[Dict[str, Any]], category: str) -> List[Dict[str, Any]]:
        """Filters out non-equipment, sentinels, archwing, exalted, and modular components."""
        cleaned = []
        seen_names = set()

        ignored_categories = {
            "SentinelWeapons", "SpaceGuns", "SpaceMelee", "CrewShipWeapons", 
            "Pets", "Sentinels", "Misc", "Components"
        }
        modular_keywords = [
            "component", "chamber", "grip", "link", "loader", "strike", "brace", 
            "prism", "scaffold", "zaw component", "kitgun component", "amp component"
        ]

        for item in raw_list:
            name = item.get("name", "").strip()
            if not name or name in seen_names or name in EXCLUDED_NAMES:
                continue

            prod_cat = item.get("productCategory", "")
            item_type = item.get("type", "")
            tags = [t.lower() for t in item.get("tags", [])]

            if prod_cat in ignored_categories:
                continue
            if "Archwing" in item_type or "Arch-Gun" in item_type or "Arch-Melee" in item_type:
                continue
            if "Exalted" in item_type or "exalted" in tags:
                continue
            if item.get("category") == "Warframes" and ("Suit" in name or "Warframe" not in item.get("category", "")):
                continue

            type_lower = item_type.lower()
            if any(mk in type_lower for mk in modular_keywords):
                continue
            if any(name.lower().endswith(f" {mk}") for mk in ["ii", "iii", "iv"]):
                continue

            image_name = item.get("imageName")
            image_url = f"https://cdn.warframestat.us/img/{image_name}" if image_name else ""

            is_prime = item.get("isPrime", False) or "Prime" in name
            is_incarnon = "incarnon" in tags or "Incarnon" in name or "Incarnon" in item.get("description", "")
            is_kuva = name.startswith("Kuva ")
            is_tenet = name.startswith("Tenet ")

            wiki_link = make_official_wiki_url(name)

            entry = {
                "name": name,
                "baseFamily": extract_base_family(name),
                "category": category,
                "type": item.get("type", category),
                "description": item.get("description", ""),
                "masteryReq": item.get("masteryReq", 0),
                "wikiUrl": wiki_link,
                "imageUrl": image_url,
                "isPrime": is_prime,
                "isIncarnon": is_incarnon,
                "isKuva": is_kuva,
                "isTenet": is_tenet,
                "polarities": item.get("polarities", []),
                "damage": item.get("damagePerShot") or item.get("totalDamage") or 0,
                "critChance": item.get("criticalChance", 0),
                "critMultiplier": item.get("criticalMultiplier", 0),
                "statusChance": item.get("procChance", 0),
                "passive": item.get("passiveDescription", "")
            }
            cleaned.append(entry)
            seen_names.add(name)

        return cleaned

    def roll_eda(self) -> Dict[str, List[Dict[str, Any]]]:
        """Generates exactly 3 base Warframes, 3 base Primaries, 3 base Secondaries, and 3 base Melees."""
        return {
            "warframes": random.sample(self.warframes, min(3, len(self.warframes))),
            "primaries": random.sample(self.primary, min(3, len(self.primary))),
            "secondaries": random.sample(self.secondary, min(3, len(self.secondary))),
            "melees": random.sample(self.melee, min(3, len(self.melee)))
        }

    def search_wiki(self, query: str, limit: int = 15) -> List[Dict[str, Any]]:
        """Searches across all cached Warframe base items."""
        q = query.strip().lower()
        if not q:
            return []

        results = []
        for item in self.all_items:
            score = 0
            name_lower = item["name"].lower()
            desc_lower = item["description"].lower()
            type_lower = item["type"].lower()
            cat_lower = item["category"].lower()

            if q == name_lower:
                score += 100
            elif name_lower.startswith(q):
                score += 50
            elif q in name_lower:
                score += 30
            
            if q in type_lower:
                score += 15
            if q in cat_lower:
                score += 10
            if q in desc_lower:
                score += 5

            if item["isIncarnon"] and ("incarnon" in q):
                score += 25

            if score > 0:
                results.append((score, item))

        results.sort(key=lambda x: x[0], reverse=True)
        return [r[1] for r in results[:limit]]

    def format_discord_markdown(self, eda_data: Dict[str, List[Dict[str, Any]]]) -> str:
        """Formats the 3-of-each loadout roll for Discord / Markdown sharing."""
        lines = [
            "🏆 **WARFRAME EDA / ETA LOADOUT PARAMETERS**",
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
            "",
            "✨ **WARFRAME (3 Choices)**"
        ]
        for w in eda_data["warframes"]:
            lines.append(f"• [{w['name']}]({w['wikiUrl']}) `MR{w['masteryReq']}`")
        
        lines.append("\n🎯 **PRIMARY WEAPONS (3 Choices)**")
        for p in eda_data["primaries"]:
            lines.append(f"• [{p['name']}]({p['wikiUrl']}) ({p['type']}) `MR{p['masteryReq']}`")

        lines.append("\n🔫 **SECONDARY WEAPONS (3 Choices)**")
        for s in eda_data["secondaries"]:
            lines.append(f"• [{s['name']}]({s['wikiUrl']}) ({s['type']}) `MR{s['masteryReq']}`")

        lines.append("\n⚔️ **MELEE WEAPONS (3 Choices)**")
        for m in eda_data["melees"]:
            lines.append(f"• [{m['name']}]({m['wikiUrl']}) ({m['type']}) `MR{m['masteryReq']}`")

        lines.append("\n🔗 *Generated with Warframe EDA Tool (Official Wiki: wiki.warframe.com)*")
        return "\n".join(lines)

