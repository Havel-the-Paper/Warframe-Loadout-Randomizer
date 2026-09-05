import urllib.request
import json
import urllib.parse

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

def extract_base_family(name: str) -> str:
    cleaned = name
    for p in DISALLOWED_PREFIXES:
        if cleaned.startswith(p):
            cleaned = cleaned[len(p):]
    for s in DISALLOWED_SUFFIXES:
        if cleaned.endswith(s):
            cleaned = cleaned[:-len(s)]
    return cleaned.strip()

items = [
    {"name": "Karak", "isKuva": False},
    {"name": "Kuva Karak", "isKuva": True},
    {"name": "Kuva Bramma", "isKuva": True},
    {"name": "Tenet Envoy", "isTenet": True},
    {"name": "Braton", "isKuva": False},
    {"name": "Braton Prime", "isPrime": True},
    {"name": "Reaper Prime", "isPrime": True},
]

for it in items:
    it["baseFamily"] = extract_base_family(it["name"])

def get_best(raw_items):
    families = {}
    for item in raw_items:
        if item["name"] in EXCLUDED_NAMES:
            continue
        bf = item["baseFamily"]
        if bf not in families:
            families[bf] = []
        families[bf].append(item)
        
    results = []
    for bf, family_items in families.items():
        pure_items = []
        for it in family_items:
            name = it["name"]
            is_pure = True
            if it.get("isPrime") or name.endswith(" Prime"): is_pure = False
            elif it.get("isKuva") or it.get("isTenet"): is_pure = False
            elif any(name.startswith(p) for p in DISALLOWED_PREFIXES): is_pure = False
            elif any(name.endswith(s) for s in DISALLOWED_SUFFIXES): is_pure = False
            
            if is_pure:
                pure_items.append(it)
        
        if pure_items:
            pure_items.sort(key=lambda x: len(x["name"]))
            results.append(pure_items[0])
        else:
            def score(it):
                if it.get("isKuva") or it.get("isTenet"): return 1
                if it.get("isPrime") or it["name"].endswith(" Prime"): return 2
                return 3
            
            family_items.sort(key=lambda x: (score(x), len(x["name"])))
            results.append(family_items[0])
            
    return results

print([x["name"] for x in get_best(items)])
