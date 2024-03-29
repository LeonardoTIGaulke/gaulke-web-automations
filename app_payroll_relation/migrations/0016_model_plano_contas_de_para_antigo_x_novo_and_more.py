# Generated by Django 4.2.6 on 2024-01-19 18:03

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_payroll_relation', '0015_alter_model_configaccounts_client_created_at_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Model_Plano_Contas_De_Para_Antigo_x_Novo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pc_old', models.CharField(max_length=8)),
                ('pc_new', models.CharField(max_length=8)),
                ('code_old', models.CharField(max_length=8)),
                ('code_new', models.CharField(max_length=8)),
                ('username', models.CharField(max_length=55)),
                ('created_at', models.DateTimeField(default=datetime.datetime(2024, 1, 19, 15, 3, 1, 342428))),
                ('update_at', models.DateTimeField(default=datetime.datetime(2024, 1, 19, 15, 3, 1, 342428))),
            ],
        ),
        migrations.AlterField(
            model_name='model_configaccounts_client',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 19, 15, 3, 1, 342428)),
        ),
        migrations.AlterField(
            model_name='model_configaccounts_client',
            name='update_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 19, 15, 3, 1, 342428)),
        ),
        migrations.AlterField(
            model_name='model_manualtags_username',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 19, 15, 3, 1, 342428)),
        ),
        migrations.AlterField(
            model_name='model_manualtags_username',
            name='update_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 19, 15, 3, 1, 342428)),
        ),
        migrations.AlterField(
            model_name='model_plano_contas_antigo_x_novo',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 19, 15, 3, 1, 342428)),
        ),
        migrations.AlterField(
            model_name='model_plano_contas_antigo_x_novo',
            name='update_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 19, 15, 3, 1, 342428)),
        ),
    ]
