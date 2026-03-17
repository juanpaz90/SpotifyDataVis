def get_distinct_color_mapping(parent_genres: list) -> dict:
    """
    Assigns a highly distinct color to each parent genre.
    """
    distinct_colors = [
        '#4e79a7', '#f28e2c', '#e15759', '#76b7b2', '#59a14f', '#edc949', 
        '#af7aa1', '#ff9da7', '#9c755f', '#bab0ab'
    ]
    mapping = {}
    for i, genre in enumerate(parent_genres):
        mapping[genre] = distinct_colors[i % len(distinct_colors)]
    return mapping
