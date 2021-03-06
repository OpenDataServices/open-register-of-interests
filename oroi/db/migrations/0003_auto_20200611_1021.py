# Generated by Django 3.0.7 on 2020-06-11 10:21

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("db", "0002_auto_20200611_0956"),
    ]

    operations = [
        migrations.RemoveField(model_name="declaration", name="disclosure_date",),
        migrations.RemoveField(model_name="declaration", name="register_date",),
        migrations.AddField(
            model_name="declaration",
            name="declared_date",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.DateField(
                    blank=True, help_text="Date(s) the interest was declared", null=True
                ),
                blank=True,
                null=True,
                size=None,
            ),
        ),
    ]
