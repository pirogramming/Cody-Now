# Generated by Django 5.1.5 on 2025-01-31 16:38

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('closet', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='outfit',
            name='image_url',
            field=models.CharField(blank=True, max_length=300),
        ),
        migrations.AddField(
            model_name='outfit',
            name='raw_response',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='outfit',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='outfits', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='outfit',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='outfits/'),
        ),
    ]
