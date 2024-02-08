import os
from django.db import connections
from django.contrib.auth.models import User
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "automations_gaulke_contabil.settings")

try:
    user = User.objects.get(username="andre_nepomuceno")

    user.set_password("gaulke_8088")
    user.save()
    print("Senha alterada com sucesso!")

except User.DoesNotExist:
    print("Usuário não encontrado.")
    exit()

