# Generated by Django 5.1 on 2024-08-25 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frameworks_project_recipes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='uploaded_image',
            field=models.ImageField(blank=True, null=True, upload_to='recipe_pics'),
        ),
    ]
