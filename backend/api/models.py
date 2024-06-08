from django.db import models
from django.contrib.sessions.models import Session

# Create your models here.

class LatestCount(models.Model):
    current_count = models.IntegerField()
    author = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='current_count')

    def __str__(self):
        return self.current_count