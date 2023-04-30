from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    color = models.CharField(max_length=9, default="#FFFFFF")

    def __str__(self) -> str:
        return f"{self.user.username}'s profile"


DEFAULT_PROJECT_IMAGE_URL = (
    "https://images.unsplash.com/photo-1518976024611-28bf4b48222e"
)


class Project(models.Model):
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=128, unique=True)
    image_url = models.CharField(default=DEFAULT_PROJECT_IMAGE_URL, max_length=512)
    is_archived = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"[{self.creator.username}]{self.name}"

    def get_notes(self):
        return Note.objects.filter(project=self)

    def get_users(self):
        return ProjectUser.objects.filter(project=self)


class ProjectUserPermission(models.TextChoices):
    DELETE = "RWCD", "Read, write, complete and delete"
    COMPLETE = "RWC-", "Read, write and complete"
    WRITE = "RW--", "Read and write"
    READ = "R---", "Read"


class ProjectUser(models.Model):
    permission = models.CharField(
        max_length=4,
        choices=ProjectUserPermission.choices,
        default=ProjectUserPermission.READ,
    )
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
        return f"{self.user.username}-{self.project.name} [{self.permission}]"

    def getProjects(user: User):
        projectUser = ProjectUser.objects.all().filter(user=user)
        temp = []
        projects = []
        for el in projectUser:
            temp.append(el.project)
        for project in temp:
            if not project.is_archived:
                projects.append(project)
        return projects

    def getArchivedProjects(user: User):
        projectUser = ProjectUser.objects.all().filter(user=user)
        projects = []
        for el in projectUser:
            projects.append(el.project)
        archived_projects = []
        for project in projects:
            if project.is_archived:
                archived_projects.append(project)
        return archived_projects


class Note(models.Model):
    text = models.CharField(max_length=256)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)

    def __str__(self) -> str:
        if self.is_completed:
            return f"[+]{self.text} on {self.project.name}"
        return f"[-]{self.text} on {self.project.name}"
