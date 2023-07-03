# Generated by Django 4.1.5 on 2023-06-30 11:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('imdb_app', '0010_alter_movielist_category_remove_userprofile_category_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='category',
        ),
        migrations.AlterField(
            model_name='movielist',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='imdb_app.category'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='category',
            field=models.ManyToManyField(to='imdb_app.category'),
        ),
    ]
