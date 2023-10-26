import os
import json
from time import time

import tabula
import pandas as pd


def read_file_data_post(df, name_user, grupo_lancamento):
    try:
        name_sheets_dafault = "Relação da Folha por Empregado"

        # 1.TIPO_LANC
        # 2.COLABORADOR
        # 3.FILIAL
        # 4.DATA_LANC
        # 5.COD_ERP_CLIENTE
        # 6.TIPO_REGISTRO
        # 7.CONTA
        # 8.SUB_CONTA
        # 9.VALOR_LIQ
        # 10.ACAO_LANC
        # 11.1_HIST_CONTA
        # 12.COD_HIST
        # 13.COMPLEM_HIST
        # 14.GRUPO_LANC
        # 15.CNPJ
        # 16.INSC_ESTADUAL
        # 17.TP_CNPJ
        # 18.CONTA_ORIGEM
        # 19.CNPJ_EMPRESA
        # 20.IE_EMPRESA

        

        # df = pd.read_excel("w_data_temp/Leonardo - data temp.xlsx")
        df.index = list(range(1, len(df.index)+1))

        # ------ VALORES ÚNICOS PARA UTILIZAÇÃO NO ERP DO CLIENTE ------
        lis_data_temp_0 = list(range(0, len(df["ID"].index)))
        lis_data_temp_1 = list(df["ID"].values)
        lis_data_temp_2 = list(df["COLABORADOR"].values)
        
        list_VALUES_to_ERP = list(map(lambda x: f"G{lis_data_temp_1[x]}{lis_data_temp_2[x][:1]}{int(time())}", lis_data_temp_0))
        list_complemento_historico = list(map(lambda x: f"{grupo_lancamento} - {lis_data_temp_2[x]}{int(time())}", lis_data_temp_0))


        list_VALUES_DEBITO = list(map(lambda x: f"D", lis_data_temp_0))
        list_VALUES_CREDITO = list(map(lambda x: f"C", lis_data_temp_0))



        list_acao_lancamento = list(map(lambda x: "0", lis_data_temp_0))
        list_primeiro_hist_conta = list(map(lambda x: 2, lis_data_temp_0))
        list_cod_historico = list(map(lambda x: "", lis_data_temp_0))

     
        list_tp_cnpj = list(map(lambda x: "", lis_data_temp_0))
        

        list_grupo_lancamento = list(map(lambda x: grupo_lancamento, lis_data_temp_0))
        list_cnpj = list(map(lambda x: "", lis_data_temp_0))
        list_inscricao_estadual = list(map(lambda x: "", lis_data_temp_0))
        list_conta_origem = list(map(lambda x: "", lis_data_temp_0))
        list_CNPJ_Empresa = list(map(lambda x: "", lis_data_temp_0))
        list_IE_Empresa = list(map(lambda x: "", lis_data_temp_0))

    
        df["TIPO_LANC"] = list(map(lambda x: "00", lis_data_temp_0))

        df["FILIAL"] = list(map(lambda x: "-", lis_data_temp_0))
        df["DATA_LANC"] = list(map(lambda x: "-", lis_data_temp_0))
        df["COD_ERP_CLIENTE"] = list_VALUES_to_ERP
        df["TIPO_REGISTRO"] = list_VALUES_DEBITO

        df["CONTA"] = list(map(lambda x: "-", lis_data_temp_0))
        df["SUB_CONTA"] = list(map(lambda x: "0", lis_data_temp_0))

        df["VALOR_LIQ"] = list(map(lambda x: x.replace(".", "").replace(",", "."), df["VALOR_LIQ"].values))

        df["ACAO_LANC"] = list_acao_lancamento
        df["PRIM_HIST_CONTA"] = list_primeiro_hist_conta
        df["COD_HIST"] = list_cod_historico
        df["COMPLEM_HIST"] = list_complemento_historico
        df["GRUPO_LANC"] = list_grupo_lancamento
        df["CNPJ"] = list_cnpj 
        df["INSC_ESTADUAL"] = list_inscricao_estadual
        df["TP_CNPJ"] = list_tp_cnpj
        df["CONTA_ORIGEM"] = list_conta_origem
        df["CNPJ_EMPRESA"] = list_CNPJ_Empresa
        df["IE_EMPRESA"] = list_IE_Empresa

        # ------ DUPLICA DATAFRAME PARA VALORES DE CRÉDITO ------
        df_credito = pd.DataFrame(df)
        df_credito["TIPO_REGISTRO"] = list_VALUES_CREDITO
        df = pd.concat([df, df_credito])

        # ----- CONCATENA E ORDENA DE FORMA ALFABÉTICA OS DATAFRAMES DE DÉBITO x CRÉDITO
        df = df.sort_values(["COLABORADOR"])
        df.index = list(range(1, len(df.index)+1))

        df = df[[
            "TIPO_LANC",
            "COLABORADOR",
            "FILIAL",
            "DATA_LANC",
            "COD_ERP_CLIENTE",
            "TIPO_REGISTRO",
            "CONTA",
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
        ]] #.set_index('TIPO_LANC')

        df = df[df["VALOR_LIQ"] != "0.00"]
        df = df[df["VALOR_LIQ"] != "0,00"]

        df_json = json.loads(df.to_json(orient="table"))
        print(f" \n\n\n ------->> {type(df_json)}")

        return df_json["data"]
    except Exception as e:
        print(f" ### ERROR ETL DATA FOLHA | ERROR? {e}")
        return None
# ----
def convert_PDF_to_DataFrame(file, grupo_lancamento):
    # data = tabula.read_pdf("Diplomata Relação da Folha por Empregado.pdf", pages="all")
    print(f"\n\n ----- Arquivo informado: {file}")
    data = tabula.read_pdf(file, pages="all")

    list_df = list()
    for i in range(len(data)):
        print(f"\n\n ----> INDEX LIST: {i}")
        contrib = data[i][ data[i]["Código Nome do empregado"] == "Contribuintes" ]
        if len(contrib) >= 1:
            index = contrib.index.values[0]
            df = data[i][data[i].index < index-1]
            print(df)
            list_df.append(df)
        else:
            list_df.append(data[i])

    df = pd.concat(list_df)
    df.index = list(range(0, len(df.index)))
    df["nome"] = df["Código Nome do empregado"]

    print("\n\n ---------------- ")
    df.dropna(subset=["Líquido"],  inplace=True)
    df["VALOR_LIQ"] = df["Líquido"]
    df[['ID', 'COLABORADOR']] = df['nome'].str.split(' ', n=1, expand=True)

    # "Unnamed: 1", 
    df.drop(["Unnamed: 0", "Código Nome do empregado", "nome"], axis=1, inplace=True)
    df = df[df["ID"] != "Empregados:"]
    df = df[
        [
            "ID", "COLABORADOR",
            "Salário", "Out.Prov.", "Sal.Fam.",
            "INSS", "IRRF", "Out.Desc.",
            "VALOR_LIQ", "FGTS"
        ]
    ]
    df = df[df["VALOR_LIQ"] != "0.00"]
    df = df[df["VALOR_LIQ"] != "0,00"]
    df = read_file_data_post(df=df, name_user="Leonardo", grupo_lancamento=grupo_lancamento)
    return df
