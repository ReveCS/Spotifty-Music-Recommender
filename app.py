import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests

from streamlit_lottie import st_lottie

# Getting Client Id and Client Secret
client_id = 'f232eda2b061463cbaa4102c5101aa7b'
client_secret = '626817ddc0a74c9c8b59da3d91095107'
auth_manage = SpotifyClientCredentials(client_id = client_id, client_secret = client_secret)
sp = spotipy.Spotify(client_credentials_manager = auth_manage) # Spotify object to access API

def load_lottie(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

def get_recommendations(track_name):
    # Getring track URI
    results = sp.search(q = track_name, type = "track")
    track_uri = results["tracks"]["items"][0]["uri"]

    # Get recommended tracks
    recommendations = sp.recommendations(seed_tracks = [track_uri], limit = 10)["tracks"]
    return recommendations


def main():
    lottie = load_lottie("https://lottie.host/41484d6f-44d0-4cce-a6f0-caf84cd11a1f/KGT0vYO2fg.json")
    st_lottie(lottie, speed=1, height=200, key="initial")

    row0_1, row0_2 = st.columns((2, 1))
    row0_1.title("Spotify Sorting Hat 🎩")

    row0_2.subheader(
        "Curated by "
        "Blake Lewinski, "
        "Jiaxin Chen, "
        "and Avery Chan"
    )

    st.markdown(
        "Welcome to the magical world of the Spotify Sorting Hat! 🧙‍♂️  \n"
        "This app will help you find your musical soulmates. 🎶  \n"
        "Simply enter a song name and we'll do the rest! 🎵👇"
    )

    track_name = st.text_input("Enter the song name:")

    if st.button("Get Recommendations"):
        recommendations = get_recommendations(track_name)

        if recommendations is not None:
            st.write("Recommended Songs Are:")
            for track in recommendations:
                st.write(track["name"])
                track_image = track["album"]["images"][0]["url"]
                st.image(track_image, width=60)

        else:
            st.error("No such song exists")

    st.markdown("")
    st.markdown("")

if __name__ == "__main__":
    main()