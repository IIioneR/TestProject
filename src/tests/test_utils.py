from django.test import SimpleTestCase
from tests import utils


class TestFrange(SimpleTestCase):

    def test_add(self):

        assert utils.add(2, 2) == 4
