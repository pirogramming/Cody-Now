# Generated by Django 5.1.5 on 2025-02-03 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('closet', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='usercategory',
            name='outfit_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
