import ast
import pandas as pd


def parse_genre_string(genre_string: str) -> list:
    """
    Safely evaluates stringified lists "['pop', 'rock']" into actual Python lists.
    Handles NaN values and malformed strings.
    """
    if pd.isna(genre_string):
        return []
    try:
        # ast.literal_eval is a safe way to evaluate strings containing Python data structures
        parsed = ast.literal_eval(genre_string)
        if isinstance(parsed, list):
            return parsed
        return []
    except (ValueError, SyntaxError):
        # Fallback if it's just a comma-separated string
        return [g.strip() for g in str(genre_string).split(',') if g.strip()]
    

def group_techno_genres(genre: str) -> str:
    """
    Groups variations of techno and tekno into a single 'techno' category.
    """
    if pd.isna(genre):
        return genre
    
    genre_lower = str(genre).lower()
    if 'techno' in genre_lower or 'tekno' in genre_lower:
        return 'techno'
    return genre


def explode_genres(df_file: pd.DataFrame) -> pd.DataFrame:
    """
    Parses the artist_genres column and explodes the dataframe so each genre 
    has its own row. Essential for accurate genre aggregations.
    """
    df_file = df_file.copy()
    
    # Apply the parsing function
    df_file['genre_list'] = df_file['artist_genres'].apply(parse_genre_string)
    
    # Explode the lists into individual rows
    df_file_exploded = df_file.explode('genre_list')
    
    # Clean up empty strings or missing genres created by the explosion
    df_file_exploded['genre_list'] = df_file_exploded['genre_list'].replace('', pd.NA)
    df_file_exploded = df_file_exploded.dropna(subset=['genre_list'])

    # Deduplicate
    # df_file_exploded = df_file_exploded.drop_duplicates(subset=['track_id', 'genre_list'])
    
    return df_file_exploded


def get_all_genres(df_file: pd.DataFrame) -> list:
    return df_file['genre_list'].value_counts().index.to_list()