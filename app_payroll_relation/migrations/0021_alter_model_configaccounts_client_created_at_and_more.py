# Generated by Django 4.2.6 on 2024-02-02 16:47

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_payroll_relation', '0020_alter_model_configaccounts_client_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='model_configaccounts_client',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 2, 2, 13, 47, 46, 778733)),
        ),
        migrations.AlterField(
            model_name='model_configaccounts_client',
            name='update_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 2, 2, 13, 47, 46, 778733)),
        ),
        migrations.AlterField(
            model_name='model_manualtags_username',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 2, 2, 13, 47, 46, 779733)),
        ),
        migrations.AlterField(
            model_name='model_manualtags_username',
            name='update_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 2, 2, 13, 47, 46, 779733)),
        ),
        migrations.AlterField(
            model_name='model_plano_contas_antigo_x_novo',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 2, 2, 13, 47, 46, 780733)),
        ),
        migrations.AlterField(
            model_name='model_plano_contas_antigo_x_novo',
            name='update_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 2, 2, 13, 47, 46, 780733)),
        ),
        migrations.AlterField(
            model_name='model_plano_contas_de_para_antigo_x_novo',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 2, 2, 13, 47, 46, 781733)),
        ),
        migrations.AlterField(
            model_name='model_plano_contas_de_para_antigo_x_novo',
            name='update_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 2, 2, 13, 47, 46, 781733)),
        ),
        migrations.AlterField(
            model_name='model_plano_contas_de_para_antigo_x_novo',
            name='update_at_JB',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]