import pandas as pd
import os
import time
import shutil
import pathlib


from basicClustering import extract_mfccs, cluster_predict
from videoToText import get_all_videos_from_channel, filtered_videos
from videoToWav import download_from_url

def getAllVideos(channel) -> pd.DataFrame:
    videoList = get_all_videos_from_channel(channel)
    videoList = filtered_videos(videoList)
    allDfs = []
    for video in videoList:
        expectedTitle = rf"{video['title']} [{video['video_id']}].wav"
        if 'Commissioners Meeting' in video['title']:
            try:
                download_from_url(video['url'])
            except Exception as e:
                print(e)


def combineAllCLusters():
    allDfs = []
    for file in os.listdir('data/'):
        if file.endswith('.wav'):
            mfccs = extract_mfccs(f'data/{file}')
            speaker_labels = cluster_predict(mfccs)
            df = pd.DataFrame(speaker_labels, columns=['speaker'])
            df['meeting'] = file
            allDfs.append(df)

    combined = pd.concat(allDfs)
    grouped = combined.value_counts(normalize=True).rename_axis('unique_values').reset_index(name='counts')
    return grouped



if __name__ == "__main__":
    channelId = 'UCI0JV91vepm1gAi6_O-5Nlg'  # this can be obtained by view page source and searching for channelId
    getAllVideos(channelId)
    #groupedClusters = combineAllCLusters()
    #groupedClusters.to_csv('allClusteredVideos.csv')
