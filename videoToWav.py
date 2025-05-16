from __future__ import unicode_literals
import yt_dlp
import ffmpeg
import sys

ydl_opts = {
    'cookiefile': 'cookies.txt', # add this from cookie extension in netscape format so it doesn't fail
    'format': 'bestaudio/best',
#    'outtmpl': 'output.%(ext)s',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'wav',
    }],
}

def download_from_url(url, filename:str|None = None):
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
        stream = ffmpeg.input('output.m4a')
        stream = ffmpeg.output(stream, 'data/output.wav')




if __name__ == '__main__':
    url = 'https://www.youtube.com/watch?v=6ugYYGyD-4k&ab_channel=CityofMuskegonMeetings'
    download_from_url(url)