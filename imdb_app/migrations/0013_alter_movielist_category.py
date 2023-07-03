# Generated by Django 4.1.5 on 2023-06-30 12:06

from django.db import migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('imdb_app', '0012_remove_userprofile_category_userprofile_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movielist',
            name='category',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('Action', 'Action'), ('Comedy', 'Comedy'), ('RPG', 'RPG')], max_length=100),
        ),
    ]
