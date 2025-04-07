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

except UnicodeDecodeError as e:
    print(f"Error reading csv file: {e}")
    
