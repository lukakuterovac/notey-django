from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm, ValidationError

from .models import Note, Profile, Project, ProjectUser


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

    def clean_email(self):
        email = self.data["email"]

        if User.objects.filter(email=email).exists():
            raise ValidationError("A user with that email already exists.")

        return email


class NewProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ["name", "image"]
        exclude = ["creator"]


class UpdateProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ["name", "image"]
        exclude = ["creator"]


class NewNoteForm(ModelForm):
    attachment = forms.FileField(
        widget=forms.ClearableFileInput(attrs={"multiple": True}),
        required=False,
    )

    class Meta:
        model = Note
        fields = ["text", "attachment"]
        exclude = ["user", "project", "is_completed"]


class NewProjectUser(ModelForm):
    class Meta:
        model = ProjectUser
        fields = ["user", "project", "permission"]
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


class ProfileUpdateForm(ModelForm):
    class Meta:
        model = Profile
        fields = ["color"]
        widgets = {"color": forms.TextInput(attrs={"type": "color"})}
