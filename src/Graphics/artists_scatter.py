import pandas as pd
import altair as alt
from Modules.prepare_artist_data import prepare_artist_data


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
