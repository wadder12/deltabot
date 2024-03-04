import os
from dotenv import load_dotenv
import aiohttp
import nextcord
from nextcord.ext import commands
load_dotenv()

class UptimeMonitoring(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.team_token = os.getenv('TEAM_TOKEN')
        self.heartbeat_id = os.getenv('HEARTBEAT_ID')

    @nextcord.slash_command()
    async def get_heartbeat_status(self, interaction: nextcord.Interaction):
        if not self.team_token or not self.heartbeat_id:
            await interaction.send("Error: Required environment variables `TEAM_TOKEN` or `HEARTBEAT_ID` are not set.")
            return

        url = f"https://uptime.betterstack.com/api/v2/heartbeats/{self.heartbeat_id}"
        headers = {"Authorization": f"Bearer {self.team_token}"}
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    heartbeat = data.get('data', {}).get('attributes', {})
                    if heartbeat:
                        color = nextcord.Color.green() if heartbeat.get('status') == "up" else nextcord.Color.red()
                        embed = nextcord.Embed(
                            title=f"🫀 Heartbeat Status: {heartbeat.get('name', 'N/A')}",
                            description=f"Status: **{heartbeat.get('status').upper()}**",
                            color=color
                        )
                        embed.add_field(name="Email Notifications", value="✅ Enabled" if heartbeat.get('email') else "❌ Disabled", inline=True)
                        embed.add_field(name="Paused", value="✅ Yes" if heartbeat.get('paused') else "❌ No", inline=True)
                        status_emoji = "✅" if heartbeat.get('status') == "up" else "❌"
                        embed.add_field(name="Current Status", value=f"{status_emoji} {heartbeat.get('status').capitalize()}", inline=False)
                        embed.set_footer(text=f"Heartbeat ID: {self.heartbeat_id}")
                        embed.timestamp = nextcord.utils.utcnow()

                        await interaction.send(embed=embed)
                    else:
                        await interaction.send("Error: Heartbeat attributes not found in the response.")
                else:
                    await interaction.send(f"Error: Unable to fetch heartbeat. Response status: {response.status}")

def setup(bot):
    bot.add_cog(UptimeMonitoring(bot))
