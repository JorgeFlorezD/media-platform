PROMPT_GENRE_SYNOPSIS = (
    "Provide a complete list of all movies and TV shows related to '{title}'. "
    "For each entry, provide the title, a detailed synopsis, and the genres. "
    "Please format the response as a JSON array, with each movie or show "
    "represented as a separate JSON object. Do not omit any related content. \n\n"
    "Only return the JSON object. \n\n"
    "Example JSON format:\n"
    "["
    "    {{"
    "        'title': 'Example Movie Title',"
    "        'synopsis': 'Example Synopsis.',"
    "        'genres': ['Genre1', 'Genre2']"
    "    }},"
    "    {{"
    "        'title': 'Another Example Movie Title',"
    "        'synopsis': 'Another Example Synopsis.',"
    "        'genres': ['GenreA', 'GenreB']"
    "    }}"
    "]"
)
