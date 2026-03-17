import pandas as pd
import altair as alt
from Modules.categorize_genre import categorize_genre


def get_distinct_color_mapping(parent_genres: list) -> dict:
    """
    Assigns a highly distinct color to each parent genre.
    """
    distinct_colors = [
        '#4e79a7', '#f28e2c', '#e15759', '#76b7b2', '#59a14f', '#edc949', 
        '#af7aa1', '#ff9da7', '#9c755f', '#bab0ab'
    ]
    mapping = {}
    for i, genre in enumerate(parent_genres):
        mapping[genre] = distinct_colors[i % len(distinct_colors)]
    return mapping

def prepare_radial_data(df_exploded: pd.DataFrame, top_n: int) -> pd.DataFrame:
    """
    Prepares data specifically for the Radial Bar Chart.
    Groups overall track counts per artist and identifies their main genre.
    """
    df = df_exploded.copy()
    
    # 1. Assign parent genre to all rows
    df['parent_genre'] = df['genre_list'].apply(categorize_genre)
    
    # 2. Identify the Primary parent and sub-genre per artist
    artist_genres = df.groupby('artist_name').agg(
        primary_parent=('parent_genre', lambda x: x.value_counts().index[0] if not x.empty else 'Other'),
        primary_sub=('genre_list', lambda x: x.value_counts().index[0] if not x.empty else 'Unknown')
    ).reset_index()
    
    # 3. Deduplicate tracks so we can count absolute volume correctly
    df_unique = df.drop_duplicates(subset=['track_id']).copy()
    
    # 4. Count total tracks per artist
    artist_counts = df_unique['artist_name'].value_counts().reset_index()
    artist_counts.columns = ['artist_name', 'track_count']
    
    # 5. Get the Top N artists overall
    top_artists = artist_counts.head(top_n)
    
    # 6. Merge the genre information back into our top artists
    radial_data = pd.merge(top_artists, artist_genres, on='artist_name', how='left')
    
    return radial_data

def plot_artist_radial(df_exploded: pd.DataFrame, top_n: int) -> alt.Chart:
    """
    Creates an interactive Radial Bar Chart (Polar Bar Chart) mapping 
    artist track volume to bar length (radius) and grouping by genre family.
    """
    trend_data = prepare_radial_data(df_exploded, top_n)
    
    # Get Color Mapping for the parent genres
    parent_genres = trend_data['primary_parent'].dropna().unique().tolist()
    color_map = get_distinct_color_mapping(parent_genres)
    domain = list(color_map.keys())
    range_ = list(color_map.values())
    
    # Create interactive highlight selection
    highlight = alt.selection_point(
        on='mouseover', 
        fields=['artist_name'], 
        clear='mouseout'
    )
    
    # Build Altair Radial Bar Chart using mark_arc
    chart = alt.Chart(trend_data).mark_arc(
        innerRadius=50,      # Creates the "donut hole" in the center
        stroke='#2b2b2b',    # Creates clean distinct lines between the bars
        strokeWidth=1.5
    ).encode(
        # Theta maps the nominal categories (artists) around the circle
        theta=alt.Theta('artist_name:N', sort=alt.EncodingSortField(field='track_count', op='sum', order='descending')),
        
        # Radius maps the quantitative value (track count) to the length of the slice
        radius=alt.Radius('track_count:Q', scale=alt.Scale(type='linear', zero=True, rangeMin=50, rangeMax=250)),
        
        # Color maps to the genre family
        color=alt.Color('primary_parent:N', 
                        title='Genre Family',
                        scale=alt.Scale(domain=domain, range=range_)),
                        
        opacity=alt.condition(highlight, alt.value(1.0), alt.value(0.5)),
        
        # Rich tooltip since text labels can get cluttered on dense radial charts
        tooltip=[
            alt.Tooltip('artist_name:N', title='Artist'),
            alt.Tooltip('primary_parent:N', title='Genre Family'),
            alt.Tooltip('primary_sub:N', title='Top Sub-genre'),
            alt.Tooltip('track_count:Q', title='Tracks Saved')
        ]
    ).add_params(
        highlight
    ).properties(
        width=650,
        height=650,
        title=f'Top {top_n} Artists by Absolute Track Volume'
    ).configure(
        background='#2b2b2b'
    ).configure_view(
        stroke='transparent'
    ).configure_legend(
        labelColor='#dddddd',
        titleColor='#dddddd',
        orient='right'
    ).configure_title(
        color='#dddddd',
        fontSize=18,
        anchor='middle'
    )
    
    return chart

# Example usage in Jupyter/Quarto:
# from q1_artist_radial import plot_artist_radial
# radial_chart = plot_artist_radial(df_exploded, top_n=25)
# radial_chart.display()