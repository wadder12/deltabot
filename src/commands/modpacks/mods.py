import os
from dotenv import load_dotenv
import nextcord
from nextcord.ext import commands
from supabase import create_client, Client
from custom.supabase_client import get_supabase_client
load_dotenv()

class ModpackCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.supabase = get_supabase_client()  # Use the utility function to get the Supabase client
        self.local_modpack_path = os.getenv('LOCAL_MODPACK_PATH', 'modpacks/')
        self.supabase_bucket_name = os.getenv('SUPABASE_BUCKET_NAME', 'clientuploads')

    @commands.command(name="upmod")
    async def uploadmodpack(self, ctx):
        """Upload a modpack to Supabase Storage."""
        allowed_ids = os.getenv('MODPACK_IDS', '')
        allowed_user_ids = [int(id.strip()) for id in allowed_ids.split(',') if id.strip().isdigit()]

        if ctx.author.id not in allowed_user_ids:
            await ctx.send("You do not have permission to upload modpacks.")
            return

        modpack_folder = os.path.join(self.local_modpack_path, str(ctx.author))
        attachment = ctx.message.attachments[0]
        local_file_path = os.path.join(modpack_folder, attachment.filename)
        supabase_file_path = f"modpacks/{ctx.author}/{attachment.filename}"

        os.makedirs(modpack_folder, exist_ok=True)
        await attachment.save(local_file_path)

        with open(local_file_path, 'rb') as file:
            response = self.supabase.storage.from_(self.supabase_bucket_name).upload(supabase_file_path, file)

        embed_title = os.getenv('UPLOAD_EMBED_TITLE')
        embed_color_success = int(os.getenv('UPLOAD_EMBED_COLOR_SUCCESS'), 16)
        embed_color_fail = int(os.getenv('UPLOAD_EMBED_COLOR_FAIL'), 16)
        emoji_success = os.getenv('EMOJI_SUCCESS')
        emoji_fail = os.getenv('EMOJI_FAIL')

        if response.status_code != 200:
            embed_description = f"{emoji_fail} " + os.getenv('UPLOAD_EMBED_DESCRIPTION_FAIL').format(status_code=response.status_code)
            embed_color = embed_color_fail
        else:
            embed_description = f"{emoji_success} " + os.getenv('UPLOAD_EMBED_DESCRIPTION_SUCCESS').format(supabase_file_path=supabase_file_path)
            embed_color = embed_color_success

        embed = nextcord.Embed(
            title=embed_title,
            description=embed_description,
            color=embed_color
        )
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar.url)
        embed.set_footer(text="Modpack System", icon_url=self.bot.user.avatar.url)

        await ctx.send(embed=embed)



    @commands.command(name="load")
    async def downloadmodpack(self, ctx, modpack_name):
        """Download a modpack from Supabase Storage."""
        destination = os.path.join(self.local_modpack_path, modpack_name)
        source = f"modpacks/{ctx.author}/{modpack_name}"

        res = self.supabase.storage.from_(self.supabase_bucket_name).download(source)
        emoji_success = os.getenv('DOWNLOAD_EMOJI_SUCCESS', '✅')
        emoji_fail = os.getenv('DOWNLOAD_EMOJI_FAIL', '❌')

        if not res:  # Assuming an empty result indicates a failed download
            embed_title = os.getenv('EMBED_TITLE', 'Modpack Download Status')
            embed_description = f"{emoji_fail} Failed to download modpack **{modpack_name}**."
            embed_color = int(os.getenv('EMBED_COLOR_FAIL', '0xff0000'), 16)
        else:
            with open(destination, 'wb+') as f:
                f.write(res)

            embed_title = os.getenv('EMBED_TITLE', 'Modpack Download Successful')
            embed_description = f"{emoji_success} Thank you for downloading the modpack **{modpack_name}**. If you encounter any issues or have questions, please contact the admins."
            embed_color = int(os.getenv('EMBED_COLOR_SUCCESS', '0x00ff00'), 16)

        embed = nextcord.Embed(
            title=embed_title,
            description=embed_description,
            color=embed_color
        )
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar.url)
        embed.set_footer(text=os.getenv('EMBED_FOOTER_TEXT', 'Modpack System'), icon_url=self.bot.user.avatar.url)
        embed_thumbnail_url = os.getenv('EMBED_THUMBNAIL_URL', '')
        if embed_thumbnail_url:
            embed.set_thumbnail(url=embed_thumbnail_url)
        embed.add_field(name="Modpack Name", value=modpack_name, inline=True)
        embed.add_field(name="Downloaded By", value=ctx.author.display_name, inline=True)

        await ctx.send(embed=embed, file=nextcord.File(destination))

def setup(bot):
    bot.add_cog(ModpackCog(bot))