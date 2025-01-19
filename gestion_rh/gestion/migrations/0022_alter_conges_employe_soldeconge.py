# Generated by Django 5.1.3 on 2025-01-17 05:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion', '0021_remove_soldeconge_employe_remove_salaire_absences_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conges',
            name='employe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestion.employe'),
        ),
        migrations.CreateModel(
            name='SoldeConge',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('solde_annuel', models.DecimalField(decimal_places=2, default=30, max_digits=5)),
                ('solde_maladie', models.DecimalField(decimal_places=2, default=15, max_digits=5)),
                ('solde_maternite', models.DecimalField(decimal_places=2, default=20, max_digits=5)),
                ('solde_sans_solde', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('solde_utilise_annuel', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('solde_utilise_maladie', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('solde_utilise_maternite', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('solde_utilise_sans_solde', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('employe', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='gestion.employe')),
            ],
        ),
    ]
