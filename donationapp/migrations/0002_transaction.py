# Generated by Django 3.1.2 on 2020-10-13 19:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    atomic = False
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('donationapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField()),
                ('date', models.DateTimeField(verbose_name='date published')),
                ('cause', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='donationapp.causes')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
