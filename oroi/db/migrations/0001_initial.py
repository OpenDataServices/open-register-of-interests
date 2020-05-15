# Generated by Django 3.0.6 on 2020-05-15 14:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Body',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300)),
                ('location', models.CharField(blank=True, max_length=300, null=True)),
                ('url', models.URLField(blank=True, null=True)),
                ('lat', models.DecimalField(blank=True, decimal_places=15, default=0, max_digits=19, null=True)),
                ('lng', models.DecimalField(blank=True, decimal_places=15, default=0, max_digits=19, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('role', models.CharField(blank=True, max_length=100, null=True)),
                ('url', models.URLField(blank=True, null=True)),
                ('political_party', models.CharField(blank=True, max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Scrape',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Declaration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('disclosure_date', models.DateField(blank=True, null=True)),
                ('source', models.URLField()),
                ('fetched', models.DateTimeField(blank=True, null=True)),
                ('category', models.CharField(blank=True, max_length=100, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('donor', models.CharField(blank=True, max_length=100, null=True)),
                ('register_date', models.DateField(blank=True, help_text='Date from register', null=True)),
                ('interest_date', models.DateField(blank=True, help_text='Date the described interest happened', null=True)),
                ('notes', models.TextField(blank=True, null=True)),
                ('body_received_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='db.Body')),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='db.Member')),
                ('scrape', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='db.Scrape')),
            ],
        ),
    ]
