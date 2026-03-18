import pandas as pd
import altair as alt
from Modules.categorize_genre import categorize_genre
from Modules.color_mapping import get_distinct_color_mapping


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

def plot_overall_popularity_donut(df_clean: pd.DataFrame) -> alt.LayerChart:
    """
    Creates a Donut Chart showing the overall proportion of tracks
    in each popularity tier for the entire dataset.
    """
    tiers = [
        'Underground', 'Cult Following', 'Established Subculture', 
        'Mid-Tier', 'Commercial', 'Highly Popular', 'Mainstream'
    ]
    # Consistent color mapping from niche (purple) to mainstream (green)
    colors = ['#4a148c', '#7b1fa2', '#9c27b0', '#1e88e5', '#00acc1', '#43a047', '#1db954']
    
    # Map popularity to tiers
    bins = [-1, 10, 25, 40, 60, 75, 90, 100]
    df_copy = df_clean.copy()
    df_copy['tier'] = pd.cut(df_copy['popularity'], bins=bins, labels=tiers)
    
    # Aggregate counts
    tier_counts = df_copy['tier'].value_counts().reset_index()
    tier_counts.columns = ['tier', 'count']
    
    # Calculate percentage for tooltip
    total_tracks = tier_counts['count'].sum()
    tier_counts['percentage'] = (tier_counts['count'] / total_tracks) * 100
    
    # Build Altair Radial Bar/Donut Chart
    base = alt.Chart(tier_counts).encode(
        theta=alt.Theta('count:Q', stack=True),
        color=alt.Color('tier:N', 
                        title='Popularity Tier',
                        scale=alt.Scale(domain=tiers, range=colors),
                        legend=alt.Legend(orient='right', titleFontSize=14, labelFontSize=12))
    )
    
    # Inner Radius creates the "donut hole"
    donut = base.mark_arc(innerRadius=120, stroke='#2b2b2b', strokeWidth=2).encode(
        tooltip=[
            alt.Tooltip('tier:N', title='Tier'),
            alt.Tooltip('count:Q', title='Tracks'),
            alt.Tooltip('percentage:Q', title='Percentage (%)', format='.1f')
        ]
    )
    
    # Add text in the middle of the donut chart
    text = alt.Chart(pd.DataFrame({'text': [f'Total Tracks:\n{total_tracks}']})).mark_text(
        align='center', baseline='middle', fontSize=18, color='#dddddd', fontWeight='bold', dy=-5
    ).encode(text='text:N')

    # Apply global dark theme configurations
    chart = (donut + text).properties(
        width=550,
        height=450,
        title='Overall Dataset Popularity Breakdown'
    ).configure(
        background='#2b2b2b'
    ).configure_legend(
        labelColor='#dddddd',
        titleColor='#dddddd'
    ).configure_title(
        color='#dddddd',
        fontSize=18
    ).configure_view(
        stroke='transparent'
    )
    return chart


def plot_genre_popularity_breakdown(df_exploded: pd.DataFrame) -> alt.Chart:
    """
    Creates a Normalized Stacked Bar Chart to identify the genre 
    composition making up each popularity level.
    """
    df = df_exploded.copy()
    
    # 1. Define Tiers and map popularity
    tiers = [
        'Underground', 'Cult Following', 'Established Subculture', 
        'Mid-Tier', 'Commercial', 'Highly Popular', 'Mainstream'
    ]
    bins = [-1, 10, 25, 40, 60, 75, 90, 100]
    df['tier'] = pd.cut(df['popularity'], bins=bins, labels=tiers)
    
    # 2. Categorize parent genres
    df['parent_genre'] = df['genre_list'].apply(categorize_genre)
    
    # 3. Aggregate data: count tracks per tier per genre
    breakdown = df.groupby(['tier', 'parent_genre']).size().reset_index(name='count')
    
    # 4. Get matching genre colors
    parent_genres = breakdown['parent_genre'].dropna().unique().tolist()
    color_map = get_distinct_color_mapping(parent_genres)
    domain = list(color_map.keys())
    range_ = list(color_map.values())
    
    # 5. Build Altair Normalized Stacked Bar Chart
    chart = alt.Chart(breakdown).mark_bar().encode(
        x=alt.X('tier:N', title='Popularity Tier', sort=tiers, axis=alt.Axis(labelAngle=-25)),
        # stack='normalize' scales the bars to 100% to show relative composition perfectly
        y=alt.Y('count:Q', stack='normalize', title='Proportion of Genres', axis=alt.Axis(format='%')),
        color=alt.Color('parent_genre:N', 
                        title='Genre Family',
                        scale=alt.Scale(domain=domain, range=range_)),
        tooltip=[
            alt.Tooltip('tier:N', title='Tier'),
            alt.Tooltip('parent_genre:N', title='Genre Family'),
            alt.Tooltip('count:Q', title='Tracks')
        ]
    ).properties(
        width=700,
        height=450,
        title='Genre Composition by Popularity Level'
    ).configure(
        background='#2b2b2b'
    ).configure_axis(
        grid=False,
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
    
    return chart

# Example usage in Jupyter/Quarto:
# from q2_popularity_bias import plot_popularity_bias, plot_overall_popularity_donut
# chart_q2_timeline = plot_popularity_bias(df_clean)
# chart_q2_overall = plot_overall_popularity_donut(df_clean)