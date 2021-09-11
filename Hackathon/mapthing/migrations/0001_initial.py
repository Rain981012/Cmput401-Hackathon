# Generated by Django 3.2.7 on 2021-09-11 18:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_name', models.CharField(max_length=200)),
                ('creator', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=400)),
                ('longitude', models.FloatField()),
                ('latitude', models.FloatField()),
                ('start_date', models.DateTimeField(verbose_name='published date')),
                ('end_date', models.DateTimeField(verbose_name='end date')),
                ('attendants', models.IntegerField(default=0)),
                ('visibility', models.BooleanField(default=True)),
            ],
        ),
    ]
