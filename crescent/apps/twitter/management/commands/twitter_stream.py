import json
import os
import random
import requests
from django.core.management.base import BaseCommand
from ._twitter import TimelineStreamer


class Command(BaseCommand):
    help = "Start listening timeline stream"

    def handle(self, *args, **options):
        self.crescent = TwitterCrescent()
        oauth_dict = {
            "api_key": os.environ["API_KEY"],
            "api_secret": os.environ["API_SECRET"],
            "access_token": os.environ["ACCESS_TOKEN"],
            "access_secret": os.environ["ACCESS_SECRET"],
        }
        streamer = TimelineStreamer(
            oauth_dict,
            on_tweet=self.crescent.on_tweet,
            on_reply=self.crescent.on_reply,
        )
        streamer.stream()


class TwitterCrescent:
    def __init__(
        self,
        interval=10,
        max_count_hotwords=300,
        max_count_members=100,
    ):
        self.max_count_hotwords = max_count_hotwords
        self.max_count_members = max_count_members
        self._hotword_ids = []
        self._members = []
        self._interval_count = 0

    def on_tweet(self, text, screen_name):
        response = requests.post(
            "http://localhost:8080/api/learn",
            json.dumps({"input_text": text}),
            headers={"Content-Type": "application/json"},
        )
        data = json.loads(response.text)
        self._store_hotwords(data["descriptions"]["input_words"])
        self._store_member(screen_name)
        self._interval_count += 1
        if self._interval_count > self._get_interval():
            self._interval_count = 0
        return self._generate()

    def on_reply(self, text):
        return self._generate(text)

    def _generate(self, input_text=None):
        data = {"options": {}}
        if input_text:
            data["input_text"] = input_text
        keyword_id = self._get_random_hotword_id()
        if keyword_id:
            data["options"]["keyword_id"] = keyword_id
        response = requests.post(
            "http://localhost:8080/api/generate",
            json.dumps(data),
            headers={"Content-Type": "application/json"},
        )
        return json.loads(response.text.encode("utf-8"))["output_text"]

    def _store_hotwords(self, words):
        word_ids = [word["id"] for word in words if word["category"] == 0]
        self._hotword_ids += word_ids
        self._hotword_ids = self._hotword_ids[-self.max_count_hotwords :]

    def _get_random_hotword_id(self):
        return random.choice(self._hotword_ids) if len(self._hotword_ids) > 0 else None

    def _store_member(self, screen_name):
        self._members += [screen_name]
        self._members = self._members[-self.max_count_members :]

    def _get_interval(self):
        return len(set(self._members))