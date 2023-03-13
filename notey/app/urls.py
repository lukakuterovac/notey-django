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
    path("projects/<int:project_id>", views.project_details, name="project_details"),
]
