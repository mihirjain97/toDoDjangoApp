import datetime

from django.db import models
from django.utils import timezone

# Create your models here.


class Question(models.Model):
    questionText = models.CharField(max_length=200)
    pubDate = models.DateTimeField('Date Published')

    def __str__(self):
        return self.questionText

    def was_published_recently(self):
        return self.pubDate >= timezone.now() - datetime.timedelta(days=1)


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choiceText = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choiceText
