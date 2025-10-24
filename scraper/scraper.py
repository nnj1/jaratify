from spotify_scraper import SpotifyClient
from spotify_scraper.core.exceptions import (
    URLError,
    ScrapingError,
    AuthenticationError,
    MediaError
)
import json
import re


class Scraper:

    def __init__(self):
        #Initialize the client
        self.client = SpotifyClient()
        self.top_playlist_urls = {
            "Today's Top Hits": "https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M",
            "Top 50 - Global": "https://open.spotify.com/playlist/37i9dQZEVXbMDoHDwVN2tF",
            "RapCaviar": "https://open.spotify.com/playlist/37i9dQZF1DX0XUfTFmZEEK",
            "Viva Latino": "https://open.spotify.com/playlist/37i9dQZF1DX10zKwpqJgqR"
        }

    def uri_to_url(self, uri):
        pattern = r"^[^:]*:[^:]*:(.*)"

        # Use re.search() to find the pattern
        match = re.search(pattern, uri)
        result = match.group(1)
        return "https://open.spotify.com/track/"+ result
    
    def get_playlist_metadata(self, playlist_url="https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M"):
        data = {}
        try:
            playlist = self.client.get_playlist_info(playlist_url)

            data['playlist_name'] = str(playlist.get('name', 'Unknown'))
            data['owner'] = playlist.get('owner', {}).get('display_name', playlist.get('owner', {}).get('id', 'Unknown'))
            data['total_tracks'] = playlist.get('track_count', 0)
            data['track_names'] = []
            data['track_urls'] = []
            # Get all tracks
            for track in playlist['tracks']:
                data['track_names'].append(f"{track.get('name', 'Unknown')} by {(track.get('artists', [{}])[0].get('name', 'Unknown') if track.get('artists') else 'Unknown')}")
                data['track_urls'].append(self.uri_to_url(track.get('uri')))
        finally:
            return data
        
    def get_track_metadata(self, url = "https://open.spotify.com/track/6rqhFgbbKwnb9MLmUQDhG6"):
        try:
            track = self.client.get_track_info(url)

            return {
                "title": track.get('name', 'Unknown'),
                "artists": [artist.get('name', 'Unknown') for artist in track['artists']],
                "album": track.get('album', {}).get('name', 'Unknown'),
                "duration_seconds": track.get('duration_ms', 0) / 1000,
                "preview_url": track.get('preview_url'),
                "explicit": track.get('explicit', False)
            }
        except URLError as e:
            return {
                "success": False,
                "error": "Invalid Spotify URL",
                "details": str(e)
            }
        except ScrapingError as e:
            return {
                "success": False,
                "error": "Failed to extract data",
                "details": str(e)
            }
        except Exception as e:
            return {
                "success": False,
                "error": "Unexpected error",
                "details": str(e)
            }
        finally:
            pass

    def __del__(self):
        """
        Deconstructor (Finalizer): Called when the object is garbage collected.
        Used for cleanup actions (like closing sessions or files).
        """
        # Always close when done
        self.client.close()
        print(f"🗑️ Deconstructor called: Closed resources for Scraper")

# --- Usage ---
# When you call the class, the __init__ method runs:
my_new_scraper = Scraper() 
# Output: Scraper initialized and ready to fetch data!

pretty_json_string = json.dumps(my_new_scraper.get_track_metadata(), indent=4, ensure_ascii=False)
print(pretty_json_string)

pretty_json_string = json.dumps(my_new_scraper.get_playlist_metadata(), indent=4, ensure_ascii=False)
print(pretty_json_string)

del my_new_scraper
#