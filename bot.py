import discord
from discord.ext import commands
import asyncio
import configparser
import yt_dlp
import youtube_dl
from get_spotify import SpotifyManager
from get_youtube import Songs
from logger import logging
from discord_manager import MusicCommands  # Import the MusicCommands cog


# Configuration
config = configparser.ConfigParser()
config.read('config.ini')
DISCORD_TOKEN = config['Configuration']['DISCORD_TOKEN']

# Set up intents
intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True
intents.members = True  # Enable members intent

# Define the MusicBot class with the MusicCommands cog
class MusicBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents)
        self.added_cog = False  # Track if the cog was added

    async def setup_hook(self):
        """Setup the bot with necessary cogs."""
        if not self.added_cog:
            await self.add_cog(MusicCommands(self))  # Add the MusicCommands cog
            self.added_cog = True

    async def on_ready(self):
        print(f"Bot is ready! Logged in as {self.user}")
        print("--Registered commands--")
        for command in self.commands:
            print(f"!{command.name}")

# Run the bot
def main():
    bot = MusicBot()
    bot.run(DISCORD_TOKEN)

if __name__ == "__main__":
    main()
