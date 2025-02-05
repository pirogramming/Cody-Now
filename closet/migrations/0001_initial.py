# Generated by Django 5.1.5 on 2025-02-05 12:55

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Outfit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='outfits/')),
                ('image_url', models.CharField(blank=True, max_length=300)),
                ('design_style', models.CharField(blank=True, choices=[('Street', 'Street'), ('Casual', 'Casual'), ('Formal', 'Formal')], max_length=50)),
                ('category', models.CharField(blank=True, choices=[('T-shirt', 'T-shirt'), ('Blouse', 'Blouse'), ('Pants', 'Pants'), ('Dress', 'Dress'), ('Skirt', 'Skirt'), ('Jacket', 'Jacket'), ('Coat', 'Coat')], max_length=50)),
                ('overall_design', models.TextField(blank=True)),
                ('logo_location', models.CharField(blank=True, max_length=100)),
                ('logo_size', models.CharField(blank=True, max_length=100)),
                ('logo_content', models.TextField(blank=True)),
                ('color_and_pattern', models.CharField(blank=True, max_length=100)),
                ('color', models.CharField(blank=True, max_length=100)),
                ('fit', models.CharField(blank=True, max_length=50)),
                ('cloth_length', models.CharField(blank=True, max_length=50)),
                ('neckline', models.CharField(blank=True, max_length=50)),
                ('detail', models.TextField(blank=True)),
                ('material', models.CharField(blank=True, max_length=100)),
                ('season', models.CharField(blank=True, max_length=50)),
                ('tag', models.JSONField(blank=True, default=list)),
                ('comment', models.TextField(blank=True)),
                ('brand', models.CharField(blank=True, max_length=100)),
                ('price', models.CharField(blank=True, max_length=50)),
                ('bookmarked', models.BooleanField(default=False)),
                ('wearable', models.BooleanField(default=False)),
                ('raw_response', models.JSONField(blank=True, null=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='outfits', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='category', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='MyCloset',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='my_closet', to=settings.AUTH_USER_MODEL)),
                ('outfit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='closet.outfit')),
                ('user_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='closet.usercategory')),
            ],
        ),
    ]
