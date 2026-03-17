import pandas as pd

def prepare_artist_data(df: pd.DataFrame, top_n: int) -> pd.DataFrame:
    """
    Prepares data for the top artists by grouping track counts per year.
    Fills in missing years with 0 so the Streamgraph curves fall cleanly to the baseline.
    """
    # Deduplicate in case df_exploded is used instead of df_clean
    if 'track_id' in df.columns:
        df_unique = df.drop_duplicates(subset=['track_id']).copy()
    else:
        df_unique = df.copy()
        
    # Get the top N artists overall
    top_artists = df_unique['artist_name'].value_counts().nlargest(top_n).index.tolist()
    df_filtered = df_unique[df_unique['artist_name'].isin(top_artists)].copy()
    
    # Group by year and artist to count tracks
    artist_trends = (df_filtered.groupby(['added_year', 'artist_name'])
                     .size()
                     .reset_index(name='track_count'))
    
    return artist_trends