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
auth_manage = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=auth_manage)  # Spotify object to access API


def load_lottie(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


def get_recommendations(track_name):
    # Get string track URI
    results = sp.search(q=track_name, type="track")
    track_uri = results["tracks"]["items"][0]["uri"]

    # Get recommended tracks
    recommendations = sp.recommendations(seed_tracks=[track_uri], limit=10)["tracks"]
    return recommendations


def get_analysis(start_year, end_year):
    st.markdown("""## Some Analysis of the year range are:
            """)

    plt.style.use("default")
    df2 = pd.read_csv("songs.csv")

    year = df2.groupby(by='year').mean(numeric_only=True).drop(columns='peak').reset_index()

    # First Row

    col1, col2 = st.columns(2)

    col1.subheader("Duration")
    fig, ax = plt.subplots()
    ax.plot(year['year'], (year['duration_ms'] / 1_000) / 60)
    ax.set_xlim(start_year, end_year)
    ax.set_ylim(0, 6.5)

    # Add in title and subtitle
    ax.set_title("""Nobody got time for Music?""")
    ax.text(x=.08, y=.86,
            s="",
            transform=fig.transFigure,
            ha='left',
            fontsize=20,
            alpha=.8)
    col1.pyplot(fig)

    col2.subheader("Loudness")
    fig, ax = plt.subplots()
    ax.plot(year['year'], year['loudness'])
    ax.set_xlim(start_year, end_year)
    ax.set_ylim(-15, -3)

    # Add in title and subtitle
    ax.set_title("""Hearing protection recommended""")
    ax.text(x=.08, y=.86,
            s="",
            transform=fig.transFigure,
            ha='left',
            fontsize=20,
            alpha=.8)
    col2.pyplot(fig)

    # Second Row

    col3, col4 = st.columns(2)

    col3.subheader("Valence & Acusticness")
    fig, ax = plt.subplots()
    ax.plot(year['year'], year['valence'])
    ax.plot(year['year'], year['acousticness'])
    ax.set_xlim(start_year, end_year)
    ax.set_ylim(0, .85)

    # Add in title and subtitle
    ax.set_title("""I've got a negative feeling...""")
    ax.text(x=.08, y=.86,
            s="",
            transform=fig.transFigure,
            ha='left',
            fontsize=20,
            alpha=.8)

    # Label the lines directly
    ax.text(x=.78, y=.66, s="""Valence""",
            transform=fig.transFigure, ha='left', fontsize=20, alpha=.7)
    ax.text(x=.73, y=.30, s="""Acousticness""",
            transform=fig.transFigure, ha='left', fontsize=20, alpha=.7)
    col3.pyplot(fig)

    col4.subheader("Danceability & Energy")
    fig, ax = plt.subplots()
    ax.plot(year['year'], year['danceability'])
    ax.plot(year['year'], year['energy'])
    ax.set_xlim(start_year, end_year)
    ax.set_ylim(0, .85)

    # Add in title and subtitle
    ax.set_title('Hmm...')
    ax.text(x=.08, y=.86,
            s="",
            transform=fig.transFigure,
            ha='left',
            fontsize=20,
            alpha=.8)

    # Label the lines directly
    ax.text(x=.7, y=.795, s="""Energy""",
            transform=fig.transFigure, ha='left', fontsize=20, alpha=.7)
    ax.text(x=.685, y=.61, s="""Danceability""",
            transform=fig.transFigure, ha='left', fontsize=20, alpha=.7)
    col4.pyplot(fig)

    # Third Row

    col5, col6 = st.columns(2)

    col5.subheader("Instrumentalness & Speechiness")
    fig, ax = plt.subplots()
    ax.plot(year['year'], year['instrumentalness'])
    ax.plot(year['year'], year['speechiness'])
    ax.set_xlim(start_year, end_year)
    ax.set_ylim(0, .32)

    ax.set_yticks(np.arange(0, .35, 0.05))

    # Add in title and subtitle
    ax.set_title("They don't sing like they used to..")
    ax.text(x=.08, y=.86,
            s="",
            transform=fig.transFigure,
            ha='left',
            fontsize=20,
            alpha=.8)

    # Label the lines directly
    ax.text(x=.57, y=.17, s="""Instrumentalness""",
            transform=fig.transFigure, ha='left', fontsize=20, alpha=.7)
    ax.text(x=.72, y=.52, s="""Speechiness""",
            transform=fig.transFigure, ha='left', fontsize=20, alpha=.7)
    col5.pyplot(fig)

    col6.subheader("Energy")
    fig, ax = plt.subplots()
    ax.plot(year['year'], year['energy'])
    ax.set_xlim(start_year, end_year)
    ax.set_ylim(0.03, 1)

    # Add in title and subtitle
    ax.set_title("""Is it increasing?""")
    ax.text(x=.08, y=.86,
            s="",
            transform=fig.transFigure,
            ha='left',
            fontsize=20,
            alpha=.8)
    col6.pyplot(fig)


def main():
    lottie = load_lottie("https://lottie.host/41484d6f-44d0-4cce-a6f0-caf84cd11a1f/KGT0vYO2fg.json")
    # st_lottie(lottie, speed=1, height=200, key="initial")

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

    track_name = st.text_input("Enter the song name with artist name:")

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

    # Get Top Singles Playlist
    st.markdown("**Let the Hat generate a playlist of songs that made\
                    the Top 10 for the years you select.**")

    df = pd.read_csv("playlist.csv")
    years = list(range(1958, 2022))

    year_range = st.slider(label="Start Year",
                           min_value=2012,
                           max_value=2022,
                           value=(2014, 2020))

    if st.button('Get Playlist'):
        if (int(year_range[0]) - int(year_range[1])) == 0:
            playlist_name = f"Top Singles: {year_range[0]}"
        else:
            playlist_name = f"Top Songs: {year_range[0]}-{year_range[1]}"

        if df[df['name'] == playlist_name].shape[0] > 0:
            playlist = df[df['name'] == playlist_name].to_dict(orient='records')[0]
        else:
            playlist = "Ooops, it looks like we didn't make that playlist yet."

        if isinstance(playlist, dict):
            link = f"#### Your Spotify Playlist: [{playlist['name']}]({playlist['link']})"
            st.markdown(link, unsafe_allow_html=True)
            get_analysis(year_range[0], year_range[1])

        else:
            st.markdown(playlist)


if __name__ == "__main__":
    main()
