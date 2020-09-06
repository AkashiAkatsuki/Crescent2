from django.test import TestCase

from apps.api.models import Word, Markov
from apps.api.modules.general import tokenize
from apps.api.modules.markov import MarkovModel


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
