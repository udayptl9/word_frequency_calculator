from django.db import models


class Word(models.Model):
    url = models.CharField(max_length=200)
    word = models.CharField(max_length=50)
    repeat = models.IntegerField()

    def __str__(self):
        return self.word
