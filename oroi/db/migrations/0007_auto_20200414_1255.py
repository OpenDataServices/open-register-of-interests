# Generated by Django 3.0.5 on 2020-04-14 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("db", "0006_otherinterest"),
    ]

    operations = [
        migrations.AddField(
            model_name="giftinterest",
            name="reason",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="member",
            name="url",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
