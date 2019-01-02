# Using: https://developers.google.com/youtube/v3/guides/auth/server-side-web-apps
from flask import Flask, request, redirect
import google.oauth2.credentials
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
import json

import iso8601

app = Flask(__name__)

# Use the client_secret.json file to identify the application requesting
# authorization. The client ID (from that file) and access scopes are required.
flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
    'client_secret.json',
    scopes=['https://www.googleapis.com/auth/youtube.force-ssl'])

# Indicate where the API server will redirect the user after the user completes
# the authorization flow. The redirect URI is required.
flow.redirect_uri = 'https://localhost:5000/oauth_callback'

@app.route('/')
def index_get():
    # Generate URL for request to Google's OAuth 2.0 server.
    # Use kwargs to set optional request parameters.
    authorization_url, state = flow.authorization_url(
        # Enable offline access so that you can refresh an access token without
        # re-prompting the user for permission. Recommended for web server apps.
        access_type='offline',
        # Enable incremental authorization. Recommended as a best practice.
        include_granted_scopes='true')

    return redirect(authorization_url)

@app.route('/oauth_callback')
def oauth_callback_get():
    flow.fetch_token(authorization_response=request.url)
    
    credentials = flow.credentials

    # Get all items from the playlist, and add to an array/list
    youtubeAPI = build('youtube','v3', credentials=credentials)

    pageToken = ''
    allItems = []
    while True:        
        response = youtubeAPI.playlistItems().list(
            part='snippet', 
            playlistId='PL3Z0xw5JKEcmg0dLCQDa7LvbzlZGPLqaV',
            maxResults=50,
            pageToken=pageToken
        ).execute()

        for anItem in response['items']:
            newItem = {}
            newItem["resourceId"] = anItem["snippet"]["resourceId"]
            newItem["timestamp"] = iso8601.parse_date(anItem["snippet"]["publishedAt"])
            allItems.append(newItem)

        if 'nextPageToken' in response:
            pageToken = response['nextPageToken']
        else:
            break
    
    # Order the items in the list by upload date ascending
    allItems.sort(key = lambda anItem: anItem["timestamp"])

    # Detect if the target playlist exists. If it does, delete it.
    targetPlaylistName = str.format("Test Playlist (Ordered Copy)")

    pageToken = ''
    targetPlaylistId = ''
    while True:
        response = youtubeAPI.playlists().list(
            part='snippet', 
            mine=True,
            maxResults=50,
            pageToken=pageToken
        ).execute()

        for aPlaylist in response['items']:
            if aPlaylist["snippet"]["title"].find(targetPlaylistName) != -1:
                targetPlaylistId = aPlaylist["id"]
                break

        if 'nextPageToken' in response:
            pageToken = response['nextPageToken']
        else:
            break

    if len(targetPlaylistId) > 0:
        youtubeAPI.playlists().delete(
            id = targetPlaylistId
        ).execute()

    # Create the target playlist
    createdPlaylistResponse = youtubeAPI.playlists().insert(
        part = 'snippet',
        body = dict(
            snippet = dict(
                title = targetPlaylistName
            )
        )
    ).execute()

    # Add all the items to the target playlist
    for anItem in allItems:
        youtubeAPI.playlistItems().insert(
            part = 'snippet',
            body = dict(
                snippet = dict(
                    playlistId = createdPlaylistResponse["id"],
                    resourceId = anItem["resourceId"]
                )
            )
        ).execute()

    return redirect(str.format("https://www.youtube.com/playlist?list={}", createdPlaylistResponse["id"]))
    
if __name__ == "__main__":
    app.run(ssl_context='adhoc')
