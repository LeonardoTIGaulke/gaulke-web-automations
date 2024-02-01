import json
import requests
import pandas as pd
from datetime import datetime
from dateutil import tz

from prepare_data.prepare_data import ConvertToDataFrame
from config_project import BASE_URL_API_GAULKE, HOST_REDIRECT

# from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth import login, logout
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required


from .models import ModelContasGNRE_Estados_X_Contas, Model_DynamicTags_Username, Model_ManualTags_Username, Model_Plano_Contas_De_Para_Antigo_x_Novo
from .models import Model_ConfigAccounts_Client

from django.db import connections
from config_project import DB_DATABASE_GAULKE_CONTABIL_TABLE_NAME, DB_DATABASE_TABLE_NAME_PLANO_CONTAS

@login_required(login_url="/automations/login/")
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
            company_session = request.POST.get("company_session")
            file = request.FILES["file"]
            print(file)

            dataJson = ConvertToDataFrame.read_pdf_relacao_folha_por_empregado(file=file, grupo_lancamento=grupo_lancamento, company_session=company_session)
            print(dataJson)
            context = {
                "code_process": True,
                "company_session": company_session,
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
            company_session = request.POST.get("company_session")
            file = request.FILES["file"]
            # grupo_lancamento = request.POST.get("grupo_lancamento")
            modelo_db = request.POST.get("modelo_db")


            query_contas = ModelContasGNRE_Estados_X_Contas.objects.filter(modelo=modelo_db)
            
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

            dataJson = ConvertToDataFrame.read_xlsx_relacao_gnre(file=file, data_contas=data_contas, company_session=company_session)
            print(dataJson)
            context = {
                "code_process": True,
                "company_session": company_session,
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
            company_session = request.POST.get("company_session")
            file = request.FILES["file"]
            print(file)

            dataJson = ConvertToDataFrame.read_pdf_relacao_entrada_titulos_desc_sicoob(file=file, company_session=company_session)
            print(dataJson)
            context = {
                "code_process": True,
                "company_session": company_session,
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
            company_session = request.POST.get("company_session")
            file = request.FILES["file"]

            dataJson = ConvertToDataFrame.read_xlsx_relacao_cobrancas_pagas(file=file, company_session=company_session)
            print(dataJson)
            context = {
                "code_process": True,
                "company_session": company_session,
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
            company_session = request.POST.get("company_session")
            file = request.FILES["file"]
            grupo_lancamento = request.POST.get("grupo_lancamento")
            print(f"\n--------------->> GRUPO LANÇ: {grupo_lancamento}")

            dataJson = ConvertToDataFrame.read_xlsx_decorise(file=file, grupo_lancamento=grupo_lancamento, company_session=company_session)
            print(dataJson)
            context = {
                "code_process": True,
                "company_session": company_session,
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
            company_session = request.POST.get("company_session")
            modelo = request.POST.get("modelo")
            file = request.FILES["file"]
            file_2 = request.FILES["file_2"]


        
            dataJson = ConvertToDataFrame.read_xlsx_arao_dos_santos(file_consulta=file,file_contabil=file_2, modelo=modelo, company_session=company_session)
            # print(dataJson)
            context = {
                "code_process": True,
                "company_session": company_session,
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
            company_session = request.POST.get("company_session")
            file = request.FILES["file"]
            file_2 = request.FILES["file_2"]

            print(file)
            print(file_2)

            dataJson = ConvertToDataFrame.read_xls_comprovante_grupo_DAB(file_suppliers=file, file_payments=file_2, company_session=company_session)
            # print(dataJson)
            context = {
                "code_process": True,
                "company_session": company_session,
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

# ------------------------
@login_required(login_url="/automations/login/")
def post_file_fastAPI_relacao_contas_a_receber_inova(request):
    # print(request.user.username)
    if request.method == "GET":
        context = {
            "visible_form_file": True,
        }
        return render(request, "app_relations/relation_contas_a_receber_inova.html", context=context)
        
    elif request.method == "POST":
        try:
            username = request.POST.get("username")
            company_session = request.POST.get("company_session")
            file = request.FILES["file"]
            print(file)

            dataJson = ConvertToDataFrame.read_xlsx_contas_a_receber_INOVA(file=file, company_session=company_session)
            
            context = {
                "code_process": True,
                "company_session": company_session,
                "data_table": dataJson["data_table"]["data"],
                "list_page_erros": dataJson["list_page_erros"],

                "tt_rows": dataJson["tt_rows"],
                "tt_debit": dataJson["tt_debit"],
                "tt_credit": dataJson["tt_credit"],
                "host_port": HOST_REDIRECT,
            }
            # print(context)
            print(f" ### PROCESSO FINALIZADO POR: {username}")
            return render(request, "app_relations/relation_contas_a_receber_inova.html", context=context)
        except Exception as e:
            context = {
                "error_code": True,
                "visible_form_file": True
            }
            return render(request, "app_relations/relation_contas_a_receber_inova.html", context=context)
        
# ------------------------
@login_required(login_url="/automations/login/")
def post_file_fastAPI_relacao_contas_a_pagar_ponto_certo(request):
    # print(request.user.username)
    if request.method == "GET":
        context = {
            "visible_form_file": True,
        }
        return render(request, "app_relations/relation_contas_a_pagar_ponto_certo.html", context=context)
        
    elif request.method == "POST":
        try:

            username = request.POST.get("username")
            company_session = request.POST.get("company_session")
            file = request.FILES["file"]
            file_2 = request.FILES["file_2"]
            dataJson = ConvertToDataFrame.read_xlsx_contas_a_pagar_PONTO_CERTO(file=file, file_2=file_2, company_session=company_session)
            
            context = {
                "code_process": True,
                "company_session": company_session,
                "data_table": dataJson["data_table"]["data"],
                "list_page_erros": dataJson["list_page_erros"],

                "tt_rows": dataJson["tt_rows"],
                "tt_debit": dataJson["tt_debit"],
                "tt_credit": dataJson["tt_credit"],
                "host_port": HOST_REDIRECT,
            }
            # print(context)
            print(f" ### PROCESSO FINALIZADO POR: {username}")
            return render(request, "app_relations/relation_contas_a_pagar_ponto_certo.html", context=context)
        except Exception as e:
            context = {
                "error_code": True,
                "visible_form_file": True
            }
            return render(request, "app_relations/relation_contas_a_pagar_ponto_certo.html", context=context)

 # ------------------------       

# ------------------------
def post_file_fastAPI_relacao_contas_a_pagar_garra(request):
    # print(request.user.username)
    if request.method == "GET":
        context = {
            "visible_form_file": True,
        }
        return render(request, "app_relations/relation_contas_a_pagar_garra.html", context=context)
        
    elif request.method == "POST":
        try:
            username = request.POST.get("username")
            company_session = request.POST.get("company_session")
            file = request.FILES["file"]
            dataJson = ConvertToDataFrame.read_xlsx_contas_a_pagar_GARRA(file=file, company_session=company_session)
            
            context = {
                "code_process": True,
                "company_session": company_session,
                "data_table": dataJson["data_table"]["data"],
                "list_page_erros": dataJson["list_page_erros"],

                "tt_rows": dataJson["tt_rows"],
                "tt_debit": dataJson["tt_debit"],
                "tt_credit": dataJson["tt_credit"],
                "host_port": HOST_REDIRECT,
            }
            # print(context)
            print(f" ### PROCESSO FINALIZADO POR: {username}")
            return render(request, "app_relations/relation_contas_a_pagar_garra.html", context=context)
        except Exception as e:
            context = {
                "error_code": True,
                "visible_form_file": True
            }
            return render(request, "app_relations/relation_contas_a_pagar_garra.html", context=context)

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
            company_session = request.POST.get("company_session")
            file = request.FILES["file"]
            print(file)

            # dataJson = ConvertToDataFrame.read_pdf_comprovante_banco_do_brasil(file=file, company_session=company_session)
            dataJson = ConvertToDataFrame.read_pdf_comprovante_banco_do_brasil_v2(file=file, company_session=company_session)
            # print(dataJson)
            context = {
                "code_process": True,
                "company_session": company_session,
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
            company_session = request.POST.get("company_session")
            file = request.FILES["file"]
            print(file)

            print(f"\n\n\n\n\n\n ------- company_session ------- ")
            print(company_session)

            dataJson = ConvertToDataFrame.read_pdf_comprovante_banco_bradesco(file=file, company_session=company_session)
            # print(dataJson)
            context = {
                "code_process": True,
                "company_session": company_session,
                "data_table": dataJson["data_table"]["data"],
                "df_tags_json": dataJson["df_tags_json"]["data"],
                "list_page_erros": dataJson["list_page_erros"],

                "tt_rows": dataJson["tt_rows"],
                "tt_debit": dataJson["tt_debit"],
                "tt_credit": dataJson["tt_credit"],
                "host_port": HOST_REDIRECT,

            }
            print(f" ### PROCESSO FINALIZADO POR: {username} | company_session: {company_session}")
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
            company_session = request.POST.get("company_session")
            # modelo_empresa = request.POST.get("modelo_empresa")

            file = request.FILES["file"]
            print(file)

        
            dataJson = ConvertToDataFrame.read_pdf_comprovante_banco_sicredi(file=file, company_session=company_session)
            # print(dataJson)
            context = {
                "code_process": True,
                "company_session": company_session,
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
            company_session = request.POST.get("company_session")
            # modelo_empresa = request.POST.get("modelo_empresa")

            file = request.FILES["file"]
            print(file)

        
            dataJson = ConvertToDataFrame.read_pdf_comprovante_banco_sicoob(file=file, company_session=company_session)
            # print(dataJson)
            context = {
                "code_process": True,
                "company_session": company_session,
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
            company_session = request.POST.get("company_session")
            type_file = request.POST.get("type_file")
            print(f"\n\n ---------> type_file: {type_file}")

            file = request.FILES["file"]
            print(file)

            if type_file == "modelo_xls":
                dataJson = ConvertToDataFrame.read_xls_comprovante_banco_itau(file=file, company_session=company_session)
            else:
                dataJson = ConvertToDataFrame.read_pdf_comprovante_banco_itau(file=file, company_session=company_session)


            # print(dataJson)
            context = {
                "code_process": True,
                "company_session": company_session,
                "data_table": dataJson["data_table"]["data"],
                "list_page_erros": dataJson["list_page_erros"],

                "tt_rows": dataJson["tt_rows"],
                "tt_debit": dataJson["tt_debit"],
                "tt_credit": dataJson["tt_credit"],
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

# ------------------------
@login_required(login_url="/automations/login/")
def post_file_fastAPI_comprovante_civia(request):
    # print(request.user.username)
    if request.method == "GET":
        context = {
            "visible_form_file": True,
        }
        return render(request, "app_relations/relation_extrato_banco_civia.html", context=context)
        
    elif request.method == "POST":
        try:
            username = request.POST.get("username")
            company_session = request.POST.get("company_session")
            file = request.FILES["file"]
            print(file)

            
            dataJson = ConvertToDataFrame.read_pdf_comprovante_banco_civia(file=file, company_session=company_session)


            # print(dataJson)
            context = {
                "code_process": True,
                "company_session": company_session,
                "data_table": dataJson["data_table"]["data"],
                "list_names": dataJson["list_names"],
                "list_page_erros": dataJson["list_page_erros"],

                "tt_rows": dataJson["tt_rows"],
                "tt_debit": dataJson["tt_debit"],
                "tt_credit": dataJson["tt_credit"],
                "host_port": HOST_REDIRECT,

            }
            print(f" ### PROCESSO FINALIZADO POR: {username}")
            return render(request, "app_relations/relation_extrato_banco_civia.html", context=context)
        except Exception as e:
            context = {
                "error_code": True,
                "visible_form_file": True
            }
            return render(request, "app_relations/relation_extrato_banco_civia.html", context=context)


# -------------------------------------------------------------------
# ------------------------ CRIAÇÃO DE REGRAS ------------------------
# -------------------------------------------------------------------

def query_all_companies():
    obj_all_companies = list()
    all_companies = connections["db_gaulke_contabil"]
    with all_companies.cursor() as cursor:
        cursor.execute(f'SELECT id_acessorias, cnpj, razao_social FROM {DB_DATABASE_GAULKE_CONTABIL_TABLE_NAME} order by razao_social ASC;')
        rows = cursor.fetchall()

        for result in rows:
            obj_all_companies.append( {"id_acessorias": result[0], "cnpj": result[1], "razao_social": result[2]} )

        # print(obj_all_companies)

    obj_all_companies = pd.DataFrame.from_dict(data=obj_all_companies, orient="columns")

    return obj_all_companies
        


# ---------------------------------------------------------------------------------
# -------------------------------- CREATE NEW RULE --------------------------------
# ---------------------------------------------------------------------------------
@login_required(login_url="/automations/login/")
def get_all_companies_clients(request):
    if request.method == "GET":
        obj_all_companies = list()

        data_accounts = dict()
        query_code_accounts = Model_ConfigAccounts_Client.objects.all()
        for x in query_code_accounts:
            data_accounts.update({
                x.id_company: x.code_account
            })
            # print(f" --> code_account: {x.code_account}")
        
        print("\n >> clientes com plano de contas")
        print(data_accounts)

        all_companies = connections["db_gaulke_contabil"]
        with all_companies.cursor() as cursor:
            cursor.execute(f'SELECT id_acessorias, cnpj, razao_social FROM {DB_DATABASE_GAULKE_CONTABIL_TABLE_NAME} order by razao_social ASC;')
            rows = cursor.fetchall()

            for result in rows:
                company_code = data_accounts.get(result[0])
                if company_code is None:
                    company_code = "-"
                obj_all_companies.append( {"id_client": result[0], "cnpj": result[1], "razao_social": result[2], "company_code": company_code} )
                
        return JsonResponse({"code": 200, "data": obj_all_companies})



@login_required(login_url="/automations/login/")
def get_all_companies_clients_generic(request):
    if request.method == "GET":
        obj_all_companies = list()
        all_companies = connections["db_gaulke_contabil"]
        with all_companies.cursor() as cursor:
            cursor.execute(f'SELECT id_acessorias, cnpj, razao_social FROM {DB_DATABASE_GAULKE_CONTABIL_TABLE_NAME} order by razao_social ASC;')
            rows = cursor.fetchall()

            for result in rows:
                obj_all_companies.append( { "id_client": result[0], "cnpj": result[1], "razao_social": result[2] } )
                
        return obj_all_companies

def get_all_plano_de_contas_generic():
    obj_plano_contas_old = list()
    obj_plano_contas_new = list()
    all_companies = connections["default"]
    with all_companies.cursor() as cursor:
        comand_query = f'''
            SELECT id, type_PC, code_pc, description_pc from {DB_DATABASE_TABLE_NAME_PLANO_CONTAS};
        '''
        cursor.execute(comand_query)
        rows = cursor.fetchall()
        print(comand_query)

        for result in rows:
            if result[1] == "old_PC":
                obj_plano_contas_old.append( { "id": result[0], "type_PC": result[1], "code_pc": result[2], "description_pc": result[3] } )
            else:
                obj_plano_contas_new.append( { "id": result[0], "type_PC": result[1], "code_pc": result[2], "description_pc": result[3] } )
            
    return [obj_plano_contas_old, obj_plano_contas_new]
    
@login_required(login_url="/automations/login/")
def query_account_all_companies_clients(request):
    if request.method == "POST":
        data = json.loads(request.body)
        print("\n\n ------------- POST QUERY ")
        print(data)

        id_company = str(data["id_company"])
        code_account = ""
        query = Model_ConfigAccounts_Client.objects.all().filter(
            id_company = id_company
        )
        if len(query) > 0:
            code_account = query[0].code_account
            print(f"\n\n >>> code_account: {code_account}")
        else:
            print(f"\n\n >>> no-code_account: {code_account}")

        return JsonResponse({"code": 200, "msg": "success query account", "code_account": code_account})
    else:
        return JsonResponse({"code": 403, "msg": "método não suportado pelo servidor."})
    
    

@login_required(login_url="/automations/login/")
def all_companies_clients(request):
    if request.method == "GET":
        obj_all_companies = list()
        all_companies = connections["db_gaulke_contabil"]
        with all_companies.cursor() as cursor:
            cursor.execute(f'SELECT id_acessorias, cnpj, razao_social FROM {DB_DATABASE_GAULKE_CONTABIL_TABLE_NAME} order by razao_social ASC;')
            rows = cursor.fetchall()

            for result in rows:
                obj_all_companies.append( {"id_client": result[0], "cnpj": result[1], "razao_social": result[2]} )

            print(obj_all_companies)

        context = {
            "all_companies_clients": obj_all_companies,
            "status_get_all_companies": True,
        }
        return render(request, "app_relations/all_companies_clients.html", context=context)
    
    elif request.method == "POST":
        try:
            data = json.loads(request.body)
            print(data)

            code_company = str(data["code_company"])
            company = data["company"]
            code_account = str(data["code_account"])

            print(f"""
                code_company: {code_company}
                company: {company}
                code_account: {code_account}
            """)

            query = Model_ConfigAccounts_Client.objects.all().filter(
                id_company = code_company
            )
            print(f"\n\n ------> query:")
            print(query)
            if len(query) == 0:
                db = Model_ConfigAccounts_Client()
                db.id_company = code_company
                db.code_account = code_account
                db.save()
                print("\n\n ------- SUCCESS SAVE ACCOUNT ON DATABASE ------- ")
            else:
                data = Model_ConfigAccounts_Client.objects.get(
                    id_company = code_company
                )
                data.code_account = code_account
                data.update_at = datetime.now(tz=tz.gettz("America/Sao Paulo"))
                data.save()
                print("\n\n ------- SUCCESS UPDATE ACCOUNT ON DATABASE ------- ")
                
            
            return JsonResponse({
                "code": 200,
                "msg": "success",
            })
        except Exception as e:
            print(f" ### ERRO AO PROCESSAR REQUISIÇÃO | ERROR: {e}")
            return JsonResponse({
                "code": 400,
                "msg": "falha ao processar requisição",
                "error": e,
            })

    else:
        return JsonResponse({
            "code": 403,
            "msg": "método de requisição não suportada",
        })

@login_required(login_url="/automations/login/")
def create_new_tag(request):
    if request.method == "GET":
        print(request.user.username)

        obj_all_companies = list()
        all_companies = connections["db_gaulke_contabil"]
        with all_companies.cursor() as cursor:
            cursor.execute(f'SELECT id_acessorias, cnpj, razao_social FROM {DB_DATABASE_GAULKE_CONTABIL_TABLE_NAME} order by razao_social ASC;')
            rows = cursor.fetchall()

            for result in rows:
                obj_all_companies.append( {"id_acessorias": result[0], "cnpj": result[1], "razao_social": result[2]} )

            print(obj_all_companies)

        query = Model_ManualTags_Username.objects.all() #.filter(username)
        print(query)

        print(f"\n\n ---------------> query: {query}")
        context = {
            "all_companies": obj_all_companies,
        }
        return render(request, "app_relations/new_rule.html", context=context)
    
    elif request.method == "POST":
        try:
            username = request.user.username #["username"]
            data = json.loads(request.body)
            numero_conta_debito = data["numero_conta_debito"]
            tags_date = data["tags_date"]
            tags_value = data["tags_value"]
            tags_cnpj_cpf = data["tags_cnpj_cpf"]
            tags_companies = data["tags_companies"]

            print(data)
            print(f"""
                \n\n---------------------------------------------
                >> username: {username} | type: {type(username)}
                >> numero_conta_debito: {numero_conta_debito} | type: {type(numero_conta_debito)}
                >> tags_date: {tags_date} | type: {type(tags_date)}
                >> tags_value: {tags_value} | type: {type(tags_value)}
                >> tags_cnpj_cpf: {tags_cnpj_cpf} | type: {type(tags_cnpj_cpf)}
                >> tags_companies: {tags_companies} | type: {type(tags_companies)}
            """)

            query = Model_ManualTags_Username.objects.filter(username=username).values()

            print(f" -----> QUERY: {query} | TT: {len(query)}")

            status_process = False

            # if len(query) == 0:
            # for x in query:
            all_companies = query_all_companies()
            print(all_companies)


            # ----------- ADD TAG COM CNPJ/CPF
            for doc in tags_cnpj_cpf:
                id_company = all_companies[all_companies["cnpj"] == doc]["id_acessorias"].values[0]
                print(f" DOC --> {doc} | id_company: {id_company}")
                for date in tags_date:
                    query = Model_ManualTags_Username.objects.filter(id_company=id_company, tag=date)
                    print("\n\n ----------------------------------------- ")
                    print(f" ----------->>>>>  query: {query} \n\n")
                    if len(query) == 0:
                        db = Model_ManualTags_Username()
                        db.id_company = id_company
                        db.username = username
                        db.numero_conta_debito = str(numero_conta_debito)
                        db.tag = date
                        db.save()
                        status_process = True
                
                for value in tags_value:
                    query = Model_ManualTags_Username.objects.filter(id_company=id_company, tag=value)
                    print("\n\n ----------------------------------------- ")
                    print(f" ----------->>>>>  query: {query} \n\n")
                    if len(query) == 0:
                        db = Model_ManualTags_Username()
                        db.id_company = id_company
                        db.username = username
                        db.numero_conta_debito = str(numero_conta_debito)
                        db.tag = value
                        db.save()
                        status_process = True

            
            # ----------- ADD TAG COM COMPANY
            for company in tags_companies:
                id_company = all_companies[all_companies["razao_social"] == company]["id_acessorias"].values[0]
                print(f" company --> {company} | id_company: {id_company}")
                for date in tags_date:
                    query = Model_ManualTags_Username.objects.filter(id_company=id_company, tag=date)
                    print("\n\n ----------------------------------------- ")
                    print(f" ----------->>>>>  query: {query} \n\n")
                    if len(query) == 0:
                        db = Model_ManualTags_Username()
                        db.id_company = id_company
                        db.username = username
                        db.numero_conta_debito = str(numero_conta_debito)
                        db.tag = date
                        db.save()
                        status_process = True
                
                for value in tags_value:
                    query = Model_ManualTags_Username.objects.filter(id_company=id_company, tag=value)
                    print("\n\n ----------------------------------------- ")
                    print(f" ----------->>>>>  query: {query} \n\n")
                    if len(query) == 0:
                        db = Model_ManualTags_Username()
                        db.id_company = id_company
                        db.username = username
                        db.numero_conta_debito = str(numero_conta_debito)
                        db.tag = value
                        db.save()
                        status_process = True

            

            return JsonResponse({"code": 200, "data": data, "status_process": status_process})
        
        except Exception as e:
            print(f" ### ERROR CREATE RULE TAG | ERROR: {e}")
            return JsonResponse({"code": 400, "msg": "requisição inválida", "erro": "objeto enviado fora do padrão."})

    else:
        return JsonResponse({"code": 500, "msg": "método da requisição não suportado."})


# ---------------------------------------------------------------------------------
# ---------------------------------- GET ALL RULE ---------------------------------
# ---------------------------------------------------------------------------------
@login_required(login_url="/automations/login/")
def get_all_tags_rules(request):
    try:
        if request.method == "POST":

            username = request.user.username
            print("\n\n ----------------- RESULT QUERY ----------------- ")
            print(f" >> USERNAME: {username}")
            query = Model_ManualTags_Username.objects.all().filter(username=username)
            all_companies = query_all_companies()
            data = list()
            print(query)
            for i in query:

                company_name = all_companies[all_companies["id_acessorias"] == i.id_company]["razao_social"].values[0]
                print(company_name)

                created_at = datetime.strftime(i.created_at, "%d/%m/%Y %H:%M:%S")
                update_at = datetime.strftime(i.update_at, "%d/%m/%Y %H:%M:%S")
                data.append({
                    "id_company": i.id_company,
                    "company_name": company_name,
                    "numero_conta_debito": i.numero_conta_debito,
                    "tag": i.tag,
                    "created_at": created_at,
                    "update_at": update_at,
                })
                print(i)

            return JsonResponse({"code": 200, "data": data})
        else:
            return JsonResponse({"code": 400, "msg": "tipo de requisição não suportada."})
    except Exception as e:
        return JsonResponse({"code": 500, "error": e, "msg": "falha ao processar requisição."})


# ------------------------
@login_required(login_url="/automations/login/")
def create_new_tag_rule(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            username = data["username"]
            numero_conta_debito = data["numero_conta_debito"]
            list_tags = " ".join(data["list_tags"])
            decription_rule = data["decription_rule"]

            print(data)
            print(f"""
                \n\n---------------------------------------------
                >> username: {username}
                >> numero_conta_debito: {numero_conta_debito}
                >> list_tags: {list_tags}
                >> decription_rule: {decription_rule}
            """)

            query = Model_DynamicTags_Username.objects.filter(username=username, tags=list_tags).values()

            print(f" -----> QUERY: {query} | TT: {len(query)}")

            status_process = False
            if len(query) == 0:
                db = Model_DynamicTags_Username()
                db.username = username
                db.numero_conta_debito = str(numero_conta_debito)
                db.tags = list_tags
                db.decription_rule = decription_rule
                db.save()
                status_process = True
                print("\n\n >> SUCCESS UPDATE RULE")

            return JsonResponse({"code": 200, "data": data, "status_process": status_process})
        
        except Exception as e:
            print(f" ### ERROR CREATE RULE TAG | ERROR: {e}")
            return JsonResponse({"code": 400, "msg": "requisição inválida", "erro": "objeto enviado fora do padrão."})

    else:
        return JsonResponse({"code": 500, "msg": "método da requisição não suportado."})

# ------------------------------------------------------------------------
# ------------------------ CONFIG PLANO DE CONTAS ------------------------
# ------------------------------------------------------------------------
@login_required(login_url="/automations/login/")
def config_plano_de_contas(request):
    try:
        show_table = False
        if request.method == "GET":
            base_plano_de_contas = get_all_plano_de_contas_generic()
            context = {
                "obj_plano_contas_old": base_plano_de_contas[0],
                "obj_plano_contas_new": base_plano_de_contas[1],
                "show_table": show_table,
            }
            return render(request, "app_automations/config_plano_de_contas.html", context=context)
        

        elif request.method == "POST":
            file = request.FILES["file"]
            company_code = request.POST.get("company_code")
            obj_plano_contas_old = request.POST.get("data-code-pc-old")
            obj_plano_contas_new = request.POST.get("data-code-pc-new")

            print(f"""
                --------------------------- POST CONFIG P.C ---------------------------
                company_code: {company_code}
                obj_plano_contas_old: {obj_plano_contas_old}
                obj_plano_contas_new: {obj_plano_contas_new}
            """)

            query = Model_Plano_Contas_De_Para_Antigo_x_Novo.objects.all().filter(
                # company_code=company_code,
                pc_old=obj_plano_contas_old,
                pc_new=obj_plano_contas_new,
            )
            data_query = dict()

            for pc in query:
                print("\n\n ------------------ ")
                data_query.update({
                    pc.code_old: pc.code_new,
                })
                print(f">> company_code: {pc.company_code}")
                print(f">> pc_old: {pc.pc_old}")
                print(f">> pc_new: {pc.pc_new}")
                print(f">> code_old: {pc.code_old}")
                print(f">> code_new: {pc.code_new}")


            print(f"\n\n ------------- DATA POST ------------- ")
            print(f"data_query: {data_query}")
            data_table = ConvertToDataFrame.read_file_plano_de_contas(file=file, data_query=data_query)
            show_table = True
            # print(data_table)
            
            base_plano_de_contas = get_all_plano_de_contas_generic()
            context = {
                "code": 200,
                "plano_contas_old": obj_plano_contas_old,
                "plano_contas_new": obj_plano_contas_new,
                "obj_plano_contas_old": base_plano_de_contas[0],
                "obj_plano_contas_new": base_plano_de_contas[1],
                "data_table": data_table["df_json"],
                "tt_rows": data_table["tt_rows"],
                "show_table": show_table,
            }
            return render(request, "app_automations/config_plano_de_contas.html", context=context)
        else:
            context = {
                "code": 400,
                "file": file,
                "msg": "método http não suportado pelo servidor.",
                "show_table": show_table,
            }
            return render(request, "app_automations/config_plano_de_contas.html", context=context)
        
    except Exception as e:
        return JsonResponse({"code": 500, "msg": "erro imprevisto no servidor.", "error": e})

@login_required(login_url="/automations/login/")
def post_plano_de_contas(request):
        data = json.loads(request.body)
        code_pc = str(data["code_PC"])
        description_PC = data["description_PC"]
        type_PC = data["type_PC"]

        print(data)

        obj_all_plano_contas = list()
        all_plano_contas = connections["default"]
        status_process_db = False

        try:
            with all_plano_contas.cursor() as cursor:
                print("\n\n\n --------------------------- RESULT QUERY --------------------------- ")
                comand_query = f'''
                    SELECT id, code_pc, description_pc from {DB_DATABASE_TABLE_NAME_PLANO_CONTAS}
                        where code_pc = "{code_pc}" and type_PC = "{type_PC}"
                '''
                cursor.execute(comand_query)
                rows = cursor.fetchall()

                if len(rows) == 0:
                    dt_created = datetime.now()
                    comand_query = f'''
                        INSERT INTO {DB_DATABASE_TABLE_NAME_PLANO_CONTAS}
                            (type_PC, code_pc, description_pc, createed_at, update_at)
                        VALUES (
                            "{type_PC}", "{code_pc}", "{description_PC}", "{dt_created}", "{dt_created}"
                        )
                    '''
                    status_process_db = True
                    cursor.execute(comand_query)
                    print(comand_query)


            for result in rows:
                obj_all_plano_contas.append( { "id": result[0], "code_pc": result[1], "description_pc": result[2] } )
        except Exception as e:
            print(f"\n\n ERROR DB | ERROR: {e}")


        return JsonResponse(
            {
                "code": 200,
                "data": obj_all_plano_contas,
                "status_process_db": status_process_db
            })

@login_required(login_url="/automations/login/")
def post_update_plano_de_contas(request):
    data = json.loads(request.body)

    code_old = data["code_old"]
    code_new = data["code_new"]
    company_code = data["company_code"]
    data_PC = data["data"]
    company_code = data["company_code"]
    username = request.user.username
    update_at = datetime.now()

    print(f"""\n\n\n
        >> code_old: {code_old}
        >> code_new: {code_new}
        >> company_code: {company_code}
    """)
    print(data_PC)
    # return JsonResponse({
    #     "code": 200,
    #     "data": data
    # })

    list_update_errors = list()
    list_update_errors_simply = list()
    list_update_success = list()
    list_update_delete = list()
    list_update_add = list()
    for pc in data_PC:
        code_old_aux = pc["code_old"]
        code_new_aux = pc["code_new"].strip()
        print(f"""\n\n\n
            >> code_old_aux: {code_old_aux}
            >> code_new_aux: {code_new_aux}
            >> company_code: {company_code}
        """)

        query = Model_Plano_Contas_De_Para_Antigo_x_Novo.objects.all().filter(
            pc_old=code_old,
            pc_new=code_new,
            code_old=code_old_aux,
            company_code=company_code,
        )

        print(f"\n\n -------------------- QUERY CODE PC -------------------- ")
        print(f"""
            >> code_old: {code_old}
            >> code_new: {code_new}
            >> code_old_aux: {code_old_aux}
            >> company_code: {company_code}
            >> username: {username}
            >> update_at: {update_at}
        """)
        print(query)
        try:
            if len(query) == 0:
                if code_new_aux.strip() != "":
                    db = Model_Plano_Contas_De_Para_Antigo_x_Novo()
                    if int(code_new_aux):
                        db.pc_old = code_old
                        db.pc_new = code_new
                        db.code_old = code_old_aux
                        db.code_new = code_new_aux
                        db.company_code = company_code
                        db.username = username
                        db.update_at = update_at
                        db.save()
                        list_update_add.append(code_old_aux)
                        print("\n ### REGISTRO INSERIDO ###")
                        print(f"""\n\n
                            ----------------------------
                            >> code_old: {code_old}
                            >> code_new: {code_new}
                            >> code_old_aux: {code_old_aux}
                            >> code_new_aux: {code_new_aux}
                            >> company_code: {company_code}
                            >> username: {username}
                            >> update_at: {update_at}
                        """)
                    else:
                        list_update_errors_simply.append(code_old_aux)
                        list_update_errors.append({
                            "company_code": company_code,
                            "code_old": code_old,
                            "code_new": code_new,
                            "code_old_aux": code_old_aux,
                            "code_new_aux": code_new_aux,
                        })
                
            else:
                query = Model_Plano_Contas_De_Para_Antigo_x_Novo.objects.all().filter(
                    pc_old=code_old,
                    pc_new=code_new,
                    code_old=code_old_aux
                )
                for x in query:
                    print(x.code_new)
                    if code_new_aux.strip() == "":
                        print(f"\n\n >>> registro deletado | PK: {x.pk}\n\n")
                        db_update = Model_Plano_Contas_De_Para_Antigo_x_Novo.objects.get(pk=x.pk)
                        db_update.delete()
                        list_update_delete.append(code_old_aux)
                    else:
                        if int(code_new_aux) > 0:
                            db_update = Model_Plano_Contas_De_Para_Antigo_x_Novo.objects.get(pk=x.pk)
                            # db_update.pc_new = code_new
                            # db_update.code_old = code_old_aux
                            # db_update.company_code = company_code
                            db_update.pc_old = code_old
                            db_update.code_new = code_new_aux
                            db_update.username = username
                            db_update.update_at = update_at
                            db_update.save()
                            list_update_success.append(code_old_aux)
                            print(f"\n\n >>> registro atualizado | PK: {x.pk} | update: {update_at}")
                            print(db_update)
                        else:
                            list_update_errors_simply.append(code_old_aux)
                            list_update_errors.append({
                                "company_code": company_code,
                                "code_old": code_old,
                                "code_new": code_new,
                                "code_old_aux": code_old_aux,
                                "code_new_aux": code_new_aux,
                            })
        except Exception as e:
            print(e)
            list_update_errors_simply.append(code_old_aux)
            list_update_errors.append({
                "company_code": company_code,
                "code_old": code_old,
                "code_new": code_new,
                "code_old_aux": code_old_aux,
                "code_new_aux": code_new_aux,
            })

    print(data_PC)
    print(f"""
        >> code_old: {code_old}
        >> code_new  : {code_new}
    """)
    print("\n\n\n -------------- list_update_errors -------------- ")
    print(list_update_errors)
    print("\n\n\n -------------- list_update_errors_simply -------------- ")
    print(list_update_errors_simply)


    return JsonResponse({
        "code": 200,
        "data": data,
        "list_update_errors": list_update_errors,
        "list_update_errors_simply": list_update_errors_simply,
        "list_update_success": list_update_success,
        "list_update_delete": list_update_delete,
        "list_update_add": list_update_add,
    })

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
        conta = ModelContasGNRE_Estados_X_Contas.objects.all()
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
            
                conta  =  ModelContasGNRE_Estados_X_Contas.objects.filter(conta_uf=data["uf"]).first()
                
                if conta is not None:
                    conta.conta_numero = data["conta_credito"]
                    conta.conta_debito = data["conta_debito"]
                    conta.save()
                    print(f" -----> update account: {conta}")
                else:
                    conta = ModelContasGNRE_Estados_X_Contas.objects.create(
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


