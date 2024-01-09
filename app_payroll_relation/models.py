from django.db import models


class Model_DynamicTags_Username(models.Model):
    username = models.CharField(max_length=55)
    numero_conta_debito = models.CharField(max_length=7)
    tags = models.CharField(max_length=155)
    decription_rule = models.CharField(max_length=125)


class Model_RelacaoContas_Fornecedores(models.Model):
    cnpj = models.CharField(max_length=25)
    nome = models.CharField(max_length=255)
    

class ModelContasGNRE_Estados_X_Contas(models.Model):
    conta_uf = models.CharField(max_length=2)
    conta_numero = models.IntegerField(default=0)
    conta_debito = models.IntegerField()
    modelo = models.CharField(max_length=25)


    


