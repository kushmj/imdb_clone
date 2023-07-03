# Generated by Django 4.1.5 on 2023-06-30 09:49

from django.db import migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('imdb_app', '0009_category_userprofile_alter_movielist_category_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movielist',
            name='category',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('Horror', 'Horror'), ('RPG', 'RPG'), ('Action', 'Action'), ('Comedy', 'Comedy')], default=[], max_length=100),
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='category',
        ),
        migrations.DeleteModel(
            name='Category',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='category',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('Horror', 'Horror'), ('RPG', 'RPG'), ('Action', 'Action'), ('Comedy', 'Comedy')], default=['None'], max_length=100),
        ),
    ]