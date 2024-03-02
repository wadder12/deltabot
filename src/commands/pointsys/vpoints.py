from nextcord.ext import commands
from nextcord import Embed, File
import configparser
from supabase import create_client, Client
import os
from custom.progress import generate_progress_bar_image
from custom.emoji_loader import load_emojis
from custom.supabase_client import get_supabase_client

class ViewPoints(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.emojis = load_emojis() # loads emojis from the emojis.yaml file (from emoji_loader.py)
        self.supabase = get_supabase_client()
        self.coin_emoji = self.emojis.get('COIN')
        self.checkmark_emoji = self.emojis.get('CHECKMARK')
        self.x_emoji = self.emojis.get('X')
        self.shuffle_emoji = self.emojis.get('SHUFFLE')
        self.autoplay_emoji = self.emojis.get('AUTOPLAY')
        
    @commands.command(name='mypoints')
    async def my_points(self, ctx):
        user_id = str(ctx.author.id)
        response = self.supabase.table('points_table').select('*').eq('user_id', user_id).execute()

        if response.data:
            points = response.data[0].get('points', 0)
            level = response.data[0].get('level', 0)
            points_for_current_level = 100 * level
            points_for_next_level = 100 * (level + 1)
            progress = points - points_for_current_level
            total_points_needed = points_for_next_level - points_for_current_level
            progress_percentage = (progress / total_points_needed) * 100
            progress_image_path = generate_progress_bar_image(progress_percentage)

            embed = Embed(title=f"{self.coin_emoji} Points and Level", description=f"**{ctx.author.display_name}**, you have **{points}** points and are at level **{level}**.\nProgress to next level: {progress_percentage:.2f}%", color=0x00ff00)
            embed.add_field(name="Points", value=f"{points} {self.coin_emoji}", inline=True)
            embed.add_field(name="Level", value=f"{level} {self.checkmark_emoji}", inline=True)
            file = File(progress_image_path, filename="progress.png")
            embed.set_image(url="attachment://progress.png")
            embed.set_footer(text=f"Powered by Delta Bot {self.shuffle_emoji}")
            embed.timestamp = ctx.message.created_at

            await ctx.send(file=file, embed=embed)
        else:
            embed = Embed(title="Points and Level", description=f"**{ctx.author.display_name}**, you have **0** points and are at level **0**.", color=0x00ff00)
            embed.add_field(name="Points", value="0", inline=True)
            embed.add_field(name="Level", value="0", inline=True)
            embed.set_footer(text=f"Powered by Delta Bot {self.autoplay_emoji}")
            embed.timestamp = ctx.message.created_at
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(ViewPoints(bot))
