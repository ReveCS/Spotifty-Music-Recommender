import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests

from streamlit_lottie import st_lottie

# Getting Client Id and Client Secret
client_id = 'YOUR_CLIENT_ID'
client_secret = 'YOUR_CLIENT_SECRET'
auth_manage = SpotifyClientCredentials(client_id = client_id, client_secret = client_secret)
sp = spotipy.Spotify(client_credentials_manager = auth_manage) # Spotify object to access API

def main():
    