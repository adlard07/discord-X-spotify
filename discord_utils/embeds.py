import discord

class View:
    """A helper class for creating fancy embeds."""

    @staticmethod
    def welcome_embed():
        """Generates a welcome embed."""
        embed = discord.Embed(
            title="🎉 Welcome to the Music Zone! 🎉",
            description="Get ready for a world of amazing tunes.",
            color=discord.Color.gold()
        )
        embed.set_image(url="https://link.to/a/fancy/banner.png")  # Add a banner image
        embed.add_field(name="How to Start?", value="Type `!help` to see all commands.", inline=False)
        embed.add_field(name="Need Assistance?", value="Ping me anytime with `@bot-name`!", inline=False)
        embed.set_footer(text="Let's rock and roll! 🤘", icon_url="https://link.to/footer/icon.png")
        return embed

    @staticmethod
    def info_embed():
        """Generates an info embed."""
        embed = discord.Embed(
            title="🎵 Fancy Music Bot 🎶",
            description="Your ultimate music companion in Discord!",
            color=discord.Color.magenta()
        )
        embed.set_thumbnail(url="https://link.to/your/avatar.png")  # Add a bot avatar thumbnail
        embed.add_field(name="Commands", value="`!play` `!pause` `!resume` `!stop`", inline=False)
        embed.add_field(name="About", value="Created to stream music seamlessly.", inline=False)
        embed.set_footer(text="Powered by Fancy Music Bot | © 2024", icon_url="https://link.to/footer/icon.png")
        return embed

    @staticmethod
    def poll_embed():
        """Generates a poll embed."""
        embed = discord.Embed(
            title="📊 Favorite Music Genre?",
            description="React to vote:\n🎸 Rock\n🎹 Jazz\n🎤 Pop\n🎧 EDM",
            color=discord.Color.blue()
        )
        return embed

    @staticmethod
    def now_playing_embed(song_title, artist, duration, thumbnail_url, progress="00:00"):
        """Generates an embed that resembles an audio player."""
        embed = discord.Embed(
            title="🎶 Now Playing",
            description=f"**{song_title}** by **{artist}**",
            color=discord.Color.green()
        )
        embed.set_thumbnail(url=thumbnail_url)  # Song thumbnail or album art
        embed.add_field(name="Duration", value=f"`{progress} / {duration}`", inline=False)
        
        # Add a pseudo-progress bar
        progress_bar_length = 20  # Length of the progress bar
        progress_seconds = int(progress.split(":")[0]) * 60 + int(progress.split(":")[1])
        total_seconds = int(duration.split(":")[0]) * 60 + int(duration.split(":")[1])
        filled_length = int(progress_bar_length * progress_seconds / total_seconds)
        progress_bar = "▬" * filled_length + "🔘" + "▬" * (progress_bar_length - filled_length)
        
        embed.add_field(name="Progress", value=f"`[{progress_bar}]`", inline=False)
        embed.set_footer(text="Use !pause, !resume, or !skip to control playback.")
        return embed
