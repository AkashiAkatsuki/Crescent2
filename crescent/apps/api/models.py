from django.db import models

class Word(models.Model):
    name = models.TextField()
    category = models.TextField()
    value = models.FloatField(default=0.5)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'words'
    def __str__(self):
        return str(self.name)

class Markov(models.Model):
    prefix1 = models.IntegerField()
    prefix2 = models.IntegerField()
    suffix = models.IntegerField()
    class Meta:
        db_table = 'markovs'
