# Generated by Django 5.1.3 on 2025-01-18 17:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion', '0022_alter_conges_employe_soldeconge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='salaire',
            name='employe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestion.employe'),
        ),
    ]
