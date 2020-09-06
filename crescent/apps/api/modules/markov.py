import random
from django.forms.models import model_to_dict
from apps.api.models import Word, Markov
from apps.api.modules.general import tokenize


class ConversationModelBase:
    def learn(self, input_text):
        pass

    def generate(self, input_text=None, options=None):
        pass


class MarkovModel(ConversationModelBase):
    def __init__(self):
        self.max_generate_length = 16

    def learn(self, input_text):
        tokens = tokenize(input_text, with_category=True)
        eos, _ = Word.objects.get_or_create(id=-1, name="EOS", category=9)
        words = [self._token2word(name, category) for name, category in tokens]
        words += [eos]
        length = len(words)
        markov_patterns = [words[i : i + 3] for i in range(length - 2)]
        for prefix1, prefix2, suffix in markov_patterns:
            Markov.objects.get_or_create(
                prefix1=prefix1.id,
                prefix2=prefix2.id,
                suffix=suffix.id,
            )
        return {
            "input_words": [model_to_dict(w) for w in words[:-1]],
        }

    def generate(self, input_text=None, options=None):
        if input_text:
            descriptions = self.learn(input_text)
            keyword_id = random.choice(descriptions["input_words"])["id"]
        elif options and "keyword_id" in options:
            descriptions = []
            keyword_id = options["keyword_id"]
        else:
            return None, {}
        suggested = Markov.objects.filter(prefix1=keyword_id)
        choiced = random.choice(suggested)
        sequence = [keyword_id, choiced.prefix2, choiced.suffix]
        for _ in range(self.max_generate_length):
            suggested = Markov.objects.filter(
                prefix1=sequence[-2],
                prefix2=sequence[-1],
            )
            choiced = random.choice(suggested)
            if choiced.suffix == -1:
                break
            sequence += [choiced.suffix]
        found = Word.objects.filter(id__in=sequence)
        found = {w.id: w for w in found}
        ordered = [found[i] for i in sequence]
        output_text = "".join([w.name for w in ordered])
        descriptions["output_words"] = [model_to_dict(w) for w in ordered]
        return output_text, descriptions

    def _token2word(self, name, category):
        word, _ = Word.objects.get_or_create(
            name=name,
            category=category,
        )
        return word
