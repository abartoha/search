import re
from fuzzywuzzy import fuzz

def search_json(data, query, selected_genres):
    results = []
    pattern = None

    # Compile regex if query is not empty
    if query.strip():
        try:
            pattern = re.compile(query, re.IGNORECASE)
        except re.error:
            return results

    for item in data:
        title = item.get("title", "")
        genres = item.get("genre", [])

        # Check regex match or fuzzy match
        if (pattern and pattern.search(title)) or (fuzz.partial_ratio(query.lower(), title.lower()) >= 70):
            if not selected_genres or all(genre in genres for genre in selected_genres):
                results.append(item)

    return results
