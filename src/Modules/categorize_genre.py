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