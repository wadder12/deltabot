import configparser
import json
import nextcord
from nextcord.ext import commands
import openai
from nextcord import Embed

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
                    {"role": "system", "content": "You are a helpful assistant knowledgeable about a Discord server."},
                    {"role": "user", "content": f"Server Data: {json.dumps(server_data)}"},
                    {"role": "user", "content": question}
                ]
            )

            if response.choices and len(response.choices) > 0 and response.choices[0].message:
                return response.choices[0].message.content
            else:
                return self.create_error_embed("Looks like I ran into a wall of confusion. Sorry, I couldn't process that.")

        except Exception as e:
            return self.create_error_embed(f"Wade wasn't a very good developer to make me do that. Oops! Error: {str(e)}")

def create_error_embed(self, message):
        embed = Embed(title="Error", description=message, color=0xff0000)
        return embed