# from app.adapters.repositories.channel_repository import ChannelRepository
import json
import os
import re
from typing import List, Optional
from app.util.exceptions import ExternalServiceException

from bson import ObjectId
import google.generativeai as genai
from app.adapters.repositories.content_repository import ContentRepository
from app.domain.content import Content
from app.util.adapters.ai_api_settings import AIApiSettings

# PROMPT_GENRE_SYNOPSIS = (
#     "Provide a brief synopsis and genre for the following "
#     "movie or TV show: {title}. "
#     "Just return the most well-known possibility "
#     " If not found, just return 'not found' as response."
# )

# PROMPT_GENRE_SYNOPSIS = (
#     "Provide synopsis, genres and IMDb rating for the movie or tv show '{title}'. "
#     "If there are multiple possible interpretations or related movies "
#     "or tv shows, provide all of them, with clear separation between each. "
#     "Format each entrie as: \n\n"
#     "interpretation: Movie Title or Interpretation\n"
#     "synopsis: Synopsis\n"
#     "genres: Genre1, Genre2, Genre3, ...\n"
#     "rating: IMDb Rating\n\n"
#     " If not found, just return 'not found' as response."
# )

PROMPT_GENRE_SYNOPSIS = (
    "Provide a complete list of all movies and TV shows related to '{title}'. "
    "For each entry, provide the title, a detailed synopsis, and the genres. "
    "Please format the response as a JSON array, with each movie or show "
    "represented as a separate JSON object. Do not omit any related content. \n\n"
    "Example JSON format:\n"
    "["
    "    {{"
    "        'interpretation': 'Example Movie Title',"
    "        'synopsis': 'Example Synopsis.',"
    "        'genres': ['Genre1', 'Genre2']"
    "    }},"
    "    {{"
    "        'interpretation': 'Another Example Movie Title',"
    "        'synopsis': 'Another Example Synopsis.',"
    "        'genres': ['GenreA', 'GenreB']"
    "    }}"
    "]"
)


class IAApiService:    
    def __init__(
        self,
        api_key: str,
        model: str,
        # ai_api_settings: AIApiSettings
    ):
        self.api_key = api_key
        genai.configure(api_key=api_key),
        self.model = genai.GenerativeModel(model)
        
        
    def get_genre_and_synopsis(self, title: str):
        prompt = PROMPT_GENRE_SYNOPSIS.format(title=title)
        response = self.model.generate_content(prompt)
        text = response.text
        
        formatted_text = self._format_json(text)
        if formatted_text:
            result = json.loads(formatted_text)
            return result
        else:
            return []

        # return self._parse_response(text)


    def _format_json(self, text: str) -> Optional[str]:
        "format the text to be a correct json"
        if len(text) > 10:
            json_string = text[7:-3]
            return json_string
        else:
            return None

    def _parse_response(self, text: str) -> List[dict]:
        fromated_entries = []
        if "not found" in text.lower():
            return []

        try:
            entries = re.split(r'\n\n(?=interpretation:)', text.strip())        
            for entry in entries:
                entry_data = {}
                lines = entry.split('\n')

                for line in lines:
                    if line.startswith("interpretation:"):
                        entry_data["title"] = line.split("interpretation:")[1].strip()
                    elif line.startswith("synopsis:"):
                        entry_data["synopsis"] = line.split("synopsis:")[1].strip()
                    elif line.startswith("genres:"):
                        genres_str = line.split("genres:")[1].strip()
                        entry_data["genres"] = [genre.strip() for genre in genres_str.strip("[]").split(",")]
                    elif line.startswith("rating:"):
                        entry_data["rating"] = line.split("rating:")[1].strip()

                fromated_entries.append(entry_data)
        except Exception as e:
            raise ExternalServiceException(f"Cannot get the information")
        
        return fromated_entries