import pandas as pd
import altair as alt

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