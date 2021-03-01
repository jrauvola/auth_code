# -*- coding: utf-8 -*-

import statistics as st
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
    #audio_analysis(track["id"])
    print(idx, track['artists'][0]['name'], " – ", track['name'])
    audio_features(track["id"])

def playlist():
    results = sp.current_user_playlists(limit = 1)
    for idx, playlist in enumerate(results['items']):
        playlist2 = playlist['name']
        print(idx, playlist2)

#def get_recommendations(seed_artists=None, seed_genres=None):


#this is hecka spaghetti code so just ask me if you wanna know wtf it does
def get_common_related_artists(artists, limit=None):
    print("Calculating results...\n")
    all_related = {}
    #nested loop kills efficiency - how to fix this?
    for a_id in artists:
        related_artists = sp.artist_related_artists(a_id)
        for artist in related_artists['artists']:
            if artist['id'] in all_related.keys():
                all_related[artist['id']] = round(all_related[artist['id']] + artists[a_id], 4)
            else:
                if artist['id'] not in artists:
                    all_related[artist['id']] = artists[a_id]
    all_related = {k: v for k, v in sorted(all_related.items(), key = lambda item: item[1], reverse=True)}
    multiple_recs = {} 
    magic_number = 1/max(all_related.values())
    for (k, v) in all_related.items():
        if v*magic_number > .66:
            multiple_recs[k] = v
    sorted_recs = sorted(multiple_recs.items(), key = lambda item: item[1], reverse=True)
    if limit:
        sorted_recs = sorted_recs[:limit]
    pair_dict = {}
    for (k, v) in sorted_recs:
        pair_dict[k] = (v*100, v*magic_number*100)
        print(sp.artist(k)['name'])
        print("Compatibility Index:", v)
        print("Compatibility Score:", str(round(v*magic_number*100, 2)) + '%\n')
    return pair_dict

#due to scoring becoming > 100%, this will only account for the first artist listed on each track
#add epsilon or some shit to round
def weighted_playlist_artists():
    print("Getting artists...")
    count_songs = count_songs_on_playlist()
    results = sp.current_user_playlists(limit = 1)
    p_ids = get_items(results['items'])
    p_id = p_ids[0]
    tracks = sp.playlist_tracks(p_id)
    artists = {}
    for track in tracks['items']:
        item = track['track']
        artist = item['artists'][0]
        if artist['id'] in artists.keys():
            artists[artist['id']] += 1
        else:
            artists[artist['id']] = 1
    test_sum = 0
    for a in artists:
        artists[a] = artists[a]/count_songs
        test_sum += artists[a]
    return artists

def playlist_artists(): 
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
                #print(artist['name'], artist['id'])
    #print(artists)
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
    #stats_magic(t_ids)
    return t_ids


def get_best_artists(a_ids_weighted, percent_len=67):
    a_ids = [k for k,v in sorted(a_ids_weighted.items(), key = lambda item: item[1], reverse=True)]
    init_len = len(a_ids)
    new_len = int(init_len*(percent_len/100))
    return (a_ids[:new_len+1])
    #print(sp.artists(a_ids[:new_len+1])['artists'])

def get_better_artists_recs(a_ids_weighted):
    #a_ids = [k for k in a_ids_weighted.keys() if a_ids_weighted[k][1] > 66]
    #print(a_ids)
    a_ids = a_ids_weighted.keys()
    recomms = []
    for a_id in a_ids:
        recs = sp.recommendations(seed_artists = [a_id], seed_genres = None, seed_tracks = None)
        #for rec in recs['tracks']:
        #    print(rec)
        
        for rec in recs['tracks']:
            print(rec['artists'][0]['name'], rec['name'])
            if rec['id'] not in recomms:
                recomms.append(rec['id'])
    print(recomms)
    return recomms

def get_artists_recs(a_ids):
    recomms = []
    for a_id in a_ids:
        recs = sp.recommendations(seed_artists = [a_id], seed_genres = None, seed_tracks = None)
        #for rec in recs['tracks']:
        #    print(rec)
        
        for rec in recs['tracks']:
            print(rec['artists'][0]['name'], rec['name'])
            if rec['id'] not in recomms:
                recomms.append(rec['id'])
    print(recomms)
    return recomms

#had to do this track by track since the stupid spotipy thing doesn't work with more than 5????? wtf dude
def get_tracks_recs(t_ids):
    recomms = []
    for t_id in t_ids:
        recs = sp.recommendations(seed_artists = None, seed_genres = None, seed_tracks = [t_id])
        for rec in recs['tracks']:
            if rec['id'] not in recomms:
                recomms.append(rec['id'])
    print(recomms)
    return recomms

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

def get_artists_genres(a_ids_weights):

    results = sp.artists(a_ids_weights.keys())
    #print(results)
    genres = {}
    for item in results['artists']:
        print(item['name'], item['id'], item['genres'], a_ids_weights[item['id']])

def get_track_genres(t_ids):
    results = sp.tracks(t_ids)
    #print(results)
    genres = {}
    for item in results['tracks']:
        print(item)
        #print(item['name'], item['id'], item['genres'])

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
    magic_numbers = {}
    for attr in data.keys():
        if attr not in ["loudness", "key", "mode", "time_signature", "instrumentalness"]: 
            #can't use harmonic mean for these. int avg/range for key, mode for mode and t_s
            magic_numbers[attr] = st.harmonic_mean(data[attr])
            #print(attr, data[attr], st.harmonic_mean(data[attr]))
            #print()
    for (k,v) in magic_numbers.items():
        print(k + ":", v)
    print()

#returns [[song1 danceability, song1 energy, ...], [song2 danceability, ....], ....]
def get_suggested_features():
    pass

#returns harmonic mean summary vector of all suggested songs
def get_suggested_summary():
    pass

#returns [[song1 danceability, song2 danceability,....], [song1 energy, .....], .....]
def get_playlist_features():
    features = [[] for i in range(9)]
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

    #playlist_tracks()
#  
# danceability, energy, key, loudness, mode, speechiness, acoustiness, acoutsticness, instrumentalness, liveness, valence, tempo, audio_features, uri, track href
# analysis_url, duration_ms, time_signature 
#

def audio_features(id):
    results = sp.audio_features(id)
    #print(type(results))
    """for idx, audio in enumerate(results):
        print(audio)"""
    return results
# can train against artist_related_artists(artist_id)? 

# reshape method - tenserflow 


def main():
    """results = sp.categories()
    for result in results['categories']['items']:
        print(result['name'])"""
    
    #get_tracks_recs(playlist_tracks())
    #get_artists_recs(playlist_artists())
    #get_better_artists_recs(weighted_playlist_artists())
    
    #playlist_tracks()
    f = get_playlist_features()
    print(f)
    #print(sp.artist('5TwydvtVAZOeVpGUioBCSn'))
    #print()
    #print(sp.track('0X0Lz7LwpiIWcdGqVWaxXD')['popularity'])
    #get_artists_recs(get_best_artists(weighted_playlist_artists()))

    #for result in results['tracks']:
    #    print(result['artists'][0]['name'], result['name'])
    
    #get_artists_genres(weighted_playlist_artists())
    #get_common_related_artists(weighted_playlist_artists())
    #weighted_playlist_artists()
    #playlist()
    #songs()

if __name__ == "__main__":
    main()


