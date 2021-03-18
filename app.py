# LOAD ENV VARIABLES FROM .ENV FILE
from dotenv import load_dotenv
load_dotenv()

# SPOTIFY API
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# load Spotify Credentials
auth_manager = SpotifyClientCredentials()

# Flask Framework for creating web page
from flask import Flask, render_template
app = Flask(__name__)

import json

# Home Page
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/getReleases')
def getReleases():
    # Authenticate to Spotify
    spotify = spotipy.Spotify(auth_manager=auth_manager)

    # Get New Releases
    releases = spotify.new_releases('PL', 20, 0)['albums']['items']

    return json.dumps(releases) # Convert dict to string

# Start Web Server
if __name__ == '__main__':
    app.run(debug=True)