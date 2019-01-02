# Using: https://developers.google.com/youtube/v3/guides/auth/server-side-web-apps

import google.oauth2.credentials
import google_auth_oauthlib.flow
from googleapiclient.discovery import build

# Use the client_secret.json file to identify the application requesting
# authorization. The client ID (from that file) and access scopes are required.
flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
    'client_secret.json',
    scopes=['https://www.googleapis.com/auth/youtube.force-ssl'])

# Indicate where the API server will redirect the user after the user completes
# the authorization flow. The redirect URI is required.
flow.redirect_uri = 'https://localhost'

# Generate URL for request to Google's OAuth 2.0 server.
# Use kwargs to set optional request parameters.
authorization_url, state = flow.authorization_url(
    # Enable offline access so that you can refresh an access token without
    # re-prompting the user for permission. Recommended for web server apps.
    access_type='offline',
    # Enable incremental authorization. Recommended as a best practice.
    include_granted_scopes='true')

print("Go to the auth url to authorise the script: ", authorization_url)
callback_url = input("Please copy and paste the response callback url: ")

flow.fetch_token(authorization_response=callback_url)
credentials = flow.credentials

youtubeAPI = build('youtube','v3', credentials=credentials)
videos = youtubeAPI.playlistItems().list(
    part='snippet', 
    playlistId='PL3Z0xw5JKEcmg0dLCQDa7LvbzlZGPLqaV',
    maxResults=50
).execute()

print(videos)