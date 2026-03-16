import pandas as pd
import altair as alt

def categorize_genre(genre: str) -> str:
    """
    Categorizes a specific sub-genre into one of 10 broader musical parent categories.
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
    distinct_colors = [
        '#4e79a7', '#f28e2c', '#e15759', '#76b7b2', '#59a14f', '#edc949', 
        '#af7aa1', '#ff9da7', '#9c755f', '#bab0ab'
    ]
    mapping = {}
    for i, genre in enumerate(parent_genres):
        mapping[genre] = distinct_colors[i % len(distinct_colors)]
    return mapping

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

def plot_genre_hierarchy(df_exploded: pd.DataFrame) -> alt.VConcatChart:
    """
    Creates an interactive dashboard. Clicking a parent genre on the left 
    filters the sub-genres on the right.
    """
    # 1. Prepare the data
    source_data = prepare_hierarchy_data(df_exploded)
    
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
    # Uses a window transform to ensure we only show the top 15 sub-genres for the selected parent
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
        alt.datum.rank <= 15 # Keep it clean: only show the top 15 sub-genres for the selected parent
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

# Example usage:
# from q1_genre_breakdown import plot_genre_hierarchy
# breakdown_chart = plot_genre_hierarchy(df_exploded)
# breakdown_chart.display()