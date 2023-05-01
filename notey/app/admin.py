from django.contrib import admin

from .models import Profile, Project, ProjectUser, Note, Attachment

admin.site.register(Profile)
admin.site.register(Project)
admin.site.register(ProjectUser)
admin.site.register(Note)
admin.site.register(Attachment)
