# Generated by Django 3.2.8 on 2021-10-25 22:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0007_alter_playlist_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playlist',
            name='name',
            field=models.CharField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='playlisttrack',
            name='artist',
            field=models.CharField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='playlisttrack',
            name='title',
            field=models.CharField(max_length=1000),
        ),
    ]
