import nextcord
from nextcord.ext import commands
import aiohttp
from openai import OpenAI
from configparser import ConfigParser
import os

class FreeToGameCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.base_url = "https://www.freetogame.com/api/games"
        self.headers = {"User-Agent": "YourBotName/1.0"}

        # Load OpenAI API key from config file, assuming working directory is project root
        config = ConfigParser()
        config.read(os.path.join('config', 'config.ini'))  # Adjusted path
        # Check to see if the 'openai' section is found
        if 'openai' in config:
            api_key = config.get('openai', 'api_key')
            # Initialize OpenAI client with the API key
            self.client = OpenAI(api_key=api_key)
        else:
            print("Error: 'openai' section not found in config.ini")

    async def fetch_games(self, session, params):
        print(f"Fetching games with params: {params}")
        async with session.get(self.base_url, params=params, headers=self.headers) as response:
            if response.status == 200:
                return await response.json()
            else:
                # Better error handling for production
                response.raise_for_status()

    @commands.command(name="findgame")
    async def find_game(self, ctx, *, preferences: str):
        """
        Finds a game based on the user's preferences.
        """
        processed_input = await self.process_preferences_with_gpt(preferences)

        async with aiohttp.ClientSession() as session:
            games = await self.fetch_games(session, processed_input)
            if games:
                games_list = [game['title'] for game in games][:10]  # Limiting to the first 10 games
                await ctx.send("\n".join(games_list))
            else:
                await ctx.send("No games found or there was an issue fetching the games.")

    async def process_preferences_with_gpt(self, preferences):
        try:
            completion = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant trained to translate game preferences into API query parameters."},
                    {"role": "user", "content": preferences}
                ]
            )

            if completion.choices:
                response_text = completion.choices[0].message.content
                print("GPT-3 Response Text:", response_text)  # Debug print
                params = self.parse_response_to_params(response_text)
                return params

            else:
                return {}
        except Exception as e:
            print(f"Error processing preferences with GPT-3: {e}")
            print(f"Processed Params: {params}")  # Add this line to debug

            return {}
    def parse_response_to_params(self, response_text):
        params = {}
        # Assume GPT-3 might list parameters in a human-readable format; looking for key phrases to identify parameters.
        lines = response_text.split('\n')
        for line in lines:
            # Looking for genre
            if 'genre' in line.lower():
                genre_search = line.lower().split('genre=')[1] if 'genre=' in line.lower() else None
                if genre_search:
                    params['genre'] = genre_search.strip().split(' ')[0].replace(',', '').replace('"', '').replace("'", "")
            
            # Looking for singleplayer/multiplayer mode
            if 'singleplayer' in line.lower():
                params['tag'] = 'singleplayer'
            elif 'multiplayer' in line.lower():
                params['tag'] = 'multiplayer'
                
            # Add more parameters as needed based on GPT-3 responses and API capabilities

        return params



def setup(bot):
    bot.add_cog(FreeToGameCog(bot))

