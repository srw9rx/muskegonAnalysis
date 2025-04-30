# script to take in files from the muskogen city council meetings and convert to text

# minutes link: https://muskegon-mi.gov/documents/type/1/2025/
# youtube link: https://www.youtube.com/c/CityofMuskegonMeetings
# https://naveen-malla.medium.com/transcribing-any-youtube-video-with-python-a-step-by-step-guide-cea7dd4e32f5

from youtube_transcript_api import YouTubeTranscriptApi
import re
import scrapetube
import datetime
import pandas as pd

YOUTUBE_RE = r'youtube.com/watch\?v=([\w-]*)' # re to parse out the video id given the youtube link


def downloadFromId(yt_api, video_link=None, video_id=None):
    ''' function to download the snippet from the video link or video id'''
    video_id = video_id if video_id else re.search(YOUTUBE_RE, video_link.strip('https://www.')).group(1)
    snippets = ytt_api.fetch(video_id)
    rawSnippets = snippets.to_raw_data()
    return rawSnippets

def getAllTranscriptsForChannel(channel_id, ytApi, cutoff_date=datetime.date(year=2022, day=3, month=1)):
    videos = scrapetube.get_channel(channel_id)
    videosDict = []
    i = 0
    for video in videos:
        i+=1
        title = video['title']['runs'][0]['text']
        datestring = None
        try:
            datestring = title.split()[0]
            if '/' in datestring:
                video_date = datetime.datetime.strptime(title.split()[0], '%m/%d/%y').date()
            elif '-' in datestring:
                video_date = datetime.datetime.strptime(title.split()[0], '%m-%d-%y').date()
        except Exception:
            video_date = datetime.date.today()
        id = video['videoId']
        if video_date >= cutoff_date:
            snippets = downloadFromId(yt_api=ytApi, video_id=id)
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
    #TODO: get channelID from selenium or bs4
    channelId = 'UCI0JV91vepm1gAi6_O-5Nlg' # this can be obtained by view page source and searching for channelId
    transcripts = getAllTranscriptsForChannel(channelId, ytt_api)
    df = pd.DataFrame(transcripts)
    df.to_csv('all_transcripts_by_snippet.tsv', sep='\t')
    
