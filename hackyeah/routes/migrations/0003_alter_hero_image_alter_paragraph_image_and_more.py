# Generated by Django 4.2.5 on 2023-10-01 03:30

import pathlib

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("routes", "0002_routepointvisit"),
    ]

    operations = [
        migrations.AlterField(
            model_name="hero",
            name="image",
            field=models.URLField(blank=True, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name="paragraph",
            name="image",
            field=models.URLField(blank=True, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name="route",
            name="image",
            field=models.URLField(blank=True, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name="routepoint",
            name="audio",
            field=models.FileField(
                blank=True,
                null=True,
                upload_to=pathlib.PurePosixPath("route_points/audio"),
            ),
        ),
        migrations.AlterField(
            model_name="routepoint",
            name="google_maps_url",
            field=models.URLField(max_length=1000),
        ),
        migrations.AlterField(
            model_name="routepoint",
            name="main_image",
            field=models.URLField(blank=True, max_length=1000, null=True),
        ),
    ]
