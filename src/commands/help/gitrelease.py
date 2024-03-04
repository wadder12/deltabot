import aiohttp
import nextcord
from nextcord.ext import commands

class GitRelease(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command()
    async def latest_release(self, interaction: nextcord.Interaction):
        url = "https://api.github.com/repos/wadder12/deltabot/releases/latest"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    latest_release = await response.json()
                    # Create an embed message
                    embed = nextcord.Embed(title=f"Latest Release: {latest_release['name']}",
                                           url=latest_release['html_url'],
                                           description="Here are the release notes:",
                                           color=nextcord.Color.blue())  # You can change the color here
                    # Format the body with YAML formatting
                    formatted_body = f"```yaml\n{latest_release['body']}\n```"
                    embed.add_field(name="Release Notes", value=formatted_body, inline=False)
                    embed.set_footer(text="Release published")
                    embed.timestamp = nextcord.utils.parse_time(latest_release['published_at'])
                    
                    await interaction.send(embed=embed)
                else:
                    await interaction.send("Error: Could not fetch the latest release.")

def setup(bot):
    bot.add_cog(GitRelease(bot))
