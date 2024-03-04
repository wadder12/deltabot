from nextcord.ext import commands

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def kick(self, ctx, member: commands.MemberConverter):
        await ctx.send(f'Kicked {member.name}')

def setup(bot):
    bot.add_cog(Admin(bot))
