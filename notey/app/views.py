from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import HttpResponseRedirect, redirect, render
from django.urls import reverse

from .forms import NewProjectForm, NewUserForm
from .models import Project, ProjectUser


def home(request):
    return render(request, "app/home.html", {})


def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("app:home")
        messages.error(request, "Unsuccessful registration. Invalid information.")

    form = NewUserForm()

    return render(
        request=request,
        template_name="app/register.html",
        context={"register_form": form},
    )


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("app:home")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(
        request=request, template_name="app/login.html", context={"login_form": form}
    )


def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("app:home")


def projects(request):
    user = request.user
    projects = ProjectUser.getProjects(user=user)
    new_project_form = NewProjectForm()
    context = {
        "projects": projects,
        "form": new_project_form,
    }
    return render(request, "app/projects.html", context)


def new_project(request):
    user = request.user
    if request.method == "POST":
        form = NewProjectForm(request.POST)
        if form.is_valid():
            project = Project(
                creator=user,
                name=form.cleaned_data["name"],
            )
            project.save()
            proj_user = ProjectUser(
                project=project,
                user=user,
            )
            proj_user.save()
            return HttpResponseRedirect(reverse("app:projects"))
    else:
        form = NewProjectForm()
    projects = ProjectUser.getProjects(user=user)
    context = {
        "projects": projects,
        "form": form,
    }
    return render(request, "app/new_project.html", context)
