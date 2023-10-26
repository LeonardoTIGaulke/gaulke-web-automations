import os
import json
import random
import pandas as pd
from time import time, strftime




def create_data_randomic(numero_cte):

    random.seed()
    hora = int(strftime("%H"))
    minuto = int(strftime("%M"))
    segundo = int(strftime("%S"))
    numero_aleatorio =f"{numero_cte}{hora}{minuto}{segundo}"
    print("\n\n ---->>>> ", numero_aleatorio)
    return int(numero_aleatorio)
# ----
def read_file_data_post_GNRE(df, name_user, grupo_lancamento):
    try:
        
       
        # df = pd.read_excel("w_data_temp/Leonardo - data temp.xlsx")
        df.index = list(range(1, len(df.index)+1))

        # ------ VALORES ÚNICOS PARA UTILIZAÇÃO NO ERP DO CLIENTE ------
    
        lis_data_temp_0 = list(range(0, len(df.index)))

        lis_data_temp_uf_inicio = list(df["UF_INÍCIO"].values)
        lis_data_temp_uf_fim = list(df["UF_FIM"].values)

        lis_data_temp_2 = list(df["CTE"].values)
        lis_data_temp_valor_ICMS = list(df["VALOR_ICMS"].values)
        
        list_VALUES_to_ERP = list(map(lambda x: f"G{lis_data_temp_2[x]}DT{int(time())}", lis_data_temp_0))
        list_complemento_historico = list(map(lambda x: f"VLR ICMS S/CTE nº {lis_data_temp_2[x]}", lis_data_temp_0))


        list_VALUES_DEBITO = list(map(lambda x: f"D", lis_data_temp_0))
        list_VALUES_CREDITO = list(map(lambda x: f"C", lis_data_temp_0))



        list_acao_lancamento = list(map(lambda x: "0", lis_data_temp_0))
        list_primeiro_hist_conta = list(map(lambda x: 2, lis_data_temp_0))
        list_cod_historico = list(map(lambda x: "", lis_data_temp_0))

     
        list_tp_cnpj = list(map(lambda x: "", lis_data_temp_0))
        
        

        list_grupo_lancamento = list(map(lambda x: f"{create_data_randomic(numero_cte=x)}", lis_data_temp_2))
        list_cnpj = list(map(lambda x: "", lis_data_temp_0))
        list_inscricao_estadual = list(map(lambda x: "", lis_data_temp_0))
        list_conta_origem = list(map(lambda x: "", lis_data_temp_0))
        list_CNPJ_Empresa = list(map(lambda x: "", lis_data_temp_0))
        list_IE_Empresa = list(map(lambda x: "", lis_data_temp_0))

    
        df["TIPO_LANC"] = list(map(lambda x: "00", lis_data_temp_0))

        df["FILIAL"] = list(map(lambda x: "-", lis_data_temp_0))
        # df["DATA_EMISSÃO"] = list(map(lambda x: "-", lis_data_temp_0))
        df["COD_ERP_CLIENTE"] = list_VALUES_to_ERP
        df["TIPO_REGISTRO"] = list_VALUES_DEBITO
        

        df["CONTA"] = list(map(lambda x: "-", lis_data_temp_0))
        df["SUB_CONTA"] = list(map(lambda x: "0", lis_data_temp_0))

        # df["VALOR_ICMS"] = list(map(lambda x: x.replace(".", "").replace(",", "."), df["VALOR_ICMS"].values))

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
        df = df.sort_values(["CTE"])
        df.index = list(range(1, len(df.index)+1))

        df = df[[
            "TIPO_LANC",
            "CTE",
            "FILIAL",
            "DATA_EMISSÃO",
            "COD_ERP_CLIENTE",
            "TIPO_REGISTRO",
            "CONTA",
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
            "UF_INÍCIO", "UF_FIM",
        ]] #.set_index('TIPO_LANC')

        df = df[df["VALOR_ICMS"] != "0.00"]
        df = df[df["VALOR_ICMS"] != "0,00"]
        print(df)

        df_json = json.loads(df.to_json(orient="table"))
        print(f" \n\n\n ------->> {type(df_json)}")
        

        return df_json["data"]
    except Exception as e:
        print(f" ### ERROR ETL DATA FOLHA | ERROR: {e}")
        return None
# ----
# ENTRATA FIXA PARA AMBIENTE DE DESENVOLVIMENTO
file_dir = r"I:\1. Gaulke Contábil\Administrativo\9. TI\1. Projetos\2. Importação GNRE\Modelo GNRE.xlsx"
def read_file_xlsx(file_dir, grupo_lancamento):
    try:

        file = pd.ExcelFile(file_dir)
        sheet_name = file.sheet_names[-1]
        data = file.parse(sheet_name=sheet_name)
        data = data[[
            "CTE", "DATA_EMISSÃO","VALOR_ICMS", "UF_INÍCIO", "UF_FIM"
        ]]
        
        data.dropna(subset=["CTE"], inplace=True)
        data["CTE"] = list(map(lambda x: int(x), data["CTE"].values))

        data["DATA_EMISSÃO"] = data['DATA_EMISSÃO'].dt.strftime('%d/%m/%Y')
        df = read_file_data_post_GNRE(
            df=data, name_user="Leonardo", grupo_lancamento=grupo_lancamento
        )

        file.close()
        return df
    except Exception as e:
        print(e)
        return None
# ----






