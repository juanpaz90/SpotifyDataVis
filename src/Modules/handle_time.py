import pandas as pd

def transform_time_and_duration(df_file: pd.DataFrame) -> pd.DataFrame:
    """
    Converts timestamps to datetime objects, extracts year/month, 
    and converts track duration from ms to minutes.
    """
    df_file = df_file.copy()
    
    # Convert 'added_at' to datetime object
    df_file['added_at'] = pd.to_datetime(df_file['added_at'])
    
    # Extract year and month for temporal analysis
    df_file['added_year'] = df_file['added_at'].dt.year
    df_file['added_month'] = df_file['added_at'].dt.month
    
    # Convert duration from milliseconds to minutes
    df_file['duration_mins'] = df_file['duration_ms'] / 60000.0

    # Drop duration_ms
    df_file = df_file.drop(columns=['duration_ms'])
    
    return df_file
