# 🎶 Spotify X Discord Bot 🎧

A Discord bot that lets you enjoy your Spotify playlists directly in your voice channel! You can play, pause, skip, and stop songs while the bot fetches YouTube links and streams them using high-quality audio via FFmpeg.

## 🚀 Features
- **Play songs from Spotify playlists**  
- **Control playback**: Pause, resume, skip, and stop songs
- **Automatic YouTube song fetching** for Spotify tracks
- **High-quality audio streaming** with FFmpeg in your Discord voice channel

## 📜 Commands
This bot comes with the following commands to make controlling your music easy:

- `!user [user_id]`: Set your Spotify user ID (replace `[user_id]` with your actual Spotify user ID).
- `!playlist [playlist_name]`: Set the name of the Spotify playlist you want to play.
- `!play`: Start playing the songs from your selected playlist.
- `!pause`: Pause the currently playing song.
- `!resume`: Resume the currently paused song.
- `!skip`: Skip to the next song in the playlist.
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

## 💡 How to Get Your Spotify User ID
To use this bot, you need your **Spotify User ID**. Here’s how to find it:

1. Go to your [Spotify Profile](https://www.spotify.com).
2. Your user ID will be displayed in your **account settings**.

Here’s an image showing exactly where to find it:

![Spotify User ID Location](assets/user_id.png)

## 🎮 How to Use the Bot
1. **Invite the Bot**  
   First, invite the bot to your Discord server.

2. **Join a Voice Channel**  
   Hop into a voice channel in your Discord server where you want to play music.

3. **Set Your Spotify User ID**  
   Use the `!user [your_spotify_user_id]` command to set your Spotify user ID.

4. **Set the Playlist**  
   Set the Spotify playlist you want to play using the `!playlist [playlist_name]` command.

5. **Start Playing**  
   Use `!play` to start the music!

6. **Control Playback**  
   You can pause, resume, skip, or stop the music with the following commands:
   - `!pause` - Pauses the song
   - `!resume` - Resumes the song
   - `!skip` - Skips to the next song
   - `!stop` - Stops the song and disconnects the bot

## 🎨 Customizing the Bot
Feel free to modify the code to suit your needs! You can change the behavior, add new features, or just enjoy the bot as is. Contributions and suggestions are always welcome!