from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Count, Sum


class Topic(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField(max_length=1024, null=True, blank=True)

    def __str__(self):
        return f'{self.title}'


class Test(models.Model):
    MIN_LIMIT = 3
    MAX_LIMIT = 20

    LEVEL_CHOICES = (
        (1, 'Basic'),
        (2, 'Middle'),
        (3, 'Advanced'),
    )

    topic = models.ForeignKey(to=Topic, related_name='tests', null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=64)
    description = models.TextField(max_length=1024, null=True, blank=True)
    level = models.PositiveSmallIntegerField(choices=LEVEL_CHOICES, default=2)
    image = models.ImageField(default='default.png', upload_to='covers')

    def __str__(self):
        return f' {self.image},' \
               f' {self.title},' \
               f' {self.description},' \
               f' {self.level},'

    def questions_count(self):
        return self.questions.count()

    def last_run(self):
        last_run = self.test_results.order_by('-id').first()
        if last_run:
            return last_run.datetime_run
        return ''


class Question(models.Model):
    MIN_LIMIT = 3
    MAX_LIMIT = 6
    test = models.ForeignKey(to=Test, related_name='questions', on_delete=models.CASCADE)
    number = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(MAX_LIMIT)])
    text = models.CharField(max_length=64)
    description = models.TextField(max_length=512, null=True, blank=True)

    def __str__(self):
        return f'{self.text}'


class Answer(models.Model):
    text = models.CharField(max_length=64)
    question = models.ForeignKey(to=Question, related_name='answers', on_delete=models.CASCADE)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.text} - {self.is_correct}'


class TestResult(models.Model):
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='test_results', on_delete=models.CASCADE)
    test = models.ForeignKey(to=Test, related_name='test_results', on_delete=models.CASCADE)
    datetime_run = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)
    is_new = models.BooleanField(default=True)
    avr_score = models.DecimalField(default=0.0, max_digits=6, decimal_places=2)

    def update_score(self):
        qs = self.test_result_details.values('question').annotate(
            num_answers=Count('question'),
            score=Sum('is_correct')
        )
        self.avr_score = sum(
            int(entry['score']) / entry['num_answers']
            for entry in qs
        )

    def question_true_answers(self):
        qs = self.test_result_details.values('question').annotate(
            num_answers=Count('question'),
            score=Sum('is_correct')
        )
        return sum(e['num_answers'] == int(e['score']) for e in qs)

    def percent_true_answers(self):
        num_questions = self.test.questions_count()
        correct = self.question_true_answers()
        result = correct / num_questions * 100
        return result

    def finish(self):
        self.update_score()
        self.is_completed = True

    def str(self):
        return f'{self.test.title}, {self.user.full_name()}, {self.datetime_run}'


class TestResultDetail(models.Model):
    test_result = models.ForeignKey(to=TestResult, related_name='test_result_details', on_delete=models.CASCADE)
    question = models.ForeignKey(to=Question, null=True, blank=True, on_delete=models.CASCADE)
    answer = models.ForeignKey(to=Answer, on_delete=models.CASCADE)
    is_correct = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(1)],
        default=0
    )

    def __str__(self):
        return f'{self.question.text}'
