import os

from dotenv import load_dotenv
from nextcord import Intents
from nextcord.ext import commands

from custom.startup.bot_startup import custom_startup
from settings.cogs import load_cogs_async

load_dotenv()

discord_token = os.getenv("DISCORD_TOKEN")
command_prefix = os.getenv("COMMAND_PREFIX")
intents = Intents.all()
bot = commands.Bot(command_prefix=command_prefix, intents=intents)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")
    await load_cogs_async(bot)


if __name__ == "__main__":
    custom_startup()
    if discord_token:
        bot.run(discord_token)
    else:
        print("Error: DISCORD_TOKEN environment variable is not set.")

    """ hello 
    - this is the first file for your bot - if you want to change be free - but make sure you don't break anything (its simple)
    """
