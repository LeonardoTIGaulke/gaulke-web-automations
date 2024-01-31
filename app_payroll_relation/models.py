from django.db import models
from datetime import datetime
from dateutil import tz

class Model_ConfigAccounts_Client(models.Model):
    id_company = models.CharField(max_length=8)
    code_account = models.CharField(max_length=8)
    created_at = models.DateTimeField(default=datetime.now(tz=tz.gettz("America/Sao Paulo")))
    update_at = models.DateTimeField(default=datetime.now(tz=tz.gettz("America/Sao Paulo")))
    


class Model_DynamicTags_Username(models.Model):
    username = models.CharField(max_length=55)
    numero_conta_debito = models.CharField(max_length=7)
    tags = models.CharField(max_length=155)
    decription_rule = models.CharField(max_length=125)

class Model_ManualTags_Username(models.Model):
    username = models.CharField(max_length=55)
    id_company = models.CharField(max_length=8)
    numero_conta_debito = models.CharField(max_length=7)
    tag = models.CharField(max_length=155)
    created_at = models.DateTimeField(default=datetime.now(tz=tz.gettz("America/Sao Paulo")))
    update_at = models.DateTimeField(default=datetime.now(tz=tz.gettz("America/Sao Paulo")))
    # decription_rule = models.CharField(max_length=125)
    # cnpj_cpf = models.CharField(max_length=25)
    # company = models.CharField(max_length=125)
    # numero_conta_credito = models.CharField(max_length=7)

class Model_RelacaoContas_Fornecedores(models.Model):
    cnpj = models.CharField(max_length=25)
    nome = models.CharField(max_length=255)
    

class ModelContasGNRE_Estados_X_Contas(models.Model):
    conta_uf = models.CharField(max_length=2)
    conta_numero = models.IntegerField(default=0)
    conta_debito = models.IntegerField()
    modelo = models.CharField(max_length=25)


    

# --------------------------------------- MODELOS PARA PLANO DE CONTAS --> ANTIGO X NOVO ---------------------------------------
class Model_Plano_Contas_Antigo_x_Novo(models.Model):
    type_accounts = models.CharField(max_length=8)
    old_account_code = models.CharField(max_length=8)
    new_account_code = models.CharField(max_length=8)
    created_at = models.DateTimeField(default=datetime.now(tz=tz.gettz("America/Sao Paulo")))
    update_at = models.DateTimeField(default=datetime.now(tz=tz.gettz("America/Sao Paulo")))

class Model_Plano_Contas_De_Para_Antigo_x_Novo(models.Model):

    company_code = models.CharField(max_length=8)
    pc_old = models.CharField(max_length=8)
    pc_new = models.CharField(max_length=8)
    code_old = models.CharField(max_length=8)
    code_new = models.CharField(max_length=8)
    
    username = models.CharField(max_length=55)
    created_at = models.DateTimeField(default=datetime.now(tz=tz.gettz("America/Sao Paulo")))
    update_at = models.DateTimeField(default=datetime.now(tz=tz.gettz("America/Sao Paulo")))

# class Model_Nomes_Plano_de_Contas_Antigo:
#     code_pc = models.CharField(max_length=8)
#     description_pc = models.CharField(max_length=8)
#     created_at = models.DateTimeField(default=datetime.now(tz=tz.gettz("America/Sao Paulo")))
#     update_at = models.DateTimeField(default=datetime.now(tz=tz.gettz("America/Sao Paulo")))
# class Model_Nomes_Plano_de_Contas_Novo:
#     code_pc = models.CharField(max_length=8)
#     description_pc = models.CharField(max_length=8)
#     created_at = models.DateTimeField(default=datetime.now(tz=tz.gettz("America/Sao Paulo")))
#     update_at = models.DateTimeField(default=datetime.now(tz=tz.gettz("America/Sao Paulo")))


