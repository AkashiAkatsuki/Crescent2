import json
import os
import requests
from django.core.management.base import BaseCommand
from ._twitter import TimelineStreamer


class Command(BaseCommand):
    help = "Search unknown words with Twitter"
    MAX_SEARCH = 150  # GET search/tweets 180req/15min

    def handle(self, *args, **options):
        oauth_dict = {
            "api_key": os.environ["API_KEY"],
            "api_secret": os.environ["API_SECRET"],
            "access_token": os.environ["ACCESS_TOKEN"],
            "access_secret": os.environ["ACCESS_SECRET"],
        }
        streamer = TimelineStreamer(oauth_dict)
        response = requests.post(
            "http://localhost:8080/api/unknown-words/pop",
            json.dumps({"limit": self.MAX_SEARCH}),
        )
        data = json.loads(response.text)
        texts = [streamer.search(word["name"]) for word in data["unknown_words"]]
        texts = sum(texts, [])
        texts = [{"input_text": streamer.clean_text(text)} for text in texts]
        requests.post(
            "http://localhost:8080/api/learn",
            json.dumps({"contexts": texts}),
        )
