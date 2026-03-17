import pandas as pd
import altair as alt
from Modules.categorize_genre import categorize_genre
from Modules.color_mapping import get_distinct_color_mapping


def prepare_hierarchy_data(df_exploded: pd.DataFrame) -> pd.DataFrame:
    """
    Groups data by Parent Genre AND Sub Genre to get the complete hierarchical counts.
    """
    df = df_exploded.copy()
    df['parent_genre'] = df['genre_list'].apply(categorize_genre)
    
    # Get total tracks per parent AND sub-genre
    hierarchy_data = (df.groupby(['parent_genre', 'genre_list'])
                      .size()
                      .reset_index(name='track_count'))
    
    return hierarchy_data

def plot_genre_hierarchy(df_exploded: pd.DataFrame, top_n_parents: int = 12) -> alt.VConcatChart:
    """
    Creates an interactive dashboard. Clicking a parent genre on the left 
    filters the sub-genres on the right.
    """
    # 1. Prepare the data
    source_data = prepare_hierarchy_data(df_exploded)

    top_parents = (source_data.groupby('parent_genre')['track_count']
                   .sum()
                   .nlargest(top_n_parents)
                   .index)
    source_data = source_data[source_data['parent_genre'].isin(top_parents)]
    
    # 2. Extract colors
    parent_genres = source_data['parent_genre'].unique()
    color_map = get_distinct_color_mapping(parent_genres)
    domain = list(color_map.keys())
    range_ = list(color_map.values())
    
    # 3. Create the interactive selection (Click on Parent Genre)
    # We set an initial state so the right chart isn't empty on load!
    click = alt.selection_point(
        fields=['parent_genre'], 
        value=[{'parent_genre': 'Electronic & Dance Music'}], # Default selection
        empty='all'
    )
    
    # 4. Create the Parent Genres Chart (Left side)
    parent_chart = alt.Chart(source_data).mark_bar(cornerRadiusEnd=4).encode(
        y=alt.Y('parent_genre:N', sort='-x', title='', axis=alt.Axis(labelLimit=250)),
        x=alt.X('sum(track_count):Q', title='Total Tracks Saved'),
        color=alt.Color('parent_genre:N', scale=alt.Scale(domain=domain, range=range_), legend=None),
        opacity=alt.condition(click, alt.value(1.0), alt.value(0.3)), # Dim unselected parents
        tooltip=[alt.Tooltip('parent_genre:N', title='Category'), alt.Tooltip('sum(track_count):Q', title='Total Tracks')]
    ).add_params(
        click
    ).properties(
        width=300,
        height=400,
        title='1. Select a Parent Genre'
    )

    # 5. Create the Sub-genres Chart (Right side)
    sub_chart = alt.Chart(source_data).mark_bar(cornerRadiusEnd=4).encode(
        y=alt.Y('genre_list:N', sort='-x', title='', axis=alt.Axis(labelLimit=250)),
        x=alt.X('track_count:Q', title='Tracks Saved'),
        color=alt.Color('parent_genre:N', scale=alt.Scale(domain=domain, range=range_), legend=None),
        tooltip=[alt.Tooltip('genre_list:N', title='Sub-genre'), alt.Tooltip('track_count:Q', title='Tracks')]
    ).transform_filter(
        click # Filter data based on what was clicked in the first chart
    ).transform_window(
        rank='rank(track_count)',
        sort=[alt.SortField('track_count', order='descending')]
    ).transform_filter(
        alt.datum.rank <= 12 # Keep it clean: only show the top 10 sub-genres for the selected parent
    ).properties(
        width=350,
        height=400,
        title='2. Top 15 Sub-genres Breakdown'
    )

    # 6. Combine side-by-side and apply dark theme
    dashboard = (parent_chart | sub_chart).resolve_scale(
        y='independent' # Ensure the Y-axes don't try to share labels!
    ).configure(
        background='#2b2b2b'
    ).configure_axis(
        grid=True,
        gridColor='#444444',
        domainColor='#777777',
        tickColor='#777777',
        labelColor='#dddddd',
        titleColor='#dddddd'
    ).configure_title(
        color='#ffffff',
        fontSize=14,
        anchor='start'
    ).configure_view(
        stroke='transparent'
    )

    return dashboard
