# Generated by Django 4.1.5 on 2023-05-11 14:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('imdb_app', '0003_remove_ottplatform_movie_list'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movielist',
            name='ott_platfor_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='movielist', to='imdb_app.ottplatform'),
        ),
    ]
