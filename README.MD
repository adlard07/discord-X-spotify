# 🎶 Spotify X Discord Bot 🎧

A Discord bot that lets you enjoy your Spotify playlists directly in your voice channel! You can play, pause, skip, shuffle, and stop songs while the bot fetches YouTube links and streams them using high-quality audio via FFmpeg.

## 🚀 Features
- **Play songs from Spotify playlists**  
- **Play individual songs**: Provide a song name to play it directly  
- **Control playback**: Pause, resume, skip, shuffle, and stop songs  
- **Automatic YouTube song fetching** for Spotify tracks or individual songs  
- **High-quality audio streaming** with FFmpeg in your Discord voice channel  

## 📜 Commands
This bot comes with the following commands to make controlling your music easy:

- `!playlist [playlist_id]`: Set the Spotify playlist you want to play (replace `[playlist_id]` with your actual Spotify playlist ID).  
- `!play`: Start playing the songs from your selected playlist.  
- `!play [song_name]`: Play a specific song by providing its name.  
- `!pause`: Pause the currently playing song.  
- `!resume`: Resume the currently paused song.  
- `!skip`: Skip to the next song in the playlist.  
- `!shuffle`: Shuffle the playlist and play songs in random order.  
- `!stop`: Stop the current song and disconnect the bot from the voice channel.  

## 🛠️ Hosting the Bot Locally
Want to host the bot on your own machine? Here's how:

1. **Install Dependencies**  
   First, you’ll need to install all the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

2. **Install FFmpeg**  
   You’ll also need FFmpeg installed and added to your system’s `PATH`.  
   - [FFmpeg Download](https://ffmpeg.org/download.html)

3. **Configure Spotify API Credentials**  
   Make sure you add your **Spotify API credentials** to the `get_spotify.py` file.

4. **Run the Bot**  
   Once you’ve got everything set up, run the bot with:
   ```bash
   python bot.py
   ```

## 💡 How to Get Your Spotify Playlist ID
To use this bot, you need your **Spotify Playlist ID**. Here’s how to find it:

1. Open Spotify and navigate to the playlist you want to use.  
2. Click the "..." menu next to the playlist name.  
3. Select **Share > Copy link to playlist**.  
4. Extract the playlist ID from the link. For example:
   ```
   https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M  
   ```
   The playlist ID is the part after `playlist/`:
   ```
   37i9dQZF1DXcBWIGoYBM5M
   ```

## 🎮 How to Use the Bot
1. **Invite the Bot**  
   First, invite the bot to your Discord server.

2. **Join a Voice Channel**  
   Hop into a voice channel in your Discord server where you want to play music.

3. **Set the Playlist**  
   Set the Spotify playlist you want to play using the `!playlist [playlist_id]` command.

4. **Start Playing**  
   - Use `!play` to start the music from the playlist.  
   - Use `!play [song_name]` to play a specific song of your choice, even if it’s not in the playlist.

5. **Control Playback**  
   You can pause, resume, skip, shuffle, or stop the music with the following commands:
   - `!pause` - Pauses the song  
   - `!resume` - Resumes the song  
   - `!skip` - Skips to the next song  
   - `!shuffle` - Shuffles the playlist and plays songs in a random order  
   - `!stop` - Stops the song and disconnects the bot  

## 🎨 Customizing the Bot
Feel free to modify the code to suit your needs! You can change the behavior, add new features, or just enjoy the bot as is. Contributions and suggestions are always welcome!