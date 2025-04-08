import pandas as pd
import numpy as np


try: 
    # have to specify encoding since it is not in utf-8
    # also added the thousands arg to specify that metric columns have commas. Before applying this arg metrics had dtype of object, now have float64.
    df = pd.read_csv('Most Streamed Spotify Songs 2024.csv', encoding='latin-1', thousands=',' )
    
    print("""
        describe function to see summary stats
          """)
    print(df.describe())
    
    print("""
        print out the columnn data types, feels like some columns are missing from the summary stats 
          """)
    column_types = df.dtypes
    print(column_types)
    
    print("""
        look to see what are some of the values contained in these fields
          """)
    pd.set_option('display.max_columns', None)
    print(df.head(5))

    print("""
          how many missing values are there in the set? 
          """)
    null_counts = df.isnull().sum()
    print(null_counts)

    print("""
          because the level of detail is at the song level, and streams are aggregated, it would not make sense to fill null values with median.
          ie; if a song was at bottom of list, and we filled with median of spotify streams for whole dataset, would inflate the score of that song.

          now check for duplicate rows
            """)
    duplicate_rows = df.duplicated()
    has_duplicates = duplicate_rows.any()
    if has_duplicates:
        print("number of duplicated rows:", duplicate_rows.sum())
        print("duplicate rows")
        print(df[duplicate_rows])

    print(f"dataset has duplicate rows {duplicate_rows}")
    
    duplicate_songs = df.duplicated(subset=['Track', 'Artist'], keep='first')
    has_duplicate_songs = duplicate_songs.any()
    print(f"dataset has duplicate songs {duplicate_songs}")
    if has_duplicate_songs:
        print("number of duplicate songs:", duplicate_songs.sum())
        print("duplicate rows:")
        print(df[duplicate_songs])

    print("""
            going to drop the duplicates that are matching over all columns, for the other artist + song combinations i am going to aggregate the metrics
          """)
    df = df.drop_duplicates()

except UnicodeDecodeError as e:
    print(f"Error reading csv file: {e}")
    
