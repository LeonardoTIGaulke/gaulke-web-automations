from django.db import models


class Model_Config_Tags_By_USER(models.Model):
    user = models.CharField(max_length=55)
    activity_id = models.IntegerField()
    tag = models.CharField(max_length=55)






class Model_RelacaoContasFornecedores(models.Model):
    cnpj = models.CharField(max_length=25)
    nome = models.CharField(max_length=255)
    




class ModelContasGNRE_Estados_x_Contas(models.Model):
    conta_uf = models.CharField(max_length=2)
    conta_numero = models.IntegerField(default=0)
    conta_debito = models.IntegerField()
    modelo = models.CharField(max_length=25)

class ModelContasGNRE_Estados_x_Contas_MODELO_2(models.Model):
    conta_uf = models.CharField(max_length=2)
    conta_numero = models.IntegerField(default=0)
    conta_debito = models.IntegerField()
    modelo = models.CharField(max_length=25)

class ModelContasGNRE_Estados_x_Contas_MODELO_3(models.Model):
    conta_uf = models.CharField(max_length=2)
    conta_numero = models.IntegerField(default=0)
    conta_debito = models.IntegerField()
    modelo = models.CharField(max_length=25)


    


