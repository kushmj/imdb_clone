# Generated by Django 4.1.5 on 2023-05-10 19:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('imdb_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OttPlatform',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ott_name', models.CharField(max_length=100)),
                ('about', models.CharField(max_length=1000)),
                ('website_url', models.URLField(max_length=500)),
                ('movie_list', models.ManyToManyField(related_name='OttPaltform', to='imdb_app.movielist')),
            ],
        ),
        migrations.AddField(
            model_name='movielist',
            name='ott_platfor_name',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='MovieList', to='imdb_app.ottplatform'),
            preserve_default=False,
        ),
    ]