# Generated by Django 3.2 on 2023-07-20 23:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0002_alter_lead_agent'),
        ('account', '0003_auto_20230720_1823'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Agent',
        ),
    ]
