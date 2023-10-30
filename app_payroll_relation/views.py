import json
import requests
import pandas as pd
from datetime import datetime



# from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth import login, logout
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required


from .models import ModelContasGNRE_Estados_x_Contas


from prepate_data.prepare_data_GNRE import read_file_xlsx
from prepate_data.prepare_data_payroll import convert_PDF_to_DataFrame
from prepate_data.prepare_data_cobran_pagas import create_base_contas_pagas
from prepate_data.prepare_data_titulos_pagos_sicoob import convert_PDF_to_DataFrame_SICOOB



def home_page(request):
    return render(request, "app/home.html")

def loginUser(request):
    if request.method == "GET":
        return render(request, "app/login.html")
    elif request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")
        print(f"""
            username: {username}
            password: {password}
        """)

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

@login_required(login_url="/automations/login/")
def payroll_relation(request):
    if request.method == "GET":
        return render(request, "app/payroll_relation.html")
    # ----
    elif request.method == "POST":
        try:
            data = request.POST
            file = request.FILES["file"]
            grupo_lancamento = data.get("grupo_lancamento")
            data_dict_folha = convert_PDF_to_DataFrame(file=file, grupo_lancamento=grupo_lancamento)
            print(data_dict_folha)
    
            print(f" \n\n\n ### grupo_lancamento: {grupo_lancamento}")
            # data_dict_folha = read_file_data_post(file_name=file, name_user="Leonardo", grupo_lancamento=grupo_lancamento)
            if data_dict_folha is not None:
                context = {
                    "code_process": True,
                    "grupo_lancamento": grupo_lancamento,
                    "data_dict_folha": data_dict_folha,
                }
                return render(request, "app/payroll_relation.html", context=context)
            else:
                context = {
                    "code_process_error": True,
                }
                return render(request, "app/payroll_relation.html", context=context)
            # return render(request, "app/payroll_relation.html")
        except Exception as e:
            context = {
                "code_process_error": True,
            }
            return render(request, "app/payroll_relation.html", context=context)

def preview_payroll_relation(request):
    try:
        if request.method == "POST":
            print("\n\n ### POST PREVIEW ### ")
            # data_post = request.POST
            data_body = json.loads(request.body)

            cod_empresa = data_body.get("cod_empresa")
            filial = data_body.get("filial")
            data_lacamento = data_body.get("data_lacamento")
            data_lacamento = datetime.strptime(data_lacamento, "%Y-%m-%d").strftime("%d%m%Y")
            numero_conta_contabil_debito = data_body.get("numero_conta_contabil_debito")
            numero_conta_contabil_credito = data_body.get("numero_conta_contabil_credito")

            print(f""""
                \n\n\n ---------------------------------
                cod_empresa: {cod_empresa}
                filial: {filial}
                data_lacamento: {data_lacamento}
                numero_conta_contabil_debito: {numero_conta_contabil_debito}
                numero_conta_contabil_credito: {numero_conta_contabil_credito}
            """)

            
            print("\n\n\n ----- POST PREVIEW PAYROLL RELATION ----- ")
            # print(data_body)
            # print(data_body["headers"])

            df = pd.DataFrame(columns=data_body["headers"], data=data_body["rows"])
            print(df)

            list_cod_empresa = list()
            list_filial = list()
            list_data_lacamento = list()
            list_numero_conta_contabil_debito = list()
            list_numero_conta_contabil_credito = list()

            for i in range(len(df.index)):
                print(">>> ", i)
                list_cod_empresa.append(cod_empresa)
                list_filial.append(filial)
                list_data_lacamento.append(data_lacamento)
                list_numero_conta_contabil_debito.append(numero_conta_contabil_debito)
                list_numero_conta_contabil_credito.append(numero_conta_contabil_credito)
                print(f"""
                    cod_empresa: {cod_empresa}
                    filial: {filial}
                    data_lacamento: {data_lacamento}
                    numero_conta_contabil_debito: {numero_conta_contabil_debito}
                    numero_conta_contabil_credito: {numero_conta_contabil_credito}
                """)



            df["COD_EMPRESA"] = list_cod_empresa
            df["FILIAL"] = list_filial
            df["DATA_LANC"] = list_data_lacamento
            # df["NUMERO_CONTA_CONTABIL_CREDITO"] = list_numero_conta_contabil_credito
        
            print(" -------------------- DATA TEMP -------------------- ")
            print(df)

            df_debito = pd.DataFrame(df)
            df_debito["NUMERO_CONTA_CONTABIL"] = list_numero_conta_contabil_debito
            df_debito.drop_duplicates(subset=["COD_EMPRESA"], keep="first")
            df_credito = pd.DataFrame(df_debito)

            # df_credito["NUMERO_CONTA_CONTABIL"] = list_numero_conta_contabil_credito
            
            df = pd.concat([df_debito, df_credito])
            df = df.drop_duplicates(subset=["COLABORADOR", "TIPO_REGISTRO"])

            for i in range(len(df.index)):
                if df["TIPO_REGISTRO"][i] == "C":
                    df["NUMERO_CONTA_CONTABIL"][i] = numero_conta_contabil_credito

                grupo_lanc = df["GRUPO_LANC"][i]
                colaborador = df["COLABORADOR"][i]
                complemento_hist = f"Pgto. Salários Ref. Mês {grupo_lanc} - {colaborador}"
                df["COMPLEM_HIST"][i] = complemento_hist
                df["GRUPO_LANC"][i] = ""


            df = df[[
                "TIPO_LANC",
                "COD_EMPRESA",
                "FILIAL",
                "DATA_LANC",
                "COD_ERP_CLIENTE",
                "TIPO_REGISTRO",
                "NUMERO_CONTA_CONTABIL",
                "SUB_CONTA",
                "VALOR_LIQ",
                "ACAO_LANC",
                "PRIM_HIST_CONTA",
                "COD_HIST",
                "COMPLEM_HIST",
                "GRUPO_LANC",
                "CNPJ",
                "INSC_ESTADUAL",
                "TP_CNPJ",
                "CONTA_ORIGEM",
                "CNPJ_EMPRESA",
                "IE_EMPRESA",
            ]]
            df = df[df["VALOR_LIQ"] != "0.00"]

            
        
            df.sort_values(["COD_ERP_CLIENTE"])            
            print("------------- data ------------- ")
            df = df.to_json(orient="records")
            print(df)


            return JsonResponse({"code": 200, "msg": "sucess", "data": df})

        else:
            return JsonResponse({"code": 401, "msg": "not-found"})
    except Exception as e:
        print(e)
        return JsonResponse({"code": 500, "msg": "error"})


# ---------------------- IMPORTAÇÃO GNRE ----------------------
@login_required(login_url="/automations/login/")
def gnre_relation(request):
    if request.method == "GET":
        return render(request, "app/relation_gnre.html")
    # ----
    elif request.method == "POST":
        try:
            data = request.POST
            file = request.FILES["file"]
            grupo_lancamento = data.get("grupo_lancamento")
            print(file)
            print(grupo_lancamento)
            data_dict_gnre = read_file_xlsx(file_dir=file, grupo_lancamento=grupo_lancamento)
            context = {
                "code_process": True,
                "grupo_lancamento": grupo_lancamento,
                "data_dict_folha": data_dict_gnre,
            }
            
            return render(request, "app/relation_gnre.html", context=context)
        except Exception as e:
            print(f"\n\n ### ERROR POST FILE EXCEL GNRE | ERROR: {e} ### ")
            context = {
                "code_process_error": True,
            }
            return render(request, "app/relation_gnre.html", context=context)

def preview_gnre_relation(request):
    try:
        if request.method == "POST":
            # ---------- QUERY ALL DATA CONTAS ----------
            query_contas = ModelContasGNRE_Estados_x_Contas.objects.all()
            data_contas = dict()
            for data in query_contas:
                data_contas.update(
                    {
                        data.conta_uf:{
                            "conta_credito": data.conta_numero,
                            "conta_debito": data.conta_debito,
                    }
                })

            print(data_contas)


            # ---------- TRATAMENTO DO POST ----------
            print("\n\n ### POST PREVIEW ### ")
            data_body = json.loads(request.body)

            cod_empresa = data_body.get("cod_empresa")
            filial = data_body.get("filial")
            modelo_gnre = data_body.get("modelo_gnre")
            
            print(f""""
                \n\n\n ------------------------------
                cod_empresa: {cod_empresa}
                filial: {filial}
                modelo_gnre: {modelo_gnre}
            """)

            
            df = pd.DataFrame(columns=data_body["headers"], data=data_body["rows"])
            print(df)

            list_cod_empresa = list()
            list_filial = list()
            list_numero_conta_contabil_debito = list()
            list_numero_conta_contabil_credito = list()

            for i in range(len(df.index)):
                list_cod_empresa.append(cod_empresa)
                list_filial.append(filial)
                list_numero_conta_contabil_debito.append("-")
                list_numero_conta_contabil_credito.append("-")
                

            df["COD_EMPRESA"] = list_cod_empresa
            df["FILIAL"] = list_filial
            
        
            print(" -------------------- DATA TEMP -------------------- ")
            df.sort_values(by=["CTE", "TIPO_REGISTRO"], inplace=True)
            print(df)

            df_debito = pd.DataFrame(df)
            df_debito["NUMERO_CONTA_CONTABIL"] = list_numero_conta_contabil_debito
            df_debito.drop_duplicates(subset=["COD_EMPRESA"], keep="first")
            df_credito = pd.DataFrame(df_debito)

            df_credito["NUMERO_CONTA_CONTABIL"] = list_numero_conta_contabil_credito
            
            df = pd.concat([df_debito, df_credito])
            df = df.drop_duplicates(subset=["CTE", "TIPO_REGISTRO"])
            
            df.index = list(range(0, len(df.index)))

            for i in range(len(df.index)):

                uf_inicio = df["UF_INÍCIO"][i]
                conta_debito = data_contas.get(uf_inicio)["conta_debito"]
                conta_credito = data_contas.get(uf_inicio)["conta_credito"]

                if df["TIPO_REGISTRO"][i] == "C":
                    df["NUMERO_CONTA_CONTABIL"][i] = conta_credito
                elif df["TIPO_REGISTRO"][i] == "D":
                    df["NUMERO_CONTA_CONTABIL"][i] = conta_debito

            df = df[[
                "TIPO_LANC",
                "COD_EMPRESA",
                "FILIAL",
                "DATA_EMISSÃO",
                "COD_ERP_CLIENTE",
                "TIPO_REGISTRO",
                "NUMERO_CONTA_CONTABIL",
                "SUB_CONTA",
                "VALOR_ICMS",
                "ACAO_LANC",
                "PRIM_HIST_CONTA",
                "COD_HIST",
                "COMPLEM_HIST",
                "GRUPO_LANC",
                "CNPJ",
                "INSC_ESTADUAL",
                "TP_CNPJ",
                "CONTA_ORIGEM",
                "CNPJ_EMPRESA",
                "IE_EMPRESA",
            ]]
            df['VALOR_ICMS'] = df['VALOR_ICMS'].str.replace(',', '.')
            df['VALOR_ICMS'] = df['VALOR_ICMS'].astype(float)
            df["DATA_EMISSÃO"] = list(map(lambda x: x.replace("/", ""), df["DATA_EMISSÃO"].values))

            
           

            # print("------------- data ------------- ")
            df = df.to_json(orient="records")
            print(df)
            return JsonResponse({"code": 200, "msg": "sucess", "data": df})
            # return JsonResponse({"code": 200, "msg": "sucess", "data": []})

        else:
            return JsonResponse({"code": 401, "msg": "not-found"})
    except Exception as e:
        print(e)
        return JsonResponse({"code": 500, "msg": "error"})


# ---------------------- IMPORTAÇÃO COBRANÇAS PAGAS ----------------------
@login_required(login_url="/automations/login/")
def relation_cobrancas_pagas(request):
    if request.method == "GET":
        return render(request, "app/relation_cobrancas_pagas.html")
    # ----
    elif request.method == "POST":
        try:
            data = request.POST
            file = request.FILES["file"]
            grupo_lancamento = data.get("grupo_lancamento")
            print(file)
            print(grupo_lancamento)
            data_dict_gnre = create_base_contas_pagas(file=file)["data"]
            # print("\n\n\n\n --------------------- JSON DATA --------------------- ")
            # print(data_dict_gnre)
            context = {
                "code_process": True,
                "data_dict_folha": data_dict_gnre,
            }
            
            return render(request, "app/relation_cobrancas_pagas.html", context=context)
        except Exception as e:
            print(f"\n\n ### ERROR POST FILE EXCEL GNRE | ERROR: {e} ### ")
            context = {
                "code_process_error": True,
            }
            return render(request, "app/relation_cobrancas_pagas.html", context=context)

def preview_relation_cobrancas_pagas(request):
    try:
        if request.method == "POST":
            print("\n\n ### POST PREVIEW ### ")
            # data_post = request.POST
            data_body = json.loads(request.body)

            cod_empresa = data_body.get("cod_empresa")
            filial = data_body.get("filial")

            numero_conta_contabil_debito = data_body.get("numero_conta_contabil_debito")
            numero_conta_contabil_credito = data_body.get("numero_conta_contabil_credito")
            numero_conta_contabil_juros = data_body.get("numero_conta_contabil_juros")
            numero_conta_contabil_desconto = data_body.get("numero_conta_contabil_desconto")

            print(f""""
                \n\n\n ---------------------------------
                cod_empresa: {cod_empresa}
                filial: {filial}
                numero_conta_contabil_debito: {numero_conta_contabil_debito}
                numero_conta_contabil_credito: {numero_conta_contabil_credito}
                numero_conta_contabil_juros: {numero_conta_contabil_juros}
                numero_conta_contabil_desconto: {numero_conta_contabil_desconto}
            """)

            
            print("\n\n\n ----- POST PREVIEW PAYROLL RELATION ----- ")
            # print(data_body)
            # print(data_body["headers"])

            df = pd.DataFrame(columns=data_body["headers"], data=data_body["rows"])
            print(df)

            list_cod_empresa = list()
            list_filial = list()
            list_data_lacamento = list()
            list_numero_conta_contabil_debito = list()
            list_numero_conta_contabil_credito = list()

            for i in range(len(df.index)):
                print(">>> ", i)
                list_cod_empresa.append(cod_empresa)
                list_filial.append(filial)
                list_numero_conta_contabil_debito.append(numero_conta_contabil_debito)
                list_numero_conta_contabil_credito.append(numero_conta_contabil_credito)
                print(f"""
                    cod_empresa: {cod_empresa}
                    filial: {filial}
                    numero_conta_contabil_debito: {numero_conta_contabil_debito}
                    numero_conta_contabil_credito: {numero_conta_contabil_credito}
                    numero_conta_contabil_juros: {numero_conta_contabil_juros}
                    numero_conta_contabil_desconto: {numero_conta_contabil_desconto}
                """)
            
            df["COD_EMPRESA"] = list_cod_empresa
            df["FILIAL"] = list_filial
        
            print("\n\n -------------------- CREATE DATAFRAME DEBITO -------------------- ")
            df_debito = pd.DataFrame(df)
            df_debito["NUMERO_CONTA_CONTABIL"] = list_numero_conta_contabil_debito
            df_debito.drop_duplicates(subset=["COD_EMPRESA", "TIPO_PROCESSO", "DATA_PAG"], keep="first")
            print(df_debito)

            print("\n\n -------------------- CREATE DATAFRAME CREDITO -------------------- ")
            df_credito = pd.DataFrame(df_debito)
            # ----
            df = pd.concat([df_debito, df_credito])

            df = df.drop_duplicates(subset=["COD_ERP_CLIENTE"])

            print(df_credito)

            print("\n\n -------------------- CREATE DATAFRAME CONCT -------------------- ")
            df.index = list(range(0, len(df.index)))

            for i in df.index:
                
                df["DATA_PAG"][i] = df["DATA_PAG"][i].replace("/", "")
                valor = df["VALOR"][i].replace(",", ".")
                valor_formatado = "{:.2f}".format(float(valor))
                df["VALOR"][i] = valor_formatado

                if df["TIPO_REGISTRO"][i] == "C" and df["TIPO_PROCESSO"][i] == "comum":
                    df["NUMERO_CONTA_CONTABIL"][i] = numero_conta_contabil_credito

                elif df["TIPO_REGISTRO"][i] == "D" and df["TIPO_PROCESSO"][i] == "comum":
                    df["NUMERO_CONTA_CONTABIL"][i] = numero_conta_contabil_debito

                # ----------------------------------------------------------------------- ATUALIZA CONTAS DE JUROS E DESCONTOS
                if df["TIPO_PROCESSO"][i] == "process_juros":
                    
                    df["TIPO_REGISTRO"][i] = "C"
                    df["NUMERO_CONTA_CONTABIL"][i] = numero_conta_contabil_juros
                    
                    data_aux  = df[df.index == i].values[0][12].replace('Receb.','Juros')
                    df["COMPLEM_HIST"][i] = data_aux

                # ----

                elif df["TIPO_PROCESSO"][i] == "process_desconto":
                    
                    df["TIPO_REGISTRO"][i] = "D"
                    df["NUMERO_CONTA_CONTABIL"][i] = numero_conta_contabil_desconto

                    data_aux  = df[df.index == i].values[0][12].replace('Receb.','Desconto')
                    df["COMPLEM_HIST"][i] = data_aux




            df.sort_values(["COMPLEM_HIST"])   
            df = df[[
                "TIPO_LANC",
                "COD_EMPRESA",
                "FILIAL",
                "DATA_PAG",
                "COD_ERP_CLIENTE",
                "TIPO_REGISTRO",
                "NUMERO_CONTA_CONTABIL",
                "SUB_CONTA",
                "VALOR",
                "ACAO_LANC",
                "PRIM_HIST_CONTA",
                "COD_HIST",
                "COMPLEM_HIST",
                "GRUPO_LANC",
                "CNPJ",
                "INSC_ESTADUAL",
                "TP_CNPJ",
                "CONTA_ORIGEM",
                "CNPJ_EMPRESA",
                "IE_EMPRESA",
                # "TIPO_PROCESSO",
            ]]
                       
            # df.to_excel("data_test.xlsx")

            df = df.to_json(orient="records")


            return JsonResponse({"code": 200, "msg": "sucess", "data": df})

        else:
            return JsonResponse({"code": 401, "msg": "not-found"})
    except Exception as e:
        print(e)
        return JsonResponse({"code": 500, "msg": "error"})


# ---------------------- IMPORTAÇÃO TITULOS PAGOS SICOOB ----------------------
@login_required(login_url="/automations/login/")
def relation_titulos_pagos_sicoob(request):
    if request.method == "GET":
        return render(request, "app/relation_titulos_pagos_sicoob.html")
    # ----
    elif request.method == "POST":
        file = request.FILES["file"]
        base = convert_PDF_to_DataFrame_SICOOB(file=file)
        # print(base)
        context = {
            "code_process": True,
            "data_dict": base["data"]
        }
        return render(request, "app/relation_titulos_pagos_sicoob.html", context=context)

def preview_titulos_pagos_sicoob(request):
    try:
        if request.method == "POST":
            data_body = json.loads(request.body)
            cod_empresa = data_body.get("cod_empresa")
            filial = data_body.get("filial")
            numero_conta_debito = data_body.get("numero_conta_debito")
            numero_conta_credito = data_body.get("numero_conta_credito")
            print(f"""
                cod_empresa: {cod_empresa}
                filial: {filial}
                numero_conta_debito: {numero_conta_debito}
                numero_conta_credito: {numero_conta_credito}
            """)
                
            df = pd.DataFrame(columns=data_body["headers"], data=data_body["rows"])
            for i in df.index:
                df["FILIAL"][i] = filial
                df["COD_EMPRESA"][i] = cod_empresa
                # ----
                if df["TIPO_REGISTRO"][i] == "D":
                    df["CONTA"][i] = numero_conta_debito
                elif df["TIPO_REGISTRO"][i] == "C":
                    df["CONTA"][i] = numero_conta_credito
            print(df)

            
            df = df.to_json(orient="records")



            return JsonResponse({
                "code": 200,
                "msg": "POST success",
                "data": df,
            })
        else:
            return JsonResponse({"code": 401, "msg": "not-found"})
    except Exception as e:
        print(e)
        return JsonResponse({"code": 500, "msg": "error"})




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


