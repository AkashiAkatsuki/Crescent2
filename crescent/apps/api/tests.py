import datetime

from django.test import TestCase
from django.utils import timezone

from .modules.general import *
from .modules.markov import *

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
