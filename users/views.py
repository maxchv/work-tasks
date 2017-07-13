from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import InvalidPage
from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import FormView, DeleteView, ListView

from db.course import Course
from db.user import User
from users.forms import CourseUserForm, CourseUserFormEdit


class UsersListView(ListView):
    template_name = 'users/index.html'
    context_object_name = 'course_users'

    def get_queryset(self):
        username = self.request.POST.get('user')
        if username:
            return tuple(User.filter(name=username))
        return tuple(User.all())

    def get_paginate_by(self, queryset):
        paginate_by = self.request.GET.get('paginate_by')
        if not paginate_by:
            paginate_by = 5
        return paginate_by

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['per_page'] = (3, 5, 10)
        return context

    def paginate_queryset(self, queryset, page_size):
        paginator = self.get_paginator(
            queryset, page_size, orphans=self.get_paginate_orphans(),
            allow_empty_first_page=self.get_allow_empty())
        page_kwarg = self.page_kwarg
        page = self.kwargs.get(page_kwarg) or self.request.GET.get(page_kwarg) or 1
        try:
            page_number = int(page)
        except ValueError:
            if page == 'last':
                page_number = paginator.num_pages
            else:
                raise Http404("Page is not 'last', nor can it be converted to an int.")
        page_number = paginator.num_pages if page_number > paginator.num_pages else page_number
        try:
            page = paginator.page(page_number)
            return (paginator, page, page.object_list, page.has_other_pages())
        except InvalidPage as e:
            raise Http404('Invalid page (%(page_number)s): %(message)s' % {
                'page_number': page_number,
                'message': e,
            })

    def post(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class CreateUserView(FormView):
    template_name = 'users/create.html'
    form_class = CourseUserForm
    success_url = reverse_lazy('user:index')

    def form_valid(self, form, **kwargs):
        user = User()
        user.name = form.cleaned_data['name']
        user.email = form.cleaned_data['email']
        user.phone = form.cleaned_data['phone']
        user.mobile_phone = form.cleaned_data['mobile_phone']
        user.status = form.cleaned_data['status']
        user.save()

        context = self.get_context_data(**kwargs)
        messages.add_message(self.request, messages.INFO, 'User created successfully')

        return render(self.request, self.get_template_names(), context=context)

    def form_invalid(self, form):
        print('invalid')
        return super().form_invalid(form)


class DeleteUserView(DeleteView):
    pk_url_kwarg = "pk"
    success_url = reverse_lazy('users:index')

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if pk:
            obj = User.get(id=pk)
            if obj:
                obj.delete()
        return redirect(self.success_url)


class EditUserViewForm(FormView):
    template_name = "users/edit.html"
    success_url = reverse_lazy('users:index')
    form_class = CourseUserFormEdit

    def get_initial(self):
        initial = super().get_initial()

        user = self.get_user()
        initial['name'] = user.name.split()[-1]
        initial['email'] = user.email
        initial['phone'] = user.phone
        initial['mobile_phone'] = user.mobile_phone
        initial['status'] = user.status
        selected_courses_id = [c.id for c in user.courses]
        initial['courses'] = selected_courses_id
        initial['selected'] = selected_courses_id
        return initial

    def get_user(self):
        try:
            _id = int(self.kwargs.get('pk'))
        except:
            raise Http404
        return User.get(id=_id)

    def form_valid(self, form):
        user = self.get_user()
        user.name = form.cleaned_data['name']
        user.email = form.cleaned_data['email']
        user.phone = form.cleaned_data['phone']
        user.mobile_phone = form.cleaned_data['mobile_phone']
        user.status = form.cleaned_data['status']
        courses = form.cleaned_data['selected']
        user.courses = [Course.get(id=_id) for _id in courses]
        user.update()

        context = self.get_context_data()
        messages.add_message(self.request, messages.INFO, 'User updated successfully')

        return render(self.request, self.get_template_names(), context=context)
