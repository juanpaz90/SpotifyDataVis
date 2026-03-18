import pandas as pd
import altair as alt

def plot_popularity_bias(df_clean: pd.DataFrame) -> alt.LayerChart:
    """
    Creates a single graphic using Stacked Density Estimates to depict 
    the distribution of track popularity (Mainstream vs. Niche) over time.
    """
    # 1. Background Reference Bands (To define Mainstream vs Niche)
    tiers = [
        'Underground', 'Cult Following', 'Established Subculture', 
        'Mid-Tier', 'Commercial', 'Highly Popular', 'Mainstream'
    ]
    
    bands_data = pd.DataFrame({
        'start': [0, 10, 25, 40, 60, 75, 90],
        'end': [10, 25, 40, 60, 75, 90, 100],
        'midpoint': [5, 17.5, 32.5, 50, 67.5, 82.5, 95], # For centering text
        'tier': tiers,
        # Alternating subtle background colors for the dark theme
        'color': ['#222222', '#2a2a2a', '#222222', '#2a2a2a', '#222222', '#2a2a2a', '#222222'] 
    })
    
    # Create the rectangular background bands
    bands = alt.Chart(bands_data).mark_rect().encode(
        x='start:Q',
        x2='end:Q',
        color=alt.Color('color:N', scale=None, legend=None)
    )
    
    # Add text labels explicitly pinned to the top of the chart with bold, white text
    labels = alt.Chart(bands_data).mark_text(
        align='center', 
        baseline='top', 
        color='#ffffff',      # High contrast white
        fontSize=11, 
        fontWeight='bold',    # Made the text bold
        angle=0
    ).encode(
        x=alt.X('midpoint:Q', title='Spotify Popularity Score (0-100)', scale=alt.Scale(domain=[0, 100])),
        y=alt.value(15),      # Pins the text exactly 15 pixels from the top edge
        text='tier:N'
    )

    # 2. Stacked Density Estimate Chart
    # We calculate the density of 'popularity' grouped by 'added_year'
    # Then we multiply it by 100 so the tooltip displays a more readable number
    density = alt.Chart(df_clean).transform_density(
        density='popularity',
        as_=['popularity', 'density'],
        groupby=['added_year']
    ).transform_calculate(
        density_scaled='datum.density * 100'
    ).mark_area(opacity=0.85).encode(
        # Lock the X-axis strictly to 0-100
        x=alt.X('popularity:Q', scale=alt.Scale(domain=[0, 100])),
        # stack='zero' stacks the densities on top of each other
        y=alt.Y('density:Q', stack='zero', title='Density (Volume of Tracks)', axis=alt.Axis(labels=False, ticks=False)),
        # Color by year to see how tastes evolved, explicitly formatting the legend with Ordinal scale for chronological order
        color=alt.Color(
            'added_year:O', 
            title='Year Added', 
            scale=alt.Scale(scheme='plasma'), 
            legend=alt.Legend(
                orient='right', 
                titleFontSize=14, 
                labelFontSize=12,
                symbolType='square'
            )
        ),
        tooltip=[
            alt.Tooltip('added_year:O', title='Year Added'),
            alt.Tooltip('popularity:Q', title='Popularity Score', format='.1f'),
            alt.Tooltip('density_scaled:Q', title='Density', format='.2f')
        ]
    ).interactive(bind_x=False) # Allows vertical scrolling but locks the 0-100 X-axis

    # 3. Combine and apply global dark theme configurations
    # We resolve the color scale independently so the background bands don't hide the density legend
    layered_chart = (bands + labels + density).resolve_scale(
        color='independent' 
    ).properties(
        width=800,
        height=400,
        title='Popularity Bias: Stacked Density Estimates (Mainstream vs. Niche)'
    ).configure(
        background='#2b2b2b'
    ).configure_axis(
        grid=False, # Turn off grid so the background bands show cleanly
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
    
    return layered_chart

# Example usage in Jupyter/Quarto:
# from q2_popularity_bias import plot_popularity_bias
# chart_q2 = plot_popularity_bias(df_clean)
# chart_q2.display()