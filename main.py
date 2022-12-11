# -*- coding: utf-8 -*-
"""
Created on Thu Nov  3 13:56:20 2022

@author: Admin
"""

import pandas as pd
albums_data=pd.read_csv("spotify_albums.csv")
artists_data=pd.read_csv("spotify_artists.csv")
tracks_data=pd.read_csv("spotify_tracks.csv")

#kết hợp năm phát hành album và thông tin thể loại nghệ sĩ với dữ liệu bản nhạc.
## join artist genre information and album release date with track dataset
# drop irrelevant columns
# get only tracks after 1990
def join_genre_and_date(artist_df, album_df, track_df):
    album = album_df.rename(columns={'id':"album_id"}).set_index('album_id')
    artist = artist_df.rename(columns={'id':"artists_id",'name':"artists_name"}).set_index('artists_id')
    track = track_df.set_index('album_id').join(album['release_date'], on='album_id' )
    track.artists_id = track.artists_id.apply(lambda x: x[2:-2])
    track = track.set_index('artists_id').join(artist[['artists_name','genres']], on='artists_id' )
    track.reset_index(drop=False, inplace=True)
    track['release_year'] = pd.to_datetime(track.release_date).dt.year
    track.drop(columns = ['Unnamed: 0','country','track_name_prev','track_number','type'], inplace = True)
    
    return track[track.release_year >= 1990]
# xoa du lieu thua
def get_filtered_track_df(df, genres_to_include):
    df['genres'] = df.genres.apply(lambda x: [i[1:-1] for i in str(x)[1:-1].split(", ")])
    df_exploded = df.explode("genres")[df.explode("genres")["genres"].isin(genres_to_include)]
    df_exploded.loc[df_exploded["genres"]=="korean pop", "genres"] = "k-pop"
    df_exploded_indices = list(df_exploded.index.unique())
    df = df[df.index.isin(df_exploded_indices)]
    df = df.reset_index(drop=True)
    return df

#genres_to_include = genres = ['dance pop', 'electronic', 'electropop', 'hip hop', 'jazz', 'k-pop', 'latin', 'pop', 'pop rap', 'r&b', 'rock']
#track_with_year_and_genre = join_genre_and_date(artists_data, albums_data, tracks_data)
#filtered_track_df = get_filtered_track_df(track_with_year_and_genre, genres_to_include)

#filtered_track_df["uri"] = filtered_track_df["uri"].str.replace("spotify:track:", "")
#filtered_track_df = filtered_track_df.drop(columns=['analysis_url', 'available_markets'])

#filtered_track_df.to_csv("filtered_track_df.csv", index=False)
print(albums_data.head().drop('Unnamed: 0', axis=1))
print(artists_data.head().drop('Unnamed: 0', axis=1))
print(tracks_data.head().drop('Unnamed: 0', axis=1))