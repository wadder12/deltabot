import configparser
import os
from PIL import Image, ImageDraw, ImageFont
import nextcord
import aiohttp
import io
from datetime import datetime
from nextcord.ext import commands
from nextcord import File, Embed
import pytz

class WelcomeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
        # Use environment variables
        self.welcome_channel_id = int(os.getenv('WELCOME_CHANNEL_ID'))
        self.font_path = os.getenv('FONT_PATH')
        self.corner_image_path = os.getenv('CORNER_IMAGE_PATH')
        self.timezone = os.getenv('TIMEZONE')
        
    async def get_avatar(self, member):
        avatar_url = str(member.display_avatar)
        async with aiohttp.ClientSession() as session:
            async with session.get(avatar_url) as response:
                avatar_bytes = await response.read()
        avatar_image = Image.open(io.BytesIO(avatar_bytes)).convert("RGBA")
        return avatar_image

    @commands.Cog.listener()
    async def on_member_join(self, member):
        image_width, image_height = 800, 600
        background = Image.new('RGBA', (image_width, image_height), (0, 0, 0, 255))
        draw = ImageDraw.Draw(background)
        font_size = 50
        font = ImageFont.truetype(self.font_path, font_size)
        text = f"Welcome {member.name}!"

        member_count = member.guild.member_count
        eastern = pytz.timezone(self.timezone)
        join_date_utc = datetime.utcnow()
        join_date_local = join_date_utc.replace(tzinfo=pytz.utc).astimezone(eastern)
        formatted_join_date = join_date_local.strftime("%Y-%m-%d %H:%M:%S %Z")

        additional_text = f"Member #{member_count}"

        text_bbox = draw.textbbox((0, 0), text, font=font)
        additional_text_bbox = draw.textbbox((0, 0), additional_text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        additional_text_width = additional_text_bbox[2] - additional_text_bbox[0]
        additional_text_height = additional_text_bbox[3] - additional_text_bbox[1]

        text_x = (image_width - text_width) / 2
        additional_text_x = (image_width - additional_text_width) / 2
        text_y = image_height - text_height - additional_text_height - 150
        additional_text_y = text_y + text_height + 10

        text_color = (255, 255, 255)
        draw.text((text_x, text_y), text, font=font, fill=text_color)
        draw.text((additional_text_x, additional_text_y), additional_text, font=font, fill=text_color)
        
        # ?Load an additional image from your files?
        corner_image = Image.open(self.corner_image_path).convert("RGBA")

        # Resize the corner image if needed (optional)
        corner_image = corner_image.resize((200, 200))  # Adjust the size (width, height) as needed (200, 200)

        # Calculate position for the corner image (top-right corner)
        corner_image_x = image_width - corner_image.width - 10  # 10 pixels from the right edge
        corner_image_y = 10  # 10 pixels from the top edge

        # Paste the corner image onto the background
        background.paste(corner_image, (corner_image_x, corner_image_y), corner_image)

        avatar_image = await self.get_avatar(member)
        avatar_size = 128
        avatar_image = avatar_image.resize((avatar_size, avatar_size))
        avatar_x = (image_width - avatar_size) / 2
        avatar_y = (image_height - text_height - additional_text_height - avatar_size) / 2 - 70

        background.paste(avatar_image, (int(avatar_x), int(avatar_y)), avatar_image)

        with io.BytesIO() as image_binary:
            background.save(image_binary, 'PNG')
            image_binary.seek(0)
            welcome_channel = self.bot.get_channel(self.welcome_channel_id)
            
            # Updated color for the embed - Olive Green
            olive_green_color = 0x808000  # Olive green hex color code

            embed = Embed(title="Welcome to the Delta Company!", description=f"{member.mention} has joined.", color=olive_green_color)
            embed.set_image(url="attachment://welcome.png")
            file = File(fp=image_binary, filename='welcome.png')
            await welcome_channel.send(embed=embed, file=file)


def setup(bot):
    bot.add_cog(WelcomeCog(bot))