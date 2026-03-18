import pandas as pd
import altair as alt
from Modules.color_mapping import get_distinct_color_mapping
from Modules.categorize_genre import categorize_genre

# Disable Altair's default 5000 row limit to allow plotting large datasets
alt.data_transformers.disable_max_rows()

def plot_duration_vs_popularity(df_clean: pd.DataFrame) -> alt.Chart:
    """
    Creates a scatter plot comparing duration (mins) and popularity,
    including a regression line to spot trends.
    """
    # Base scatter plot without interactive yet
    base = alt.Chart(df_clean).encode(
        x=alt.X('duration_mins:Q', title='Track Duration (Minutes)'),
        y=alt.Y('popularity:Q', title='Popularity Score')
    )

    scatter = base.mark_circle(size=40, opacity=0.4).encode(
        color=alt.Color('explicit:N', 
                        title='Explicit', 
                        scale=alt.Scale(domain=[True, False], range=['#E91E63', '#1DB954'])),
        tooltip=['track_name', 'artist_name', 'duration_mins', 'popularity']
    ).interactive() # Apply interactive ONLY to the scatter points

    # Add a linear regression trendline derived from base chart
    trendline = base.transform_regression(
        'duration_mins', 'popularity'
    ).mark_line(color='red', strokeWidth=3)

    return (scatter + trendline).properties(
        width=700,
        height=400,
        title='Track Duration vs. Popularity'
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
        fontSize=18
    ).configure_view(
        stroke='transparent'
    )

def plot_genre_duration_vs_popularity(df_exploded: pd.DataFrame, top_n: int = 100) -> alt.Chart:
    """
    Creates an aggregated bubble chart showing the average duration vs. average 
    popularity of the Top N genres, colored by their parent genre family.
    """
    # 1. Isolate the top N genres to prevent chart clutter
    top_genres = df_exploded['genre_list'].value_counts().nlargest(top_n).index.tolist()
    df_filtered = df_exploded[df_exploded['genre_list'].isin(top_genres)].copy()
    
    # 2. Aggregate metrics by genre
    genre_stats = df_filtered.groupby('genre_list').agg(
        avg_duration=('duration_mins', 'mean'),
        avg_popularity=('popularity', 'mean'),
        track_count=('track_id', 'nunique') # Use nunique to avoid any accidental duplication
    ).reset_index()
    
    # 3. Add parent genres for color grouping
    genre_stats['parent_genre'] = genre_stats['genre_list'].apply(categorize_genre)
    
    # 4. Generate color mapping
    parent_genres = genre_stats['parent_genre'].unique().tolist()
    color_map = get_distinct_color_mapping(parent_genres)
    domain = list(color_map.keys())
    range_ = list(color_map.values())
    
    # 5. Build the Bubble Chart
    bubbles = alt.Chart(genre_stats).mark_circle(opacity=0.8, stroke='#2b2b2b', strokeWidth=1).encode(
        x=alt.X('avg_duration:Q', title='Average Duration (Minutes)', scale=alt.Scale(zero=False)),
        y=alt.Y('avg_popularity:Q', title='Average Popularity Score', scale=alt.Scale(zero=False)),
        size=alt.Size('track_count:Q', title='Track Count', scale=alt.Scale(range=[50, 1500])),
        color=alt.Color('parent_genre:N', 
                        title='Genre Family',
                        scale=alt.Scale(domain=domain, range=range_)),
        tooltip=[
            alt.Tooltip('genre_list:N', title='Genre'),
            alt.Tooltip('parent_genre:N', title='Family'),
            alt.Tooltip('avg_duration:Q', title='Avg Duration (mins)', format='.2f'),
            alt.Tooltip('avg_popularity:Q', title='Avg Popularity', format='.1f'),
            alt.Tooltip('track_count:Q', title='Total Tracks')
        ]
    ).properties(
        width=700,
        height=450,
        title=f'Genre Popularity vs. Average Track Duration)'
    ).interactive().configure(
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
        fontSize=18
    ).configure_view(
        stroke='transparent'
    )
    
    return bubbles