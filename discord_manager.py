import discord
from discord.ext import commands
import asyncio
import yt_dlp
from get_spotify import SpotifyManager
from get_youtube import Songs
import youtube_dl
from discord import FFmpegOpusAudio

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


ffmpeg_options = {
    'options': '-vn -reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5'
}

# Instantiate the SpotifyManager
sp = SpotifyManager()


class MusicCommands(commands.Cog):
    """A cog for music commands."""

    def __init__(self, bot):
        self.bot = bot
        self.voice_client = None
        self.tracks = []  # List of track names
        self.current_track_index = 0  # Pointer to current track
        self.user_id = None
        self.playlist_name = None
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

    async def play_song(self, ctx):
        """Play the current song using the track pointer."""
        # Ensure the bot is connected to the voice channel
        if not await self.connect_to_voice(ctx):
            return

        # Check if there are tracks in the playlist
        if not self.tracks:
            await ctx.send("No tracks in the playlist. Please set a playlist first.")
            return

        # Check if current_track_index is out of bounds
        if self.current_track_index < 0 or self.current_track_index >= len(self.tracks):
            await ctx.send("End of playlist reached.")
            self.is_playing = False
            return

        # Get the current track
        current_song = self.tracks[self.current_track_index]
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

                # Use FFmpegPCMAudio to stream the audio directly
                source = await discord.FFmpegOpusAudio.from_probe(audio_url, **ffmpeg_options)

                # Play the audio in the voice client
                if not ctx.voice_client.is_playing():
                    ctx.voice_client.play(
                        source,
                        after=lambda e: asyncio.run_coroutine_threadsafe(self.song_finished(ctx, e), self.bot.loop)
                    )

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
        if self.current_track_index < len(self.tracks):
            await self.play_song(ctx)
        else:
            await ctx.send("End of playlist reached.")


    @commands.command(name='user')
    async def set_user(self, ctx, user_id: str):
        """Set the Spotify user ID."""
        self.user_id = user_id
        await ctx.send(f"User ID set to {user_id}")

    @commands.command(name='playlist')
    async def set_playlist(self, ctx, playlist_name: str):
        """Set the Spotify playlist name."""
        if not self.user_id:
            await ctx.send("Please set the user ID first using !user [user_id]")
            return

        self.playlist_name = playlist_name
        playlists = sp.get_playlists(self.user_id)
        if playlist_name in playlists:
            self.playlist_id = playlists[playlist_name]
            track_dict = sp.get_tracks(playlist_name)
            
            # Convert track dictionary to a list of track names
            self.tracks = [f"{index}: {track}" for index, track in track_dict.items()]
            
            self.current_track_index = 0  # Reset track pointer
            await ctx.send(f"Playlist set to {playlist_name}. Found {len(self.tracks)} tracks.")
        else:
            await ctx.send(f"Playlist {playlist_name} not found.")


    @commands.command(name='play')
    async def play(self, ctx):
        """Play songs from the selected playlist."""
        if not self.playlist_name:
            await ctx.send("Please set the playlist first using !playlist [playlist_name]") 
            return

        # Check if tracks exist
        if not self.tracks:
            await ctx.send("No tracks in the playlist. Please set a playlist first.")
            return

        # Connect to voice channel
        connected = await self.connect_to_voice(ctx)
        if not connected:
            return

        # Reset track index if needed
        if self.current_track_index >= len(self.tracks):
            self.current_track_index = 0

        # Start playing if not already playing
        if not ctx.voice_client.is_playing():
            await self.play_song(ctx)

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
        if ctx.voice_client and ctx.voice_client.is_playing():
            ctx.voice_client.stop()
            await ctx.send("Stopped the song.")
        
        await ctx.voice_client.disconnect()
        self.voice_client = None
        self.current_track_index = 0  # Reset track index
        await ctx.send("Disconnected from the voice channel.")