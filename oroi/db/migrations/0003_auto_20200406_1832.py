# Generated by Django 3.0.4 on 2020-04-06 18:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("db", "0002_auto_20200406_1829"),
    ]

    operations = [
        migrations.RemoveField(model_name="declaration", name="description",),
        migrations.AddField(
            model_name="declaration",
            name="fetched",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="declaration",
            name="disclosure_date",
            field=models.DateField(blank=True, null=True),
        ),
    ]