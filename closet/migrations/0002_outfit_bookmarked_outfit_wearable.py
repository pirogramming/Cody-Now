# Generated by Django 5.1.5 on 2025-02-02 05:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('closet', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='outfit',
            name='bookmarked',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='outfit',
            name='wearable',
            field=models.BooleanField(default=False),
        ),
    ]
