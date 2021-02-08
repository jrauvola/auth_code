# -*- coding: utf-8 -*-

import spotipy
from spotipy.oauth2 import SpotifyOAuth

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id='e2d254e0598f4ff49c5ce98717d35334',
                                               client_secret='db0d037ea3fe46d4b62c205ce5208d63',
                                               redirect_uri='http://localhost:8888/callback',
                                               scope="user-library-read"))

def songs():
    results = sp.current_user_saved_tracks(limit=10)
    for idx, item in enumerate(results['items']):
        track = item['track']
    audio_analysis(track["id"])
    #audio_features(track["id"])
        #print(idx, track['artists'][0]['name'], " – ", track['name'])

def playlist():
    results = sp.current_user_playlists(limit = 10)
    for idx, playlist in enumerate(results['items']):
        playlist2 = playlist['name']
        print(idx, playlist2)

# 
# audio analysis for project - titles include 
#
# meta = analyzer_version platform detailed_status status_code timestamp analysis_time input_process? 
# track = num_samples, duration, sample_md5, offset_seconds, window_seconds, analysis_sample_rate, analysis_channels ,end_of_fade_in - 
# start_of_fade_out, loudness, tempo, tempo_confidence, time_signature, time_signature_confidence, key, key_confidence, mode, mode_confidence
# codestring, code_version, echoprintstring, echoprint_version, synchstring synch_version, rhythmstring, rhythm_version
# bars = start, duration, confidence 
# beats = start, duration, confidence 
# sections = start, duration, confidence, loudness, tempo, temp_confidence, key_confidence, mode_confidence, time_signature, time_signature_confidence
# segments = start, duration, confidence, loudness_start, loudness_max_time, loudness_max, loudness_end, pitches, timbre
# tatums = start, duration, confidence
#

def audio_analysis(id):
    results = sp.audio_analysis(id)
    print(type(results))
    for idx, audio in enumerate(results['track']):
        #print(idx, audio)
        print(audio)

#  
# danceability, energy, key, loudness, mode, speechiness, acoustiness, acoutsticness, instrumentalness, liveness, valence, tempo, audio_features, uri, track href
# analysis_url, duration_ms, time_signature 
#

def audio_features(id):
    results = sp.audio_features(id)
    print(type(results))
    for idx, audio in enumerate(results):
        print(audio)
# can train against artist_related_artists(artist_id)? 

# reshape method - tenserflow 

def main():
    #playlist()
    songs()


if __name__ == "__main__":
    main()


