# Generated by Django 4.2.1 on 2023-06-25 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_customuser_playlists_list'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='photo',
            field=models.ImageField(default=0, upload_to='photos/%Y/%m/%d/', verbose_name='Фото'),
        ),
    ]