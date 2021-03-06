# Generated by Django 3.2.7 on 2021-09-13 16:26

from django.db import migrations, models
import task4.models


class Migration(migrations.Migration):

    dependencies = [
        ("task4", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Check",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.TextField(blank=True, null=True)),
                ("ip", models.TextField(blank=True, null=True)),
                ("service", models.TextField(blank=True, null=True)),
                ("at", models.DateTimeField(default=task4.models.utcnowtz)),
                ("ok", models.BooleanField(default=False)),
                ("description", models.TextField(blank=True, null=True)),
                ("ms", models.IntegerField(blank=True, null=True)),
            ],
        ),
    ]
