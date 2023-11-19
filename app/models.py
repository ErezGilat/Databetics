from django.db import models
from django.contrib.auth.models import User


class DIAGNOSE(models.Model):
    details = models.TextField()
    diagnosed = models.BooleanField(default=False)
    output = models.IntegerField(null=True, blank=True)
    result = models.CharField(max_length=256)

    def __str__(self):
        return f"{self.output} || {self.result}"
