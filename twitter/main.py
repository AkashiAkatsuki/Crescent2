import fire
import json
import requests
from twitter_crescent.timeline_streamer import TimelineStreamer
from twitter_crescent.twitter_crescent import TwitterCrescent


def start():
    crescent = TwitterCrescent()
    streamer = TimelineStreamer(
        on_tweet=crescent.on_tweet,
        on_reply=crescent.on_reply,
    )
    streamer.stream()


def search():
    streamer = TimelineStreamer()
    response = requests.post(
        "http://crescent:8080/api/unknown-words/pop",
        json.dumps({"limit": 10}),
    )
    data = json.loads(response.text)
    texts = [streamer.search(word["name"]) for word in data["unknown_words"]]
    texts = sum(texts, [])
    texts = [{"input_text": streamer.clean_text(text)} for text in texts]
    requests.post(
        "http://crescent:8080/api/learn",
        json.dumps({"contexts": texts}),
    )


if __name__ == "__main__":
    fire.Fire(
        {
            "start": start,
            "search": search,
        }
    )
