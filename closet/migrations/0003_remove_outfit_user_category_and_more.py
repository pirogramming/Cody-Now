# Generated by Django 5.1.5 on 2025-02-05 07:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('closet', '0002_usercategory_outfit_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='outfit',
            name='user_category',
        ),
        migrations.RemoveField(
            model_name='usercategory',
            name='outfit_id',
        ),
    ]
