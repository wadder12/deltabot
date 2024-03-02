from nextcord.ext import commands
import configparser
import os
from supabase import create_client, Client
from custom.supabase_client import get_supabase_client

class InventoryManagementCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.supabase = get_supabase_client()

    @commands.command()
    async def buy_item(self, ctx, *, item_name: str):
        item_response = self.supabase.table('shop_items').select('*').ilike('name', f'%{item_name}%').execute()
        if not item_response.data or len(item_response.data) == 0:
            await ctx.send("This item does not exist.")
            return

        item = item_response.data[0]
        currency_response = self.supabase.table('currency_table').select('currency').eq('user_id', str(ctx.author.id)).execute()
        if not currency_response.data or len(currency_response.data) == 0 or currency_response.data[0]['currency'] < item['cost']:
            await ctx.send("You do not have enough coins to buy this item.")
            return
        new_balance = currency_response.data[0]['currency'] - item['cost']

        update_response = self.supabase.table('currency_table').update({'currency': new_balance}).eq('user_id', str(ctx.author.id)).execute()

        if hasattr(update_response, 'data') and update_response.data:
            inventory_response = self.supabase.table('user_inventory').insert({
                'user_id': str(ctx.author.id),
                'item_id': item['item_id'],
                'quantity': 1  # Assumes a quantity of 1
            }).execute()

            if hasattr(inventory_response, 'data') and inventory_response.data:
                await ctx.send(f"You have successfully purchased {item['name']} for {item['cost']} coins! Your new balance is {new_balance} coins, and the item has been added to your inventory.")
            else:
                print(f"Failed to add item to inventory. Response: {inventory_response}")
                await ctx.send("Purchase successful, but there was an error adding the item to your inventory.")
        else:
            print(f"Failed to update currency. Response: {update_response}")
            await ctx.send("There was an error processing your purchase. Please try again.")

def setup(bot):
    bot.add_cog(InventoryManagementCog(bot))



## currently not updating the users balance after buying somthing