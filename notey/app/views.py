from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import HttpResponseRedirect, redirect, render
from django.urls import reverse
from django.contrib.auth.decorators import login_required


from .forms import (
    NewProjectForm,
    NewUserForm,
    NewNoteForm,
    UpdateProjectForm,
    NewProjectUser,
    ProfileUpdateForm,
)
from .models import Project, ProjectUser, Note


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


@login_required
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
            form_errors = True
            return HttpResponseRedirect(reverse("app:projects"))
        else:
            form_errors = False
    else:
        form = NewProjectForm()
    projects = ProjectUser.getProjects(user=user)
    form_errors = True
    context = {
        "projects": projects,
        "form": form,
        "form_errors": form_errors,
    }
    return render(request, "app/projects.html", context)


def delete_project(request, project_id):
    project = Project.objects.get(pk=project_id)
    project.delete()
    return HttpResponseRedirect(reverse("app:projects"))


def project_details(request, project_id):
    project = Project.objects.get(pk=project_id)
    notes = project.get_notes()
    note_form = NewNoteForm()
    context = {
        "project": project,
        "notes": notes,
        "form": note_form,
    }
    return render(request, "app/project_details.html", context)


def new_note(request, project_id):
    user = request.user
    project = Project.objects.get(pk=project_id)
    if request.method == "POST":
        form = NewNoteForm(request.POST)
        if form.is_valid():
            note = Note(
                text=form.cleaned_data["text"],
                user=user,
                project=project,
                is_completed=False,
            )
            note.save()
            return HttpResponseRedirect(
                reverse("app:project_details", args=[project_id])
            )
    else:
        form = NewNoteForm()

    notes = project.get_notes()
    context = {
        "project": project,
        "notes": notes,
    }
    return render(request, "app/project_details.html", context)


def delete_note(request, project_id, note_id):
    note = Note.objects.get(pk=note_id)
    note.delete()
    return HttpResponseRedirect(reverse("app:project_details", args=[project_id]))


def complete_note(request, project_id, note_id):
    note = Note.objects.get(pk=note_id)
    note.is_completed = not (note.is_completed)
    note.save()
    return HttpResponseRedirect(reverse("app:project_details", args=[project_id]))


def project_settings(request, project_id):
    user = request.user
    project = Project.objects.get(pk=project_id)
    users = project.get_users()

    if request.method == "POST":
        form = UpdateProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(
                reverse("app:project_settings", args=[project_id])
            )
    else:
        form = UpdateProjectForm(instance=project)

    add_user_form = NewProjectUser(initial={"project": project})

    context = {
        "project": project,
        "user": user,
        "form": form,
        "add_user_form": add_user_form,
        "users": users,
    }
    return render(request, "app/project_settings.html", context)


def add_user(request, project_id):
    user = request.user
    project = Project.objects.get(pk=project_id)
    users = project.get_users()

    if request.method == "POST":
        add_user_form = NewProjectUser(request.POST, initial={"project": project})
        if add_user_form.is_valid():
            instance = add_user_form.save(commit=False)
            instance.save()
            return HttpResponseRedirect(
                reverse("app:project_settings", args=[project_id])
            )
    else:
        add_user_form = NewProjectUser(initial={"project": project})

    form = UpdateProjectForm(instance=project)

    context = {
        "project": project,
        "user": user,
        "form": form,
        "add_user_form": add_user_form,
        "users": users,
    }
    return render(request, "app/project_settings.html", context)


def remove_user(request, project_id, user_id):
    project = Project.objects.get(pk=project_id)
    user = User.objects.get(pk=user_id)
    project_user = ProjectUser.objects.get(project=project, user=user)
    project_user.delete()
    return HttpResponseRedirect(reverse("app:project_settings", args=[project_id]))


def profile(request):
    user = request.user
    profile = user.profile
    if request.method == "POST":
        form = ProfileUpdateForm(request.POST)
        if form.is_valid():
            profile.color = form.cleaned_data["color"]
            profile.save()
            return HttpResponseRedirect(reverse("app:profile"))
    else:
        form = ProfileUpdateForm(instance=profile)

    context = {"user": user, "profile": profile, "form": form}
    return render(request, "app/profile.html", context)
