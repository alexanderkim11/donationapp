# Generated by Django 3.1.1 on 2020-10-18 15:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donationapp', '0007_remove_transaction_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='date',
            field=models.DateTimeField(null=True, verbose_name='date published'),
        ),
    ]
