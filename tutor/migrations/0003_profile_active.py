# Generated by Django 3.0.2 on 2020-02-23 21:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tutor', '0002_auto_20200216_2024'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='active',
            field=models.BooleanField(default=False),
        ),
    ]
