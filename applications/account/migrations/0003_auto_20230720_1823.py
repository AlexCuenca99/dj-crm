# Generated by Django 3.2 on 2023-07-20 23:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_delete_lead'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='agent',
            name='organization',
        ),
        migrations.RemoveField(
            model_name='agent',
            name='user',
        ),
    ]
