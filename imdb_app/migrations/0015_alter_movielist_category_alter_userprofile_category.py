# Generated by Django 4.1.5 on 2023-06-30 16:08

from django.db import migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('imdb_app', '0014_delete_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movielist',
            name='category',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('Action', 'Action'), ('Comedy', 'Comedy'), ('RPG', 'RPG'), ('Horror', 'Horror')], max_length=100),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='category',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('Action', 'Action'), ('Comedy', 'Comedy'), ('RPG', 'RPG'), ('Horror', 'Horror')], max_length=100),
        ),
    ]
