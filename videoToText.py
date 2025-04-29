# script to take in files from the muskogen city council meetings and convert to text

# minutes link: https://muskegon-mi.gov/documents/type/1/2025/
# youtube link: https://www.youtube.com/c/CityofMuskegonMeetings
# https://naveen-malla.medium.com/transcribing-any-youtube-video-with-python-a-step-by-step-guide-cea7dd4e32f5

from youtube-transcript-api import YouTubeTranscriptApi
import re
import scrapetube

YOUTUBE_RE = r'youtube.com/watch\?v=([\w-]*)' # re to parse out the video id given the youtube link


def downloadFromId(yt_api, video_link=None, video_id=None):
    ''' function to download the snippet from the video link or video id'''
    video_id = video_id if video_id else re.search(YOUTUBE_RE, video_link.strip('https://www.')).group(1)
    snippets = ytt_api.fetch(video_id)
    rawSnippets = snippets.to_raw_data()
    return rawSnippets

def getAllTranscriptsForChannel(channelId, ytApi)
    videos = scrapetube.get_channel(channelId)
    for video in videos:
        print(video)
        downloadFromId(yt_api=ytApi, video_id=video['videoId'])
        #TODO: export these to a csv




if __name__ == '__main__':
    ytt_api = YouTubeTranscriptApi()
    channelId = 'UCI0JV91vepm1gAi6_O-5' # this can be obtained by view page source and searching for channelId
    transcripts = getAllTransciptsForChannel(channelId, ytt_api)
    
