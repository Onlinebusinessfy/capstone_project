# Generated by Django 5.1.6 on 2025-03-21 02:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_remove_profile_street_remove_profile_zip_code_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
