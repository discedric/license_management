# Generated by Django 5.1.6 on 2025-03-18 12:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('license_management', '0006_alter_licenseassignment_device'),
    ]

    operations = [
        migrations.RenameField(
            model_name='license',
            old_name='software_name',
            new_name='name',
        ),
    ]
