from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import ModelForm

from garden_app.models import Plant, PlantType, Unit, Task, PlanOfWork


class AddTypeForm(ModelForm):
    class Meta:
        model = PlantType
        fields = ["name"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
        }


class AddUnit(ModelForm):
    class Meta:
        model = Unit
        fields = ["name"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
        }


class AddPlantForm(forms.ModelForm):
    class Meta:
        model = Plant
        fields = ["name", "species", "description", "amount", "unit", "type"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "species": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control"}),
            "amount": forms.NumberInput(attrs={"class": "form-control"}),
            "unit": forms.Select(attrs={"class": "form-control"}),
            "type": forms.Select(attrs={"class": "form-control"}),
        }


class AddTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["name", "description", "plant", "plan"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control"}),
            "plan": forms.SelectMultiple(attrs={"class": "form-control"}),
            "plant": forms.Select(attrs={"class": "form-control"}),
        }


class AddPlanOfWorkForm(forms.ModelForm):

    task = forms.ModelMultipleChoiceField(
        queryset=Task.objects.all(), widget=forms.CheckboxSelectMultiple, required=False
    )

    class Meta:
        model = PlanOfWork
        fields = ["name", "description", "date", "task"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control"}),
            "date": forms.SelectDateWidget(attrs={"class": "form-control"}),
        }


def validate_password_length(value):
    if len(value) < 6:
        raise ValidationError("Password is to short")


def validate_password_has_number(value):
    if not any(i for i in value if i.isdigit()):
        raise ValidationError("Password must have a number")


class CreateUserForm(forms.ModelForm):
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        validators=[validate_password_length, validate_password_has_number],
        help_text="Password must be at least 6 characters long and has a number.",
    )
    password2 = forms.CharField(label="re-Password", widget=forms.PasswordInput(attrs={"class": "form-control"}))
    username = forms.CharField(label="Username", widget=forms.TextInput(attrs={"class": "form-control"}))

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class ": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
        }

    def clean(self):
        data = super().clean()
        pass_to_check1 = data.get("password1")
        login = data.get("username")
        try:
            user = User.objects.get(username=login)
        except User.DoesNotExist:
            return None
        if user.username == login:
            raise ValidationError("The given username is already taken")
        if pass_to_check1 is not None and pass_to_check1 != data.get("password2"):
            raise ValidationError("Passwords do not match")
        return data


class LoginForm(forms.Form):
    login = forms.CharField(max_length=60)
    password = forms.CharField(max_length=60, widget=forms.PasswordInput)
