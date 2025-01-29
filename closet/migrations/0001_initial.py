# Generated by Django 5.1.5 on 2025-01-29 04:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Outfit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
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
                ('image', models.ImageField(upload_to='outfits/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
