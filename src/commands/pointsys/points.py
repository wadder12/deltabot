from nextcord.ext import commands
from nextcord import Embed
from supabase import create_client, Client
import configparser
import os
from custom.emoji_loader import load_emojis
from custom.supabase_client import get_supabase_client


class PointsSystem(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.emojis = load_emojis() # loads emojis from the emojis.yaml file (from emoji_loader.py)
        self.supabase = get_supabase_client()

        self.coin_emoji = self.emojis.get('COIN')
        self.checkmark_emoji = self.emojis.get('CHECKMARK')
        self.x_emoji = self.emojis.get('X')
        self.shuffle_emoji = self.emojis.get('SHUFFLE')
        self.autoplay_emoji = self.emojis.get('AUTOPLAY')

    def calculate_level(self, points):
        return points // 100 

    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.author.bot and message.guild:
            points_to_add = 1
            user_id = str(message.author.id)

            response = self.supabase.table('points_table').select('*').eq('user_id', user_id).execute()
            current_points = 0
            current_level = 0
            if response.data:
                current_points = response.data[0].get('points', 0)
                current_level = response.data[0].get('level', 0)
            
            new_points = current_points + points_to_add
            new_level = self.calculate_level(new_points)

            if new_level > current_level:
                self.supabase.table('points_table').upsert({'user_id': user_id, 'points': new_points, 'level': new_level}, on_conflict='user_id').execute()
                embed = Embed(title=f"{self.x_emoji} Level Up! {self.x_emoji}", description=f"{message.author.display_name}, you've reached level {new_level}!", color=0x00ff00)
                await message.channel.send(embed=embed)
            else:
                self.supabase.table('points_table').upsert({'user_id': user_id, 'points': new_points}, on_conflict='user_id').execute()

def setup(bot):
    bot.add_cog(PointsSystem(bot))
