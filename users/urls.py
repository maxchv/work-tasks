from django.conf.urls import url
from users.views import CreateUserView, DeleteUserView, EditUserViewForm, UsersListView

app_name = 'users'
urlpatterns = [
    url(r'^$', UsersListView.as_view(), name='index', ),
    url(r'^create/', CreateUserView.as_view(), name='create', ),
    url(r'^delete/(?P<pk>\d+)', DeleteUserView.as_view(), name="delete", ),
    url(r'^edit/(?P<pk>\d+)', EditUserViewForm.as_view(),
        name="edit")
]
