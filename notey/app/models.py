from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.user.username}'s profile"


class Project(models.Model):
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=128, unique=True)

    def __str__(self) -> str:
        return f"[{self.creator.username}]{self.name}"

    def get_notes(self):
        return Note.objects.filter(project=self)


class ProjectUser(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="user",
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="project",
    )

    class Meta:
        unique_together = ("user", "project")

    def __str__(self) -> str:
        return f"{self.user.username}-{self.project.name}"

    def getProjects(user):
        projectUser = ProjectUser.objects.all().filter(user=user)
        projects = []
        for el in projectUser:
            projects.append(el.project)
        return projects


class Note(models.Model):
    text = models.CharField(max_length=256)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)

    def __str__(self) -> str:
        if self.is_completed:
            return f"[+]{self.text} on {self.project.name}"
        return f"[-]{self.text} on {self.project.name}"
