from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm, ValidationError

from .models import Project, Note, ProjectUser


class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class NewProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ["name"]
        exclude = ["creator", "image_url"]


class UpdateProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ["name", "image_url"]
        exclude = ["creator"]


class NewNoteForm(ModelForm):
    class Meta:
        model = Note
        fields = ["text"]
        exclude = ["user", "project", "is_completed"]


class NewProjectUser(ModelForm):
    class Meta:
        model = ProjectUser
        fields = ["user", "project"]
        widgets = {
            "project": forms.HiddenInput(),
        }

    def clean_user(self):
        user = self.cleaned_data["user"]
        if (
            ProjectUser.objects.filter(project=self.data["project"])
            .filter(user=user)
            .exists()
        ):
            raise ValidationError("This user has already been added.")

        return user
