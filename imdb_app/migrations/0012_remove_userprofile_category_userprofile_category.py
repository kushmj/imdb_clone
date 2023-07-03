# Generated by Django 4.1.5 on 2023-06-30 11:34

from django.db import migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('imdb_app', '0011_category_remove_userprofile_category_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='category',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='category',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('Action', 'Action'), ('Comedy', 'Comedy'), ('RPG', 'RPG')], default=1, max_length=100),
            preserve_default=False,
        ),
    ]