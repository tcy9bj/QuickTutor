# Generated by Django 3.0.2 on 2020-04-13 19:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_profile_current_client'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='num_ratings',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='profile',
            name='tutor_score',
            field=models.DecimalField(decimal_places=2, max_digits=2, null=True),
        ),
    ]