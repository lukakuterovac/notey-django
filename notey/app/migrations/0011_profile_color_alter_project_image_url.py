# Generated by Django 4.1.7 on 2023-03-29 08:47

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0010_project_image_url"),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="color",
            field=models.CharField(
                choices=[("Red", "red"), ("Green", "green"), ("Blue", "blue")],
                default=("Red", "red"),
                max_length=32,
            ),
        ),
        migrations.AlterField(
            model_name="project",
            name="image_url",
            field=models.CharField(
                default="https://images.unsplash.com/photo-1518976024611-28bf4b48222e",
                max_length=512,
            ),
        ),
    ]
