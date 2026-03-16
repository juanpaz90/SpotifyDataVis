import pandas as pd
import altair as alt

def get_all_genres(df_exploded: pd.DataFrame) -> list:
    """
    Extracts a list of all unique genres present in the dataset.
    """
    return df_exploded['genre_list'].dropna().unique().tolist()

def categorize_genre(genre: str) -> str:
    """
    Categorizes a specific sub-genre into one of 10 broader musical parent 
    categories based on a detailed music taxonomy.
    """
    genre = str(genre).lower()
    
    # 1. Electronic & Dance Music
    if genre in ['techno', 'melodic techno', 'acid techno', 'hard techno', 'minimal techno', 'tekno', 'hardcore techno', 'frenchcore', 'gabber', 'speedcore', 'hardstyle', 'happy hardcore', 'house', 'deep house', 'tech house', 'melodic house', 'progressive house', 'french house', 'hard house', 'disco house', 'future house', 'electro house', 'tropical house', 'funky house', 'lo-fi house', 'organic house', 'afro house', 'afro tech', 'g-house', 'bass house', 'slap house', 'tribal house', 'chicago house', 'latin house', 'jazz house', 'trance', 'progressive trance', 'psytrance', 'dubstep', 'uk garage', 'drum and bass', 'liquid funk', 'future bass', 'melodic bass', 'breakbeat', 'drumstep', 'jungle', 'bassline', 'bass music', 'riddim', 'uk funky', 'footwork', 'baltimore club', 'edm', 'big room', 'electronica', 'electro', 'electroclash', 'eurodance', 'italo dance', 'italo disco', 'nu disco', 'post-disco', 'hypertechno', 'melbourne bounce', 'bounce', 'brazilian bass', 'moombahton', 'glitch', 'rally house', 'hi-nrg', 'electro swing', 'techengue', 'cedm', 'gqom', '3 step', 'ballroom vogue', 'edm trap']:
        return 'Electronic & Dance Music'
    
    # 2. Rock, Punk & Heavy Metal
    if genre in ['rock', 'classic rock', 'rock and roll', 'hard rock', 'soft rock', 'blues rock', 'garage rock', 'surf rock', 'glam rock', 'progressive rock', 'acid rock', 'art rock', 'aor', 'rockabilly', 'yacht rock', 'punk', 'pop punk', 'skate punk', 'hardcore punk', 'post-hardcore', 'melodic hardcore', 'screamo', 'proto-punk', 'queercore', 'riot grrrl', 'folk punk', 'ska punk', 'metal', 'nu metal', 'alternative metal', 'glam metal', 'symphonic metal', 'gothic metal', 'metalcore', 'mathcore', 'alternative rock', 'indie rock', 'emo', 'grunge', 'post-grunge', 'noise rock', 'math rock', 'stoner rock', 'industrial rock', 'funk rock', 'rap rock', 'post-punk', 'gothic rock', 'deathrock', 'cold wave', 'latin rock', 'rock en español', 'argentine rock', 'mexican rock', 'j-rock', 'finnish rock', 'ska', 'reggae rock']:
        return 'Rock, Punk & Heavy Metal'

    # 3. Pop & Vocal
    if genre in ['pop', 'art pop', 'soft pop', 'acoustic pop', 'electropop', 'synthpop', 'bubblegum pop', 'pop soul', 'baroque pop', 'indie pop', 'bedroom pop', 'dream pop', 'french indie pop', 'german indie pop', 'jangle pop', 'europop', 'k-pop', 'j-pop', 'swedish pop', 'french pop', 'german pop', 'norwegian pop', 'dansk pop', 'malaysian pop', 'malay', 'pop québécoise', 'pop urbaine', 'variété française', 'chanson', 'schlager', 'dansktop', 'nederpop', 'anime', 'k-ballad', 'singer-songwriter']:
        return 'Pop & Vocal'

    # 4. Hip Hop, Rap & Trap
    if genre in ['hip hop', 'rap', 'old school hip hop', 'boom bap', 'east coast hip hop', 'west coast hip hop', 'southern hip hop', 'alternative hip hop', 'experimental hip hop', 'jazz rap', 'g-funk', 'drill', 'uk drill', 'grime', 'uk grime', 'phonk', 'drift phonk', 'crunk', 'cloud rap', 'lo-fi hip hop', 'emo rap', 'rap metal', 'christian hip hop', 'trip hop', 'french rap', 'german hip hop', 'turkish hip hop', 'chinese hip hop', 'portuguese hip hop']:
        return 'Hip Hop, Rap & Trap'

    # 5. R&B, Soul, Funk & Disco
    if genre in ['r&b', 'soul', 'classic soul', 'neo soul', 'retro soul', 'northern soul', 'philly soul', 'uk r&b', 'alternative r&b', 'french r&b', 'gospel r&b', 'indie r&b', 'indie soul', 'quiet storm', 'motown', 'funk', 'disco', 'jazz funk', 'acid jazz']:
        return 'R&B, Soul, Funk & Disco'

    # 6. Indie, Alternative & Experimental
    if genre in ['indie', 'indie dance', 'alternative dance', 'indie electronic', 'new rave', 'chillwave', 'synthwave', 'hyperpop', 'german indie', 'latin indie', 'mexican indie', 'chinese indie', 'experimental', 'idm', 'downtempo', 'shoegaze', 'slowcore', 'minimalism', 'ebm', 'darkwave', 'neue deutsche welle', 'visual kei', 'witch house', 'vaporwave', 'madchester', 'free jazz']:
        return 'Indie, Alternative & Experimental'

    # 7. Latin, Caribbean & Global Rhythms
    if genre in ['dancehall', 'reggae', 'roots reggae', 'reggaeton', 'ragga', 'soca', 'latin', 'latin alternative', 'latin folk', 'tango', 'folklore argentino', 'flamenco', 'trova', 'nueva trova', 'candombe', 'neoperreo', 'latin hip hop', 'afrobeats', 'azonto', 'hiplife', 'nova mpb']:
        return 'Latin, Caribbean & Global Rhythms'

    # 8. Jazz & Blues
    if genre in ['smooth jazz', 'nu jazz', 'jazz beats', 'blues', 'modern blues', 'jazz blues']:
        return 'Jazz & Blues'

    # 9. Folk, Country & Acoustic Roots
    if genre in ['folk', 'folk rock', 'indie folk', 'celtic', 'folk pop', 'country', 'pop country', 'acoustic country', 'jam band']:
        return 'Folk, Country & Acoustic Roots'

    # 10. Classical, Cinematic & Ambient
    if genre in ['ambient', 'dark ambient', 'lo-fi', 'lo-fi beats', 'classical', 'neoclassical', 'orchestral', 'chamber music', 'opera', 'soundtrack', 'christmas']:
        return 'Classical, Cinematic & Ambient'

    # --- FALLBACK KEYWORD MATCHING ---
    # Catches unlisted micro-genres based on prominent root words
    if any(k in genre for k in ['techno', 'house', 'edm', 'dance', 'trance', 'dubstep', 'garage']): return 'Electronic & Dance Music'
    if any(k in genre for k in ['rock', 'punk', 'metal', 'core']): return 'Rock, Punk & Heavy Metal'
    if 'pop' in genre: return 'Pop & Vocal'
    if any(k in genre for k in ['hip hop', 'rap', 'trap']): return 'Hip Hop, Rap & Trap'
    if any(k in genre for k in ['r&b', 'soul', 'funk', 'disco']): return 'R&B, Soul, Funk & Disco'
    if any(k in genre for k in ['indie', 'alternative']): return 'Indie, Alternative & Experimental'
    if any(k in genre for k in ['latin', 'reggaeton', 'afro']): return 'Latin, Caribbean & Global Rhythms'
    if any(k in genre for k in ['jazz', 'blues']): return 'Jazz & Blues'
    if any(k in genre for k in ['folk', 'country', 'acoustic']): return 'Folk, Country & Acoustic Roots'
    if any(k in genre for k in ['ambient', 'classical', 'orchestral']): return 'Classical, Cinematic & Ambient'
    
    return 'Other'

def get_distinct_color_mapping(parent_genres: list) -> dict:
    """
    Assigns a highly distinct color to each parent genre.
    Uses a curated list of vibrant colors that stand out on a dark background.
    """
    distinct_colors = [
        '#4e79a7', '#f28e2c', '#e15759', '#76b7b2', '#59a14f', '#edc949', 
        '#af7aa1', '#ff9da7', '#9c755f', '#bab0ab'
    ]
    
    mapping = {}
    for i, genre in enumerate(parent_genres):
        mapping[genre] = distinct_colors[i % len(distinct_colors)]
        
    return mapping

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

# Example usage in Jupyter/Quarto:
# from q1_taste_evolution import plot_taste_evolution
# chart_q1 = plot_taste_evolution(df_exploded, top_parents_n=6)
# chart_q1.display()