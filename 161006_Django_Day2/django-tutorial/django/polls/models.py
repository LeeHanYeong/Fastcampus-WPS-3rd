import datetime
from django.utils import timezone
from django.db import models


class Question(models.Model):
    question_text = models.CharField('질문 내용', max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return '질문(%s)' % self.question_text

    def was_published_recently(self):
        # 자신의 pub_date가 timezone.now() [현재시간] 에서 1일을 마이너스 한 값보다 큰지?
        # return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

        is_recently = self.pub_date >= timezone.now() - datetime.timedelta(days=1)
        return is_recently


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField('선택한 내용', max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return '%s - %s (%s)' % (
            self.question.question_text,
            self.choice_text,
            self.votes
        )