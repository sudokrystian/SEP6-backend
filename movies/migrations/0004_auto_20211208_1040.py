# Generated by Django 3.2.9 on 2021-12-08 10:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0003_alter_rating_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movielist',
            name='movie_id',
        ),
        migrations.AlterField(
            model_name='rating',
            name='date',
            field=models.CharField(default='2021-12-08T10:40:15.402779', max_length=50),
        ),
        migrations.CreateModel(
            name='MoviesInList',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('movie_id', models.IntegerField()),
                ('list', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.movielist')),
            ],
        ),
    ]
