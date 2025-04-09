import pandas as pd
import numpy as np


try: 
    # ---------------------------------------------------------------------
    #                               Cleaning                              |
    # ---------------------------------------------------------------------
    # have to specify encoding since it is not in utf-8
    # also added the thousands arg to specify that metric columns have commas. Before applying this arg metrics had dtype of object, now have float64.
    df = pd.read_csv('Most Streamed Spotify Songs 2024.csv', encoding='latin-1', thousands=',' )
    
    print("\n--- Summary Statistics ---")
    # updating these options to make the summary more readable, instead of scientific notation
    pd.set_option('display.float_format', '{:.2f}'.format) # show 2 decimal places
    pd.set_option('display.max_columns', None) # show all columns
    pd.set_option('display.width', 200) # widen the display

    numeric_cols = df.select_dtypes(include=['float64','int64']).columns
    print(df[numeric_cols].describe().T)

    
    print("\n--- Data Types Summary ---")
    column_types = df.dtypes
    print(column_types)

    print("\n--- Date Type Conversion ---")
    df['Release Date'] = pd.to_datetime(df['Release Date'], errors='coerce')
    print("converted 'Release Date' to datetime")

    
    print("\n how many missing values are there in the set?")
    null_counts = df.isnull().sum()
    print(null_counts)

    print(f"\n number of rows before removing null artists: {len(df)}")
    df = df.dropna(subset=['Artist'])
    print(f"\n number of rows after removing null artists: {len(df)}")
    print("\nupdated null counts")
    print(df.isnull().sum())

    print("\nnot replacing nulls since granularity is song level")
    print("\nchecking for duplicates now")
    duplicate_rows = df.duplicated()
    has_duplicates = duplicate_rows.any()
    if has_duplicates:
        print("number of duplicated rows:", duplicate_rows.sum())
        print("duplicate rows")
        print(df[duplicate_rows])

    print(f"dataset has duplicate rows {duplicate_rows}")

    print("\ndropping duplicates")
    df = df.drop_duplicates()

    print("\n--- Checking for inconsistent values ---")
# Print total number of unique artists
    print(f"Total unique artists: {df['Artist'].nunique()}")
    print(f"Total unique artists (case insensitive): {df['Artist'].str.lower().nunique()}")

# If these numbers match, there are likely no capitalization variations
        
        # Optional: Standardize artist names (example for one artist)
        # df.loc[df['Artist'].str.lower() == 'drake', 'Artist'] = 'Drake'   


    # ------------------------------------------------------------------------
    #                           Post cleaning, early EDA                     |
    # ------------------------------------------------------------------------
    '''
    
    unique_songs = df['Track'].nunique()
    print(f"Number of unique songs: {unique_songs}")

# 3. Count of unique artists
    unique_artists = df['Artist'].nunique()
    print(f"Number of unique artists: {unique_artists}")

# 4. Find the top 5 artists with the most songs
    artist_counts = df['Artist'].value_counts().head(10)
    print("\nTop 5 artists with the most songs:")
    for artist, count in artist_counts.items():
        print(f"{artist}: {count} songs")

# Optional: If you want to see the distribution of songs per artist more broadly
    print("\nDistribution of songs per artist:")
    songs_per_artist = df['Artist'].value_counts()
    artist_song_counts = songs_per_artist.value_counts().sort_index()
    print(artist_song_counts)
    print("This shows how many artists have 1 song, 2 songs, etc.")
    '''

except UnicodeDecodeError as e:
    print(f"Error reading csv file: {e}")
    
