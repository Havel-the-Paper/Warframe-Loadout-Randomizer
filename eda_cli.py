#!/usr/bin/env python3
"""
Warframe EDA/ETA CLI Interface
Outputs 3 of each: Warframe, Primary, Secondary, Melee with Official Wiki (wiki.warframe.com) links.
"""

import sys
import argparse
import os
from typing import Dict, Any, List

try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.prompt import Prompt
    from rich import print as rprint
except ImportError:
    print("Rich is required. Installing rich...")
    os.system("pip install rich")
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.prompt import Prompt
    from rich import print as rprint

from eda_engine import EDADatabase

console = Console()

OROKIN_BANNER = r"""
[bold gold1]
 ╔═══════════════════════════════════════════════════════════════════════════╗
 ║  ███████╗██████╗  █████╗     ███████╗████████╗ █████╗                     ║
 ║  ██╔════╝██╔══██╗██╔══██╗    ██╔════╝╚══██╔══╝██╔══██╗                    ║
 ║  █████╗  ██║  ██║███████║    █████╗     ██║   ███████║                    ║
 ║  ██╔══╝  ██║  ██║██╔══██║    ██╔══╝     ██║   ██╔══██║                    ║
 ║  ███████╗██████╔╝██║  ██║    ███████╗   ██║   ██║  ██║                    ║
 ║  ╚══════╝╚═════╝ ╚═╝  ╚═╝    ╚══════╝   ╚═╝   ╚═╝  ╚═╝                    ║
 ║              [dim yellow]EDA / ETA LOADOUT PARAMETERS • 3 OF EACH[/dim yellow]             ║
 ╚═══════════════════════════════════════════════════════════════════════════╝
[/bold gold1]"""


def create_category_table(category_name: str, items: List[Dict[str, Any]], color: str, icon: str) -> Table:
    table = Table(
        title=f"[{color} bold]{icon} {category_name.upper()} (3 CHOICES)[/{color} bold]",
        title_justify="left",
        border_style=color,
        header_style=f"bold {color}",
        expand=True,
        show_header=True
    )
    table.add_column("#", style="dim", width=3)
    table.add_column("Equipment", style="bold white")
    table.add_column("Type / Class", style="cyan")
    table.add_column("MR", justify="center", style="yellow", width=4)
    table.add_column("Official Wiki Link (wiki.warframe.com)", style="blue underline")

    for i, item in enumerate(items, 1):
        name_styled = item["name"]
        if item.get("isPrime"):
            name_styled = f"[bold gold1]{item['name']}[/bold gold1] [dim](Prime)[/dim]"
        elif item.get("isIncarnon"):
            name_styled = f"[bold magenta]{item['name']}[/bold magenta] [dim](Incarnon)[/dim]"
        elif item.get("isKuva"):
            name_styled = f"[bold red]{item['name']}[/bold red] [dim](Kuva)[/dim]"
        elif item.get("isTenet"):
            name_styled = f"[bold blue]{item['name']}[/bold blue] [dim](Tenet)[/dim]"

        mr_str = f"{item['masteryReq']}" if item['masteryReq'] > 0 else "-"
        wiki_link = f"[link={item['wikiUrl']}]{item['wikiUrl']}[/link]"
        table.add_row(str(i), name_styled, item["type"], mr_str, wiki_link)

    return table


def render_eda_roll(roll_data: Dict[str, Any]):
    console.print(OROKIN_BANNER)
    
    # 4 Category Tables
    t_frames = create_category_table("Warframe", roll_data["warframes"], "gold1", "🛡️")
    t_primaries = create_category_table("Primary Weapon", roll_data["primaries"], "bright_cyan", "🎯")
    t_secondaries = create_category_table("Secondary Weapon", roll_data["secondaries"], "bright_green", "🔫")
    t_melees = create_category_table("Melee Weapon", roll_data["melees"], "bright_magenta", "⚔️")

    console.print(t_frames)
    console.print(t_primaries)
    console.print(t_secondaries)
    console.print(t_melees)
    console.print("[dim cyan]Tip: Click any wiki URL above to inspect the weapon/warframe on wiki.warframe.com[/dim cyan]\n")


def search_cli(query: str):
    db = EDADatabase()
    results = db.search_wiki(query, limit=15)
    
    console.print(f"\n[bold gold1]🔍 OFFICIAL WIKI SEARCH RESULTS FOR:[/bold gold1] [bold white]'{query}'[/bold white]")
    if not results:
        console.print("[bold red]No matching items found on the official wiki index.[/bold red]\n")
        return

    table = Table(border_style="gold1", expand=True, header_style="bold gold1")
    table.add_column("Item Name", style="bold white", width=24)
    table.add_column("Category", style="cyan", width=12)
    table.add_column("Type", style="yellow", width=15)
    table.add_column("MR", justify="center", width=4)
    table.add_column("Official Wiki Link (wiki.warframe.com)", style="blue underline")

    for item in results:
        name_str = item["name"]
        if item.get("isPrime"):
            name_str = f"[bold gold1]{item['name']}[/bold gold1]"
        elif item.get("isIncarnon"):
            name_str = f"[bold magenta]{item['name']}[/bold magenta]"

        mr_str = f"{item['masteryReq']}" if item['masteryReq'] > 0 else "-"
        table.add_row(
            name_str,
            item["category"],
            item["type"],
            mr_str,
            f"[link={item['wikiUrl']}]{item['wikiUrl']}[/link]"
        )

    console.print(table)
    console.print(f"[dim]Found {len(results)} matches from official Warframe Wiki index.[/dim]\n")


def interactive_mode():
    db = EDADatabase()
    roll_data = db.roll_eda()
    locked = {"warframes": [False, False, False], "primaries": [False, False, False], "secondaries": [False, False, False], "melees": [False, False, False]}

    while True:
        console.clear()
        render_eda_roll(roll_data)
        console.print("[bold yellow]Interactive Controls:[/bold yellow]")
        console.print("[bold cyan][r][/bold cyan] Reroll unlocked gear  |  [bold cyan][s][/bold cyan] Search Wiki  |  [bold cyan][e][/bold cyan] Export Discord/MD  |  [bold cyan][q][/bold cyan] Quit")
        
        cmd = Prompt.ask("\n[bold gold1]Enter command[/bold gold1]", default="r").strip().lower()

        if cmd == "q":
            console.print("[bold green]Exiting EDA Loadout Generator. Good hunting, Tenno![/bold green]")
            break
        elif cmd == "r":
            new_roll = db.roll_eda()
            for cat in ["warframes", "primaries", "secondaries", "melees"]:
                for i in range(3):
                    if not locked[cat][i]:
                        roll_data[cat][i] = new_roll[cat][i]
        elif cmd == "s":
            q = Prompt.ask("Search wiki for")
            if q:
                search_cli(q)
                Prompt.ask("\nPress Enter to return to EDA loadout")
        elif cmd == "e":
            text = db.format_discord_markdown(roll_data)
            console.print("\n[bold green]=== EXPORTED MARKDOWN (Copy below) ===[/bold green]\n")
            print(text)
            Prompt.ask("\nPress Enter to continue")


def main():
    parser = argparse.ArgumentParser(description="Warframe EDA/ETA Loadout Generator (3 of each: Warframe, Primary, Secondary, Melee)")
    parser.add_argument("action", nargs="?", default="roll", choices=["roll", "search", "interactive", "export", "update"], help="Action to perform")
    parser.add_argument("query", nargs="?", default="", help="Query string for search")
    parser.add_argument("--json", action="store_true", help="Output raw JSON format")

    args = parser.parse_args()
    db = EDADatabase()

    if args.action == "update":
        console.print("[bold yellow]Syncing fresh item database from official Warframe repositories...[/bold yellow]")
        db.load_or_sync_data(force_refresh=True)
        console.print(f"[bold green]Sync complete! Loaded {len(db.all_items)} total items.[/bold green]")
    elif args.action == "search":
        if not args.query:
            console.print("[bold red]Please specify a search term: python eda_cli.py search <query>[/bold red]")
            sys.exit(1)
        search_cli(args.query)
    elif args.action == "interactive":
        interactive_mode()
    elif args.action == "export":
        roll_data = db.roll_eda()
        print(db.format_discord_markdown(roll_data))
    else:  # roll
        roll_data = db.roll_eda()
        if args.json:
            import json
            print(json.dumps(roll_data, indent=2))
        else:
            render_eda_roll(roll_data)


if __name__ == "__main__":
    main()
