# Generated by Django 5.1.4 on 2025-03-19 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('license_management', '0007_rename_software_name_license_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='license',
            name='comments',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='licenseassignment',
            name='comments',
            field=models.TextField(blank=True),
        ),
    ]
