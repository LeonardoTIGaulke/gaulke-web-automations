# Generated by Django 4.2.6 on 2024-01-18 18:39

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_payroll_relation', '0014_alter_model_configaccounts_client_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='model_configaccounts_client',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 18, 15, 39, 49, 350728)),
        ),
        migrations.AlterField(
            model_name='model_configaccounts_client',
            name='update_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 18, 15, 39, 49, 350728)),
        ),
        migrations.AlterField(
            model_name='model_manualtags_username',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 18, 15, 39, 49, 350728)),
        ),
        migrations.AlterField(
            model_name='model_manualtags_username',
            name='update_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 18, 15, 39, 49, 350728)),
        ),
        migrations.AlterField(
            model_name='model_plano_contas_antigo_x_novo',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 18, 15, 39, 49, 350728)),
        ),
        migrations.AlterField(
            model_name='model_plano_contas_antigo_x_novo',
            name='update_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 18, 15, 39, 49, 350728)),
        ),
    ]
