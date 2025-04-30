# script to take in files from the muskogen city council meetings and convert to text

# minutes link: https://muskegon-mi.gov/documents/type/1/2025/
# youtube link: https://www.youtube.com/c/CityofMuskegonMeetings
# https://naveen-malla.medium.com/transcribing-any-youtube-video-with-python-a-step-by-step-guide-cea7dd4e32f5

from youtube_transcript_api import YouTubeTranscriptApi
from googleapiclient.discovery import build
import re
import datetime
import pandas as pd
from tqdm import tqdm
import argparse

# global variables
YOUTUBE_RE = r'youtube.com/watch\?v=([\w-]*)' # re to parse out the video id given the youtube link

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

def get_all_videos_from_channel(youtube, channel_id):
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
    for video in tqdm(videos, "transcribing videos:"):
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

def parse_arguments():
    parser = argparse.ArgumentParser(description='Download and transcribe YouTube videos from Muskegon City Council meetings')
    parser.add_argument('--api-key', required=True, help='YouTube API key')
    parser.add_argument('--channel-id', default='UCI0JV91vepm1gAi6_O-5Nlg',
                      help='YouTube channel ID (default: City of Muskegon Meetings channel)')
    parser.add_argument('--output', default='all_transcripts_by_snippet.tsv',
                      help='Output file path (default: all_transcripts_by_snippet.tsv)')
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_arguments()
    
    # Initialize YouTube API client
    youtube = build('youtube', 'v3', developerKey=args.api_key)
    
    # Initialize YouTube Transcript API
    ytt_api = YouTubeTranscriptApi()
    
    # Get videos and transcripts
    videoList = get_all_videos_from_channel(youtube, args.channel_id)
    transcripts = get_all_transcripts_for_videos(videoList, ytt_api)
    
    # Save results
    df = pd.DataFrame(transcripts)
    df.to_csv(args.output, sep='\t')
    
