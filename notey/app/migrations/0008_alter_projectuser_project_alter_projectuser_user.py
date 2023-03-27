# Generated by Django 4.1.7 on 2023-03-13 12:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("app", "0007_alter_projectuser_project"),
    ]

    operations = [
        migrations.AlterField(
            model_name="projectuser",
            name="project",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="project",
                to="app.project",
            ),
        ),
        migrations.AlterField(
            model_name="projectuser",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="user",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]