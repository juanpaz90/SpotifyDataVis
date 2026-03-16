import pandas as pd
import altair as alt

def get_top_genres(df_exploded: pd.DataFrame, n: int = 10) -> list:
    """
    Identifies the top 'n' most frequent genres in the exploded dataframe.
    """
    return df_exploded['genre_list'].value_counts().nlargest(n).index.tolist()

def prepare_q1_data(df_exploded: pd.DataFrame, top_genres: list) -> pd.DataFrame:
    """
    Filters the dataset for top genres and calculates the frequency 
    of each genre per year.
    """
    # Filter for only the top genres
    df_filtered = df_exploded[df_exploded['genre_list'].isin(top_genres)]
    
    # Group by year and genre to get counts
    genre_trends = (df_filtered.groupby(['added_year', 'genre_list'])
                    .size()
                    .reset_index(name='track_count'))
    
    return genre_trends

def plot_taste_evolution(df_exploded: pd.DataFrame, top_n: int = 10) -> alt.Chart:
    """
    Creates a Normalized Stacked Area Chart showing how the proportion 
    of top genres changes over the years.
    """
    # 1. Prepare data
    top_genres = get_top_genres(df_exploded, n=top_n)
    trend_data = prepare_q1_data(df_exploded, top_genres)
    
    # 2. Build Altair Chart
    chart = alt.Chart(trend_data).mark_area().encode(
        x=alt.X('added_year:O', title='Year Added', axis=alt.Axis(labelAngle=0)),
        y=alt.Y('track_count:Q', stack='normalize', title='Proportion of Tracks', axis=alt.Axis(format='%')),
        color=alt.Color('genre_list:N', title='Genre', scale=alt.Scale(scheme='tableau10')),
        tooltip=[
            alt.Tooltip('added_year:O', title='Year'),
            alt.Tooltip('genre_list:N', title='Genre'),
            alt.Tooltip('track_count:Q', title='Tracks Added')
        ]
    ).properties(
        width=700,
        height=400,
        title=f'Evolution of Top {top_n} Genres Over Time'
    ).interactive()
    
    return chart

# Example usage in Jupyter/Quarto:
# from q1_taste_evolution import plot_taste_evolution
# chart_q1 = plot_taste_evolution(df_exploded, top_n=10)
# chart_q1.display()