import httplib2
import os
import sys

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow


# The CLIENT_SECRETS_FILE variable specifies the name of a file that contains
# the OAuth 2.0 information for this application, including its client_id and
# client_secret. You can acquire an OAuth 2.0 client ID and client secret from
# the {{ Google Cloud Console }} at
# {{ https://cloud.google.com/console }}.
# Please ensure that you have enabled the YouTube Data API for your project.
# For more information about using OAuth2 to access the YouTube Data API, see:
#   https://developers.google.com/youtube/v3/guides/authentication
# For more information about the client_secrets.json file format, see:
#   https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
#PLAYLIST_ID = "PLIRGLFbqXK1VsMTxdkVoppfw8bx-bt0H4"
CLIENT_SECRETS_FILE = "client_secrets.json"

# This variable defines a message to display if the CLIENT_SECRETS_FILE is
# missing.
MISSING_CLIENT_SECRETS_MESSAGE = """
WARNING: Please configure OAuth 2.0

To make this sample run you will need to populate the client_secrets.json file
found at:

   %s

with information from the {{ Cloud Console }}
{{ https://cloud.google.com/console }}

For more information about the client_secrets.json file format, please visit:
https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
""" % os.path.abspath(os.path.join(os.path.dirname(__file__),
                                   CLIENT_SECRETS_FILE))

# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account.
YOUTUBE_READ_WRITE_SCOPE = "https://www.googleapis.com/auth/youtube"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE,
  message=MISSING_CLIENT_SECRETS_MESSAGE,
  scope=YOUTUBE_READ_WRITE_SCOPE)

storage = Storage("%s-oauth2.json" % sys.argv[0])
credentials = storage.get()

if credentials is None or credentials.invalid:
  flags = argparser.parse_args()
  credentials = run_flow(flow, storage, flags)

youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
  http=credentials.authorize(httplib2.Http()))

def create_playlist():
    # Create vidbot playlist
    playlists_insert_response = youtube.playlists().insert(
      part="snippet,status",
          body={
            'snippet':{
              'title':"VidBot Playlist",
              'description':"MTV DJBot"
            },
            'status':{
              'privacyStatus':"public"
            }
        }
    ).execute()

    print("New playlist id: %s" % playlists_insert_response["id"])
    return playlists_insert_response["id"]

'''playlist_info = youtube.playlists().list(
    part = 'snippet',
    id = PLAYLIST_ID
).execute()
print(playlist_info)'''

def add_video(PLAYLIST_ID, VIDEO_ID):
    add_video_request = youtube.playlistItems().insert(
        part="snippet",
          body={
                'snippet': {
                  'playlistId': PLAYLIST_ID,
                  'resourceId': {
                          'kind': 'youtube#video',
                      'videoId': VIDEO_ID
                    }
                #'position': 0
                # by default adds video to last position
                }
        }
    ).execute()

    print(add_video_request)

def delete_playlist(PLAYLIST_ID):
    # Delete vidbot playlist
    playlists_insert_response = youtube.playlists().delete(
        part="snippet",
        id = PLAYLIST_ID
    ).execute()

    print("New playlist id: %s" % playlists_insert_response["id"])
    return playlists_insert_response["id"]