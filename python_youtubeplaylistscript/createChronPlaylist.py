import json
from requests_oauthlib import OAuth2Session

auth_url = 'https://accounts.google.com/o/oauth2/auth'
token_url = 'https://www.googleapis.com/oauth2/v3/token'
client_id = r'36353489037-lquttng6c2r2pr9rlr5hgmcfk0ehh9e3.apps.googleusercontent.com'
client_secret = r'lmsDFVcn81_ezKq0BDuNqpcq'
redirect_uri = 'http://localhost'
scope = ['https://www.googleapis.com/auth/youtube']

oauth = OAuth2Session(client_id, redirect_uri=redirect_uri, scope=scope)
manual_auth_url, state = oauth.authorization_url(auth_url, access_type = "offline", prompt = "select_account")

print('Please go to >> ', manual_auth_url, ' << and authorize access.')
authorization_response = input('Enter the full callback URL')

token = oauth.fetch_token(token_url, authorization_response=authorization_response, client_secret=client_secret)

# Continue - https://requests-oauthlib.readthedocs.io/en/latest/oauth2_workflow.html#web-application-flow