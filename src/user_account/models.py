import datetime
from time import strptime

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Count, Sum
from django.shortcuts import render
from django.utils.datetime_safe import strftime


class User(AbstractUser):
    image = models.ImageField(default='default.jpg', upload_to='pics')
    avr_score = models.PositiveIntegerField(null=True, blank=True)
    number_tests_passed = models.PositiveIntegerField(null=True, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True, default=datetime.date.today)

    def update_score(self):
        self.avr_score = (self.test_results.aggregate(score=Sum('avr_score')).get('score'))
        return self.avr_score

    def last_launch(self):
        datetime_run = self.test_results.order_by('-datetime_run').first().datetime_run
        return datetime_run

    def num_runs(self):
        num_runs = self.test_results.count()
        return num_runs
