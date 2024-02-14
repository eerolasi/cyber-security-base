from django.db import models
from django.contrib.auth.models import User
#import datetime
from datetime import datetime


class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()

    def __str__(self):
        return self.title
