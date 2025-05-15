import librosa
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

def extract_mfccs(audio_path:str) -> np.ndarray:
    audio, sr = librosa.load(audio_path, sr=None)
    mfccs = librosa.feature.mfcc(y=audio, sr=sr) # https://librosa.org/doc/main/generated/librosa.feature.mfcc.html
    return mfccs

def cluster_predict(mfccs: np.ndarray) -> np.ndarray:
    scaler = StandardScaler()
    mfccs_scaled = scaler.fit_transform(mfccs.T)
    # get n_clusters based on the number of distinct people that introduce themselves
    kmeans = KMeans(n_clusters=2)  # Adjust based on the expected number of speakers
    speaker_labels = kmeans.fit_predict(mfccs_scaled)
    return speaker_labels



if __name__ == "__main__":
    mfccs = extract_mfccs("data/051325_City_Of_Muskegon_Commissioners_Meeting_[OeFJ4qCVDgI].wav")
    speaker_labels = cluster_predict(mfccs)
    for i, label in enumerate(speaker_labels):
        print(f"Time Segment {i}: Speaker {label}")