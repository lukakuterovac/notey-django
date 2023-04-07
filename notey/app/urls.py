from django.urls import path

from . import views

app_name = "app"
urlpatterns = [
    path("", views.home, name="home"),
    path("register", views.register_request, name="register"),
    path("login", views.login_request, name="login"),
    path("logout", views.logout_request, name="logout"),
    path("projects", views.projects, name="projects"),
    path("projects/new", views.new_project, name="new_project"),
    path(
        "projects/delete/<int:project_id>", views.delete_project, name="delete_project"
    ),
    path("projects/<int:project_id>", views.project_details, name="project_details"),
    path("projects/<int:project_id>/new", views.new_note, name="new_note"),
    path(
        "projects/<int:project_id>/delete/<int:note_id>",
        views.delete_note,
        name="delete_note",
    ),
    path(
        "projects/<int:project_id>/complete/<int:note_id>",
        views.complete_note,
        name="complete_note",
    ),
    path(
        "projects/<int:project_id>/settings",
        views.project_settings,
        name="project_settings",
    ),
    path(
        "projects/<int:project_id>/settings/add_user",
        views.add_user,
        name="add_user",
    ),
    path(
        "projects/<int:project_id>/settings/remove_user/<int:user_id>",
        views.remove_user,
        name="remove_user",
    ),
    path("projects/<int:project_id>/leave", views.leave_project, name="leave_project"),
    path("profile", views.profile, name="profile"),
]
