import json
import nextcord
import os
import time  # Import the time module
from nextcord.ext import commands

class EmbedSender(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.allowed_user_ids = [int(id.strip()) for id in os.getenv('ALLOWED_USER_IDS', '').split(',')]

    @commands.command()
    async def send_embed(self, ctx, channel: nextcord.TextChannel, *, json_string):
        if ctx.author.id not in self.allowed_user_ids:
            await ctx.send("You do not have permission to use this command.")
            return

        try:
            data = json.loads(json_string)
            content = data.get("content", "")
            embed_data = data.get("embeds", [])

            if not embed_data or not isinstance(embed_data, list):
                await ctx.send("No valid embeds found in the JSON.")
                return

            embeds = [self.construct_embed(embed_dict) for embed_dict in embed_data if self.construct_embed(embed_dict)]

            if embeds:
                start_time = time.time()  # Capture start time
                await channel.send(content, embeds=embeds)
                end_time = time.time()  # Capture end time
                elapsed_time = end_time - start_time  # Calculate elapsed time
                await ctx.send(embed=self.success_embed(channel, elapsed_time))
            else:
                await ctx.send("Failed to create any valid embeds.")

        except json.JSONDecodeError:
            await ctx.send("Invalid JSON.")
        except Exception as e:
            await ctx.send(f"An error occurred: {e}")

    def construct_embed(self, embed_dict):
        try:
            if 'color' in embed_dict and embed_dict['color'] is None:
                del embed_dict['color']
            return nextcord.Embed.from_dict(embed_dict)
        except Exception as e:
            print(f"Embed construction error: {e}")
            return None

    def success_embed(self, channel, elapsed_time):
        return nextcord.Embed(
            title="✅ Message Sent Successfully",
            description=f"The message has been sent to {channel.mention}. It took {elapsed_time:.2f} seconds.",
            color=0x00ff00  
        )

def setup(bot):
    bot.add_cog(EmbedSender(bot))