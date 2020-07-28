import datetime

from django.core.management import call_command
from django.test import TestCase

from test_set.models import Test, Question


class TestModelTest(TestCase):

    def setUp(self):
        call_command('loaddata', 'test_set/tests/fixtures/account.json', verbosity=0)
        call_command('loaddata', 'test_set/tests/fixtures/tests.json', verbosity=0)

    def test_questions_count(self):
        test = Test.objects.create(title='Test title')
        question = Question.objects.create(test=test, number=1, text='Question text')

        self.assertEqual(test.questions_count(), 1)

    def test_last_run(self):
        test = Test.objects.first()
        dt = datetime.datetime.strptime('2020-07-01T07:49:51.573Z', "%Y-%m-%dT%H:%M:%S.%fz")
        self.assertEqual(test.last_run().replace(tzinfo=None), dt)
