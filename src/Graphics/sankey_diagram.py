import pandas as pd
import plotly.graph_objects as go
from Modules.categorize_genre import categorize_genre
from Modules.color_mapping import get_distinct_color_mapping


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
