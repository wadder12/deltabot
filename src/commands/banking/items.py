import nextcord
from nextcord.ext import commands
from nextcord.ui import View, Select
from nextcord import SelectOption, Embed
import configparser
import os
from supabase import create_client, Client
from custom.supabase_client import get_supabase_client
from dotenv import load_dotenv
load_dotenv()

class ShopItemsSelect(Select):
    def __init__(self, items):
        options = [
            SelectOption(label=item['name'], description=f"Cost: {item['cost']} coins", value=str(item['item_id']))
            for item in items[:25]  # Limit to 25 items to adhere to Discord's limits
        ]
        super().__init__(placeholder="Select an item for more details...", min_values=1, max_values=1, options=options)
        self.items = items

    async def callback(self, interaction: nextcord.Interaction):
        item_id = int(self.values[0])
        item = next((item for item in self.items if item['item_id'] == item_id), None)
        
        if item:
            description = f"**Description:** {item['description']}\n**Cost:** {item['cost']} coins"
            await interaction.response.send_message(description, ephemeral=True)

class ShopItemsView(View):
    def __init__(self, items):
        super().__init__()
        self.add_item(ShopItemsSelect(items))
        self.supabase = get_supabase_client()

class ItemListCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot


    @commands.command()
    async def list_items(self, ctx):
        response = self.supabase.table('shop_items').select('*').execute()
        if response.data:
            view = ShopItemsView(response.data)
            await ctx.send("Select an item to view details:", view=view)
        else:
            await ctx.send("The shop is currently empty. Check back later!")

def setup(bot):
    bot.add_cog(ItemListCog(bot))
