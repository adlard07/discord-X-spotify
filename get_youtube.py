import yt_dlp
from logger import logging

class Songs:
    def __init__(self, query):
        self.query = query

    def find_song(self):
        ydl_opts = {
            'quiet': True,
            'extract_flat': True, 
            'force_generic_extractor': True, 
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                result = ydl.extract_info(f"ytsearch:{self.query}", download=False)

                if 'entries' in result:
                    video_url = result['entries'][0]['url']
                    logging.info(f"Successfully found song for query '{self.query}': {video_url}")
                    return video_url
                else:
                    logging.warning(f"No video found for query: {self.query}")
                    return None

        except Exception as e:
            logging.error(f"An error occurred while searching for song: {e}")
            return None


if __name__ == '__main__':
    query = "computer talk austenyo"
    song = Songs(query)
    logging.info(song.find_song())
