# Generated by Django 3.2.9 on 2021-12-11 22:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0008_auto_20211211_2240'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='date',
            field=models.CharField(default='2021-12-11T22:44:20.260148', max_length=50),
        ),
        migrations.AlterField(
            model_name='rating',
            name='date',
            field=models.CharField(default='2021-12-11T22:44:20.259944', max_length=50),
        ),
    ]