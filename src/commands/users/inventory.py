from nextcord import Embed
from nextcord.ext import commands
import configparser
import os
from supabase import create_client
from custom.emoji_loader import load_emojis
from custom.supabase_client import get_supabase_client


class InventoryViewCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        emoji_config = load_emojis()
        self.supabase = get_supabase_client()
        self.coin_emoji = emoji_config.get('COIN')

    @commands.command()
    async def view_inventory(self, ctx):
        user_id = str(ctx.author.id)

        inventory_response = self.supabase.table('user_inventory').select('*').eq('user_id', user_id).execute()
        
        if not inventory_response.data or len(inventory_response.data) == 0:
            await ctx.send("Your inventory is empty.")
            return
        
        embed = Embed(title="Inventory", description=f"{ctx.author.display_name}'s Items", color=0x00ff00)
        
        for item in inventory_response.data:
            item_details = self.supabase.table('shop_items').select('*').eq('item_id', item['item_id']).execute()
            if item_details.data:
                item_name = item_details.data[0]['name']
                item_quantity = item['quantity']
                embed.add_field(name=f"{self.coin_emoji} {item_name}", value=f"Quantity: x{item_quantity}", inline=False)
            else:
                embed.add_field(name="Unknown Item", value="Quantity: ❓", inline=False)
        
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(InventoryViewCog(bot))

