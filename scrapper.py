# -*- coding: utf-8 -*-

import statistics as st
import spotipy
from spotipy.oauth2 import SpotifyOAuth

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id='e2d254e0598f4ff49c5ce98717d35334',
                                               client_secret='db0d037ea3fe46d4b62c205ce5208d63',
                                               redirect_uri='http://localhost:8888/callback',
                                               scope="user-library-read"))

def songs():
    results = sp.current_user_saved_tracks(limit=1)
    for idx, item in enumerate(results['items']):
        track = item['track']
    audio_analysis(track["id"])
    print(idx, track['artists'][0]['name'], " – ", track['name'])
    audio_features(track["id"])

def playlist():
    results = sp.current_user_playlists(limit = 1)
    for idx, playlist in enumerate(results['items']):
        playlist2 = playlist['name']
        print(idx, playlist2)

def get_common_related_artists(artists):
    all_related = {}
    for a_id in artists:
        related_artists = sp.artist_related_artists(a_id)
        for artist in related_artists['artists']:
            if artist['id'] in all_related.keys():
                all_related[artist['id']] += 1
            else:
                all_related[artist['id']] = 1
    all_related = {k: v for k, v in sorted(all_related.items(), key = lambda item: item[1], reverse=True)}
    not_on_playlist = {}
    for (k, v) in all_related.items():
        if (v > 1) and (k not in artists):
            print(k,v)
            print(sp.artist(k)['name'], v)
            print()
            #common_related[k] = v

def playlist_artists(): 
    #note: there's no way to get genre of a song...... wtf?
    results = sp.current_user_playlists(limit = 1)
    p_ids = get_items(results['items'])
    p_id = p_ids[0]
    tracks = sp.playlist_tracks(p_id)
    artists = []
    for track in tracks['items']:
        item = track['track']
        for artist in item['artists']:
            if artist['id'] not in artists:
                artists.append(artist['id'])
                print(artist['name'], artist['id'])
    print(artists)
    return artists

def playlist_tracks(): 
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
    stats_magic(t_ids)


#helper function, don't remember what it does, im tired
def print_results(results):
    for item in results:
        if str(item) == 'items':
            print("Playlists:" + "\n")
            print_items(results[item])
            print()
        else:
            print(str(item) + ": " + str(results[item]))
            print()

#prints playlist(s)
def print_items(items):
    for item in items:
        print("name: " + item['name'])
        for elem in item:
            if elem != 'name':
                print(str(elem) + ": " + str(item[elem]))
        print()

#returns list of playlist ids
def get_items(items):
    ids = []
    for item in items:
        ids.append(item['id'])
    return ids


def pretty_audio_features(id):
    results = sp.audio_features(id)
    for idx, audio in enumerate(results):
        for attr in audio:
            print(attr, audio[attr])
        print()

def audio_features_stats(id):
    results = sp.audio_features(id)
    attr_stats = {}
    for idx, audio in enumerate(results):
        for attr in audio:
            if attr in attr_stats.keys():
                attr_stats[attr].append(audio[attr])
            else:
                attr_stats[attr] = [audio[attr]]
    ret_stats = {}
    for key in attr_stats.keys():
        if key not in ["type", "id", "uri", "track_href", "analysis_url", "duration_ms"]:
            ret_stats[key] = attr_stats[key] #just cleaning the clutter here
    return ret_stats

def stats_magic(t_ids):
    data = audio_features_stats(t_ids)
    for attr in data.keys():
        if attr not in ["loudness", "key", "mode", "time_signature", "instrumentalness"]: 
            #can't use harmonic mean for these. int avg/range for key, mode for mode and t_s
            print(attr, data[attr], st.harmonic_mean(data[attr]))
            print()

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
    #playlist_tracks()
    get_common_related_artists(playlist_artists())
    #print(sp.recommendation_genre_seeds())
    #playlist()
    #songs()


if __name__ == "__main__":
    main()


