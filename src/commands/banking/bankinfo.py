from nextcord.ext import commands
from nextcord import Embed
from supabase import create_client, Client
import configparser
import os
from custom.emoji_loader import load_emojis
from custom.supabase_client import get_supabase_client
import yaml

class BankSystem(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.emojis = load_emojis() # loads emojis from the emojis.yaml file (from emoji_loader.py)
        self.supabase = get_supabase_client() # loads supabase client from the custom/supabase_client.py file
        self.paid_emoji = self.emojis.get('PAID')

    @commands.command()
    async def bank_account(self, ctx):
        user_id = str(ctx.author.id)
        response = self.supabase.table('currency_table').select('*').eq('user_id', user_id).execute()
        if response.data:
            currency = response.data[0].get('currency', 0)
            
            embed = Embed(title=f"{self.paid_emoji} Bank Account Statement", color=0x00ff00)
            embed.add_field(name="Account Holder", value=f"**{ctx.author.display_name}**", inline=False)
            embed.add_field(name="Current Balance", value=f"```yaml\n${currency:.2f}\n```", inline=False)
            
            creative_footer = "As fresh as your morning coffee ☕"
            embed.set_footer(text=creative_footer)

            await ctx.send(embed=embed)
        else:
            await ctx.send("You do not have an account or any currency yet.")

def setup(bot):
    bot.add_cog(BankSystem(bot))

