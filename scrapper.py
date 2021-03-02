# -*- coding: utf-8 -*-

import statistics as st
import spotipy
from spotipy.oauth2 import SpotifyOAuth

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id='e2d254e0598f4ff49c5ce98717d35334',
                                               client_secret='db0d037ea3fe46d4b62c205ce5208d63',
                                               redirect_uri='http://localhost:8888/callback',
                                               scope="user-library-read"))

def print_playlist_tracks(): 
    #note: there's no way to get genre of a song...... wtf?
    results = sp.current_user_playlists(limit = 1)
    p_ids = get_items(results['items'])
    p_id = p_ids[0]
    #print_tracks('4sJBQ3gA3wjVN8REraatpo') #one-song playlist, for testing sake
    tracks = sp.playlist_tracks(p_id)
    t_ids = []
    for track in tracks['items']:
        item = track['track']
        t_ids.append(item['id'])
        print('Song name:        ', item['name'])
        print('Artist name(s):   ', item['artists'][0]['name'])
        if len(item['artists']) > 1:
            for artist in item['artists'][1:]:
                print("                  ", artist['name'])
    print()
    #stats_magic(t_ids)
    return t_ids

def playlist_tracks(): 
    #note: there's no way to get genre of a song...... wtf?
    results = sp.current_user_playlists(limit = 1)
    print()
    print(results['items'][0]['name'])
    print()
    p_ids = get_items(results['items'])
    p_id = p_ids[0]
    tracks = sp.playlist_tracks(p_id)
    t_ids = []
    for track in tracks['items']:
        item = track['track']
        t_ids.append(item['id'])
    #stats_magic(t_ids)
    return t_ids

#had to do this track by track since the stupid spotipy thing doesn't work with more than 5????? wtf dude
def get_tracks_recs(t_ids, limit=None):
    recomms = []
    for t_id in t_ids:
        if limit:
            if len(recomms) >= limit:
                break
        recs = sp.recommendations(seed_artists = None, seed_genres = None, seed_tracks = [t_id])
        for rec in recs['tracks']:
            if rec['id'] not in recomms:
                recomms.append(rec['id'])
    return recomms

#prints playlist(s)
def print_items(items):
    for item in items:
        print("name: " + item['name'])
        for elem in item:
            if elem != 'name':
                print(str(elem) + ": " + str(item[elem]))
        print()

def normalize_pop(pop):
    return float(pop/100)

def normalize_tempo(tempo):
    lower_limit = 20
    upper_limit = 180
    if tempo < lower_limit:
        new_tempo = 0.0
    elif tempo > upper_limit:
        new_tempo = 1.0
    else:
        new_tempo = tempo/(lower_limit+upper_limit)
    return new_tempo

#returns number of songs on first playlist, can change this to certain playlist by using ID instead
def count_songs_on_playlist():
    results = sp.current_user_playlists(limit = 1)
    num_songs = results['items'][0]['tracks']['total']
    return num_songs

#returns list of playlist ids
def get_items(items):
    ids = []
    for item in items:
        ids.append(item['id'])
    return ids

# returns [[song1 danceability, song1 energy, ...], [song2 danceability, ....], ....]
# suggested songs 
def get_suggested_features(t_ids=None, limit=20):
    features = []
    if t_ids == None:
        t_ids = playlist_tracks()
    recs = get_tracks_recs(t_ids, limit)
    data = audio_features(recs)
    for song in data:
        f = [song['danceability'], song['energy'], song['speechiness'], 
             song['acousticness'], song['liveness'], 
             song['valence'], normalize_tempo(song['tempo']), 
             normalize_pop(sp.track(song['id'])['popularity']), song['valence']]
        features.append(f)
    return features

#returns harmonic mean summary vector of all suggested songs
def get_suggested_summary(t_ids=None, limit=20, features=None):
    d = []
    e = []
    s = []
    a = [] 
    l = [] 
    v = [] 
    t = [] 
    p = [] 
    v2 = []
    if t_ids == None:
        t_ids = playlist_tracks()
    if features == None:
        features = get_suggested_features(t_ids, limit)
    print(features)
    for f in features:
        d.append(f[0])
        e.append(f[1])
        s.append(f[2])
        a.append(f[3])
        l.append(f[4])
        v.append(f[5])
        t.append(f[6])
        p.append(f[7])
        v2.append(f[8])
    summary = [float(st.harmonic_mean(x)) for x in [d, e, s, a, l, v, t, p, v2]]
    return summary

#returns [[song1 danceability, song2 danceability,....], [song1 energy, .....], .....]
# songs on the playlist
def get_playlist_features(t_ids=None):
    features = [[] for i in range(9)]
    if t_ids == None:
        t_ids = playlist_tracks()
    for t_id in t_ids:
        features[7].append(normalize_pop(sp.track(t_id)['popularity']))
    data = audio_features(t_ids)
    for song in data:
        features[0].append(song['danceability'])
        features[1].append(song['energy'])
        features[2].append(song['speechiness'])
        features[3].append(song['acousticness'])
        features[4].append(song['liveness'])
        features[5].append(song['valence'])
        features[6].append(normalize_tempo(song['tempo']))
        features[8].append(song['instrumentalness'])
    #print(features)
    return features

# danceability, energy, key, loudness, mode, speechiness, acoustiness, acoutsticness, instrumentalness, liveness, valence, tempo, audio_features, uri, track href
# analysis_url, duration_ms, time_signature 
#

def audio_features(id):
    results = sp.audio_features(id)
    #print(type(results))
    """for idx, audio in enumerate(results):
        print(audio)"""
    return results

def main():
    #f = get_playlist_features()
    #print(f)
    #get_suggested_features()
    print(get_suggested_summary())

if __name__ == "__main__":
    main()


