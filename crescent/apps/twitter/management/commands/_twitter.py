import re
import time
from tweepy import API, OAuthHandler, Stream, StreamListener, TweepError, RateLimitError


def request_api(func, api_retry=0):
    def wrapper(*args, **kargs):
        for _ in range(api_retry + 1):
            try:
                return func(*args, **kargs)
            except TweepError:
                pass
            except RateLimitError:
                time.sleep(15 * 60)

    return wrapper


class TimelineStreamer:
    def __init__(self, oauth_dict, on_tweet=None, on_reply=None):
        auth = OAuthHandler(
            oauth_dict["api_key"],
            oauth_dict["api_secret"],
        )
        auth.set_access_token(
            oauth_dict["access_token"],
            oauth_dict["access_secret"],
        )
        self.on_tweet = on_tweet
        self.on_reply = on_reply
        self._api = API(auth)
        self._screen_name = self._get_screen_name()
        self._friend_ids = self._get_friend_ids()
        stream_listener = StreamListener()
        stream_listener.on_status = self._on_status
        self._stream = Stream(auth=self._api.auth, listener=stream_listener)

    @request_api
    def stream(self):
        self._stream.filter(follow=self._friend_ids)

    @request_api
    def search(self, text):
        result = self._api.search(text, lang="ja", count=self.SEARCH_LIMIT)
        return [status.text for status in result]

    @request_api
    def _get_screen_name(self):
        return self._api.me().screen_name

    @request_api
    def _get_friend_ids(self):
        return [str(id) for id in self._api.friends_ids()]

    @request_api
    def _tweet(self, text, target_status_id=None):
        text = re.sub("#", "", text)
        try:
            self._api.update_status(text, in_reply_to_status_id=target_status_id)
        except Exception:
            return

    def _on_status(self, status):
        if status.user.id_str not in self._friend_ids or hasattr(
            status, "retweeted_status"
        ):
            return
        text = self._clean_text(status.text)
        screen_name = status.user.screen_name
        if self.on_reply and re.search("@" + self._screen_name, status.text):
            output_text = "@" + status.author.screen_name + " "
            output_text += self.on_reply(text)
            target_status_id = status.id
        else:
            output_text = self.on_tweet(text, screen_name)
            target_status_id = None
        if output_text:
            self._tweet(output_text, target_status_id)

    def _clean_text(self, text):
        text = re.sub(r"(\s|^)@[0-9a-zA-Z_]*", "", text)
        text = re.sub(r"https?://[\w/:%#\$&\?\(\)~\.=\+\-]+", "", text)
        text = re.sub(r"#[0-9a-zA-Z_-]+", "", text)
        text = re.sub(r"\n", " ", text)
        return text
