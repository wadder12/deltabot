import nextcord
from nextcord.ext import commands

class SimpleHelpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="helpme")
    async def help_command(self, ctx):
        """Displays help information."""
        embed = nextcord.Embed(title="Help", description="List of available commands:", color=nextcord.Color.blue())
        
        for cog_name, cog in self.bot.cogs.items():
            commands = cog.get_commands()
            command_list = [command.name for command in commands if not command.hidden]
            if command_list:
                embed.add_field(name=cog_name, value=", ".join(command_list), inline=False)

        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(SimpleHelpCog(bot))