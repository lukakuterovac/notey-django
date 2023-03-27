# Generated by Django 4.1.7 on 2023-03-12 11:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0004_projectuser"),
    ]

    operations = [
        migrations.AlterField(
            model_name="projectuser",
            name="project",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="project_user",
                to="app.project",
            ),
        ),
    ]