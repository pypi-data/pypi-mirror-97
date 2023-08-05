import json
import logging
import os
import re
import unittest

from pararamio import Pararamio


class SensitiveFormatter(logging.Formatter):
    """Formatter that removes sensitive information in urls."""

    @staticmethod
    def _filter(s):
        return re.sub(r'password":\s*\"\w+\"', r'password": "*******"', s)

    def format(self, record):
        original = logging.Formatter.format(self, record)
        return self._filter(original)


class BasePararamioTest(unittest.TestCase):
    def setUp(self):
        self.user1 = json.loads(os.environ.get('PARARAMIO_FIRST_USER', '{}'))
        self.user2 = json.loads(os.environ.get('PARARAMIO_SECOND_USER', '{}'))
        self.client = Pararamio(**self.user1, cookie_path='test.cookie')
        self.client2 = Pararamio(**self.user2, cookie_path='test.cookie2')
        self.__post = None
        if bool(os.environ.get('DEBUG', False)):
            logger = logging.getLogger('pararamio')
            logger.setLevel(logging.DEBUG)
            ch = logging.StreamHandler()
            ch.setLevel(logging.DEBUG)
            ch.setFormatter(SensitiveFormatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
            logger.addHandler(ch)
