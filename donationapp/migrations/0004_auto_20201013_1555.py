# Generated by Django 3.1.2 on 2020-10-13 19:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('donationapp', '0003_auto_20201013_1547'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Causes',
            new_name='Cause',
        ),
    ]
