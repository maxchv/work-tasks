from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

from db.course import Course


class CourseUserForm(forms.Form):
    name = forms.CharField(max_length=100, label="Name", required=True, label_suffix="")
    email = forms.EmailField(required=True,
                             label="E-mail",
                             error_messages={'required': "This field is required"},
                             label_suffix="")
    phone_pattern = r'\+\s?\d{1,2}\s?\(?\d{3}\)?\s?\d{3}\s?\d{2}\s?\d{2}'
    phone_validators = (
        RegexValidator(
            regex=phone_pattern,
            message='Please enter a valid phone number'
        ),
    )
    phone_widget = forms.TextInput(attrs={'pattern': phone_pattern})

    phone = forms.CharField(max_length=100, required=False, validators=phone_validators, widget=phone_widget,
                            label_suffix="")
    mobile_phone = forms.CharField(max_length=100, required=False, validators=phone_validators, widget=phone_widget,
                                   label_suffix="")

    STATUS_CHOICE = (('inactive', 'Inactive'), ('active', 'Active'))
    status = forms.ChoiceField(choices=STATUS_CHOICE, label_suffix="")


class CourseChoiceField(forms.ChoiceField):

    def to_python(self, value):
        return [int(item) for item in value]

    def validate(self, value):
        call = set(c.id for c in Course.all())
        c = set(value)
        if not c.issubset(call):
            raise ValidationError(
                'Invalid value: %(value)s',
                code='invalid course',
                params={'value': ', '.join([str(s) for s in value])},
            )


class CourseUserFormEdit(CourseUserForm):
    COURSES_CHOICE = [(c.id, c.name) for c in tuple(Course.all())[:5]]

    courses = CourseChoiceField(choices=COURSES_CHOICE.copy(),
                                required=False,
                                label_suffix="",
                                widget=forms.SelectMultiple(attrs={"class": "courses_select"}))

    selected = CourseChoiceField(choices=COURSES_CHOICE.copy(),
                                 label="",
                                 label_suffix="",
                                 required=False,
                                 widget=forms.SelectMultiple(attrs={"class": "invisible"}))
