from __future__ import unicode_literals
import yt_dlp
import ffmpeg
import sys

ydl_opts = {
    'format': 'bestaudio/best',
#    'outtmpl': 'output.%(ext)s',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'wav',
    }],
}
def download_from_url(url):
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
        stream = ffmpeg.input('output.m4a')
        stream = ffmpeg.output(stream, 'data/output.wav')




if __name__ == '__main__':
    url = 'https://www.youtube.com/watch?v=OeFJ4qCVDgI&ab_channel=CityofMuskegonMeetings'
    download_from_url(url)

