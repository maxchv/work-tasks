from django.conf.urls import url
from django.views.generic import ListView

from courses.views import CourseList
from db.course import Course

app_name = 'courses'
urlpatterns = [
    url(r'^$', CourseList.as_view(), name='index'),
]
