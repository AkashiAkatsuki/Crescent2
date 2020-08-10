import datetime

from django.test import TestCase
from django.utils import timezone

from .modules.general import *

class ModuleTests(TestCase):
    def test_tokenize(self):
        tokens = tokenize("テストです")
        self.assertIs(tokens[0][0] == "テスト", True)
        self.assertIs(tokens[0][1] == "名詞", True)
