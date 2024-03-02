from rich.console import Console
from rich.table import Table
from rich import box
import sys
import nextcord  # Ensure Nextcord is installed and imported

console = Console()

def custom_startup():
    console.print("[bold magenta]Bot Startup Sequence Initiated[/bold magenta]", justify="center")

    table = Table(box=box.ROUNDED, show_header=True, header_style="bold blue")
    table.add_column("Info", style="dim", width=20)
    table.add_column("Details", justify="left")

    # Example data - replace with your bot's actual data
    bot_made_by = "Delta Team (Wade)"
    version = "0.0.1"
    support_server = "https://your.support.server"
    python_version = sys.version.split()[0]  # Get the Python version (only the version number)
    nextcord_version = nextcord.__version__  # Get the Nextcord version

    table.add_row("Bot Made By", bot_made_by)
    table.add_row("Version", version)
    table.add_row("Support Server", support_server)
    table.add_row("Python Version", python_version)  # Add Python version row
    table.add_row("Nextcord Version", nextcord_version)  # Add Nextcord version row

    console.print(table)

    console.print("[green]Custom startup tasks completed.[/green]", justify="center")
