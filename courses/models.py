from django.db import models


class Course(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["pk"]

