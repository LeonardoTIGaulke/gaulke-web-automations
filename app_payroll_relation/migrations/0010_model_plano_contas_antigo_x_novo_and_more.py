# Generated by Django 4.2.6 on 2024-01-18 14:34

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_payroll_relation', '0009_model_configaccounts_client_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Model_Plano_Contas_Antigo_x_Novo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_accounts', models.CharField(max_length=8)),
                ('old_account_code', models.CharField(max_length=8)),
                ('new_account_code', models.CharField(max_length=8)),
                ('created_at', models.DateTimeField(default=datetime.datetime(2024, 1, 18, 11, 34, 29, 599483))),
                ('update_at', models.DateTimeField(default=datetime.datetime(2024, 1, 18, 11, 34, 29, 599483))),
            ],
        ),
        migrations.AlterField(
            model_name='model_configaccounts_client',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 18, 11, 34, 29, 583865)),
        ),
        migrations.AlterField(
            model_name='model_configaccounts_client',
            name='update_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 18, 11, 34, 29, 583865)),
        ),
        migrations.AlterField(
            model_name='model_manualtags_username',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 18, 11, 34, 29, 583865)),
        ),
        migrations.AlterField(
            model_name='model_manualtags_username',
            name='update_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 18, 11, 34, 29, 583865)),
        ),
    ]
