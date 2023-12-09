import spotipy
import spotipy.oauth2 as oauth2
from spotipy.oauth2 import SpotifyOAuth
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

client_id = 'f232eda2b061463cbaa4102c5101aa7b'
client_secret = '626817ddc0a74c9c8b59da3d91095107'

# function to get client ID and client secret
auth_manage = SpotifyClientCredentials(client_id = client_id, client_secret = client_secret)

# spotify object to access API
sp = spotipy.Spotify(client_credentials_manager = auth_manage)

# reading in data set
songs = pd.read_csv("/Users/blewinski/Downloads/songs.csv")

# filling in missing values
for col in songs:
    if songs[col].dtypes == 'float64':
        songs[col] = songs[col].fillna(0)
    elif songs[col].dtypes == 'object':
        songs[col] = songs[col].fillna("-")

def extract_features(dataset):
    """
    Compartmentalizes the important features of each song
    in the songs.csv dataset that will be used in the
    similarity scoring algorithm.
    """
    features = []
    for idx, row in dataset.iterrows():
        feature_vector = [
            row['id'],
            row['title'],
            row['artist'],
            row['danceability'],
            row['energy'],
            row['energy'],
            row['loudness'],
            row['speechiness'],
            row['acousticness'],
            row['instrumentalness'],
            row['valence'],
            row['tempo'],
        ]
        features.append(feature_vector)
        
    return np.array(features)

def recommend_songs(song_name, dataset_features, dataset, num_recommendations=10):
    """
    Prints out the top num_recommendations song recommendations from the songs.csv
    dataset, given a song name. Prints an error message if the provided song
    name can not be found within Spotify API.
    """
    query = sp.search(q=song_name, type='track', limit=1)
    if not query['tracks']['items']:
        print(f"No results found for {song}")
        return
    query_track = query['tracks']['items'][0]
    query_features = sp.audio_features(query_track['id'])[0]
    query_features = np.array([
        query_track['id'],
        query_track['name'],
        query_track['artists'][0]['name'],
        query_features['danceability'],
        query_features['energy'],
        query_features['energy'],
        query_features['loudness'],
        query_features['speechiness'],
        query_features['acousticness'],
        query_features['instrumentalness'],
        query_features['valence'],
        query_features['tempo'],
    ]).reshape(1, -1)
    
    similarity_scores = cosine_similarity(query_features[:, 3:], dataset_features[:, 3:])
    recommended_indices = np.argsort(similarity_scores[0])[::-1][:num_recommendations]
    
    print(f"Recommended songs for '{song_name}':")
    
    for index in recommended_indices:
        recommended_track = dataset.loc[index]
        print(f"{recommended_track['title']} by {recommended_track['artist']}")


# creating array of desired features for every song in dataset
dataset_features = extract_features(songs)
# testing to show that it works properly
song_name = input("Enter a song name: ")
recommend_songs(song_name, dataset_features, songs)