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

# fixing title column of songs dataset, as some song title strings have brackets
# at the end that need to be gotten rid of in order to print out song titles neatly
def rid_brackets(string):
    if "[" in string:
        string = string[:string.find("[")]
    return string
songs['title'] = songs['title'].apply(rid_brackets)

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
            row['loudness'],
            row['speechiness'],
            row['acousticness'],
            row['instrumentalness'],
            row['valence'],
            row['tempo'],
        ]
        features.append(feature_vector)
        
    return np.array(features)

# store array of features for each song in songs.csv
dataset_features = extract_features(songs)

def recommend_songs(song_name, dataset_features=dataset_features, dataset=songs, num_recommendations=10):
    """
    Returns the top num_recommendations songs recommendations from the songs.csv
    dataset as an array, given a song name. Prints an error message and returns None if the provided 
    song name can not be found within the Spotify API.
    """
    query = sp.search(q=song_name, type='track', limit=1)
    if not query['tracks']['items']:
        print(f"No results found for {song_name}")
        return
    query_track = query['tracks']['items'][0]
    query_features = sp.audio_features(query_track['id'])[0]
    query_features = np.array([
        query_track['id'],
        query_track['name'],
        query_track['artists'][0]['name'],
        query_features['danceability'],
        query_features['energy'],
        query_features['loudness'],
        query_features['speechiness'],
        query_features['acousticness'],
        query_features['instrumentalness'],
        query_features['valence'],
        query_features['tempo'],
    ]).reshape(1, -1)
    
    similarity_scores = cosine_similarity(query_features[:, 3:], dataset_features[:, 3:])
    recommended_indices = np.argsort(similarity_scores[0])[::-1]
    first_song = dataset.loc[recommended_indices[0]]
    # checks if the provided song was already in the dataset and therefore
    # was the first song in the list of recommendations: skips it
    # if so
    if first_song['title'].replace('"', '').lower() == query_track['name'].lower():
        if first_song['artist'] == query_track['artists'][0]['name']:
            recommended_indices = recommended_indices[1:num_recommendations+1]
    else:
        recommended_indices = recommended_indices[:num_recommendations]
    
    recommendations = []

    print(f"Recommended songs for {song_name}:")

    for index in recommended_indices:
        recommendations.append(dataset.loc[index])

    return recommendations

# main method, receives song name as input and runs the recommendation function
# to print out 10 recommended songs
def main():
    song_name = input("Enter the name of a song: ")
    recs = recommend_songs(song_name)
    if recs is not None:
        for rec in recs:
            print(f"{rec['title']} by {rec['artist']}")

if __name__ == "__main__":
    main()