# Generated by Django 4.1.5 on 2023-07-03 16:11

from django.db import migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('imdb_app', '0015_alter_movielist_category_alter_userprofile_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movielist',
            name='category',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('Action', 'Action'), ('Adventure', 'Adventure'), ('Drama', 'Drama'), ('Comedy', 'Comedy'), ('RPG', 'RPG'), ('Horror', 'Horror'), ('Romance', 'Romance'), ('Fantasy', 'Fantasy')], max_length=100),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='category',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('Action', 'Action'), ('Adventure', 'Adventure'), ('Drama', 'Drama'), ('Comedy', 'Comedy'), ('RPG', 'RPG'), ('Horror', 'Horror'), ('Romance', 'Romance'), ('Fantasy', 'Fantasy')], max_length=100),
        ),
    ]
