# Generated by Django 5.1.6 on 2025-03-18 08:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_event_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='visibility',
            field=models.CharField(choices=[('GLOBAL', 'Global'), ('PRIVATE', 'Private')], max_length=10),
        ),
    ]
