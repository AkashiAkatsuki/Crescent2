import datetime

from django.test import TestCase
from django.utils import timezone

from .modules.general import *

class ModuleTests(TestCase):
    def test_tokenize(self):
        tokens = tokenize("テストです", with_category=True)
        self.assertIs(tokens[0][0] == "テスト", True)
        self.assertIs(tokens[0][1] == 0, True)
