# Generated by Django 4.0.6 on 2023-03-09 19:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('management', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('faculty', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='facultyuser',
            name='department',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='management.department'),
        ),
        migrations.AddField(
            model_name='facultyuser',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]