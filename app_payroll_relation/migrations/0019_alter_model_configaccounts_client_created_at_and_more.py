# Generated by Django 4.2.6 on 2024-02-02 16:39

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_payroll_relation', '0018_model_plano_contas_de_para_antigo_x_novo_insert_jb_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='model_configaccounts_client',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 2, 2, 13, 39, 29, 419330)),
        ),
        migrations.AlterField(
            model_name='model_configaccounts_client',
            name='update_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 2, 2, 13, 39, 29, 419827)),
        ),
        migrations.AlterField(
            model_name='model_manualtags_username',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 2, 2, 13, 39, 29, 420823)),
        ),
        migrations.AlterField(
            model_name='model_manualtags_username',
            name='update_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 2, 2, 13, 39, 29, 420823)),
        ),
        migrations.AlterField(
            model_name='model_plano_contas_antigo_x_novo',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 2, 2, 13, 39, 29, 422323)),
        ),
        migrations.AlterField(
            model_name='model_plano_contas_antigo_x_novo',
            name='update_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 2, 2, 13, 39, 29, 422827)),
        ),
        migrations.AlterField(
            model_name='model_plano_contas_de_para_antigo_x_novo',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 2, 2, 13, 39, 29, 423371)),
        ),
        migrations.AlterField(
            model_name='model_plano_contas_de_para_antigo_x_novo',
            name='insert_JB',
            field=models.CharField(default='0', max_length=2),
        ),
        migrations.AlterField(
            model_name='model_plano_contas_de_para_antigo_x_novo',
            name='update_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 2, 2, 13, 39, 29, 423371)),
        ),
        migrations.AlterField(
            model_name='model_plano_contas_de_para_antigo_x_novo',
            name='update_at_JB',
            field=models.DateTimeField(default=datetime.datetime(2024, 2, 2, 13, 39, 29, 423371)),
        ),
    ]
