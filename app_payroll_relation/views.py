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
# ------------------------
@login_required(login_url="/automations/login/")
def post_file_fastAPI_folha_por_empregado(request):
    if request.method == "GET":
        context = {
            "visible_form_file": True,
        }
        return render(request, "app_relations/relation_folha_de_pagamento.html", context=context)
        
    elif request.method == "POST":
        try:
            username = request.POST.get("username")
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
            print(f" ### PROCESSO FINALIZADO POR: {username}")
            
            return render(request, "app_relations/relation_folha_de_pagamento.html", context=context)
        except Exception as e:
            context = {
                "error_code": True,
                "visible_form_file": True
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
        try:
            username = request.POST.get("username")
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
            print(f" ### PROCESSO FINALIZADO POR: {username}")
            return render(request, "app_relations/relation_GNRE.html", context=context)
        except Exception as e:
            context = {
                "error_code": True,
                "visible_form_file": True
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
        try:
            username = request.POST.get("username")
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
            print(f" ### PROCESSO FINALIZADO POR: {username}")
            return render(request, "app_relations/relation_entrada_titulos_desc_sicoob.html", context=context)
        except Exception as e:
            context = {
                "error_code": True,
                "visible_form_file": True
            }
            return render(request, "app_relations/relation_entrada_titulos_desc_sicoob.html", context=context)

# ------------------------
@login_required(login_url="/automations/login/")
def post_file_fastAPI_relacao_cobrancas_pagas(request):
    if request.method == "GET":
        context = {
            "visible_form_file": True,
        }
        return render(request, "app_relations/relation_cobrancas_pagas.html", context=context)
        
    elif request.method == "POST":
        print("\n\n ---------- IMPORTAÇÃO COBRANÇAS PAGAS ---------- ")
        try:
            username = request.POST.get("username")
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
            print(f" ### PROCESSO FINALIZADO POR: {username}")
            return render(request, "app_relations/relation_cobrancas_pagas.html", context=context)
        except Exception as e:
            context = {
                "error_code": True,
                "visible_form_file": True
            }
            return render(request, "app_relations/relation_cobrancas_pagas.html", context=context)

# ------------------------
@login_required(login_url="/automations/login/")
def post_file_fastAPI_relacao_decorise(request):
    if request.method == "GET":
        context = {
            "visible_form_file": True,
        }
        return render(request, "app_relations/relation_decorise.html", context=context)
        
    elif request.method == "POST":
        print("\n\n ---------- IMPORTAÇÃO DECORISE ---------- ")
        try:
            username = request.POST.get("username")
            file = request.FILES["file"]
            grupo_lancamento = request.POST.get("grupo_lancamento")
            print(f"\n--------------->> GRUPO LANÇ: {grupo_lancamento}")

            dataJson = ConvertToDataFrame.read_xlsx_decorise(file=file, grupo_lancamento=grupo_lancamento)
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
            print(f" ### PROCESSO FINALIZADO POR: {username}")
            return render(request, "app_relations/relation_decorise.html", context=context)
        except Exception as e:
            context = {
                "error_code": True,
                "visible_form_file": True
            }
            return render(request, "app_relations/relation_decorise.html", context=context)

# ------------------------
@login_required(login_url="/automations/login/")
def post_file_fastAPI_relacao_arao_dos_santos(request):
    if request.method == "GET":
        context = {
            "visible_form_file": True,
        }
        return render(request, "app_relations/relation_arao_dos_santos.html", context=context)
        
    elif request.method == "POST":
        print("\n\n ---------- IMPORTAÇÃO ARÃO DOS SANTOS ---------- ")
        try:
            username = request.POST.get("username")
            modelo = request.POST.get("modelo")
            file = request.FILES["file"]
            file_2 = request.FILES["file_2"]


        
            dataJson = ConvertToDataFrame.read_xlsx_arao_dos_santos(file_consulta=file,file_contabil=file_2, modelo=modelo)
            # print(dataJson)
            context = {
                "code_process": True,
                "data_table": dataJson["data_table"]["data"],
                "data_table_03": dataJson["data_json_03"]["data"],
                "df_json_pendencias": dataJson["df_json_pendencias"]["data"],
                "list_page_erros": dataJson["list_page_erros"],

                "btn_pendencias": dataJson["btn_pendencias"],
                "tt_pendencias": dataJson["tt_pendencias"],
                "tt_rows": dataJson["tt_rows"],
                "tt_debit": dataJson["tt_debit"],
                "tt_credit": dataJson["tt_credit"],
                "tt_rows_03": dataJson["tt_rows_03"],
                "tt_debit_03": dataJson["tt_debit_03"],
                "tt_credit_03": dataJson["tt_credit_03"],
                "host_port": HOST_REDIRECT,

            }
            print(f" ### PROCESSO FINALIZADO POR: {username} | MODELO ARQUIVO CONSULTA: {modelo}")
            return render(request, "app_relations/relation_arao_dos_santos.html", context=context)
        except Exception as e:
            context = {
                "error_code": True,
                "visible_form_file": True
            }
            return render(request, "app_relations/relation_arao_dos_santos.html", context=context)

# ------------------------
@login_required(login_url="/automations/login/")
def post_file_fastAPI_relacao_grupo_DAB(request):
    # print(request.user.username)
    if request.method == "GET":
        context = {
            "visible_form_file": True,
            "post_file": "/automations/relacao-grupo-DAB/",
            "info_01": "Importação Grupo DAB",
        }
        return render(request, "app_relations/relation_grupo_DAB.html", context=context)
        
    elif request.method == "POST":
        try:
            username = request.POST.get("username")
            file = request.FILES["file"]
            file_2 = request.FILES["file_2"]

            print(file)
            print(file_2)

            dataJson = ConvertToDataFrame.read_xls_comprovante_grupo_DAB(file_suppliers=file, file_payments=file_2)
            # print(dataJson)
            context = {
                "code_process": True,
                "data_table": dataJson["data_table"]["data"],
                "list_page_erros": dataJson["list_page_erros"],

                "tt_rows": dataJson["tt_rows"],
                "tt_debit": dataJson["tt_debit"],
                "tt_credit": dataJson["tt_credit"],
                "host_port": HOST_REDIRECT,

            }
            print(f" ### PROCESSO FINALIZADO POR: {username}")
            return render(request, "app_relations/relation_grupo_DAB.html", context=context)
        except Exception as e:
            context = {
                "error_code": True,
                "error": e,
                "visible_form_file": True
            }
            return render(request, "app_relations/relation_grupo_DAB.html", context=context)




# ----------------------------------------------------------------------------
# ------------------------ COMPROVANTES DE PAGAMENTOS ------------------------
# ----------------------------------------------------------------------------
@login_required(login_url="/automations/login/")
def post_file_fastAPI_comprovante_banco_do_brasil(request):
    if request.method == "GET":
        context = {
            "visible_form_file": True,
        }
        return render(request, "app_relations/relation_extrato_banco_do_brasil.html", context=context)
        
    elif request.method == "POST":
        try:
            username = request.POST.get("username")
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
            print(f" ### PROCESSO FINALIZADO POR: {username}")
            return render(request, "app_relations/relation_extrato_banco_do_brasil.html", context=context)
        except Exception as e:
            context = {
                "error_code": True,
                "visible_form_file": True
            }
            return render(request, "app_relations/relation_extrato_banco_do_brasil.html", context=context)

# ------------------------
@login_required(login_url="/automations/login/")
def post_file_fastAPI_comprovante_banco_bradesco(request):
    # print(request.user.username)
    if request.method == "GET":
        context = {
            "visible_form_file": True,
        }
        return render(request, "app_relations/relation_extrato_banco_bradesco.html", context=context)
        
    elif request.method == "POST":
        try:
            username = request.POST.get("username")
            file = request.FILES["file"]
            print(file)

            dataJson = ConvertToDataFrame.read_pdf_comprovante_banco_bradesco(file=file)
            # print(dataJson)
            context = {
                "code_process": True,
                "data_table": dataJson["data_table"]["data"],
                "list_page_erros": dataJson["list_page_erros"],

                "tt_rows": dataJson["tt_rows"],
                "tt_debit": dataJson["tt_debit"],
                "tt_credit": dataJson["tt_credit"],
                "host_port": HOST_REDIRECT,

            }
            print(f" ### PROCESSO FINALIZADO POR: {username}")
            return render(request, "app_relations/relation_extrato_banco_bradesco.html", context=context)
        except Exception as e:
            context = {
                "error_code": True,
                "visible_form_file": True
            }
            return render(request, "app_relations/relation_extrato_banco_bradesco.html", context=context)
        
# ------------------------
@login_required(login_url="/automations/login/")
def post_file_fastAPI_comprovante_banco_sicredi(request):
    # print(request.user.username)
    if request.method == "GET":
        context = {
            "visible_form_file": True,
        }
        return render(request, "app_relations/relation_extrato_banco_sicredi.html", context=context)
        
    elif request.method == "POST":
        try:
            username = request.POST.get("username")
            # modelo_empresa = request.POST.get("modelo_empresa")

            file = request.FILES["file"]
            print(file)

        
            dataJson = ConvertToDataFrame.read_pdf_comprovante_banco_sicredi(file=file)
            # print(dataJson)
            context = {
                "code_process": True,
                "data_table": dataJson["data_table"]["data"],
                "list_page_erros": dataJson["list_page_erros"],

                "tt_rows": dataJson["tt_rows"],
                "tt_debit": dataJson["tt_debit"],
                "tt_credit": dataJson["tt_credit"],
                "host_port": HOST_REDIRECT,

            }
            print(f" ### PROCESSO FINALIZADO POR: {username}")
            return render(request, "app_relations/relation_extrato_banco_sicredi.html", context=context)
        except Exception as e:
            context = {
                "error_code": True,
                "visible_form_file": True
            }
            return render(request, "app_relations/relation_extrato_banco_sicredi.html", context=context)

# ------------------------
@login_required(login_url="/automations/login/")
def post_file_fastAPI_comprovante_banco_sicoob(request):
    # print(request.user.username)
    if request.method == "GET":
        context = {
            "visible_form_file": True,
        }
        return render(request, "app_relations/relation_extrato_banco_sicoob.html", context=context)
        
    elif request.method == "POST":
        try:
            username = request.POST.get("username")
            # modelo_empresa = request.POST.get("modelo_empresa")

            file = request.FILES["file"]
            print(file)

        
            dataJson = ConvertToDataFrame.read_pdf_comprovante_banco_sicoob(file=file)
            # print(dataJson)
            context = {
                "code_process": True,
                "data_table": dataJson["data_table"]["data"],
                "list_page_erros": dataJson["list_page_erros"],

                "tt_rows": dataJson["tt_rows"],
                "tt_debit": dataJson["tt_debit"],
                "tt_credit": dataJson["tt_credit"],
                "host_port": HOST_REDIRECT,

            }
            print(f" ### PROCESSO FINALIZADO POR: {username}")
            return render(request, "app_relations/relation_extrato_banco_sicoob.html", context=context)
        except Exception as e:
            context = {
                "error_code": True,
                "visible_form_file": True
            }
            return render(request, "app_relations/relation_extrato_banco_sicoob.html", context=context)

# ------------------------
@login_required(login_url="/automations/login/")
def post_file_fastAPI_comprovante_itau(request):
    # print(request.user.username)
    if request.method == "GET":
        context = {
            "visible_form_file": True,
        }
        return render(request, "app_relations/relation_extrato_banco_itau.html", context=context)
        
    elif request.method == "POST":
        try:
            username = request.POST.get("username")
            # modelo_empresa = request.POST.get("modelo_empresa")

            file = request.FILES["file"]
            print(file)

        
            dataJson = ConvertToDataFrame.read_xls_comprovante_banco_itau(file=file)
            # print(dataJson)
            context = {
                "code_process": True,
                # "data_table": dataJson["data_table"]["data"],
                # "list_page_erros": dataJson["list_page_erros"],

                # "tt_rows": dataJson["tt_rows"],
                # "tt_debit": dataJson["tt_debit"],
                # "tt_credit": dataJson["tt_credit"],
                "host_port": HOST_REDIRECT,

            }
            print(f" ### PROCESSO FINALIZADO POR: {username}")
            return render(request, "app_relations/relation_extrato_banco_itau.html", context=context)
        except Exception as e:
            context = {
                "error_code": True,
                "visible_form_file": True
            }
            return render(request, "app_relations/relation_extrato_banco_itau.html", context=context)





# ------------------------------------------------------------
# ------------------------ DASHBOARDS ------------------------
# ------------------------------------------------------------
@login_required(login_url="/automations/login/")
def dashboard_visao_geral(request):
    if request.method == "GET":
        return render(request, "app_dashboard/dashboard_visao_geral.html")
    return render(request, "app/error_404.html")





# ------------------------------------------------------------
# ------------------------ TUTORIALS -------------------------
# ------------------------------------------------------------
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


