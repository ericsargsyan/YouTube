from django.db import models
from django.contrib.auth.models import User


class URLS(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    url = models.CharField(max_length=222)

    def __str__(self):
        return self.url


