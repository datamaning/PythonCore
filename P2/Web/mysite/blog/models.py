from __future__ import unicode_literals

from django.db import models

class BlogPost(models.Model):
    title=models.CharField(max_length=150)
    body=models.TextField()
    timestamp=model.DateTimeField()
# Create your models here.
