# Generated by Django 3.0.6 on 2020-05-12 16:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Body",
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
                ("name", models.CharField(max_length=300)),
                ("location", models.CharField(blank=True, max_length=300, null=True)),
                ("website", models.URLField(blank=True, null=True)),
                (
                    "lat",
                    models.DecimalField(
                        blank=True,
                        decimal_places=15,
                        default=0,
                        max_digits=19,
                        null=True,
                    ),
                ),
                (
                    "lng",
                    models.DecimalField(
                        blank=True,
                        decimal_places=15,
                        default=0,
                        max_digits=19,
                        null=True,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Declaration",
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
                ("disclosure_date", models.DateField(blank=True, null=True)),
                ("source", models.URLField()),
                ("fetched", models.DateTimeField(blank=True, null=True)),
                (
                    "body_received_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="db.Body"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Scrape",
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
                ("datetime", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name="Member",
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
                ("name", models.CharField(max_length=100)),
                ("role", models.CharField(blank=True, max_length=100, null=True)),
                ("url", models.CharField(blank=True, max_length=200, null=True)),
                ("related_to", models.ManyToManyField(blank=True, to="db.Member")),
            ],
        ),
        migrations.CreateModel(
            name="Interest",
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
                ("donor", models.CharField(max_length=100)),
                (
                    "date",
                    models.DateField(
                        blank=True, help_text="Date gift received", null=True
                    ),
                ),
                (
                    "declaration",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="db.Declaration"
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="declaration",
            name="member",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="db.Member"
            ),
        ),
        migrations.AddField(
            model_name="declaration",
            name="scrape",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="db.Scrape"
            ),
        ),
    ]
