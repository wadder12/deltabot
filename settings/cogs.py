import os
import traceback
from nextcord.ext import commands
from rich.console import Console
from rich.markup import escape
from rich.traceback import install
from rich.text import Text

# Install rich traceback globally for prettier error messages
install(show_locals=True)

console = Console()

async def load_cogs_async(bot):
    cogs_dir = 'src'
    for root, dirs, files in os.walk(cogs_dir):
        for file in files:
            if file.endswith('.py') and not file.startswith('_'):
                cog = os.path.join(root, file).replace('/', '.').replace('\\', '.')[:-3]
                try:
                    # Assuming bot.load_extension is synchronous, it doesn't need to be awaited
                    bot.load_extension(cog)
                    console.print(f"[green]✔ Successfully loaded:[/green] [bold]{escape(cog)}[/bold]")
                except Exception as e:
                    console.print(f"[red]✘ Failed to load cog:[/red] [bold]{escape(cog)}[/bold]", style="bold red")
                    # Using rich's print_exception to neatly display errors
                    console.print_exception()
