# script to take in files from the muskogen city council meetings and convert to text

# minutes link: https://muskegon-mi.gov/documents/type/1/2025/
# youtube link: https://www.youtube.com/c/CityofMuskegonMeetings
# https://naveen-malla.medium.com/transcribing-any-youtube-video-with-python-a-step-by-step-guide-cea7dd4e32f5

from youtube_transcript_api import YouTubeTranscriptApi
from googleapiclient.discovery import build
import re
import datetime
import pandas as pd

# global variables
API_KEY = 'YOUR_API_KEY_HERE'
YOUTUBE_RE = r'youtube.com/watch\?v=([\w-]*)' # re to parse out the video id given the youtube link
youtube = build('youtube', 'v3', developerKey=API_KEY)  


def download_from_id(yt_api, video_link=None, video_id=None):
    ''' function to download the snippet from the video link or video id'''
    video_id = video_id if video_id else re.search(YOUTUBE_RE, video_link.strip('https://www.')).group(1)
    try: 
        snippets = ytt_api.fetch(video_id)
    except Exception as e:
        print(e)
        return None
    rawSnippets = snippets.to_raw_data()
    return rawSnippets

def get_all_videos_from_channel(channel_id):
    response = youtube.channels().list(
        part='contentDetails',
        id=channel_id
    ).execute()

    # find the uploads playlist for the yt channel and get all videos from this playlist
    uploads_playlist_id = response['items'][0]['contentDetails']['relatedPlaylists']['uploads']

    videos = []
    next_page_token = None

    while True:
        response = youtube.playlistItems().list(
            part='snippet',
            playlistId=uploads_playlist_id,
            maxResults=50,
            pageToken=next_page_token
        ).execute()

        for item in response['items']:
            video_title = item['snippet']['title']
            video_id = item['snippet']['resourceId']['videoId']
            videos.append({
                'title': video_title,
                'video_id': video_id,
                'url': f'https://www.youtube.com/watch?v={video_id}'
            })

        next_page_token = response.get('nextPageToken')
        if not next_page_token:
            break

    return videos

def get_all_transcripts_for_videos(videos, ytApi, cutoff_date=datetime.date(year=2022, day=3, month=1)):
    videosDict = []
    i = 0
    for video in videos:
        i+=1
        title = video['title']
        datestring = None
        try:
            datestring = title.split()[0]
            if '/' in datestring:
                video_date = datetime.datetime.strptime(title.split()[0], '%m/%d/%y').date()
            elif '-' in datestring:
                video_date = datetime.datetime.strptime(title.split()[0], '%m-%d-%y').date()
        except Exception:
            video_date = datetime.date.today()
        id = video['video_id']
        if video_date >= cutoff_date and "commission" in title.lower():
            snippets = download_from_id(yt_api=ytApi, video_id=id)
            if snippets:
                for snippet in snippets:
                    snippetdict = {
                        'title': title,
                        'date': video_date,
                        'video_id': id,
                        'text': snippet['text'],
                        'start': snippet['start'],
                        'duration': snippet['duration']
                    }
                    videosDict.append(snippetdict)
    return videosDict
        



if __name__ == '__main__':
    ytt_api = YouTubeTranscriptApi()
    # Replace with your own API key
    # Create the YouTube service
    #TODO: get channelID from selenium or bs4
    channelId = 'UCI0JV91vepm1gAi6_O-5Nlg' # this can be obtained by view page source and searching for channelId
    #channelUrl = 'https://www.youtube.com/c/CityofMuskegonMeetings'
    videoList = get_all_videos_from_channel(channelId)
    transcripts = get_all_transcripts_for_videos(videoList, ytt_api)
    df = pd.DataFrame(transcripts)
    df.to_csv('all_transcripts_by_snippet.tsv', sep='\t')
    
