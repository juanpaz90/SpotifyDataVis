import pandas as pd
import plotly.graph_objects as go

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

def hex_to_rgba(hex_color: str, opacity: float = 0.5) -> str:
    """Helper to convert hex colors to rgba for semi-transparent Sankey links."""
    hex_color = hex_color.lstrip('#')
    r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    return f'rgba({r},{g},{b},{opacity})'

def prepare_sankey_data(df_exploded: pd.DataFrame, top_parents_n: int = 5, top_subs_n: int = 7):
    """
    Transforms the dataframe into Nodes and Links format required by Plotly Sankey.
    """
    df = df_exploded.copy()
    df['parent_genre'] = df['genre_list'].apply(categorize_genre)
    
    # 1. Isolate the top N Parent Genres to keep the diagram clean
    top_parents = df['parent_genre'].value_counts().nlargest(top_parents_n).index.tolist()
    df_filtered = df[df['parent_genre'].isin(top_parents)].copy()
    
    # 2. Limit to top M sub-genres per parent (group the rest into "Other [Parent]")
    final_dfs = []
    for parent in top_parents:
        parent_df = df_filtered[df_filtered['parent_genre'] == parent].copy()
        top_subs = parent_df['genre_list'].value_counts().nlargest(top_subs_n).index.tolist()
        parent_df.loc[~parent_df['genre_list'].isin(top_subs), 'genre_list'] = f'Other {parent}'
        final_dfs.append(parent_df)
        
    df_final = pd.concat(final_dfs)
    
    # 3. Create the Links (Source -> Target -> Weight)
    links_df = df_final.groupby(['parent_genre', 'genre_list']).size().reset_index(name='value')
    
    # 4. Create the Nodes (Unique list of all parents and sub-genres)
    all_nodes = list(links_df['parent_genre'].unique()) + list(links_df['genre_list'].unique())
    nodes = list(dict.fromkeys(all_nodes)) # Deduplicate preserving order
    node_indices = {node: i for i, node in enumerate(nodes)}
    
    # Map node names to their index values for Plotly
    links_df['source'] = links_df['parent_genre'].map(node_indices)
    links_df['target'] = links_df['genre_list'].map(node_indices)
    
    return nodes, links_df

def plot_genre_sankey(df_exploded: pd.DataFrame, top_parents_n: int = 5, top_subs_n: int = 7) -> go.Figure:
    """
    Generates an interactive Plotly Sankey diagram to show the flow
    from Parent Genres into specific Sub-genres.
    """
    # 1. Get nodes and links
    nodes, links_df = prepare_sankey_data(df_exploded, top_parents_n, top_subs_n)
    
    # 2. Get Colors
    parent_colors = get_distinct_color_mapping(list(links_df['parent_genre'].unique()))
    
    # Assign colors to nodes (Sub-genres inherit their parent's color)
    node_colors = []
    for node in nodes:
        if node in parent_colors:
            node_colors.append(parent_colors[node])
        else:
            # Find the parent of this sub-genre to match the color
            parent = links_df[links_df['genre_list'] == node]['parent_genre'].iloc[0]
            node_colors.append(parent_colors[parent])
            
    # Assign semi-transparent colors to links (Inherit from Source Parent)
    link_colors = [hex_to_rgba(parent_colors[row['parent_genre']]) for _, row in links_df.iterrows()]

    # 3. Build Plotly Sankey
    fig = go.Figure(data=[go.Sankey(
        node = dict(
            pad = 30,           # Increased padding for better vertical spacing
            thickness = 20,
            line = dict(color = "#111111", width = 0.5),
            label = nodes,
            color = node_colors
        ),
        link = dict(
            source = links_df['source'],
            target = links_df['target'],
            value = links_df['value'],
            color = link_colors
        )
    )])

    # 4. Apply Dark Theme Styling
    fig.update_layout(
        title_text=f"Genre Hierarchy Breakdown (Top {top_parents_n} Families)",
        title_font_size=18,
        font_size=12,
        paper_bgcolor='#2b2b2b',
        plot_bgcolor='#2b2b2b',
        font=dict(color='#dddddd'),
        width=900,
        height=800,           # Increased overall height to give nodes room to breathe
        margin=dict(l=20, r=20, t=50, b=20)
    )

    return fig

# Example usage in Jupyter/Quarto:
# from q1_genre_breakdown import plot_genre_sankey
# sankey_chart = plot_genre_sankey(df_exploded, top_parents_n=5, top_subs_n=7)
# sankey_chart.show()