import json
from django.test import TestCase
from apps.api.models import Word, Markov, UnknownWord
from apps.api.modules.general import tokenize
from apps.api.modules.markov import MarkovModel


def post_api(url, request_dict={}):
    def wrapper(func):
        def inner(test_case):
            response = test_case.client.post(
                url, data=request_dict, content_type="application/json"
            )
            response_dict = json.loads(response.content)
            return func(test_case, response, response_dict)

        return inner

    return wrapper


class ApiTests(TestCase):
    def setUp(self):
        self.word_unknown = Word.objects.create(name="Unknown", category=0)
        UnknownWord.objects.create(word_id=self.word_unknown.id)

    @post_api("/api/unknown-words/pop", {"limit": 10})
    def test_unknown_words_pop(self, response, json_dict):
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_dict["unknown_words"][0]["name"], self.word_unknown.name)


class ModuleTests(TestCase):
    def test_tokenize(self):
        tokens = tokenize("テストです", with_category=True)
        self.assertIs(tokens[0][0] == "テスト", True)
        self.assertIs(tokens[0][1] == 0, True)


class MarkovTest(TestCase):
    def setUp(self):
        self.markov_model = MarkovModel()
        self.known_name = "Known"
        self.unknown_name = "Unknown"
        self.known_word = Word.objects.create(name="Known", category=0)

    def test_token2word_known(self):
        word = self.markov_model._token2word(self.known_name, 0)
        self.assertEqual(word, self.known_word)

    def test_token2word_unknown(self):
        word = self.markov_model._token2word(self.unknown_name, 0)
        self.assertEqual(word, Word.objects.last())
        self.assertEqual(1, UnknownWord.objects.count(word_id=word.id))

    def test_learn(self):
        descriptions = self.markov_model.learn("これは学習のテストです")
        words = descriptions["input_words"]
        self.assertEqual(words[0]["name"], "これ")

        last_markov = Markov.objects.last()
        learned = [last_markov.prefix1, last_markov.prefix2, last_markov.suffix]
        expected = [words[-2]["id"], words[-1]["id"], -1]
        self.assertListEqual(learned, expected)

    def test_generate(self):
        self.markov_model.learn("これは学習のテストです")
        output_text, descriptions = self.markov_model.generate("これ")
        words = descriptions["output_words"]
        self.assertEqual(output_text, "これは学習のテストです")
        self.assertEqual(words[0]["name"], "これ")
