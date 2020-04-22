# Generated by Django 3.0.2 on 2020-04-22 00:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0018_auto_20200421_2004'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='reviewee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviewee', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='comment',
            name='reviewer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviewer', to=settings.AUTH_USER_MODEL),
        ),
    ]
