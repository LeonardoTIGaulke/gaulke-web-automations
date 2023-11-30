import io
import json
import random
import tabula
import pandas as pd
from time import time
from PyPDF2 import PdfReader
import datetime


class ConvertToDataFrame:
    # def __init__(self):
    #     self.api = ""

    def data_strip(data):
        return data.strip()
    
    def create_data_randomic():
        number = random.randint(10**17, 10**18 - 1)
        return number
    # ----

    def create_text_compl_grupo_lancamento(model, dict_data_replace: dict, grupo_lancamento="-", value_generic=None):
        try:
            if model == "-":
                return model
            else:
                data_model_text = {
                    # exemplo 1: Pgto. [Nome do cliente] - Data Venc: [data completa]
                    "model_1": "Pgto. [v1] - Data Venc: [v2]",
                    # ----
                    # exemplo 2: Pgto. Salários Ref. Mês [mês/ano] - [nome do cliente]
                    "model_2": f"Pgto. Salários Ref. Mês {grupo_lancamento} - [v1]",
                    # ----
                    # exemplo 3: VLR ICMS S/CTE nº [número CTE]
                    "model_3": f"VLR ICMS S/CTE nº [v1]",
                    # ----
                    # exemplo 4: Receb. Dupl [nome cliente] venc [data vencimento]
                    "model_4": f"Receb. Dupl [v1] venc [v2]",
                    # ----
                    # exemplo 5: Entrada Títulos Desc. [nome cliente] venc [data vencimento] [Sicoob, Itau, ...]
                    "model_5": f"Entrada Títulos Desc. {value_generic} Dupl. [v1] - [v2] - venc [v3]",
                    # ----
                    # exemplo 6: Entrada Decorise 22/11/2023
                    "model_6": f"Pgto. Decorise {grupo_lancamento} - Gateway [v1] [v2]",
                    # ----
                    # exemplo 7: Entrada Decorise 22/11/2023
                    "model_7": f"Recebimento Dupl. nº NF [v1] - [v2]",
                    
                }
                text = data_model_text.get(model)
                for k,v in dict_data_replace.items():
                    text = text.replace(k, str(v))
                
                return text
        except Exception as e:
            print(f"\n\n ### ERROR CREATE TEXT COMPL. HOST | ERROR: {e}")
            return None
        
    def create_dict_data_replace(dataframe, list_col_name, index):
        """ return: texto alternativo para uso no complemento de histórico.  """

        dict_data_replace=dict()
        print(">>>>>>>\n", dataframe, index)
        print(dataframe.info())
        for i in range(len(list_col_name)):
            print(f" -----------> COLS: {list_col_name}")
            data_aux =  dataframe[list_col_name[i]][index]
            value = {f"[v{i+1}]": data_aux}
            print(f" ****** {value}")
            dict_data_replace.update(value)

        return dict_data_replace
        
    def create_layout_JB(dataframe, model="-", grupo_lancamento="", value_generic=None):
        """ return: DataFrame Lançamentos Contábeis - Importação no Sistema JB.  """
        LIST_TP_REGISTRO = list()
        LIST_EMPRESA = list()
        LIST_COD_EMPRESA = list()
        LIST_FILIAL = list()
        LIST_DATA = list()
        LIST_NR_L_CTO_ERP = list()
        LIST_TP = list()
        LIST_CONTA = list()
        LIST_SUBCONTA = list()
        LIST_VALOR = list()
        LIST_ACAO = list()
        LIST_PRIMEIRO_HIST_CTA = list()
        LIST_COD_HISTORICO = list()
        LIST_COMPL_HISTORICO = list()
        LIST_GRUPO_LCTO = list()
        LIST_CNPJ = list()
        LIST_IESTADUAL = list()
        LIST_TP_CNPJ = list()
        LIST_CONTA_ORIGEM = list()
        LIST_CNPJ_EMPRESA = list()
        LIST_IE_EMPRESA = list()
        LIST_TYPE_PROCESS = list()

        for i in dataframe.index:
            print(f" INDEX JB: {i}")
            LIST_TP_REGISTRO.append("00")
            LIST_EMPRESA.append("") # MANUAL
            LIST_COD_EMPRESA.append("")
            # LIST_FILIAL.append("") # MANUAL
            LIST_DATA.append("-")
            LIST_NR_L_CTO_ERP.append("-") # GERAR ALFANUMERICO
            LIST_TP.append("D") # CRIAR LINHAS ---> D e C (débito/crédito)
            LIST_CONTA.append("-") # MANUAL)
            LIST_SUBCONTA.append("0")
            LIST_VALOR.append("-")
            LIST_ACAO.append("0")
            LIST_COD_HISTORICO.append(grupo_lancamento)
            # LIST_PRIMEIRO_HIST_CTA.append("2")
            
            filial = ""
            text = "-"
            value_primeiro_hist_cta = ""
            value_tp_cnpj = ""
            value_cnpj = ""
            try:
                if model == "model_1":
                    # modelo: ?
                    value_primeiro_hist_cta = "2"
                    dict_data_replace = ConvertToDataFrame.create_dict_data_replace(dataframe=dataframe, list_col_name=["beneficiario_final", "data_vencimento"], index=i)
                    text = ConvertToDataFrame.create_text_compl_grupo_lancamento(model=model, dict_data_replace=dict_data_replace)

                elif model == "model_2":
                    # modelo: ?
                    value_primeiro_hist_cta = "2"
                    dict_data_replace = ConvertToDataFrame.create_dict_data_replace(dataframe=dataframe, list_col_name=["NOME_TEMP"], index=i)
                    text = ConvertToDataFrame.create_text_compl_grupo_lancamento(model=model, dict_data_replace=dict_data_replace, grupo_lancamento=grupo_lancamento)

                elif model == "model_3":
                    # modelo: ?
                    value_primeiro_hist_cta = "2"
                    dict_data_replace = ConvertToDataFrame.create_dict_data_replace(dataframe=dataframe, list_col_name=["CTE"], index=i)
                    print("\n\n >>>>>>> DICT DATA TO REPLACE:  ", dict_data_replace)
                    text = ConvertToDataFrame.create_text_compl_grupo_lancamento(model=model, dict_data_replace=dict_data_replace)

                elif model == "model_4":
                    # modelo: ?
                    value_primeiro_hist_cta = "2"
                    value_tp_cnpj = "1"
                    value_cnpj = dataframe["CNPJ"][i]
                    dict_data_replace = ConvertToDataFrame.create_dict_data_replace(dataframe=dataframe, list_col_name=["Nome Cliente", "Vencimento"], index=i)
                    print("\n\n >>>>>>> DICT DATA TO REPLACE:  ", dict_data_replace)
                    text = ConvertToDataFrame.create_text_compl_grupo_lancamento(model=model, dict_data_replace=dict_data_replace)

                elif model == "model_5":
                    # modelo: SICOOB
                    value_primeiro_hist_cta = "2"
                    dict_data_replace = ConvertToDataFrame.create_dict_data_replace(dataframe=dataframe, list_col_name=["SEU_NUMERO", "NOME", "DATA_VENCIMENTO"], index=i)
                    text = ConvertToDataFrame.create_text_compl_grupo_lancamento(model=model, dict_data_replace=dict_data_replace, value_generic=value_generic)
                    print("\n\n >>>>>>> DICT DATA TO REPLACE:  ", dict_data_replace)
                    print(f">>>>>>>>>>>>>>>> TEXT: {text}")

                elif model == "model_6":
                    # modelo: DECORISE
                    value_primeiro_hist_cta = "2"
                    # dict_data_replace = ConvertToDataFrame.create_dict_data_replace(dataframe=dataframe, list_col_name=["Conf. Gateway", "DATA_TEMP"], index=i)
                    # text = ConvertToDataFrame.create_text_compl_grupo_lancamento(model=model, dict_data_replace=dict_data_replace, grupo_lancamento=grupo_lancamento, value_generic=value_generic)
                    text = "Recebimento ref. e-commerce Megapay"
                    # print("\n\n >>>>>>> DICT DATA TO REPLACE:  ", dict_data_replace)
                    print(f">>>>>>>>>>>>>>>> TEXT: {text}")

                elif model == "model_7":
                    # modelo: Arão dos Santos

                    filial = dataframe["Filial"][i]
                    value_primeiro_hist_cta = "2"
                    dict_data_replace = ConvertToDataFrame.create_dict_data_replace(dataframe=dataframe, list_col_name=["Nº NF", "Nome Cliente"], index=i)
                    text = ConvertToDataFrame.create_text_compl_grupo_lancamento(model=model, dict_data_replace=dict_data_replace, value_generic=value_generic)
                    print("\n\n >>>>>>> DICT DATA TO REPLACE:  ", dict_data_replace)
                    print(f">>>>>>>>>>>>>>>> TEXT: {text}")

                
            except Exception as e:
                print(f"\n\n\n -------------->>>> ERROR : {e}")
                return
            
            LIST_FILIAL.append(filial) # MANUAL
            LIST_PRIMEIRO_HIST_CTA.append(value_primeiro_hist_cta)
            LIST_COMPL_HISTORICO.append(text) # TEXTO ALTERNATIVO --> CONCATENAR COM?

            # ----
            LIST_GRUPO_LCTO.append(ConvertToDataFrame.create_data_randomic()) # CÓDIGO ÚNICO DE ATÉ 18 CARACTERES
            LIST_CNPJ.append(value_cnpj)
            LIST_IESTADUAL.append("")
            LIST_TP_CNPJ.append(value_tp_cnpj)
            LIST_CONTA_ORIGEM.append("")
            LIST_CNPJ_EMPRESA.append("")
            LIST_IE_EMPRESA.append("")
            LIST_TYPE_PROCESS.append("comum")


        

        
        dataframe["TP_REGISTRO"] = LIST_TP_REGISTRO
        dataframe["NOME"] = LIST_EMPRESA
        dataframe["COD_EMPRESA"] = LIST_COD_EMPRESA
        dataframe["FILIAL"] = LIST_FILIAL
        dataframe["DATA"] = LIST_DATA
        dataframe["NR_L_CTO_ERP"] = LIST_NR_L_CTO_ERP
        dataframe["TP"] = LIST_TP
        dataframe["CONTA"] = LIST_CONTA
        dataframe["SUBCONTA"] = LIST_SUBCONTA
        dataframe["VALOR"] = LIST_VALOR
        dataframe["ACAO"] = LIST_ACAO
        dataframe["PRIMEIRO_HIST_CTA"] = LIST_PRIMEIRO_HIST_CTA
        dataframe["COD_HISTORICO"] = LIST_COD_HISTORICO
        dataframe["COMPL_HISTORICO"] = LIST_COMPL_HISTORICO
        dataframe["GRUPO_LCTO"] = LIST_GRUPO_LCTO
        dataframe["CNPJ"] = LIST_CNPJ
        dataframe["IESTADUAL"] = LIST_IESTADUAL
        dataframe["TP_CNPJ"] = LIST_TP_CNPJ
        dataframe["CONTA_ORIGEM"] = LIST_CONTA_ORIGEM
        dataframe["CNPJ_EMPRESA"] = LIST_CNPJ_EMPRESA
        dataframe["IE_EMPRESA"] = LIST_IE_EMPRESA
        dataframe["TYPE_PROCESS"] = LIST_TYPE_PROCESS

        # print( "\n\n\n\n ################################################# ")
        # print(dataframe)

        return dataframe
    
    # ----

    def create_additional_columns(dataframe, column_name, default_value):
        dataframe[f"{column_name}"] = default_value
        return dataframe
        
    # ----
    
    def drop_columns_dataframe(dataframe, list_columns: list):
        if len(list_columns) > 0:
            for col_name in list_columns:
                dataframe = dataframe.drop(labels=col_name, axis=1)
        return dataframe
    
    # ----
    
    def transpose_values(dataframe, dict_cols_transpose):
        if len(dict_cols_transpose.keys()) > 0:
            for k,v in dict_cols_transpose.items():
                dataframe[k] = dataframe[v]
        return dataframe
    
    # ----
    
    def rename_columns_dataframe(dataframe, dict_replace_names):
        dataframe = dataframe.rename(columns=dict_replace_names)
        return dataframe
    
    # ----
    
    def duplicate_dataframe_rows(dataframe, TP_account="C"):
        """" return: DataFrame atualizado com linhas duplicadas. Será atualizado apenas os valoes de "TP" de lançamento. """
        df_copy = dataframe.copy()
        df_copy.loc[:, 'TP'] = TP_account
        new_dataframe = pd.concat([dataframe, df_copy])
        return new_dataframe
    
    # ----
    
    def duplicate_dataframe_rows_lote(dataframe, list_update_cols=list):
        """
            return: DataFrame atualizado com linhas duplicadas em lote. Serão atualizados os valoes de "TP" e "TYPE_PROCESS".
        """

        new_dataframe = None
        list_dataframes = list()
        for x in list_update_cols:
            df_copy = dataframe.copy()
            print(f"""\n
                ----> TP: {x["TP"]}
                ----> TYPE_PROCESS: {x["TYPE_PROCESS"]}
            """)
            df_copy.loc[:, 'TP'] = x["TP"]
            df_copy["TYPE_PROCESS"] = x["TYPE_PROCESS"]
            list_dataframes.append(df_copy)

        list_dataframes.append(dataframe)
        new_dataframe = pd.concat(list_dataframes)

        return new_dataframe
    
    # ----
    def check_discount_or_fees(document_value, amount_paid):
        document_value = float(str(document_value).replace(".", "").replace(",", "."))
        amount_paid = float(str(amount_paid).replace(".", "").replace(",", "."))
        print(f"""\n
            ---------------------------------------------------------
            -----> document_value: {document_value}
            -----> amount_paid: {amount_paid}
        """)
        if amount_paid > document_value:
            return "fees"
        elif amount_paid < document_value:
            return "discount"
        
        return "normal"
    

    # ----
    def create_dataframe_discount_and_fees_cobrancas_pagas(dataframe):
        print("\n\n ----------------------- CRIA DATAFRAME DE JUTOS E DESCONTOS -----------------------  ")
        print("\n\n -------- JUROS -------- ")

        list_data_calculate = list()
        for i in dataframe.index:
            valor = float(dataframe["Valor"][i].values[0])
            valor_pago = float(dataframe["Valor pago"][i].values[0])
            dataframe["Valor"][i] = valor
            dataframe["Valor pago"][i] = valor_pago
            calculate = abs( valor_pago - valor )
            list_data_calculate.append(calculate)
        
        dataframe["calculo"] = list_data_calculate
        
        dataframe_juros = dataframe.copy()
        dataframe_juros = dataframe_juros[ (dataframe_juros["calculo"] > 0) & (dataframe_juros["TP"] == "D") ]

        dataframe_juros.index = list(range(0, len(dataframe_juros.index)))
        if len(dataframe_juros.index) >= 1:
            for i in dataframe_juros.index:
                dataframe_juros["TP"][i] == "C"
                dataframe_juros["TYPE_PROCESS"][i] = "process_juros"

                new_value = str(round(dataframe_juros["Valor pago"][i] - (dataframe_juros["Valor pago"][i] - dataframe_juros["calculo"][i]), 2))
                dataframe_juros["VALOR_PAGO"][i] = new_value

        print(dataframe_juros)
        
        print("\n\n\n -------- DESCONTO -------- ")
        dataframe_desconto = dataframe.copy()
        dataframe_desconto = dataframe_desconto[ (dataframe_desconto["calculo"] < 0) & (dataframe_desconto["TP"] == "C") ]

        if len(dataframe_desconto.index) >= 1:
            for i in dataframe_desconto.index:
                dataframe_desconto["TYPE_PROCESS"][i] = "process_desconto"
                new_value = str(round(dataframe_juros["Valor pago"][i] - (dataframe_juros["Valor pago"][i] - dataframe_juros["calculo"][i]), 2))
                dataframe_juros["VALOR_PAGO"][i] = new_value

    
        print(dataframe_desconto)

        dataframe = pd.concat([dataframe, dataframe_juros, dataframe_desconto])
        for i in dataframe.index:
            dataframe
        return dataframe

    # ----
    def create_dataframe_discount_and_fees(dataframe):
        df_discount = dataframe[dataframe["tipo_registro"] == "discount"].drop_duplicates(subset=["GRUPO_LCTO"])
        df_fees = dataframe[dataframe["tipo_registro"] == "fees"].drop_duplicates(subset=["GRUPO_LCTO"])
        
        if len(df_discount) > 0:
            df_discount.loc[:, 'TYPE_PROCESS'] = 'process_discount'
            dataframe = pd.concat([dataframe, df_discount])
        elif len(df_fees) > 0:
            df_fees.loc[:, 'TYPE_PROCESS'] = 'process_fess'
            dataframe = pd.concat([dataframe, df_fees])    
        return dataframe
    
    # ----
    
    def convert_dataframe_to_excel(dataframe, file_name):
        try:
            return dataframe.to_excel(file_name)
        except:
            return
    
    # ----
    
    def readjust_values_dataframe(dataframe):
        for i in dataframe.index:
            dataframe["NR_L_CTO_ERP"][i] = f"COD{i}TM{int(time())}"
            if dataframe["TYPE_PROCESS"][i] in ["process_discount" , "process_fess"]:
                dataframe["VALOR"][i] = dataframe["valor_dif"][i]
                dataframe["VALOR"][i-2] = dataframe["valor_documento"][i-2]
                dataframe["VALOR"][i-1] = dataframe["valor_cobrado"][i-1]
            else:
                dataframe["VALOR"][i] = dataframe["valor_cobrado"][i]
        return dataframe
    
    # ----
    
    def create_cod_erp_to_dataframe(dataframe, index_default=0):
        for i in dataframe.index:
            print("\n --------------  ")
            print(f">>>> COD{i+index_default}TM{int(time())}")
            numero_lanc_cto_erp = f"COD{i+index_default}TM{int(time())}"
            dataframe["NR_L_CTO_ERP"][i] = numero_lanc_cto_erp
        print(" ------ DF ERP FINISH ------ ")
        print(dataframe)
        return dataframe
    
    # ----
    
    def filter_columns_dataframe(daraframe, list_columns: list):
        daraframe = daraframe[list_columns]
        return daraframe
    
    # ----
    
    def filter_data_dataframe(daraframe, name_column: str, list_remove_values: list):
        daraframe = daraframe[~daraframe[name_column].isin(list_remove_values)]

        return daraframe
    
    # ----
    
    def readjust_values_dataframe_decimal(dataframe, list_cols_name: list, replace_values_list=True):
        for col in list_cols_name:
            dataframe[col] = dataframe[col].str.replace('.', '').str.replace(',', '.')
        if replace_values_list:
            for i in dataframe.index:
                for col in list_cols_name:
                    dataframe[col][i] = dataframe[col][i].split()[1]
        return dataframe
    
    # ----
    
    def read_pdf_comprovante_banco_do_brasil(file):
        
        contents = file.read()
        pdf_bytes = io.BytesIO(contents)
        pdf_reader = PdfReader(pdf_bytes)

        list_data_pages = list()
        list_page_erros = list()
        index_page = 0
        print(f" TT PAGES: {len(pdf_reader.pages)}")
        for index_page in range(len(pdf_reader.pages)):
            try:
                print(f"\n\n\n ---- INDEX PAGE: {index_page}")
                
                page = pdf_reader.pages[index_page]
                
                
                data_page = page.extract_text()
                print(data_page)

                data_extract = {
                    "index": {"text": 0},
                    "beneficiario_final": {"data_init": 0, "data_final": 0, "text": ""},
                    "cnpj": {"text": ""},
                    "data_vencimento": {"text": ""},
                    "data_pagamento": {"text": ""},
                    "valor_documento": {"text": ""},
                    "valor_cobrado": {"text": ""},
                    "valor_dif": {"text": ""},
                    "tipo_registro": {"text": "normal"},
                }
                if "COMPROVANTE DE PAGAMENTO DE TITULOS" in data_page[0: 300]:

                    
                    for i in range(len(data_page)):
                        
                        index_aux = 0
                        check_aux = False
                        if data_page[i: i+18] == "BENEFICIARIO FINAL":
                            check_aux = True
                        elif data_page[i: i+13] == "NOME FANTASIA":
                            check_aux = True
                        
                        if check_aux:
                            data_aux = data_page[i: i+18]

                            print( data_aux )
                            index_aux = i+21
                            data_extract["beneficiario_final"]["data_init"] = index_aux
                            data_temp = data_page[i:]

                            for j in range(len(data_temp)):
                                if "CPF" in data_temp[j:j+5]:
                                    index_aux = j-1
                                    data_extract["beneficiario_final"]["data_final"] = i + index_aux
                                    init = data_extract["beneficiario_final"]["data_init"]
                                    final = data_extract["beneficiario_final"]["data_final"]
                                    data_extract["beneficiario_final"]["text"] = data_page[ init: final ].strip()
                                    cnpj_aux = data_page[ final-5: final+35 ].strip().split(":")[1].strip()
                                    data_extract["cnpj"]["text"] = cnpj_aux
                                    break
                                elif "CNPJ" in data_temp[j:j+5]:
                                    index_aux = j-1
                                    data_extract["beneficiario_final"]["data_final"] = i + index_aux
                                    init = data_extract["beneficiario_final"]["data_init"]
                                    final = data_extract["beneficiario_final"]["data_final"]
                                    data_extract["beneficiario_final"]["text"] = data_page[ init: final ].strip()
                                    cnpj_aux = data_page[ final-5: final+35 ].strip().split(":")[1].strip()
                                    data_extract["cnpj"]["text"] = cnpj_aux
                                    data_extract["index"]["text"] = index_page
                                    break

                        elif "DATA DE VENCIMENTO" in data_page[i: i+18]:
                            data_extract["data_vencimento"]["text"] = data_page[i+38: i+48]
                            data_extract["data_pagamento"]["text"]  = data_page[i+87: i+97]
                            # ----
                            valor_documento = ConvertToDataFrame.data_strip(data_page[i+130: i+146])
                            valor_cobrado = ConvertToDataFrame.data_strip(data_page[i+170: i+195])

                            if valor_documento != valor_cobrado:
                                
                                data_extract["valor_dif"]["text"] = ConvertToDataFrame.data_strip(data_page[i+170: i+195])
                                # ----
                                valor_cobrado = ConvertToDataFrame.data_strip(data_page[i+230: i+245])
                                data_extract["tipo_registro"]["text"] = ConvertToDataFrame.check_discount_or_fees(
                                    document_value=valor_documento,
                                    amount_paid=valor_cobrado)

                            data_extract["valor_documento"]["text"] = ConvertToDataFrame.data_strip(valor_documento)
                            data_extract["valor_cobrado"]["text"] = ConvertToDataFrame.data_strip(valor_cobrado)

                            list_data_pages.append(data_extract)
                            print(f"\n\n\n ---------------- { index_page }")
                            print(data_extract)
                            index_page += 1
                            break
                else:
                    list_page_erros.append(index_page)


            except Exception as e:
                print(f" ### ERROR EXTRACT DATA PDF | ERROR: {e}")
                list_page_erros.append({index_page: e})
            
        print(list_data_pages)

        data_to_dataframe = list()
        for data in list_data_pages:
            data_to_dataframe.append({
                "beneficiario_final": data["beneficiario_final"]["text"],
                "cnpj": data["cnpj"]["text"],
                "data_vencimento": data["data_vencimento"]["text"],
                "data_pagamento": data["data_pagamento"]["text"],
                "valor_documento": data["valor_documento"]["text"],
                "valor_cobrado": data["valor_cobrado"]["text"],
                "valor_dif": data["valor_dif"]["text"],
                "tipo_registro": data["tipo_registro"]["text"],
            })
        
        # -------------- CRIAÇÃO DA BASE EM DATAFRAME --------------
        df = pd.DataFrame(data_to_dataframe)

        df = ConvertToDataFrame.create_layout_JB(dataframe=df, model="model_1")

        df = ConvertToDataFrame.transpose_values(dataframe=df, dict_cols_transpose={
            "CNPJ": "cnpj",
            "NOME": "beneficiario_final",
            "DATA": "data_pagamento",
            })
        df = ConvertToDataFrame.drop_columns_dataframe(dataframe=df, list_columns=["cnpj", "beneficiario_final", "data_pagamento"])
        df = ConvertToDataFrame.duplicate_dataframe_rows(dataframe=df)
        df = ConvertToDataFrame.create_dataframe_discount_and_fees(dataframe=df)

        print(df)
        print(f"\n\n\ {list_page_erros}")
        print(f" TT PAGES: {len(pdf_reader.pages)}")
        df = df.sort_values(by=[ "NOME", "GRUPO_LCTO", "TP" ])
        df.index = list(range(0, len(df.index)))

        df = ConvertToDataFrame.readjust_values_dataframe(dataframe=df)
        
        tt_rows = len(df)
        tt_debit    = len(df[df["TP"] == "C"])
        tt_credit   = len(df[df["TP"] == "D"])

        
        # file_name = r"I:\\1. Gaulke Contábil\\Administrativo\\9. TI\\1. Projetos\\7.  Importação Comp. - Banco do Brasil\\base_extrato_banco_do_brasil.xlsx"
        # ConvertToDataFrame.convert_dataframe_to_excel(dataframe=df, file_name=file_name)
        data_json = json.loads(df.to_json(orient="table"))
        print(data_json)

        return {
            "data_table": data_json,
            "tt_rows": tt_rows,
            "tt_debit": tt_debit,
            "tt_credit": tt_credit,
            "list_page_erros": [],
             }
    
    # ----
    
    def read_pdf_relacao_folha_por_empregado(file, grupo_lancamento):
        print(f"\n\n ----- Arquivo informado folha de pagamento: {file}")
        contents = file.read()
        pdf_bytes = io.BytesIO(contents)        

        data = tabula.read_pdf(pdf_bytes, pages="all")
        print(" <<<< ----------------- >>>> ")
        print(data)
        print(" <<<< ----------------- >>>> ")
        list_df = list()

        for i in range(len(data)):
            # contrib = data[i][ data[i]["Código Nome do empregado"] == "Contribuintes" ]
            df_aux = data[i]
            

            for j in df_aux.index:
                index = 0
                if "Contribuintes:" in df_aux["Código Nome do empregado"][j]:
                    index = j
                    df_aux = df_aux[df_aux.index < index]
                    print(f" \n\n ---------------- FILTER df_aux CONTRIBUINTES ---------------- INDEX: {index} \n\n")
                    break
                elif "Empregados:" in df_aux["Código Nome do empregado"][j]:
                    index = j
                    df_aux = df_aux[df_aux.index < index]
                    print(f" \n\n ---------------- FILTER df_aux EMPREGADOS ---------------- INDEX: {index} \n\n")
                    break
            
            print(f"\n\n ----> INDEX LIST: {i}")
            print(df_aux)
            list_df.append(df_aux)
            print(f"\n\n ------------------------- LIST DF: {len(list_df)}")
        
        print(list_df)
        df = pd.concat(list_df)
        
        df.index = list(range(0, len(df.index)))
        
        # df.dropna(subset=["Líquido"],  inplace=True)
        
        df[['ID', 'NOME_TEMP']] = df['Código Nome do empregado'].str.split(' ', n=1, expand=True)

        # ----
        df = ConvertToDataFrame.drop_columns_dataframe(dataframe=df, list_columns=["Unnamed: 0", "Código Nome do empregado"])
        print("\n\n ******************************************** ")
        print(df)     
        
        df = ConvertToDataFrame.create_layout_JB(dataframe=df, model="model_2", grupo_lancamento=grupo_lancamento)
        df = ConvertToDataFrame.transpose_values(dataframe=df, dict_cols_transpose={
            "VALOR": "Líquido",
            })

        df = ConvertToDataFrame.filter_data_dataframe(
            daraframe=df,
            name_column="VALOR",
            list_remove_values=["0.00", "0,00"])
        df = ConvertToDataFrame.transpose_values(dataframe=df, dict_cols_transpose={
            "NOME": "NOME_TEMP",
        })
        
        # df = ConvertToDataFrame.drop_columns_dataframe(dataframe=df, list_columns=["NOME_TEMP"])

        df = ConvertToDataFrame.duplicate_dataframe_rows(dataframe=df)
        df = df.sort_values(by=[ "NOME", "GRUPO_LCTO", "TP" ])
        print(" ***** ---------------------------- ***** ")

        df.index = list(range(0, len(df.index)))
        df = df.dropna(subset=["VALOR"])
        df = ConvertToDataFrame.create_cod_erp_to_dataframe(dataframe=df)
        print(df)

        tt_rows = len(df)
        tt_debit    = len(df[df["TP"] == "C"])
        tt_credit   = len(df[df["TP"] == "D"])
        
        # file_name = r"I:\\1. Gaulke Contábil\\Administrativo\\9. TI\\1. Projetos\\7.  Importação Comp. - Banco do Brasil\\base_extrato_banco_do_brasil.xlsx"
        # ConvertToDataFrame.convert_dataframe_to_excel(dataframe=df, file_name=file_name)

        data_json = json.loads(df.to_json(orient="table"))
        print(data_json)

        return {
            "data_table": data_json ,
            "tt_rows": tt_rows,
            "tt_debit": tt_debit,
            "tt_credit": tt_credit,
            "list_page_erros": [],
             }

    # ----
    
    def read_xlsx_relacao_gnre(file, data_contas):

        print(f"\n\n ----- Arquivo informado GNRE: {file}")
        contents = file.read()
        xlsx_bytes = io.BytesIO(contents)

        print("\n\n ---------------------------------------------- DF READ - STEP 1 ")

        file = pd.ExcelFile(xlsx_bytes)
        sheet_name = file.sheet_names[0]

        print("\n\n ---------------------------------------------- DF READ - STEP 2 ")

        df = file.parse(sheet_name=sheet_name, dtype='str')

        print("\n\n ---------------------------------------------- DF READ - STEP 3 ")
        print(df)

        print("\n\n ---------------------------------------------- DF READ - STEP 4 ")
        df = pd.read_excel(xlsx_bytes)
        df.rename(columns={
            "C笈_UF_IN沊IO_PREST": "UF_INÍCIO",
            "C笈_UF_FIM_PREST": "UF_FIM",
            "N渧ERO_CTE": "CTE",
            "DATA_EMISS鬃": "DATA_EMISSÃO"
        }, inplace=True)
        
        print("\n\n ---------------------------------------------- DF READ - STEP 5 ")

        df = df[(df["UF_INÍCIO"] != "SC") & (df["SITUACAO"] != "CANCELADO")]

        print("\n\n ---------------------------------------------- DF READ - STEP 6 ")

        df = df[["CTE", "DATA_EMISSÃO", "VALOR_ICMS", "UF_INÍCIO", "UF_FIM"]]

        print("\n\n ---------------------------------------------- DF READ - STEP 6 ")


        df = ConvertToDataFrame.filter_columns_dataframe(daraframe=df, list_columns=["CTE", "DATA_EMISSÃO","VALOR_ICMS", "UF_INÍCIO", "UF_FIM"])

        print("\n\n ---------------------------------------------- DF READ - STEP 7 ")

        df['VALOR_ICMS'] = df['VALOR_ICMS'].round(2)
        df["VALOR_ICMS"] = df['VALOR_ICMS'].astype(str)

        print(df.info())
        
        for i in df.index:
            if "." not in df["VALOR_ICMS"][i]:
                df["VALOR_ICMS"][i] = df["VALOR_ICMS"][i] + ".00"
            elif df["VALOR_ICMS"][i].split(".")[1] in ['0','1','2','3','4','5','6','7','8','9']:
                print(" -------------- SPLIT ")
                df["VALOR_ICMS"][i] = df["VALOR_ICMS"][i] + "0"
            
            print(">>>>> ", df["VALOR_ICMS"][i], type( df["VALOR_ICMS"][i] ) )
        
        df.dropna(subset=["CTE"], inplace=True)
        df["CTE"] = list(map(lambda x: int(x), df["CTE"].values))
        

        print(" ----------------  STEP ADJUST DT ---------------- ")
        print(df.info())
        dt = pd.to_datetime(df['DATA_EMISSÃO'])
        formatted_date = dt.dt.strftime("%d/%m/%Y")
        df['DATA_EMISSÃO'] = formatted_date
        

        print(df)
        
        file.close()

        print(" <<<< --------- GNRE --------- >>>> ")
        df = ConvertToDataFrame.create_layout_JB(dataframe=df, model="model_3")
        df = ConvertToDataFrame.transpose_values(dataframe=df, dict_cols_transpose={
            "VALOR": "VALOR_ICMS",
            "DATA": "DATA_EMISSÃO",
            })
        # ----
        df = ConvertToDataFrame.filter_data_dataframe(daraframe=df, name_column="VALOR", list_remove_values=["0.00", "0,00"])
        # ----
        df = ConvertToDataFrame.duplicate_dataframe_rows(dataframe=df)
        df = ConvertToDataFrame.create_additional_columns(dataframe=df, column_name="NUMERO_CONTA_CONTABIL", default_value="-")

        df = df.sort_values(by=[ "CTE", "TP" ])
        print(" <<<< ---------------------------- >>>> ")

        df.index = list(range(0, len(df.index)))

        df = ConvertToDataFrame.create_cod_erp_to_dataframe(dataframe=df)

        for i in range(len(df.index)):

            uf_inicio = df["UF_INÍCIO"][i]
            print(f" ----> INDEX REPLACE ACCOUNTS VALUES: {i} | uf_inicio: {uf_inicio}")

            conta_debito = data_contas.get(uf_inicio)["conta_debito"]
            conta_credito = data_contas.get(uf_inicio)["conta_credito"]

            print(f"""
                --------- CONFIG CONTAS POR UF
                --> uf_inicio: {uf_inicio}
                --> conta_debito: {conta_debito}
                --> conta_credito: {conta_credito}
            """)
            
            if df["TP"][i] == "C":
                df["NUMERO_CONTA_CONTABIL"][i] = conta_credito
            elif df["TP"][i] == "D":
                df["NUMERO_CONTA_CONTABIL"][i] = conta_debito

        df = ConvertToDataFrame.transpose_values(dataframe=df, dict_cols_transpose={
            "CONTA": "NUMERO_CONTA_CONTABIL",
        })

        print(df)
        tt_rows = len(df)
        tt_debit    = len(df[df["TP"] == "C"])
        tt_credit   = len(df[df["TP"] == "D"])


        print(f"""
            --------- CONFIG CONTAS POR UF
            --> tt_rows: {tt_rows}
            --> tt_debit: {tt_debit}
            --> tt_credit: {tt_credit}
        """)

        # file_name = r"I:\\1. Gaulke Contábil\\Administrativo\\9. TI\\1. Projetos\\2. Importação GNRE\NOVO MODELO AUTOMACAO\\base_GNRE.xlsx"
        # ConvertToDataFrame.convert_dataframe_to_excel(dataframe=df, file_name=file_name)
        print(" <<<< ----------------- >>>> ")

        data_json = json.loads(df.to_json(orient="table"))
        # print(data_json)

        return {
            "data_table": data_json ,
            "tt_rows": tt_rows,
            "tt_debit": tt_debit,
            "tt_credit": tt_credit,
            "list_page_erros": [],
             }
    
    # ----
    
    def read_pdf_relacao_entrada_titulos_desc_sicoob(file):
        try:
            print(f"\n\n ----- Arquivo informado SICOOB: {file}")

            contents = file.read()
            pdf_bytes = io.BytesIO(contents)
            dataframes = tabula.read_pdf( pdf_bytes, pages="all" )

            list_df = list()
            for df in dataframes:
                print(" ------------------------ df ------------------------ ")
                print(df)
                list_df.append(df)
            
            df = pd.concat(list_df)
            df.index = list(range(0, len(df.index)))

            print(" <<<< ----------------- >>>> ")

            print(df)

            df = ConvertToDataFrame.transpose_values(dataframe=df, dict_cols_transpose={
                "NOME": "Sacado",
                "VALOR": "Valor (R$)",
                "DATA_VENCIMENTO": "Vencimento",
                "DT_LIMITE_PGTO": "Dt. Limite Pgto",
                "NOSSO_NUMERO": "Nosso Número",
                "SEU_NUMERO": "Seu Número",
                })
            df = ConvertToDataFrame.readjust_values_dataframe_decimal(dataframe=df, list_cols_name=["VALOR"], replace_values_list=False)
            df = ConvertToDataFrame.create_layout_JB(dataframe=df, model="model_5", value_generic="Sicoob")
            df = ConvertToDataFrame.transpose_values(dataframe=df, dict_cols_transpose={
                "DATA": "Entrada",
                "VALOR": "Valor (R$)",
                })
            
            df = ConvertToDataFrame.duplicate_dataframe_rows(dataframe=df)
            df.index = list(range(0, len(df.index)))
            for i in df.index:
                if df["TP"][i] == "C":
                    print(df["TP"][i], "524")
                    df["CONTA"][i] = "524"
                elif df["TP"][i] == "D":
                    print(df["TP"][i], "11")
                    df["CONTA"][i] = "11"
            

            df = df.sort_values(by=[ "NOME", "NOSSO_NUMERO", "TP" ])

            # file_name = "base_entrada_titulos_desc_sicoob.xlsx"
            # ConvertToDataFrame.convert_dataframe_to_excel(dataframe=df, file_name=file_name)
            df = ConvertToDataFrame.create_cod_erp_to_dataframe(dataframe=df)
            
            tt_rows = len(df)
            tt_debit    = len(df[df["TP"] == "C"])
            tt_credit   = len(df[df["TP"] == "D"])
            data_json = json.loads(df.to_json(orient="table"))
            print(data_json)
            print(f"""
                --------- CONFIG CONTAS POR UF
                --> tt_rows: {tt_rows}
                --> tt_debit: {tt_debit}
                --> tt_credit: {tt_credit}
            """)

            return {
                "data_table": data_json ,
                "tt_rows": tt_rows,
                "tt_debit": tt_debit,
                "tt_credit": tt_credit,
                "list_page_erros": [],
                }
        except Exception as e:
            print(f" ### ERROR GENERATE DATAFRAME | ERROR: {e}")
    
    # ----
    
    def read_xlsx_relacao_cobrancas_pagas(file):
        try:
            print(f"\n\n ----- Arquivo informado cobranças pagas: {file}")
            contents = file.read()
            xlsx_bytes = io.BytesIO(contents)

            file = pd.ExcelFile(xlsx_bytes)
            sheet_name = file.sheet_names[0]
            df = file.parse(sheet_name=sheet_name)
            df = df.rename(columns=df.iloc[0]).drop(df.index[0])
            df.index = list(range(0, len(df.index)))

            df = ConvertToDataFrame.rename_columns_dataframe(dataframe=df, dict_replace_names={
                "CPF/CNPJ": "CNPJ",
                })
            df = ConvertToDataFrame.readjust_values_dataframe_decimal(dataframe=df, list_cols_name=["Valor", "Valor pago"])
            df = ConvertToDataFrame.create_layout_JB(dataframe=df, model="model_4")


            df = ConvertToDataFrame.transpose_values(dataframe=df, dict_cols_transpose={
                "VALOR": "Valor",
                "VALOR_PAGO": "Valor pago",
                })
            
            df = ConvertToDataFrame.duplicate_dataframe_rows(dataframe=df)
                       
            df = ConvertToDataFrame.create_dataframe_discount_and_fees_cobrancas_pagas(dataframe=df)

            df.index = list(range(0, len(df.index)))

            for i in df.index:
                if df["TP"][i] == "C" and df["TYPE_PROCESS"][i] == "comum":
                    df["VALOR"][i]  = str(df["VALOR"][i])
                # ----
                elif df["TP"][i] == "D" and df["TYPE_PROCESS"][i] == "comum":
                    df["VALOR"][i]  = str(df["VALOR_PAGO"][i])
                # ----
                elif df["TYPE_PROCESS"][i] != "comum":
                    value_aux = float(df["VALOR_PAGO"][i])
                    if value_aux < 1:
                        value_aux = str(value_aux).replace(",", ".")
                    else:
                        value_aux = str(value_aux).replace(".", "").replace(",", ".")
                    
                    df["VALOR"][i]  = value_aux
            
            df = ConvertToDataFrame.create_cod_erp_to_dataframe(dataframe=df)

            df = ConvertToDataFrame.transpose_values(dataframe=df, dict_cols_transpose={
                "DATA": "Vencimento",
                "NOME": "Nome Cliente",
            })

            df.sort_values(by=["COMPL_HISTORICO", "VALOR"], inplace=True)

            # file_name = r"I:\\1. Gaulke Contábil\\Administrativo\\9. TI\\1. Projetos\\4. Importação WB Telecom Recebimento\\base_contas_pagas.xlsx"
            # ConvertToDataFrame.convert_dataframe_to_excel(dataframe=df, file_name=file_name)
            
            tt_rows = len(df)
            tt_debit    = len(df[df["TP"] == "C"])
            tt_credit   = len(df[df["TP"] == "D"])
            data_json = json.loads(df.to_json(orient="table"))
            # print(data_json)

            print(f"""
                --------- CONFIG CONTAS
                --> tt_rows: {tt_rows}
                --> tt_debit: {tt_debit}
                --> tt_credit: {tt_credit}
            """)

            return {
                "data_table": data_json ,
                "tt_rows": tt_rows,
                "tt_debit": tt_debit,
                "tt_credit": tt_credit,
                "list_page_erros": [],
                }

            
        except Exception as e:
            print(f" \n\n ERROR GENERATE COBRANÇAS PAGAS | ERROR: {e}")
            return {"code": 500, "msg": "erro ao gerar pacote cobranças pagas.", "error": e}
    
    # ----
    
    def read_xlsx_decorise(file, grupo_lancamento):
        try:
            print(f"\n\n ----- Arquivo informado decorise: {file} | grupo_lancamento: {grupo_lancamento}")
            contents = file.read()
            xlsx_bytes = io.BytesIO(contents)

            file = pd.ExcelFile(xlsx_bytes)
            sheet_name = file.sheet_names[-1]
            df = file.parse(sheet_name=sheet_name)
            print(df.columns)
            df = ConvertToDataFrame.filter_columns_dataframe(daraframe=df, list_columns=[
                "Conf. Gateway",
                "Id",
                "Valor Recebível",
                "Valor Total",
                "Comissão Paga",
                "Data/Hora",
                "Data Esperada",
            ])

            # df["Data/Hora"] = pd.to_datetime(df["Data/Hora"].values, errors="raise", format="%d/%m/%Y %H:%M:%S")
            df["Data/Hora"] = list(map(lambda x: x.split()[0], df["Data/Hora"].values ))
            df = ConvertToDataFrame.rename_columns_dataframe(dataframe=df, dict_replace_names={
                "Data/Hora": "DATA_TEMP"
            })
            df = ConvertToDataFrame.create_layout_JB(dataframe=df, model="model_6", grupo_lancamento=grupo_lancamento)

            #  ----------------------- necessário para criar o Dataframe de Commissões -----------------------
            df_commission  = df.copy()
            df_commission = df_commission[ df_commission["TP"] == "D" ]
            df = ConvertToDataFrame.duplicate_dataframe_rows(dataframe=df)
            df = pd.concat([df, df_commission])
            # ------------------------------------------------------------------------------------------------

            df = ConvertToDataFrame.transpose_values(dataframe=df, dict_cols_transpose={
                "DATA": "DATA_TEMP",
                "VALOR": "Valor Recebível",
            })


            df.sort_values(by=["Id", "VALOR", "TP"], inplace=True)
            df.index = list( range(0, len(df.index)) )

            # df = ConvertToDataFrame.create_cod_erp_to_dataframe(dataframe=df)

            #  REAJUSTE DO VALOR DE COD_HISTORICO, necessário para não ser enviado com o valor de grupo_lancamento.
            df = ConvertToDataFrame.create_additional_columns(dataframe=df, column_name="COD_HISTORICO", default_value="")

            cont_aux = 0
            for i in df.index:
                print(f' ------ INDEX LOOP VALUES: {i}| {df["VALOR"][i]}')
                if cont_aux == 0:
                    df["VALOR"][i] = df["Valor Total"][i]
                    df["TYPE_PROCESS"][i] = "process_credit"
                    cont_aux += 1
                elif cont_aux == 1:
                    df["VALOR"][i] = df["Valor Recebível"][i]
                    df["TYPE_PROCESS"][i] = "process_debit_valor_receb"
                    cont_aux += 1
                elif cont_aux == 2:
                    df["VALOR"][i] = df["Comissão Paga"][i]
                    df["TYPE_PROCESS"][i] = "process_debit_valor_comissao"
                    cont_aux = 0

            
            df['VALOR'] = df['VALOR'].round(2)
            df["VALOR"] = df['VALOR'].astype(str)

            for i in df.index:
                if "." not in df["VALOR"][i]:
                    df["VALOR"][i] = df["VALOR"][i] + ".00"
                elif df["VALOR"][i].split(".")[1] in ['0','1','2','3','4','5','6','7','8','9']:
                    print(" -------------- SPLIT ")
                    df["VALOR"][i] = df["VALOR"][i] + "0"
                
                print(">>>>> ", df["VALOR"][i], type( df["VALOR"][i] ) )


            # file_name = r"I:\\1. Gaulke Contábil\\Administrativo\\9. TI\\1. Projetos\\6. Importação DECORISE\\base_test_Leonardo.xlsx"
            # ConvertToDataFrame.convert_dataframe_to_excel(dataframe=df, file_name=file_name)

            print(df.info())
            print(df)

            tt_rows = len(df)
            tt_debit    = len(df[df["TP"] == "C"])
            tt_credit   = len(df[df["TP"] == "D"])

            data_json = json.loads(df.to_json(orient="table"))
            # print(data_json)

            print(f"""
                --------- CONFIG CONTAS
                --> tt_rows: {tt_rows}
                --> tt_debit: {tt_debit}
                --> tt_credit: {tt_credit}
            """)

            return {
                "data_table": data_json ,
                "tt_rows": tt_rows,
                "tt_debit": tt_debit,
                "tt_credit": tt_credit,
                "list_page_erros": [],
                }

            
        except Exception as e:
            print(f" \n\n ERROR GENERATE COBRANÇAS PAGAS | ERROR: {e}")
            return {"code": 500, "msg": "erro ao gerar pacote cobranças pagas.", "error": e}

    # ----
    
    # 
    #  ----------------------------------- ETL ARAO DOS SANTOS -----------------------------------
    #  file_populate: Base Arão dos Santos -> Para preenchimento
    #  file_base_query: Base Arão dos Santos -> Base de consulta

    def read_Excel_File(contents):
        xlsx_bytes = io.BytesIO(contents)
        file = pd.ExcelFile(xlsx_bytes)
        sheet_name = file.sheet_names[0]
        df = file.parse(sheet_name=sheet_name)
        return df
    
    # ----

    def read_xlsx_arao_dos_santos(file_contabil, file_consulta):
        try:
            print(f"\n\n ----- Arquivo informado arão dos santos | file_contabil: {file_contabil} | file_consulta: {file_consulta}")
            
            # contents = file_populate.read()
            # xlsx_bytes = io.BytesIO(contents)
            # file = pd.ExcelFile(xlsx_bytes)
            # sheet_name = file.sheet_names[-1]
            # df = file.parse(sheet_name=sheet_name)
            # df_temp_consulta = ConvertToDataFrame.read_Excel_File(contents=file_consulta)
            # df_temp_contabil = ConvertToDataFrame.read_Excel_File(contents=file_contabil)

            contents = file_consulta.read()
            df_temp_consulta = ConvertToDataFrame.read_Excel_File(contents=contents)
            print("\n\n ------------------------ df_temp_consulta ------------------------ ")
            print(df_temp_consulta)

            contents = file_contabil.read()
            df_temp_contabil = ConvertToDataFrame.read_Excel_File(contents=contents)

            # Formata a data como 'dd/mm/yyyy'
            df_temp_consulta['Data'] = pd.to_datetime(df_temp_consulta['Data'])
            df_temp_consulta['Data'] = df_temp_consulta['Data'].dt.strftime('%d/%m/%Y')

            print("\n\n ------------------------ df_temp_contabil ------------------------ ")
            print(df_temp_contabil)

            # df_temp_contabil []

            list_pendencias = list()
            for i in df_temp_contabil.index:
                
                nf = df_temp_contabil["Nº NF"][i]
                query_df_contabil = df_temp_consulta[df_temp_consulta["Nota Fiscal"] == nf ][["Data", "Nota Fiscal"]]
                
                if len(query_df_contabil) >= 1:
                    df_temp_contabil["Data Recebim. NF"][i] = query_df_contabil["Data"].values[0]
                else:
                    list_pendencias.append(nf)
            
                print(f" -------------------- QUERY RESULT -------------------- NF: {nf}")
                print(query_df_contabil)

            # 
            # 
            # ------------------------------------------------- DF PENDÊNCIAS -------------------------------------------------
            print(" \n\n ----------------- DF PENDÊNCIAS ----------------- ")
            df_pendencias = df_temp_contabil[df_temp_contabil["Nº NF"].isin(list_pendencias)]
            df_pendencias.index = list(range(0, len(df_pendencias)))
            print(df_pendencias)
            
            #
            # 
            #  ------------------------------------------------- DF PENDÊNCIAS -------------------------------------------------
            print("\n\n ------------------------ query_df_contabil TRATADO ------------------------ ")
            df_temp_contabil.index = list(range(0, len(df_temp_contabil)))
            print(df_temp_contabil)
            print(df_temp_contabil.info())
            
            df_temp_contabil = ConvertToDataFrame.rename_columns_dataframe(dataframe=df_temp_contabil, dict_replace_names={
                "CNPJ": "CNPJ_ORIGIN"
            })

            df = ConvertToDataFrame.create_layout_JB(dataframe=df_temp_contabil, model="model_7")

            df["VALOR_NF_LIQ"] = df["Valor Bruto NF"] - df["IRPJ Retido"]
            df["VLR_LIQUIDO"] = df["VALOR_NF_LIQ"] - df["CSLL Retida"] - df["Cofins Retido"] - df["PIS Retido"]

            df = ConvertToDataFrame.duplicate_dataframe_rows_lote(dataframe=df, list_update_cols=[
                {"TP": "C", "TYPE_PROCESS": "comum"},
                {"TP": "D", "TYPE_PROCESS": "debit_PIS"},
                {"TP": "D", "TYPE_PROCESS": "debit_CSLL"},
                {"TP": "D", "TYPE_PROCESS": "debit_COFINS"},
            ])

            df.sort_values(by=["Nº NF", "Nome Cliente", "TP", "TYPE_PROCESS"], inplace=True)
            df.index = list(range(0, len(df.index)))
            #
            # 
            #  ------------------------------------------------- CÁLCULO DE IMPOSTOS -------------------------------------------------
            # TP | CONTA
            # -- - --------------
            # C  | crédito
            # D  | débito
            # D  | Cofins Retido
            # D  | CSLL Retida
            # D  | PIS Retido

            cont_aux = 0
            for i in df.index:
                
                # df["COMPL_HISTORICO"][i] = f"Recebimento dupl. nr {numero_NF} - {nome_cliente}"

                if cont_aux == 0:

                    df["VALOR"][i] = df["VALOR_NF_LIQ"][i]
                    df["CONTA"][i] = ""
                    cont_aux += 1

                elif cont_aux == 1:

                    df["VALOR"][i] = df["VLR_LIQUIDO"][i]
                    df["CONTA"][i] = "-"
                    cont_aux += 1

                elif cont_aux == 2:

                    df["VALOR"][i] = df["Cofins Retido"][i]
                    df["COMPL_HISTORICO"][i] = df["COMPL_HISTORICO"][i].replace("Recebimento", "COFINS")
                    df["CONTA"][i] = "88"
                    cont_aux += 1

                elif cont_aux == 3:

                    df["VALOR"][i] = df["CSLL Retida"][i]
                    df["COMPL_HISTORICO"][i] = df["COMPL_HISTORICO"][i].replace("Recebimento", "CSLL")
                    df["CONTA"][i] = "94"
                    cont_aux += 1

                elif cont_aux == 4:

                    df["VALOR"][i] = df["PIS Retido"][i]
                    df["COMPL_HISTORICO"][i] = df["COMPL_HISTORICO"][i].replace("Recebimento", "PIS")
                    df["CONTA"][i] = "87"
                    cont_aux = 0
            
            # ------------------------------------------------------------------------



            # df['VALOR'] = df['VALOR'].astype('float64')
            # df['VALOR'] = df['VALOR'].round(2)
            # df["VALOR"] = df['VALOR'].astype(str)

            # for i in df.index:
            #     if "." not in df["VALOR"][i]:
            #         df["VALOR"][i] = df["VALOR"][i] + ".00"
            #     elif df["VALOR"][i].split(".")[1] in ['0','1','2','3','4','5','6','7','8','9']:
            #         print(" -------------- SPLIT ")
            #         df["VALOR"][i] = df["VALOR"][i] + "0"
                
            #     print(">>>>> ", df["VALOR"][i], type( df["VALOR"][i] ) )

            
            print(" \n\n ---------------------- TRANSPOSE VALUES DATAFRAME ---------------------- ")

            df = ConvertToDataFrame.transpose_values(dataframe=df, dict_cols_transpose={
                "CNPJ": "CNPJ_ORIGIN",
                "DATA": "Data Recebim. NF",
                "NOME": "Nome Cliente",

            })

            df = ConvertToDataFrame.create_cod_erp_to_dataframe(dataframe=df)

            print(df)
            print(df.info())

            # ------------------------------------------------------------------------------------
            # ---------------------- AJUSTE PARA MODELO TP_REGISTRO ===> 03 ----------------------
            # ------------------------------------------------------------------------------------

            df_tp_registro_03 = df.copy()

            list_remove = [0, 0.0, "0.0", "0.00", "0.00", "0,00"]
            df_tp_registro_03 = df_tp_registro_03[~df_tp_registro_03['VALOR'].isin(list_remove)]
            df_tp_registro_03 = df_tp_registro_03.dropna(subset=['DATA'])
            

            df_tp_registro_03 = df_tp_registro_03[  df_tp_registro_03["TYPE_PROCESS"] != "comum"  ]
            df_tp_registro_03["TP_REGISTRO"] = "03"

            df_tp_registro_03 = ConvertToDataFrame.create_additional_columns(dataframe=df_tp_registro_03, column_name="IMPOSTO", default_value="")
            df_tp_registro_03["CODIGO_IMPOSTO"] = "5952"
            df_tp_registro_03["BC_IMPOSTO"] = df_tp_registro_03["Valor Bruto NF"]
            df_tp_registro_03["ALIQUOTA"] = "-"
            df_tp_registro_03["VALOR_IMPOSTO"] = "-"
            df_tp_registro_03["TP_RETENCAO"] = "3"
            df_tp_registro_03["COD_MINICIPIO_DEVIDO_ISS"] = ""
            df_tp_registro_03["NAT_RETENCAO"] = "3"
            df_tp_registro_03["TP_RECEITA"] = "1"
            df_tp_registro_03["CNPJ_EMPRESA_03"] = ""
            df_tp_registro_03["IE_EMPRESA_03"] = ""

            for i in df_tp_registro_03.index:
                if df_tp_registro_03["TYPE_PROCESS"][i] == "debit_COFINS":
                    df_tp_registro_03["IMPOSTO"][i] = "1102"
                    df_tp_registro_03["ALIQUOTA"][i] = "3,00"
                    df_tp_registro_03["VALOR_IMPOSTO"][i] = df_tp_registro_03["VALOR"][i]

                # ----
                elif df_tp_registro_03["TYPE_PROCESS"][i] == "debit_PIS":
                    df_tp_registro_03["IMPOSTO"][i] = "1101"
                    df_tp_registro_03["ALIQUOTA"][i] = "0,65"
                    df_tp_registro_03["VALOR_IMPOSTO"][i] = df_tp_registro_03["VALOR"][i]
                # ----
                elif df_tp_registro_03["TYPE_PROCESS"][i] == "debit_CSLL":
                    df_tp_registro_03["IMPOSTO"][i] = "1103"
                    df_tp_registro_03["ALIQUOTA"][i] = "1,00"
                    df_tp_registro_03["VALOR_IMPOSTO"][i] = df_tp_registro_03["VALOR"][i]


            #  --------------------------------------

            df_tp_registro_03 = ConvertToDataFrame.create_additional_columns(dataframe=df_tp_registro_03, column_name="COL_AUX__18", default_value="")
            df_tp_registro_03 = ConvertToDataFrame.create_additional_columns(dataframe=df_tp_registro_03, column_name="COL_AUX__19", default_value="")
            df_tp_registro_03 = ConvertToDataFrame.create_additional_columns(dataframe=df_tp_registro_03, column_name="COL_AUX__20", default_value="")
            df_tp_registro_03 = ConvertToDataFrame.create_additional_columns(dataframe=df_tp_registro_03, column_name="COL_AUX__21", default_value="")
            
            df_tp_registro_03 = df_tp_registro_03[[
                
                # ------------------ BASE LAYOUT JB 03 ------------------

                "TP_REGISTRO", # 01
                "NOME",
                "COD_EMPRESA", # 02
                "FILIAL", # 03
                "NR_L_CTO_ERP", # 04
                "TP", # 05
                "CNPJ", # 06
                "IMPOSTO", # 07
                "CODIGO_IMPOSTO", # 08
                "BC_IMPOSTO", # 09
                "ALIQUOTA", # 10
                "VALOR_IMPOSTO", # 11
                "TP_RETENCAO", # 12
                "COD_MINICIPIO_DEVIDO_ISS", # 13
                "NAT_RETENCAO", # 14
                "TP_RECEITA", # 15
                "CNPJ_EMPRESA_03", # 16
                "IE_EMPRESA_03", # 17

                "COL_AUX__18",
                "COL_AUX__19",
                "COL_AUX__20",
                "COL_AUX__21",
                
                "TYPE_PROCESS",    
            ]]

            tt_index_00 = len(df.index)
            tt_index_03 = len(df_tp_registro_03.index)

            # df_tp_registro_03["NR_L_CTO_ERP"] = ConvertToDataFrame.create_cod_erp_to_dataframe(dataframe=df_tp_registro_03, index_default=tt_index_00)

            print(df_tp_registro_03)


            
            list_remove = [0, 0.0, "0.0", "0.00", "0.00", "0,00"]

            df = df.dropna(subset=['DATA'])
            df = df[~df['VALOR'].isin(list_remove)]

            df_tp_registro_03 = df_tp_registro_03[~df_tp_registro_03['VALOR_IMPOSTO'].isin(list_remove)]
            
            print("\n\n -------------- DF 00 -------------- ")
            print(df)
            print(df.info())

            print("\n\n -------------- DF 03 -------------- ")
            print(df_tp_registro_03)
            print(df_tp_registro_03.info())

            data_json = json.loads(df.to_json(orient="table"))
            data_json_03 = json.loads(df_tp_registro_03.to_json(orient="table"))
            # print(data_json)


            tt_rows = len(df)
            tt_debit    = len(df[df["TP"] == "C"])
            tt_credit   = len(df[df["TP"] == "D"])

            # ------------

            tt_rows_03 = len(df_tp_registro_03)
            tt_debit_03    = len(df_tp_registro_03[df_tp_registro_03["TP"] == "C"])
            tt_credit_03   = len(df_tp_registro_03[df_tp_registro_03["TP"] == "D"])

            print(f"""
                --------- CONFIG CONTAS
                --> tt_rows: {tt_rows}
                --> tt_debit: {tt_debit}
                --> tt_credit: {tt_credit}

                --> tt_index_00: {tt_index_00}
                --> tt_index_03: {tt_index_03}

                --> tt_rows_03: {tt_rows_03}
                --> tt_debit_03: {tt_debit_03}
                --> tt_credit_03: {tt_credit_03}
            """)

            file_name = r"I:\\1. Gaulke Contábil\\Administrativo\\9. TI\\1. Projetos\\8. Importação Arão dos Santos Recebimentos\\00_base_tratada_arao_dos_santos.xlsx"
            ConvertToDataFrame.convert_dataframe_to_excel(dataframe=df, file_name=file_name)

            file_name = r"I:\\1. Gaulke Contábil\\Administrativo\\9. TI\\1. Projetos\\8. Importação Arão dos Santos Recebimentos\\03_base_tratada_arao_dos_santos.xlsx"
            ConvertToDataFrame.convert_dataframe_to_excel(dataframe=df_tp_registro_03, file_name=file_name)

            return {
                "data_table": data_json,
                "data_json_03": data_json_03,
                "tt_rows": tt_rows,
                "tt_debit": tt_debit,
                "tt_credit": tt_credit,
                "tt_rows_03": tt_rows_03,
                "tt_debit_03": tt_debit_03,
                "tt_credit_03": tt_credit_03,
                "list_page_erros": [],
                }
            
        except Exception as e:
            print(f" \n\n ERROR GENERATE ARÃO DOS SANTOS | ERROR: {e}")
            return {"code": 500, "msg": "erro ao gerar pacote Arão dos Santos.", "error": e}
        
    # ----
    
    def read_pdf_comprovante_banco_bradesco(file):

        print(f"\n\n ----- Arquivo informado comprovante Bradesco | arquivo: {file}")

        contents = file.read()
        pdf_bytes = io.BytesIO(contents)
        pdf_reader = PdfReader(pdf_bytes)

        list_data_pages = list()
        list_page_erros = list()
        index_page = 0
        print(f" TT PAGES: {len(pdf_reader.pages)}")


        data_to_table = {
            # ---------- IDENTIFICADORES
            # "nome_beneficiario": list(),
            "cnpj_beneficiario": list(),

            # "nome_pagador": list(),
            "cnpj_pagador": list(),

            # # ---------- DATAS
            "data_de_debito": list(),
            "data_de_vencimento": list(),

            # ---------- VALORES
            "valor": list(),
            "desconto": list(),
            "abatimento": list(),
            "bonificacao": list(),
            "multa": list(),
            "juros": list(),
            "valor_total": list(),

        }

        for index_page in range(len(pdf_reader.pages)):
            try:
                print(f"\n\n\n ---- INDEX PAGE: {index_page}")
                
                page = pdf_reader.pages[index_page]
                
                
                data_page = page.extract_text()
                print("\n\n ----------------------- DATA EXTRACT ----------------------- ")
                print(data_page)
                cont_aux = 0
                for i in range(len(data_page)):
                    
                    if "Beneficiário Final" in data_page[i:i+18]:
                        print(f" << {data_page[i:i+18]} >>")
                        print(f" ---> CNPJ BENEFICIARIO {i} / {data_page[i+19:i+38]}")
                        data_to_table["cnpj_beneficiario"].append( data_page[i+19:i+38] )

                    if data_page[ i : i+23 ] == "CPF/CNPJ Beneficiário:":
                        print(f" << {data_page[i+22 : i+50]} >>")
                        data_temp = data_page[i+22 :]
                        
                        for j in range(len(data_temp)):
                            if "Nome" in data_temp[j:j+5]:
                                print(f"\n ---> NOME BENEFICIARIO {i} / {data_page[i+j+8:i+(j+20)]}")
                                break
                            
                        # data_to_table["cnpj_beneficiario"].append( data_page[i+19:i+38] )



                   
                    if data_page[i:i+2] == "R$":
                        value_aux = data_page[i:i+15]
                        print(f" -------------->>>> {value_aux}")
                        index_fim = None

                        data_aux = data_page[i:i+18]
                        for j in range(len(data_aux)):
                            if data_aux[j] == ",":
                                index_fim = i + (j+3)
                                break
                        value = data_page[i:index_fim]
                        print(f" ---> VALOR: {value}")
                        
                        if " V" in value_aux:
                            data_to_table["valor_total"].append(value)

                        elif "Va" in value_aux:
                            data_to_table["valor"].append(value)
                            data_de_vencimento = data_page[index_fim+5:index_fim+15]
                            cnpj_pagador = data_page[index_fim+61:index_fim+80]

                            data_de_debito = data_page[index_fim+35:index_fim+45]
                            data_to_table["data_de_debito"].append(data_de_debito)
                            data_to_table["data_de_vencimento"].append(data_de_vencimento)

                            data_to_table["cnpj_pagador"].append( cnpj_pagador )
                        
                        elif "Descont" in data_aux:
                            data_to_table["desconto"].append(value)

                        elif "Abatime" in data_aux:
                            data_to_table["abatimento"].append(value)

                        elif "Bonific" in data_aux:
                            data_to_table["bonificacao"].append(value)

                        elif "Multa" in data_aux:
                            data_to_table["multa"].append(value)

                        elif "Juros" in data_aux:
                            data_to_table["juros"].append(value)
                        

                    
            except Exception as e:
                print(f" ### ERROR EXTRACT DATA PDF | ERROR: {e}")
                list_page_erros.append({index_page: e})
            
        print(data_to_table)
        df = pd.DataFrame.from_dict(data_to_table)
        print(df)

        # return {
        #     "data_table": data_json,
        #     "tt_rows": tt_rows,
        #     "tt_debit": tt_debit,
        #     "tt_credit": tt_credit,
        #     "list_page_erros": [],
        #      }
        return {}