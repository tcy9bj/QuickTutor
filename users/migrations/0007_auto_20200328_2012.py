# Generated by Django 3.0.2 on 2020-03-29 00:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_auto_20200328_2003'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='second_major',
            new_name='major2',
        ),
    ]
