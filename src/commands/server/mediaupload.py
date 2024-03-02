import aiofiles
import aiofiles.os
import nextcord
from nextcord.ext import commands
from supabase import create_client
import os
import yaml
from nextcord import Embed


class SupabaseUploader:

    def __init__(self, supabase_url: str, supabase_key: str, bucket_name: str):
        self.client = create_client(supabase_url, supabase_key)
        self.bucket_name = bucket_name

    async def upload_file(self, local_path: str, storage_path: str) -> bool:
        async with aiofiles.open(local_path, 'rb') as file:
            data = await file.read()
            response = self.client.storage.from_(self.bucket_name).upload(storage_path, data)
            return response.status_code == 200

class MediaUploadCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        with open('config/emojis.yaml', 'r') as file:
            self.emojis = yaml.safe_load(file).get('emojis', {})
        self.supabase_url = os.getenv('SUPABASE_URL')
        self.supabase_key = os.getenv('SUPABASE_KEY')
        self.bucket_name = os.getenv('SUPABASE_BUCKET_NAME', 'clientuploads')
        self.local_media_path = os.getenv('LOCAL_MEDIA_PATH', 'utils/media/')
        
        self.success_emoji = self.emojis.get('CHECKMARK')
        self.error_emoji = self.emojis.get('X')
        
    @commands.command()
    async def uploadmedia(self, ctx: commands.Context):
        if not ctx.message.attachments:
            await ctx.send(f"{self.error_emoji} Please attach a file to upload.")
            return

        user_folder = os.path.join(self.local_media_path, str(ctx.author))
        attachment = ctx.message.attachments[0]
        local_file_path = os.path.join(user_folder, attachment.filename)
        supabase_file_path = f"uploads/{ctx.author}/{attachment.filename}"

        await aiofiles.os.makedirs(user_folder, exist_ok=True)
        await attachment.save(local_file_path)

        success = await self.uploader.upload_file(local_file_path, supabase_file_path)
        embed = Embed(color=0x7289DA)  # Discord Blurple
        
        if success:
            embed.title = f"{self.success_emoji} File Uploaded Successfully"
            embed.description = f"Your file has been uploaded to: ```{supabase_file_path}```"
        else:
            embed.title = f"{self.error_emoji} Upload Failed"
            embed.description = "There was an issue uploading your file. Please try again later."
        
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(MediaUploadCog(bot))