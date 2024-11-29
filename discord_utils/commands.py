import discord
from discord.ext import commands
import asyncio
import yt_dlp
from utils.get_spotify import SpotifyManager
from utils.get_youtube import Songs
import youtube_dl
from discord import FFmpegPCMAudio
import pafy
import random

# Remove the bug_reports_message line to avoid conflict
youtube_dl.utils.bug_reports_message = lambda: ''

# Add your ytdl options and ffmpeg options
ytdl_format_options = {
    'format': 'bestaudio/best',
    'nooverwrites': True,
    'no_warnings': True,
    'ignoreerrors': False,
    'no_color': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0',
    'quiet': True,
    'nocheckcertificate': True
}

ffmpeg_options = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5','options': '-vn'}

# Instantiate the SpotifyManager
sp = SpotifyManager()

class MusicCommands(commands.Cog):
    """A cog for music commands."""

    def __init__(self, bot):
        self.bot = bot
        self.voice_client = None
        self.playlist_id = None
        self.current_track_index = 0  # Pointer to current track
        self.is_playing = False

    async def connect_to_voice(self, ctx):
        """Ensure the bot is connected to the user's voice channel."""
        if not ctx.voice_client:
            if ctx.author.voice:
                self.voice_client = await ctx.author.voice.channel.connect()
                await ctx.send(f"Connected to {ctx.author.voice.channel}")
            else:
                await ctx.send("You must be in a voice channel for the bot to join.")
                return False
        return True

    async def play_song(self, ctx, song_url=None, song_name=None):
        """Play the current song using the track pointer or a YouTube URL."""
        # Ensure the bot is connected to the voice channel
        if not await self.connect_to_voice(ctx):
            return

        if song_url:
            try:
                async with ctx.typing():
                    # Extract audio stream URL using yt-dlp
                    with yt_dlp.YoutubeDL(ytdl_format_options) as ydl:
                        info = ydl.extract_info(song_url, download=False)
                        audio_url = info['url']

                    # Play the audio in the voice client
                    if not ctx.voice_client.is_playing():
                        source = FFmpegPCMAudio(audio_url, **ffmpeg_options)  # converts the youtube audio source into a source discord can use
                        ctx.voice_client.play(source, after=lambda e: self.bot.loop.create_task(self.song_finished(ctx, e)))
                    await ctx.send(f"**Now playing:** {song_name}")
                    self.is_playing = True

            except Exception as e:
                await ctx.send(f"Error playing song: {song_name}. Skipping...")
                print(f"Error: {e}")
                self.current_track_index += 1
                await self.play_song(ctx)

        else:
            # Fetch the playlist again
            track_dict = sp.get_tracks(self.playlist_id)
            track_keys = list(track_dict.keys())

            # Check if current_track_index is out of bounds
            if self.current_track_index < 0 or self.current_track_index >= len(track_keys):
                await ctx.send("End of playlist reached.")
                self.is_playing = False
                return

            # Get the current track
            current_track_key = track_keys[self.current_track_index]
            current_song = track_dict[current_track_key]
            song = Songs(current_song.split(": ", 1)[-1])  # Extract "TrackName - ArtistName"
            song_url = song.find_song()

            if not song_url:
                await ctx.send(f"Could not find a YouTube video for {current_song}. Skipping...")
                self.current_track_index += 1
                await self.play_song(ctx)  # Proceed to next track
                return

            try:
                async with ctx.typing():
                    # Extract audio stream URL using yt-dlp
                    with yt_dlp.YoutubeDL(ytdl_format_options) as ydl:
                        info = ydl.extract_info(song_url, download=False)
                        audio_url = info['url']

                    # Play the audio in the voice client
                    if not ctx.voice_client.is_playing():
                        source = FFmpegPCMAudio(audio_url, **ffmpeg_options)  # converts the youtube audio source into a source discord can use
                        ctx.voice_client.play(source, after=lambda e: self.bot.loop.create_task(self.song_finished(ctx, e)))
                    await ctx.send(f"**Now playing:** {current_song}")
                    self.is_playing = True

            except Exception as e:
                await ctx.send(f"Error playing song: {current_song}. Skipping...")
                print(f"Error: {e}")
                self.current_track_index += 1
                await self.play_song(ctx)

    async def song_finished(self, ctx, error):
        """Callback when a song finishes playing."""
        if error:
            print(f"Error in playback: {error}")

        self.is_playing = False  # Reset the playback flag

        # Advance the track index
        self.current_track_index += 1

        # Check if there are more tracks to play
        track_dict = sp.get_tracks(self.playlist_id)
        track_keys = list(track_dict.keys())
        if self.current_track_index < len(track_keys):
            await self.play_song(ctx)
        else:
            await ctx.send("End of playlist reached.")

    @commands.command(name='playlist')
    async def set_playlist(self, ctx, playlist_id: str):
        """Set the Spotify playlist ID."""
        self.playlist_id = playlist_id
        track_dict = sp.get_tracks(playlist_id)

        self.current_track_index = 0  # Reset track pointer
        await ctx.send(f"Playlist set to ID {playlist_id}. Found {len(track_dict)} tracks.")

    @commands.command(name='play')
    async def play(self, ctx, *, query=None):
        """Play songs from the selected playlist or a YouTube query."""
        # If no query is provided, play from the Spotify playlist
        if query is None:
            if not self.playlist_id:
                await ctx.send("Please set the playlist first using !playlist [playlist_id]")
                return

            # Connect to voice channel
            connected = await self.connect_to_voice(ctx)
            if not connected:
                return

            # Reset track index if needed
            if self.current_track_index >= len(sp.get_tracks(self.playlist_id)):
                self.current_track_index = 0

            # Start playing if not already playing
            if not ctx.voice_client.is_playing():
                await self.play_song(ctx)

        else:
            # If a query is provided, search for it on YouTube
            await ctx.send(f"Searching YouTube for: {query}")

            # Use yt_dlp to fetch the first video URL based on the query
            try:
                with yt_dlp.YoutubeDL(ytdl_format_options) as ydl:
                    info = ydl.extract_info(f"ytsearch:{query}", download=False)
                    if 'entries' in info and len(info['entries']) > 0:
                        video_url = info['entries'][0]['url']
                    else:
                        await ctx.send("No results found on YouTube for your query.")
                        return

                # Connect to the voice channel
                connected = await self.connect_to_voice(ctx)
                if not connected:
                    return

                # Play the video in the voice channel
                if not ctx.voice_client.is_playing():
                    source = FFmpegPCMAudio(video_url, **ffmpeg_options)
                    ctx.voice_client.play(source, after=lambda e: self.bot.loop.create_task(self.song_finished(ctx, e)))
                    await ctx.send(f"**Now playing (YouTube):** {query}")
                    self.is_playing = True

            except Exception as e:
                await ctx.send(f"Error playing the YouTube query: {query}")
                print(f"Error: {e}")

    @commands.command(name='pause')
    async def pause(self, ctx):
        """Pause the current song."""
        if ctx.voice_client and ctx.voice_client.is_playing():
            ctx.voice_client.pause()
            await ctx.send("Paused the song.")

    @commands.command(name='resume')
    async def resume(self, ctx):
        """Resume the current song."""
        if ctx.voice_client and ctx.voice_client.is_paused():
            ctx.voice_client.resume()
            await ctx.send("Resumed the song.")

    @commands.command(name='skip')
    async def skip(self, ctx):
        """Skip the current song."""
        # Ensure that a skip is not already in progress
        if getattr(self, 'is_skipping', False):
            await ctx.send("A skip is already in progress. Please wait.")
            return

        # Set the skip flag
        self.is_skipping = True

        # Stop the current song to trigger `song_finished`
        if ctx.voice_client and ctx.voice_client.is_playing():
            ctx.voice_client.stop()
            await ctx.send("Skipped the current song.")
        else:
            await ctx.send("No song is currently playing to skip.")

        # Reset the skip flag after processing
        self.is_skipping = False

    @commands.command(name='stop')
    async def stop(self, ctx):
        """Stop the current song and disconnect."""
        if ctx.voice_client:
            await ctx.voice_client.disconnect()
            await ctx.send("Disconnected from the voice channel.")


    @commands.command(name='shuffle')
    async def shuffle_playlist(self, ctx):
        """Shuffle the playlist and play tracks in random order."""
        if not self.playlist_id:
            await ctx.send("Please set the playlist first using !playlist [playlist_id]")
            return

        # Create a list of indices from 0 to len(track_keys)
        track_indices = list(range(len(track_keys)))

        