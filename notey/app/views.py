from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.shortcuts import HttpResponseRedirect, redirect, render
from django.urls import reverse

from .forms import (
    NewNoteForm,
    NewProjectForm,
    NewProjectUser,
    NewUserForm,
    ProfileUpdateForm,
    UpdateProjectForm,
    UserUpdateForm,
)
from .models import (
    DEFAULT_PROJECT_IMAGE,
    Attachment,
    Note,
    Project,
    ProjectUser,
    ProjectUserPermission,
)


def home(request):
    return render(request, "app/home.html", {})


def register_request(request):
    context = {}

    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("app:home")
    else:
        form = NewUserForm()

    context["register_form"] = form

    return render(request, "app/register.html", context)


def login_request(request):
    context = {}

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username, password = (
                form.cleaned_data["username"],
                form.cleaned_data["password"],
            )
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect("app:home")
    else:
        form = AuthenticationForm()

    context["login_form"] = form

    return render(request, "app/login.html", context)


def logout_request(request):
    logout(request)
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
        form = NewProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = Project(
                creator=user,
                name=form.cleaned_data["name"],
                image=request.FILES.get("image", DEFAULT_PROJECT_IMAGE),
            )
            project.save()
            proj_user = ProjectUser(
                project=project, user=user, permission=ProjectUserPermission.DELETE
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
    user = request.user
    project = Project.objects.get(pk=project_id)
    project_user = ProjectUser.objects.get(user=user, project=project)
    notes = project.get_notes()
    note_form = NewNoteForm()
    context = {
        "project": project,
        "project_user": project_user,
        "notes": notes,
        "form": note_form,
    }
    return render(request, "app/project_details.html", context)


def new_note(request, project_id):
    user = request.user
    project = Project.objects.get(pk=project_id)
    if request.method == "POST":
        form = NewNoteForm(request.POST, request.FILES)
        if form.is_valid():
            note = Note(
                text=form.cleaned_data["text"],
                user=user,
                project=project,
                is_completed=False,
            )
            note.save()

            attachments = request.FILES.getlist("attachment")
            for attachment in attachments:
                Attachment.objects.create(note=note, file=attachment).save()

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
    notes = project.get_notes()
    is_archiveable = True

    for note in notes:
        if not note.is_completed:
            is_archiveable = False
            break

    if len(notes) == 0:
        is_archiveable = False

    if request.method == "POST":
        form = UpdateProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            project.image = form.cleaned_data.get("image")
            project.save()
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
        "is_archiveable": is_archiveable,
    }
    return render(request, "app/project_settings.html", context)


def add_user(request, project_id):
    user = request.user
    project = Project.objects.get(pk=project_id)
    users = project.get_users()
    notes = project.get_notes()
    is_archiveable = True

    for note in notes:
        if not note.is_completed:
            is_archiveable = False
            break

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
        "is_archiveable": is_archiveable,
    }
    return render(request, "app/project_settings.html", context)


def remove_user(request, project_id, user_id):
    project = Project.objects.get(pk=project_id)
    user = User.objects.get(pk=user_id)
    project_user = ProjectUser.objects.get(project=project, user=user)
    project_user.delete()
    return HttpResponseRedirect(reverse("app:project_settings", args=[project_id]))


def leave_project(request, project_id):
    project = Project.objects.get(pk=project_id)
    user = request.user
    project_user = ProjectUser.objects.get(project=project, user=user)
    project_user.delete()
    return HttpResponseRedirect(reverse("app:projects"))


@login_required
def profile(request):
    user = request.user
    profile = user.profile
    if request.method == "POST":
        user_form = UserUpdateForm(request.POST, instance=request.user)
        form = ProfileUpdateForm(request.POST)
        if user_form.is_valid() and form.is_valid():
            user_form.save()
            profile.color = form.cleaned_data["color"]
            profile.save()
            return HttpResponseRedirect(reverse("app:profile"))
    else:
        user_form = UserUpdateForm(instance=request.user)
        form = ProfileUpdateForm(instance=profile)

    context = {
        "user": user,
        "profile": profile,
        "form": form,
        "user_form": user_form,
    }
    return render(request, "app/profile.html", context)


def archive(request):
    user = request.user
    projects = ProjectUser.getArchivedProjects(user=user)
    print("Aaaaaa", len(projects))
    context = {
        "projects": projects,
    }
    return render(request, "app/archive.html", context)


def archive_project_details(request, project_id):
    user = request.user
    project = Project.objects.get(pk=project_id)
    project_user = ProjectUser.objects.get(user=user, project=project)
    notes = project.get_notes()
    note_form = NewNoteForm()
    context = {
        "project": project,
        "project_user": project_user,
        "notes": notes,
        "form": note_form,
    }
    return render(request, "app/archive_project_details.html", context)


def archive_project(request, project_id):
    project = Project.objects.get(pk=project_id)
    project.is_archived = True
    project.save()
    return HttpResponseRedirect(reverse("app:projects"))
