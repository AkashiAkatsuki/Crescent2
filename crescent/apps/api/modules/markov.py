from .general import tokenize
from apps.api.models import Word, Markov

class ConversationModelBase:
    def learn(self, input_text):
        pass

    def generate(self, input_text=None):
        pass

class MarkovModel(ConversationModelBase):
    def learn(self, input_text):
        pass

    def generate(self, input_text=None, keyword=None):
        pass

    def _token2word(self, name, category):
        word, created = Word.objects.get_or_create(
            name=name,
            category=category,
        )
        return word
