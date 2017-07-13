from django.shortcuts import render
from django.views.generic import ListView

from db.course import Course


class CourseList(ListView):
    template_name = 'courses/index.html'
    context_object_name = 'courses'

    def get_queryset(self):
        return Course.all()




