import pandas as pd
import altair as alt


def prepare_artist_data(df: pd.DataFrame, top_n: int) -> pd.DataFrame:
    """
    Prepares data for the top artists by grouping track counts per year.
    To avoid overcounting if an exploded dataframe is accidentally passed, 
    we ensure each track is only counted once.
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

def plot_artist_scatter(df: pd.DataFrame, top_n: int) -> alt.LayerChart:
    """
    Creates an interactive Bubble Chart (Scatter Plot) with connecting lines,
    showing the volume of tracks saved per top artist over the years. 
    """
    trend_data = prepare_artist_data(df, top_n)
    
    # Create interactive highlight selection
    highlight = alt.selection_point(
        on='mouseover', 
        fields=['artist_name'], 
        clear='mouseout'
    )
    
    # Base encoding shared by both lines and circles
    base = alt.Chart(trend_data).encode(
        # Use Quantitative for X-axis to allow horizontal zooming/panning
        # scale=alt.Scale(zero=False) ensures the timeline starts from the lowest year, not year 0.
        x=alt.X('added_year:Q', title='Year Added', scale=alt.Scale(zero=False), axis=alt.Axis(format='d', grid=True)),
        # Sort artists so the most popular overall are at the top of the Y-axis
        y=alt.Y('artist_name:N', title='Artist', sort=alt.EncodingSortField(field='track_count', op='sum', order='descending')),
        color=alt.Color('artist_name:N', legend=None, scale=alt.Scale(scheme='tableau20'))
    )
    
    # Add connecting lines to show the trajectory over time
    lines = base.mark_line(strokeWidth=2).encode(
        opacity=alt.condition(highlight, alt.value(0.8), alt.value(0.1))
    )
    
    # Build Altair Scatter / Bubble Chart
    bubbles = base.mark_circle().encode(
        # Bubble size represents the number of tracks saved that year
        size=alt.Size('track_count:Q', title='Tracks Added', scale=alt.Scale(range=[50, 1500]), legend=alt.Legend(clipHeight=30)),
        opacity=alt.condition(highlight, alt.value(1.0), alt.value(0.2)),
        tooltip=[
            alt.Tooltip('artist_name:N', title='Artist'),
            alt.Tooltip('added_year:O', title='Year'), # Keep nominal in tooltip so commas don't appear
            alt.Tooltip('track_count:Q', title='Tracks Added')
        ]
    ).add_params(
        highlight
    )
    
    # Layer the lines behind the bubbles
    chart = (lines + bubbles).properties(
        width=800,
        height=400,
        title=f'Top {top_n} Artists Evolution (Tracks Added per Year)'
    ).interactive(
        bind_y=False # Lock vertical scrolling for clarity
    ).configure(
        background='#2b2b2b'
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
# from q1_genre_breakdown import plot_genre_sankey, plot_artist_scatter
# sankey_chart = plot_genre_sankey(df_exploded, top_parents_n=5, top_subs_n=7)
# sankey_chart.show()
# 
# artist_chart = plot_artist_scatter(df_clean, top_n=15)
# artist_chart.display()