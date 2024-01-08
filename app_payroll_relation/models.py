from django.db import models



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


    


