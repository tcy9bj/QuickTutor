# Generated by Django 3.0.2 on 2020-04-13 20:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tutor', '0013_ask_declined'),
        ('users', '0013_auto_20200413_1536'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='current_client',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='tutor.Ask'),
        ),
    ]