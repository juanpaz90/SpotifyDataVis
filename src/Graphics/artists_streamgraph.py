import pandas as pd
import altair as alt
from Modules.prepare_artist_data import prepare_artist_data


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
