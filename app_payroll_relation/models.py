from django.db import models


class ModelContasGNRE_Estados_x_Contas(models.Model):
    conta_uf = models.CharField(max_length=2)
    conta_numero = models.IntegerField(default=0)
    conta_debito = models.IntegerField()

class ModelContasGNRE_Estados_x_Contas_MODELO_2(models.Model):
    conta_uf = models.CharField(max_length=2)
    conta_numero = models.IntegerField(default=0)
    conta_debito = models.IntegerField()

class ModelContasGNRE_Estados_x_Contas_MODELO_3(models.Model):
    conta_uf = models.CharField(max_length=2)
    conta_numero = models.IntegerField(default=0)
    conta_debito = models.IntegerField()


    


