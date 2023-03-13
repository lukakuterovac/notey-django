# Generated by Django 4.1.7 on 2023-03-13 12:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0006_alter_projectuser_unique_together"),
    ]

    operations = [
        migrations.AlterField(
            model_name="projectuser",
            name="project",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="project_user_link",
                to="app.project",
            ),
        ),
    ]
