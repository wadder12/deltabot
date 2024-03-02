import configparser
import json
import os
import nextcord
from nextcord.ext import commands
import openai
from nextcord import Embed
import time  # Import time to calculate response time

from dotenv import load_dotenv
load_dotenv()

class AIDiscordBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.openai_api_key = os.getenv('API_KEY')
        self.client = openai.OpenAI(api_key=self.openai_api_key)
        
    @nextcord.slash_command()
    async def ask(self, interaction: nextcord.Interaction, *, question):
        """Ask a question about the server."""
        start_time = time.time()  # Start timing
        await interaction.response.defer()

        server_data = self.get_server_data(interaction.guild)
        response, is_error = self.get_ai_response(question, server_data)
        response_time = time.time() - start_time  # Calculate response time

        # Create embed with AI-like color
        if is_error:
            embed = Embed(title="Oops! 🤖", description=response, color=0xFF5733)  # Orange-ish color for errors
        else:
            embed = Embed(title="AI Response 🧠", description=f"```{response}```", color=0x7289DA)  # Discord Blurple
            embed.set_footer(text=f"Response time: {response_time:.2f} seconds")

        await interaction.followup.send(embed=embed)

    def get_server_data(self, guild):
        server_data = {
            "server_name": guild.name,
            "member_count": guild.member_count,
            "roles": [role.name for role in guild.roles],
            "owner": str(guild.owner),
            "channels": [channel.name for channel in guild.channels],
            "emojis": [emoji.name for emoji in guild.emojis],
            "region": str(guild.region),
            "verification_level": str(guild.verification_level),
            "explicit_content_filter": str(guild.explicit_content_filter),
            "features": guild.features,
            "mfa_level": str(guild.mfa_level),
            "created_at": str(guild.created_at),
            "system_channel": str(guild.system_channel),
            "system_channel_flags": str(guild.system_channel_flags),
            "description": guild.description,
            "banner": str(guild.banner),
            "premium_tier": str(guild.premium_tier),
            "premium_subscription_count": guild.premium_subscription_count,
            "preferred_locale": str(guild.preferred_locale),
            "rules_channel": str(guild.rules_channel),
            "public_updates_channel": str(guild.public_updates_channel),
            "max_presences": guild.max_presences,
            "max_members": guild.max_members,
        }
        specific_data = self.load_specific_data()
        server_data.update(specific_data)

        return server_data

    def load_specific_data(self):
        try:
            with open('custom/database/_data.json', 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            print("Specific data JSON file not found.")
            return {}

    def get_ai_response(self, question, server_data):
        try:
            response = self.client.chat.completions.create(
                model="gpt-4-1106-preview",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant knowledgeable about a Discord server & you are very smartasses and a bully and funny and military grade secure and make sure if someone asks you a stupid question and also be a smartass"},
                    {"role": "user", "content": f"Server Data: {json.dumps(server_data)}"},
                    {"role": "user", "content": question}
                ]
            )

            # Check if the response is valid and has content
            if response.choices and len(response.choices) > 0 and response.choices[0].message.content:
                return response.choices[0].message.content, False  # False indicates no error
            else:
                # If there's no valid response content, return an error message
                return "Looks like I ran into a wall of confusion. Sorry, I couldn't process that.", True

        except Exception as e:
            # On exception, return the exception message as error
            return f"Wade wasn't a very good developer to make me do that. Oops! Error: {str(e)}", True


    def create_error_embed(self, message):
        embed = Embed(title="Error", description=message, color=0xff0000)
        return embed


def setup(bot):
    bot.add_cog(AIDiscordBot(bot))
