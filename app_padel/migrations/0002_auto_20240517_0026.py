# Generated by Django 2.2.28 on 2024-05-17 00:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_padel', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='club',
            name='admin_id',
            field=models.IntegerField(default=0),
        ),
    ]
