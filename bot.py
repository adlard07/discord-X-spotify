import discord
from discord.ext import commands
import asyncio
import configparser
from discord_utils.embeds import View
from utils.get_spotify import SpotifyManager
from utils.get_youtube import Songs
from utils.logger import logging
from discord_utils.commands import MusicCommands  # Import the MusicCommands cog

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
        """Event triggered when the bot is ready."""
        # Set a custom presence
        activity = discord.Activity(type=discord.ActivityType.listening, name="Spotify Playlists 🎧")
        await self.change_presence(status=discord.Status.online, activity=activity)
        print(f"Bot is ready! Logged in as {self.user}")

# Create bot instance in main function
def main():
    bot = MusicBot()

    @bot.command(name="welcome")
    async def welcome(ctx):
        """Send a fancy welcome embed."""
        embed = View.welcome_embed()
        await ctx.send(embed=embed)

    @bot.command(name="info")
    async def info(ctx):
        """Send a fancy info embed."""
        embed = View.info_embed()
        await ctx.send(embed=embed)

    @bot.command(name="poll")
    async def poll(ctx):
        """Send a poll embed with reactions."""
        embed = View.poll_embed()
        message = await ctx.send(embed=embed)
        await message.add_reaction("🎸")
        await message.add_reaction("🎹")
        await message.add_reaction("🎤")
        await message.add_reaction("🎧")

    bot.run(DISCORD_TOKEN)

if __name__ == "__main__":
    main()
