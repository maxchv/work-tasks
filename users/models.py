from django.db import models

from courses.models import Course


class CourseUser(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=100, blank=True, null=True)
    mobile_phone = models.CharField(max_length=100, blank=True, null=True)
    STATUS_CHOICE = (('inactive', 'Inactive'), ('active', 'Active'))
    status = models.CharField(max_length=8, choices=STATUS_CHOICE, default='inactive')
    created = models.DateTimeField(auto_now_add=True, editable=True, blank=True, null=True)
    updated = models.DateTimeField(auto_now=True, editable=True, blank=True, null=True)
    courses = models.ManyToManyField(Course, default=None, blank=True)

    def __str__(self):
        return self.name

