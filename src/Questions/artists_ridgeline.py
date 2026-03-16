import pandas as pd
import altair as alt


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
                     
    # Create a complete grid of all years and top artists so streams drop to zero for empty years
    if not artist_trends.empty:
        years = range(artist_trends['added_year'].min(), artist_trends['added_year'].max() + 1)
        idx = pd.MultiIndex.from_product([years, top_artists], names=['added_year', 'artist_name'])
        grid = pd.DataFrame(index=idx).reset_index()
        artist_trends = grid.merge(artist_trends, on=['added_year', 'artist_name'], how='left').fillna({'track_count': 0})
    
    return artist_trends

def plot_artist_streamgraph(df: pd.DataFrame, top_n: int) -> alt.Chart:
    """
    Creates an interactive Streamgraph showing the evolving volume of 
    tracks saved per top artist over the years.
    """
    trend_data = prepare_artist_data(df, top_n)
    
    # Create interactive highlight selection
    highlight = alt.selection_point(
        on='mouseover', 
        fields=['artist_name'], 
        clear='mouseout'
    )
    
    # Build the Altair Streamgraph (Area chart with stack='center')
    chart = alt.Chart(trend_data).mark_area(
        interpolate='basis', # Smooth continuous curves
        line=True            # Adds a distinct line to the top of each stream layer
    ).encode(
        x=alt.X('added_year:Q', title='Year Added', scale=alt.Scale(zero=False), axis=alt.Axis(format='d', grid=True)),
        y=alt.Y('track_count:Q', stack='center', title='Volume of Tracks', axis=None),
        color=alt.Color('artist_name:N', 
                        title='Artist', 
                        scale=alt.Scale(scheme='tableau20'),
                        sort=alt.EncodingSortField(field='track_count', op='sum', order='descending')),
        opacity=alt.condition(highlight, alt.value(1.0), alt.value(0.1)),
        tooltip=[
            alt.Tooltip('artist_name:N', title='Artist'),
            alt.Tooltip('added_year:O', title='Year'),
            alt.Tooltip('track_count:Q', title='Tracks Added')
        ]
    ).add_params(
        highlight
    ).properties(
        width=900,
        height=400,
        title=f'Top {top_n} Artists Evolution (Tracks Added per Year)'
    ).interactive(
        bind_y=False # Lock vertical scrolling for clarity
    ).configure(
        background='#2b2b2b' # Matching dark theme
    ).configure_axis(
        grid=True,
        gridColor='#444444',
        domainColor='#777777',
        tickColor='#777777',
        labelColor='#dddddd',
        titleColor='#dddddd'
    ).configure_legend(
        labelColor='#dddddd',
        titleColor='#dddddd'
    ).configure_title(
        color='#dddddd',
        fontSize=16
    ).configure_view(
        stroke='transparent'
    )
    
    return chart

# Example usage in Jupyter/Quarto:
# from q1_genre_breakdown import plot_genre_sankey, plot_artist_streamgraph
# sankey_chart = plot_genre_sankey(df_exploded, top_parents_n=5, top_subs_n=7)
# sankey_chart.show()
# 
# artist_chart = plot_artist_streamgraph(df_clean, top_n=15)
# artist_chart.display()