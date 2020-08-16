from .general import tokenize
from apps.api.models import Word, Markov

class ConversationModelBase:
    def learn(self, input_text):
        pass

    def generate(self, input_text=None):
        pass

class MarkovModel(ConversationModelBase):
    def learn(self, input_text):
        tokens = tokenize(input_text, with_category=True)
        eos, _ = Word.objects.get_or_create(id=-1, name="EOS", category=9)
        words = [self._token2word(name, category) for name, category in tokens]
        words += [eos]
        length = len(words)
        markov_patterns = [words[i:i+3] for i in range(length-2)]
        for prefix1, prefix2, suffix in markov_patterns:
            Markov.objects.get_or_create(
                prefix1=prefix1.id,
                prefix2=prefix2.id,
                suffix=suffix.id,
            )
        return words[:-1]

    def generate(self, input_text=None, keyword=None):
        pass

    def _token2word(self, name, category):
        word, created = Word.objects.get_or_create(
            name=name,
            category=category,
        )
        return word
