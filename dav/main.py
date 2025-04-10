import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


try: 
    print("""---------------------------------------------------------------------
                                   Cleaning                              |
            ---------------------------------------------------------------------""")
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
    
    print("\n--- Null Values Check ---")
    null_counts = df.isnull().sum()
    print(null_counts)

    print("\n--- Remove Null Artist Rows ---")
    print(f"\n number of rows before removing null artists: {len(df)}")
    df = df.dropna(subset=['Artist'])
    print(f"\n number of rows after removing null artists: {len(df)}")
    print("\nupdated null counts")
    print(df.isnull().sum())

    print("\n--- Duplicate Row Check ---")
    duplicate_rows = df.duplicated()
    has_duplicates = duplicate_rows.any()
    if has_duplicates:
        print("number of duplicated rows:", duplicate_rows.sum())
    print(f"row count before duplicates dropped {len(df)}")

    print("\n--- Dropping Duplicates ---")
    df = df.drop_duplicates()
    print(f"row count after duplicates dropped {len(df)}")

    print("\n--- Compare Count of Normal Case Artist Names vs Lowercase ---")
    print(f"Total unique artists: {df['Artist'].nunique()}")
    print(f"Total unique artists (case insensitive): {df['Artist'].str.lower().nunique()}")

    print("\n--- Compare Count of Normal Case Album Names vs Lowercase ---")
    print(f"Total unique artists: {df['Album Name'].nunique()}")
    print(f"Total unique artists (case insensitive): {df['Album Name'].str.lower().nunique()}")
   
    print("\n--- Compare Count of Normal Case Track Names vs Lowercase ---")
    print(f"Total unique artists: {df['Track'].nunique()}")
    print(f"Total unique artists (case insensitive): {df['Track'].str.lower().nunique()}")

    print("\n--- Convert Artist, Album, and Song Names to Lowercase")
    df['Artist'] = df['Artist'].str.lower()
    df['Album Name'] = df['Album Name'].str.lower()
    df['Track'] = df['Track'].str.lower()
    

    print("\n--- Checking for outliers ---")
    for col in ['Spotify Streams', 'YouTube Views', 'TikTok Views']:
        if col in df.columns:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            outliers = df[(df[col] > Q3 + 1.5*IQR) | (df[col] < Q1 - 1.5*IQR)]
            print(f"{col}: {len(outliers)} potential outliers ({len(outliers)/len(df):.2%})")
            
            # Print top 5 outliers
            print(f"\nTop 5 highest outlier values for {col}:")
            top_outliers = outliers.sort_values(by=col, ascending=False).head(5)
            for idx, row in top_outliers.iterrows():
                print(f"  {row['Track']} by {row['Artist']}: {row[col]:,.0f}")
            
            # Print bottom 5 outliers
            print(f"\nBottom 5 lowest outlier values for {col}:")
            bottom_outliers = outliers.sort_values(by=col).head(5)
            for idx, row in bottom_outliers.iterrows():
                print(f"  {row['Track']} by {row['Artist']}: {row[col]:,.0f}")
            
            print("-" * 50)

    print("\n--- Checking for impossible values ---")
    for col in numeric_cols:
        # Simple check for negative values in metrics that should be positive
        neg_count = (df[col] < 0).sum()
        if neg_count > 0:
            print(f"{col}: {neg_count} negative values found")
# If these numbers match, there are likely no capitalization variations
        
        # Optional: Standardize artist names (example for one artist)
        # df.loc[df['Artist'].str.lower() == 'drake', 'Artist'] = 'Drake'   


    print("""---------------------------------------------------------------------\n|                    EDA                                       |\n---------------------------------------------------------------------""")

    for col in ['Spotify Streams', 'Spotify Popularity', 'YouTube Views'][:2]:  # Limit to 2 for example
        plt.figure()
        plt.title(f'Distribution of {col}')
        # Use log scale for highly skewed data
        if df[col].skew() > 1:
            sns.histplot(df[col], kde=True, log_scale=True)
            plt.xlabel(f'{col} (log scale)')
        else:
            sns.histplot(df[col], kde=True)
            plt.xlabel(col)
        plt.ylabel('Frequency')
        plt.tight_layout()
        plt.show()



    print("\n--- Feature Relationships ---")
# Find highest correlated features
    corr_matrix = df[numeric_cols].corr()
# Get upper triangle mask
    mask = np.triu(np.ones_like(corr_matrix), k=1).astype(bool)
    corr_pairs = corr_matrix.mask(~mask).stack().sort_values(ascending=False)
    print("Top 5 highest correlated features:")
    for i, ((feat1, feat2), corr) in enumerate(corr_pairs.head(5).items()):
        print(f"  {i+1}. {feat1} & {feat2}: {corr:.4f}")

    plt.figure(figsize=(14, 10))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt='.2f', 
                linewidths=0.5, vmin=-1, vmax=1)
    plt.title('Correlation Matrix of Numeric Features')
    plt.tight_layout()
    plt.show()      

except UnicodeDecodeError as e:
    print(f"Error reading csv file: {e}")
    
