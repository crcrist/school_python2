import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Set a consistent style and color
sns.set_theme(style="whitegrid")
MAIN_COLOR = '#72B7B2'  # Teal color
SECONDARY_COLOR = '#F67280'  # Pink/red color

# Create a results directory if it doesn't exist
if not os.path.exists('results'):
    os.makedirs('results')

try:
    print("""---------------------------------------------------------------------
                               Cleaning & EDA                            |
        ---------------------------------------------------------------------""")
    # Read in the data with specific encoding and comma formatting
    df = pd.read_csv('Most Streamed Spotify Songs 2024.csv', encoding='latin-1', thousands=',')
    
    print("\n--- Basic Dataset Information ---")
    print(f"Dataset shape: {df.shape}")
    print(f"Total entries: {len(df)}")
    
    print("\n--- Summary Statistics ---")
    pd.set_option('display.float_format', '{:.2f}'.format)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 200)

    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
    print(df[numeric_cols].describe().T)
    
    print("\n--- Data Types Summary ---")
    column_types = df.dtypes
    print(column_types)

    print("\n--- Date Type Conversion ---")
    df['Release Date'] = pd.to_datetime(df['Release Date'], errors='coerce')
    print(f"Earliest release date: {df['Release Date'].min()}")
    print(f"Latest release date: {df['Release Date'].max()}")
    
    # Add release year and month columns for analysis
    df['Release Year'] = df['Release Date'].dt.year
    df['Release Month'] = df['Release Date'].dt.month
    df['Month Name'] = df['Release Date'].dt.month_name()
    
    print("\n--- Null Values Check ---")
    null_counts = df.isnull().sum()
    print(null_counts)

    print("\n--- Remove Null Artist Rows ---")
    print(f"Number of rows before removing null artists: {len(df)}")
    df = df.dropna(subset=['Artist'])
    print(f"Number of rows after removing null artists: {len(df)}")
    print("\nUpdated null counts:")
    print(df.isnull().sum())

    print("\n--- Duplicate Row Check ---")
    duplicate_rows = df.duplicated()
    has_duplicates = duplicate_rows.any()
    if has_duplicates:
        print("Number of duplicated rows:", duplicate_rows.sum())
    print(f"Row count before duplicates dropped: {len(df)}")

    print("\n--- Dropping Duplicates ---")
    df = df.drop_duplicates()
    print(f"Row count after duplicates dropped: {len(df)}")

    print("\n--- Case Standardization for Text Columns ---")
    print(f"Total unique artists: {df['Artist'].nunique()}")
    print(f"Total unique artists (case insensitive): {df['Artist'].str.lower().nunique()}")
    print(f"Total unique albums: {df['Album Name'].nunique()}")
    print(f"Total unique albums (case insensitive): {df['Album Name'].str.lower().nunique()}")
    print(f"Total unique tracks: {df['Track'].nunique()}")
    print(f"Total unique tracks (case insensitive): {df['Track'].str.lower().nunique()}")

    print("\n--- Convert Artist, Album, and Song Names to Lowercase ---")
    df['Artist'] = df['Artist'].str.lower()
    df['Album Name'] = df['Album Name'].str.lower()
    df['Track'] = df['Track'].str.lower()
    
    print("\n--- Checking for impossible values ---")
    for col in numeric_cols:
        neg_count = (df[col] < 0).sum()
        if neg_count > 0:
            print(f"{col}: {neg_count} negative values found")
    
    # Additional cleaning: Convert text columns with numbers to numeric
    numeric_cols_to_convert = ['Spotify Streams', 'YouTube Views', 'TikTok Likes', 
                              'Spotify Playlist Count', 'YouTube Likes', 'Shazam Counts']
    
    print("\n--- Converting Text Columns with Numbers to Numeric ---")
    for col in numeric_cols_to_convert:
        if col in df.columns and df[col].dtype == 'object':
            df[col] = pd.to_numeric(df[col], errors='coerce')
            print(f"Converted {col} to numeric type")
    
    # Save the cleaned dataset
    df.to_csv('results/cleaned_spotify_songs.csv', index=False)
    print("\nCleaned dataset saved to 'results/cleaned_spotify_songs.csv'")
    
    print("""---------------------------------------------------------------------
                           Visualizations                                |
    ---------------------------------------------------------------------""")

    # Distribution plots
    print("\n--- Distribution Plots ---")
    for col in ['Spotify Streams', 'YouTube Views', 'TikTok Likes']:  
        plt.figure(figsize=(10, 6))
        plt.title(f'Distribution of {col}', fontsize=14)
        # Use log scale for highly skewed data
        if df[col].skew() > 1:
            sns.histplot(df[col], kde=True, log_scale=True, color=MAIN_COLOR)
            plt.xlabel(f'{col} (log scale)', fontsize=12)
        else:
            sns.histplot(df[col], kde=True, color=MAIN_COLOR)
            plt.xlabel(col, fontsize=12)
        plt.ylabel('Frequency', fontsize=12)
        plt.tight_layout()
        plt.savefig(f'results/distribution_{col.lower().replace(" ", "_")}.png')
        plt.close()
    
    # Top artists charts
    print("\n--- Top Artists Analysis ---")
    for metric in ['Spotify Streams', 'YouTube Views', 'TikTok Likes']:
        if metric in df.columns:
            top_artists = df.groupby('Artist')[metric].sum().sort_values(ascending=False).head(10)
            
            plt.figure(figsize=(12, 7))
            
            # Create the bar chart
            plt.bar(top_artists.index, top_artists.values, color=MAIN_COLOR)
            
            plt.title(f'Top 10 Artists by {metric}', fontsize=14)
            plt.xlabel('Artist', fontsize=12)
            plt.ylabel(f'Total {metric}', fontsize=12)
            plt.xticks(rotation=45, ha='right')
            
            # Add value labels to the bars
            for i, v in enumerate(top_artists.values):
                if v >= 1_000_000_000:
                    value_text = f'{v/1_000_000_000:.1f}B'
                elif v >= 1_000_000:
                    value_text = f'{v/1_000_000:.1f}M'
                else:
                    value_text = f'{v/1_000:.1f}K'
                plt.text(i, v * 0.9, value_text, ha='center', color='white', fontsize=11)
            
            plt.tight_layout()
            plt.savefig(f'results/top_artists_by_{metric.lower().replace(" ", "_")}.png')
            plt.close()
    
    # Correlation matrix
    print("\n--- Correlation Analysis ---")
    numeric_cols_for_corr = ['Spotify Streams', 'YouTube Views', 'TikTok Likes', 
                            'Spotify Popularity', 'Shazam Counts', 'Track Score']
    
    # Filter to just columns that exist and are numeric
    numeric_cols_for_corr = [col for col in numeric_cols_for_corr if col in df.columns 
                           and pd.api.types.is_numeric_dtype(df[col])]
    
    corr_matrix = df[numeric_cols_for_corr].corr()
    
    plt.figure(figsize=(12, 10))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt='.2f', 
                linewidths=0.5, vmin=-1, vmax=1)
    plt.title('Correlation Matrix of Key Features', fontsize=14)
    plt.tight_layout()
    plt.savefig('results/correlation_matrix.png')
    plt.close()

    # Scatter plots
    print("\n--- Key Relationship Visualizations ---")
    plt.figure(figsize=(10, 6))
    sns.regplot(x='Spotify Streams', y='YouTube Views', data=df, 
                scatter_kws={'alpha': 0.4, 's': 15, 'color': MAIN_COLOR}, 
                line_kws={'color': SECONDARY_COLOR})
    plt.title('Relationship Between Spotify Streams and YouTube Views', fontsize=14)
    plt.xlabel('Spotify Streams', fontsize=12)
    plt.ylabel('YouTube Views', fontsize=12)
    plt.grid(True, alpha=0.2)
    plt.tight_layout()
    plt.savefig('results/spotify_vs_youtube.png')
    plt.close()
    
    if 'Spotify Streams' in df.columns and 'Shazam Counts' in df.columns:
        plt.figure(figsize=(10, 6))
        sns.regplot(x='Spotify Streams', y='Shazam Counts', data=df, 
                    scatter_kws={'alpha': 0.4, 's': 15, 'color': MAIN_COLOR}, 
                    line_kws={'color': SECONDARY_COLOR})
        plt.title('Relationship Between Spotify Streams and Shazam Counts', fontsize=14)
        plt.xlabel('Spotify Streams', fontsize=12)
        plt.ylabel('Shazam Counts', fontsize=12)
        plt.grid(True, alpha=0.2)
        plt.tight_layout()
        plt.savefig('results/spotify_vs_shazam.png')
        plt.close()
    
    # Year-based analysis
    print("\n--- Time Series Analysis ---")
    if 'Release Year' in df.columns:
        yearly_streams = df.groupby('Release Year')['Spotify Streams'].sum()
        
        plt.figure(figsize=(14, 6))
        plt.bar(yearly_streams.index, yearly_streams.values, color=MAIN_COLOR)
        
        plt.title('Total Spotify Streams by Release Year', fontsize=16)
        plt.xlabel('Year', fontsize=14)
        plt.ylabel('Total Spotify Streams', fontsize=14)
        plt.xticks(rotation=45)
        plt.grid(axis='y', alpha=0.3)
        plt.tight_layout()
        plt.savefig('results/yearly_streams.png')
        plt.close()
    
    # Monthly pattern analysis
    print("\n--- Monthly Pattern Analysis ---")
    if 'Month Name' in df.columns:
        # Count songs by month
        monthly_counts = df['Month Name'].value_counts()
        
        # Reorder by calendar month instead of frequency
        month_order = ['January', 'February', 'March', 'April', 'May', 'June', 
                      'July', 'August', 'September', 'October', 'November', 'December']
        monthly_counts = monthly_counts.reindex(month_order)
        
        # Create the plot
        plt.figure(figsize=(12, 6))
        plt.bar(monthly_counts.index, monthly_counts.values, color=MAIN_COLOR)
        
        # Add data labels on top of each bar
        for i, v in enumerate(monthly_counts):
            plt.text(i, v + 5, str(v), ha='center', fontsize=10)
        
        plt.title('Number of Song Releases by Month (Seasonal Pattern)', fontsize=16)
        plt.xlabel('Month', fontsize=14)
        plt.ylabel('Number of Songs', fontsize=14)
        plt.grid(axis='y', alpha=0.3)
        plt.tight_layout()
        plt.savefig('results/monthly_seasonal_pattern.png')
        plt.close()
    
# Explicit vs non-explicit analysis with combined metrics
    print("\n--- Explicit Track Analysis ---")
    if 'Explicit Track' in df.columns:
        # Get counts and calculate metrics
        explicit_data = df.groupby('Explicit Track').agg({
            'Spotify Streams': ['mean', 'count', 'sum'],
        })
        
        # Format column names
        explicit_data.columns = ['_'.join(col).strip() for col in explicit_data.columns.values]
        
        # Calculate percentages
        total_songs = explicit_data['Spotify Streams_count'].sum()
        explicit_data['percent'] = (explicit_data['Spotify Streams_count'] / total_songs * 100)
        
        # Create the donut chart with combined metrics
        plt.figure(figsize=(10, 10))
        
        # Define labels with both percentage and average streams
        labels = []
        for i in range(len(explicit_data)):
            if i == 0 and 0 in explicit_data.index:
                label = 'Non-Explicit'
            else:
                label = 'Explicit'
            
            avg_streams = explicit_data['Spotify Streams_mean'][i] / 1_000_000
            pct = explicit_data['percent'][i]
            labels.append(f"{label}: {pct:.1f}%, {avg_streams:.1f}M")
        
        # Create the donut chart
        colors = [MAIN_COLOR, SECONDARY_COLOR]
        wedges, texts = plt.pie(
            explicit_data['Spotify Streams_count'], 
            labels=labels,
            colors=colors,
            startangle=90, 
            wedgeprops=dict(width=0.5)  # Creates the donut hole
        )
        
        # Style the text
        plt.setp(texts, size=14)
        
        plt.title('Explicit vs Non-Explicit Tracks\n(% of Tracks, Avg Streams per Track)', fontsize=16)
        plt.tight_layout()
        plt.savefig('results/explicit_vs_nonexplicit.png')
        plt.close()
    
    # Generate report
    print("""---------------------------------------------------------------------
                                Summary Report                            |
    ---------------------------------------------------------------------""")
    
    # Calculate key statistics for the report
    total_songs = len(df)
    total_artists = df['Artist'].nunique()
    total_streams = df['Spotify Streams'].sum() if 'Spotify Streams' in df.columns else "N/A"
    top_artist = df.groupby('Artist')['Spotify Streams'].sum().idxmax() if 'Spotify Streams' in df.columns else "N/A"
    latest_year = df['Release Year'].max() if 'Release Year' in df.columns else "N/A"
    
    # Generate a text report
    with open('results/analysis_report.txt', 'w') as f:
        f.write("# Analysis of Most Streamed Spotify Songs 2024 Dataset\n\n")
        f.write("## Dataset Overview\n")
        f.write(f"- Total songs analyzed: {total_songs}\n")
        f.write(f"- Total unique artists: {total_artists}\n")
        f.write(f"- Total Spotify streams: {total_streams:,.0f}\n")
        f.write(f"- Top artist by streams: {top_artist}\n")
        f.write(f"- Most recent year: {latest_year}\n\n")
        
        f.write("## Key Findings\n")
        f.write("1. Stream Distribution: The dataset exhibits a highly skewed distribution of streams, with a small number of songs receiving an extremely high number of streams, while the majority of songs have relatively fewer streams.\n\n")
        
        # Add correlation findings
        if len(numeric_cols_for_corr) > 1:
            # Get upper triangle mask
            mask = np.triu(np.ones_like(corr_matrix), k=1).astype(bool)
            corr_pairs = corr_matrix.mask(~mask).stack().sort_values(ascending=False)
            
            f.write("2. Platform Correlations: ")
            for i, ((feat1, feat2), corr) in enumerate(corr_pairs.head(3).items()):
                f.write(f"{feat1} and {feat2} show a {corr:.2f} correlation. ")
            f.write("\n\n")
        
        f.write("3. Top Artists: The analysis reveals that certain artists dominate across multiple platforms, suggesting a strong cross-platform presence.\n\n")
        
        if 'Explicit Track' in df.columns:
            explicit_pct = df['Explicit Track'].mean() * 100
            f.write(f"4. Explicit Content: {explicit_pct:.1f}% of the songs in the dataset contain explicit content.\n\n")
        
        if 'Release Year' in df.columns:
            recent_years = df[df['Release Year'] >= df['Release Year'].max() - 2]
            recent_pct = len(recent_years) / len(df) * 100
            f.write(f"5. Release Trends: {recent_pct:.1f}% of the most streamed songs were released in the past 3 years.\n\n")
        
        # Add monthly pattern findings
        if 'Month Name' in df.columns:
            top_month = monthly_counts.idxmax()
            f.write(f"6. Seasonal Patterns: {top_month} is the month with the most song releases ({monthly_counts.max()} songs), suggesting potential seasonal patterns in music release strategies.\n\n")
        
        f.write("## Conclusion\n")
        f.write("This analysis provides insights into streaming patterns across multiple platforms. The strong correlations between different platform metrics suggest that popular content tends to perform well across platforms. The data shows a concentration of success among a small group of artists, highlighting the winner-takes-all nature of music streaming. Future research could explore genre-specific trends and the impact of release timing on streaming success.\n")
    
    print("\nAnalysis complete! All results and visualizations saved to the 'results' directory.")
    print("Report saved as 'results/analysis_report.txt'")

except Exception as e:
    print(f"Error during analysis: {e}")
    import traceback
    traceback.print_exc()
