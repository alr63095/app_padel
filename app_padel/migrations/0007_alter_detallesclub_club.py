# Generated by Django 4.2.5 on 2024-05-23 10:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_padel', '0006_alter_club_admin_id_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detallesclub',
            name='club',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='detalles', serialize=False, to='app_padel.club'),
        ),
    ]