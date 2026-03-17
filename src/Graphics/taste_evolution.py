import pandas as pd
import altair as alt
from Modules.categorize_genre import categorize_genre
from Modules.color_mapping import get_distinct_color_mapping


def get_top_parent_categories(df_exploded: pd.DataFrame, n: int = 5) -> list:
    """
    Step 1 & 2: Get all genres, group them by parent category, 
    and identify the top 'n' parent categories overall.
    """
    parent_series = df_exploded['genre_list'].apply(categorize_genre)
    return parent_series.value_counts().nlargest(n).index.tolist()

def prepare_q1_data(df_exploded: pd.DataFrame, top_parents: list) -> pd.DataFrame:
    """
    Step 3: Filters data for the top parent categories and aggregates counts
    by Year-Month and parent level. Also extracts the top sub-genres for tooltips.
    """
    df = df_exploded.copy()
    
    # Ensure added_at is a datetime object, then floor it to the start of the month
    df['added_at'] = pd.to_datetime(df['added_at'])
    df['added_year_month'] = df['added_at'].dt.to_period('M').dt.to_timestamp()
    
    # Apply groups to all rows
    df['parent_genre'] = df['genre_list'].apply(categorize_genre)
    
    # Filter for only the top parent genres
    df_filtered = df[df['parent_genre'].isin(top_parents)].copy()
    
    # Group by YEAR-MONTH and parent_genre to get total track count
    genre_trends = (df_filtered.groupby(['added_year_month', 'parent_genre'])
                    .size()
                    .reset_index(name='track_count'))
                    
    # Get the top 3 sub-genres for each parent group in that month to show in the tooltip
    top_subs = (df_filtered.groupby(['added_year_month', 'parent_genre'])['genre_list']
                .apply(lambda x: ', '.join(x.value_counts().head(3).index))
                .reset_index(name='top_sub_genres'))
                
    # Merge the sub-genres into our trends dataframe
    genre_trends = pd.merge(genre_trends, top_subs, on=['added_year_month', 'parent_genre'])
    
    return genre_trends

def plot_taste_evolution(df_exploded: pd.DataFrame, top_parents_n: int) -> alt.Chart:
    """
    Creates an interactive Streamgraph showing how the volume of Parent 
    Genre Families changes over the years and months smoothly.
    """
    # 1. Prepare data (Aggregated by Parent Genre and Year-Month)
    top_parents = get_top_parent_categories(df_exploded, n=top_parents_n)
    trend_data = prepare_q1_data(df_exploded, top_parents)
    
    # 2. Generate Color Mapping for the parent genres
    display_genres = trend_data['parent_genre'].unique().tolist()
    color_map = get_distinct_color_mapping(display_genres)
    domain = list(color_map.keys())
    range_ = list(color_map.values())
    
    # 3. Create interactive highlight selection
    highlight = alt.selection_point(
        on='mouseover', 
        fields=['parent_genre'], 
        clear='mouseout'
    )
    
    # 4. Build Altair Streamgraph
    chart = alt.Chart(trend_data).mark_area(
        interpolate='basis', 
        line=True
    ).encode(
        # Changed to :T (Temporal) for intelligent date scaling.
        # It handles months/years zooming automatically without overlap!
        x=alt.X('added_year_month:T', title='Time Added', axis=alt.Axis(grid=True)),
        y=alt.Y('track_count:Q', stack='center', title='Volume of Tracks', axis=None),
        color=alt.Color('parent_genre:N', 
                        title='Genre Family', 
                        scale=alt.Scale(domain=domain, range=range_),
                        sort=domain),
        opacity=alt.condition(highlight, alt.value(1), alt.value(0.1)),
        tooltip=[
            # Format tooltip to show Month and Year nicely (e.g., "March 2022")
            alt.Tooltip('added_year_month:T', title='Date', format='%B %Y'),
            alt.Tooltip('parent_genre:N', title='Category'),
            alt.Tooltip('top_sub_genres:N', title='Top Sub-genres'),
            alt.Tooltip('track_count:Q', title='Tracks Added')
        ]
    ).add_params(
        highlight
    ).properties(
        width=750,
        height=450,
        title=f'Evolution of Top {top_parents_n} Genre Families Over Time'
    ).interactive(
        bind_y=False # Restrict interactive panning/zooming to the horizontal axis only
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
        color='#dddddd'
    ).configure_view(
        stroke='transparent'
    )
    
    return chart
