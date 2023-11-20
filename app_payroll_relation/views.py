import json
import requests
import pandas as pd
from datetime import datetime

from prepare_data.prepare_data import ConvertToDataFrame
from config_project import BASE_URL_API_GAULKE, HOST_REDIRECT

# from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth import login, logout
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required


from .models import ModelContasGNRE_Estados_x_Contas


def home_page(request):
    return render(request, "app/home.html")

def loginUser(request):
    if request.method == "GET":
        return render(request, "app/login.html")
    elif request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        # print(f"""
        #     username: {username}
        #     password: {password}
        # """)

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            context = {
                "username": username,
                "password": password,
                "error_credencials": True,
            }
            return render(request, "app/login.html", context=context)
    return

def logoutUser(request):
    logout(request)
    return redirect("login_user")

def error_404_view(request, exception):
    # data = {"rota_app_padrao": "http://app.contabilgaulke.com.br/automations"}
    # return JsonResponse(data=data)
    return render(request, "app/error_404.html")



# -------------------------------------------- IMPORTAÇÃO DE ARQUIVOS --------------------------------------------
@login_required(login_url="/automations/login/")
def post_file_fastAPI_comprovante_banco_do_brasil(request):
    if request.method == "GET":
        context = {
            "visible_form_file": True,
        }
        return render(request, "app_relations/relation_extrato_banco_do_brasil.html", context=context)
        
    elif request.method == "POST":
        file = request.FILES["file"]
        print(file)

        dataJson = ConvertToDataFrame.read_pdf_comprovante_banco_do_brasil(file=file)
        print(dataJson)
        context = {
            "code_process": True,
            "data_table": dataJson["data_table"]["data"],
            "list_page_erros": dataJson["list_page_erros"],

            "tt_rows": dataJson["tt_rows"],
            "tt_debit": dataJson["tt_debit"],
            "tt_credit": dataJson["tt_credit"],
            "host_port": HOST_REDIRECT,

        }
        
        return render(request, "app_relations/relation_extrato_banco_do_brasil.html", context=context)

# ------------------------
@login_required(login_url="/automations/login/")
def post_file_fastAPI_folha_por_empregado(request):
    if request.method == "GET":
        context = {
            "visible_form_file": True,
        }
        return render(request, "app_relations/relation_folha_de_pagamento.html", context=context)
        
    elif request.method == "POST":
        grupo_lancamento = request.POST.get("grupo_lancamento")
        file = request.FILES["file"]
        print(file)

        dataJson = ConvertToDataFrame.read_pdf_relacao_folha_por_empregado(file=file, grupo_lancamento=grupo_lancamento)
        print(dataJson)
        context = {
            "code_process": True,
            "data_table": dataJson["data_table"]["data"],
            "list_page_erros": dataJson["list_page_erros"],

            "tt_rows": dataJson["tt_rows"],
            "tt_debit": dataJson["tt_debit"],
            "tt_credit": dataJson["tt_credit"],
            "host_port": HOST_REDIRECT,

        }
        
        return render(request, "app_relations/relation_folha_de_pagamento.html", context=context)

# ------------------------
@login_required(login_url="/automations/login/")
def post_file_fastAPI_relacao_GNRE(request):
    if request.method == "GET":
        context = {
            "visible_form_file": True,
        }
        return render(request, "app_relations/relation_GNRE.html", context=context)
        
    elif request.method == "POST":
        print("\n\n ---------- IMPORTAÇÃO GNRE ---------- ")
        file = request.FILES["file"]
        # grupo_lancamento = request.POST.get("grupo_lancamento")
        modelo_db = request.POST.get("modelo_db")


        query_contas = ModelContasGNRE_Estados_x_Contas.objects.filter(modelo=modelo_db)
        
        data_contas = dict()
        for data in query_contas:
            data_contas.update(
                {
                    data.conta_uf:{
                        "conta_credito": data.conta_numero,
                        "conta_debito": data.conta_debito,
                }
            })

        print(f"\n\n ------------------------ ")
        print(data_contas)

        dataJson = ConvertToDataFrame.read_xlsx_relacao_gnre(file=file, data_contas=data_contas)
        print(dataJson)
        context = {
            "code_process": True,
            "data_table": dataJson["data_table"]["data"],
            "list_page_erros": dataJson["list_page_erros"],
            'data_contas': json.dumps(data_contas),

            "tt_rows": dataJson["tt_rows"],
            "tt_debit": dataJson["tt_debit"],
            "tt_credit": dataJson["tt_credit"],
            "host_port": HOST_REDIRECT,

        }
        
        return render(request, "app_relations/relation_GNRE.html", context=context)


# ------------------------
@login_required(login_url="/automations/login/")
def post_file_entrada_titulos_desc_sicoob(request):
    if request.method == "GET":
        context = {
            "visible_form_file": True,
        }
        return render(request, "app_relations/relation_entrada_titulos_desc_sicoob.html", context=context)
        
    elif request.method == "POST":
        file = request.FILES["file"]
        print(file)

        dataJson = ConvertToDataFrame.read_pdf_relacao_entrada_titulos_desc_sicoob(file=file)
        print(dataJson)
        context = {
            "code_process": True,
            "data_table": dataJson["data_table"]["data"],
            "list_page_erros": dataJson["list_page_erros"],

            "tt_rows": dataJson["tt_rows"],
            "tt_debit": dataJson["tt_debit"],
            "tt_credit": dataJson["tt_credit"],
            "host_port": HOST_REDIRECT,

        }
        
        return render(request, "app_relations/relation_entrada_titulos_desc_sicoob.html", context=context)

# ------------------------ DESENVOLVIMENTO ADIADO: PRIODADE ENTRADA DE TITULOS DESCONTADOS SICCOB
@login_required(login_url="/automations/login/")
def post_file_fastAPI_relacao_cobrancas_pagas(request):
    if request.method == "GET":
        context = {
            "visible_form_file": True,
        }
        return render(request, "app_relations/relation_cobrancas_pagas.html", context=context)
        
    elif request.method == "POST":
        print("\n\n ---------- IMPORTAÇÃO GNRE ---------- ")
        file = request.FILES["file"]

        dataJson = ConvertToDataFrame.read_xlsx_relacao_cobrancas_pagas(file=file)
        print(dataJson)
        context = {
            "code_process": True,
            "data_table": dataJson["data_table"]["data"],
            "list_page_erros": dataJson["list_page_erros"],

            "tt_rows": dataJson["tt_rows"],
            "tt_debit": dataJson["tt_debit"],
            "tt_credit": dataJson["tt_credit"],
            "host_port": HOST_REDIRECT,

        }
        
        return render(request, "app_relations/relation_cobrancas_pagas.html", context=context)







# ------------------------- TUTORIALS -------------------------
@login_required(login_url="/automations/login/")
def use_mode(request):
    if request.method == "GET":
        return render(request, "app_use/use_mode.html")
# ----
@login_required(login_url="/automations/login/")
def use_login_logout(request):
    if request.method == "GET":
        return render(request, "app_use/use_login_logout.html")
    
# ----
@login_required(login_url="/automations/login/")
def config_contas_gnre(request):
    if request.method == "GET":
        conta = ModelContasGNRE_Estados_x_Contas.objects.all()
        data = list()
        for i in conta:
            data.append({"uf": i.conta_uf, "conta": i.conta_numero, "conta_debito": i.conta_debito})
        print(data)
        context = {
            "contas": data,
        }
        return render(request, "app/config_contas_gnre.html", context=context)

    # ----
    elif request.method == "POST":
        try:
            body = json.loads(request.body)
            for data in body:
                print(data)
            
                conta  =  ModelContasGNRE_Estados_x_Contas.objects.filter(conta_uf=data["uf"]).first()
                
                if conta is not None:
                    conta.conta_numero = data["conta_credito"]
                    conta.conta_debito = data["conta_debito"]
                    conta.save()
                    print(f" -----> update account: {conta}")
                else:
                    conta = ModelContasGNRE_Estados_x_Contas.objects.create(
                        conta_uf = data["uf"],
                        conta_numero = data["conta_credito"],
                        conta_debito = data["conta_debito"],
                    ).save()
                    print(f" -----> new account: {conta}")

            return JsonResponse(
                {
                    "code": 200,
                    "msg": "success",
                })
        except Exception as e:
            print(f"\n\n ### ERROR UDATE/CREATE CONTA GNRE | ERROR: {e}")
            return JsonResponse(
                {
                    "code": 400,
                    "msg": "failed-update-create-conta-gnre",
                    "error": e,
                })


