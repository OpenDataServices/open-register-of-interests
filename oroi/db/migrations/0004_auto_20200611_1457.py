# Generated by Django 3.0.7 on 2020-06-11 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("db", "0003_auto_20200611_1021"),
    ]

    operations = [
        migrations.AlterField(
            model_name="declaration",
            name="donor",
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
