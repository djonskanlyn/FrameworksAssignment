# Generated by Django 5.1 on 2024-08-23 21:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frameworks_project_users', '0002_alter_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='default.jpg', upload_to='profile_pics'),
        ),
    ]
