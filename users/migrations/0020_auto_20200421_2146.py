# Generated by Django 3.0.2 on 2020-04-22 01:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0019_auto_20200421_2005'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='comment_text',
            field=models.TextField(verbose_name='comment'),
        ),
    ]