# Generated by Django 3.0.4 on 2020-04-07 16:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("db", "0005_auto_20200406_2216"),
    ]

    operations = [
        migrations.CreateModel(
            name="OtherInterest",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("category", models.CharField(blank=True, max_length=100, null=True)),
                ("description", models.TextField(blank=True, null=True)),
                (
                    "declaration",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="db.Declaration"
                    ),
                ),
            ],
            options={"abstract": False,},
        ),
    ]
