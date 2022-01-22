import json
import base64
import requests
import urllib.parse as urllibparse
import os

# ----- API Base Url -----

SPOTIFY_API_BASE_URL = 'https://api.spotify.com'
API_VERSION = "v1"
SPOTIFY_API_URL = "{}/{}".format(SPOTIFY_API_BASE_URL, API_VERSION)

# ----- User Auth -----

### Endpoints
SPOTIFY_AUTH_BASE_URL = "https://accounts.spotify.com/{}"
SPOTIFY_AUTH_URL = SPOTIFY_AUTH_BASE_URL.format('authorize')
SPOTIFY_TOKEN_URL = SPOTIFY_AUTH_BASE_URL.format('api/token')

### Client Keys
CLIENT_ID = os.environ.get('CLIENT_ID', '')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET', '')

### Server parameters
CLIENT_SIDE_URL = os.environ.get('APP_URL', '')
REDIRECT_URI = "{}/callback/".format(CLIENT_SIDE_URL)
SCOPE = "playlist-modify-public playlist-modify-private user-read-recently-played user-top-read user-read-private"
STATE = ""
SHOW_DIALOG_bool = True
SHOW_DIALOG_str = str(SHOW_DIALOG_bool).lower()

auth_query_parameters = {
    "response_type": "code",
    "redirect_uri": REDIRECT_URI,
    "scope": SCOPE,
    # "state": STATE,
    # "show_dialog": SHOW_DIALOG_str,
    "client_id": CLIENT_ID
}

URL_ARGS = "&".join(["{}={}".format(key, urllibparse.quote(val))
                    for key, val in list(auth_query_parameters.items())])

AUTH_URL = "{}/?{}".format(SPOTIFY_AUTH_URL, URL_ARGS)


def authorize(auth_token, scopes=[]):
    code_payload = {
        "grant_type": "authorization_code",
        "code": str(auth_token),
        "redirect_uri": REDIRECT_URI
    }

    base64encoded = base64.b64encode(("{}:{}".format(CLIENT_ID, CLIENT_SECRET)).encode())
    headers = {"Authorization": "Basic {}".format(base64encoded.decode())}

    post_request = requests.post(SPOTIFY_TOKEN_URL, data=code_payload, headers=headers)
    print(post_request.json())
    # Return tokens to backend
    response_data = json.loads(post_request.text)
    access_token = response_data["access_token"]

    # Use access token for Spotify API
    auth_header = {"Authorization": "Bearer {}".format(access_token)}
    return auth_header
