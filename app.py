# LOAD ENV VARIABLES FROM .ENV FILE
from os import environ
from dotenv import load_dotenv
load_dotenv()

# SPOTIFY API
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# load Spotify Credentials
auth_manager = SpotifyClientCredentials()

# Flask Framework for creating web page
from flask import Flask, render_template, request, json
app = Flask(__name__)


# Home Page
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/getReleases', methods=['POST'])
def getReleases():
    if request.method == 'POST':
        # Authenticate to Spotify
        spotify = spotipy.Spotify(auth_manager=auth_manager)

        # Get country chosen by user
        country = request.get_data().decode('utf-8')
        if country == 'ALL': country = None

        # Get New Releases
        releases = spotify.new_releases(country=country, limit=30)['albums']['items']

        if len(releases) < 1: return 404 # Return fail code if nothing was returned from Spotify

        return json.dumps(releases) # Convert dict to string

@app.route('/getCountryCodes', methods=['POST'])
def getCountryCodes():
    if request.method == 'POST':

        import pycountry
        countriesList = list(pycountry.countries) # Get all ISO 3166 countries

        codes = {}

        for country in countriesList:
            codes[countriesList.index(country)] = country.alpha_2

        return  json.dumps(list(codes.values()))# Convert dict to list then to string

# Start Web Server
if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0',port=port)