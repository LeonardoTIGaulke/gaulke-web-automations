import json
import random
import pandas as pd
from time import time, strftime


# impotação WB Telecom


def create_data_randomic():
    number = random.randint(10**17, 10**18 - 1)
    return number

def convert_string_to_float(data_string):
    try:
        data = float(data_string)
        return data
    except Exception as e:
        print(f" ### ERROR CONVET STRING TP FLOAT | ERRRO: {e}")
        return 0.0

def create_base_contas_pagas(file):
    df = pd.read_excel(file)
    df = df.rename(columns=df.iloc[0]).drop(df.index[0])
    df.index = list(range(0, len(df.index)))

    
    df['Valor'] = df['Valor'].str.replace('.', '').str.replace(',', '.')
    df['Valor pago'] = df['Valor pago'].str.replace('.', '').str.replace(',', '.')

    df["GRUPO_LANC"] = list(map(lambda x: create_data_randomic(), df.index))

    df.rename(columns={"CPF/CNPJ": "CNPJ"})

    list_data_calculate = list()
    list_debito = list()
    list_credito = list()
    list_tipo_processo = list()
    for i in df.index:
        df["Valor"][i] = convert_string_to_float(df["Valor"][i].split()[1])
        df["Valor pago"][i] = convert_string_to_float(df["Valor pago"][i].split()[1])
        calculate = abs(df["Valor pago"][i] - df["Valor"][i])
        list_data_calculate.append(calculate)
        list_debito.append("D")
        list_credito.append("C")
        list_tipo_processo.append("comum")
    
    df["calculo"] = list_data_calculate
    df["TIPO_PROCESSO"] = list_tipo_processo
    df_debito = pd.DataFrame(df)
    df_credito = pd.DataFrame(df)
    # ----
    df_debito["TIPO_REGISTRO"] = list_debito
    df_credito["TIPO_REGISTRO"] = list_credito


    df = pd.concat([df_debito, df_credito])

    # ----------------------- CRIA DATAFRAME DE JUTOS E DESCONTOS -----------------------
    print("\n\n\n -------- JUROS -------- ")
    df_juros = df[ (df["calculo"] > 0) & (df["TIPO_REGISTRO"] == "D") ]
    df_juros.index = list(range(0, len(df_juros.index)))
    if len(df_juros.index) >= 1:
        for i in df_juros.index:
            df_juros["TIPO_PROCESSO"][i] = "process_juros"
            df_juros["Valor pago"][i] = df_juros["Valor pago"][i] - (df_juros["Valor pago"][i] - df_juros["calculo"][i])
    print(df_juros)
    
    print("\n\n\n -------- DESCONTO -------- ")
    df_desconto = df[ (df["calculo"] < 0) & (df["TIPO_REGISTRO"] == "C") ]

    
    if len(df_desconto.index) >= 1:
        for i in df_desconto.index:
            df_desconto["TIPO_PROCESSO"][i] = "process_desconto"
            df_desconto["Valor pago"][i] = (df_desconto["Valor pago"][i] - df_desconto["calculo"][i]) - df_desconto["Valor pago"][i]
    
    print(df_desconto)

    df = pd.concat([df, df_juros, df_desconto])

    # df.index = list(range(0, len(df.index)))
    

    # -------------- 
    list_complem_hist = list()
    list_VALUES_to_ERP = list()
    df.index = list(range(0, len(df.index)))

    for i in df.index:
        nome = df["Nome Cliente"][i] #.values[0]
        data_venc = df["Vencimento"][i] #.values[0]
        print(f"\n --> nome: {nome} | data_venc: {data_venc}")
        list_complem_hist.append(f"Receb. Dupl {nome} venc {data_venc}")
        list_VALUES_to_ERP.append(f"COD{i}TM{int(time())}")
    

    df["TIPO_LANC"] = list(map(lambda x: "00", df.index))
    df["COMPLEM_HIST"] = list_complem_hist
    
    df["COD_ERP_CLIENTE"] = list_VALUES_to_ERP
    # ----
    df["FILIAL"] = list(map(lambda x: "-", df.index))
    df["CONTA"] = list(map(lambda x: "-", df.index))
    df["SUB_CONTA"] = list(map(lambda x: 0, df.index))
    df["ACAO_LANC"] = list(map(lambda x: 0, df.index))
    # ----
    df["PRIM_HIST_CONTA"] = list(map(lambda x: 2, df.index))
    df["COD_HIST"] = list(map(lambda x: "", df.index))

    list_numero_doc = list(df["CPF/CNPJ"].values)
    

    df["INSC_ESTADUAL"] = list(map(lambda x: "", df.index))
    df["TP_CNPJ"] = list(map(lambda x: "1", df.index))
    df["CONTA_ORIGEM"] = list(map(lambda x: "", df.index))
    df["CNPJ_EMPRESA"] = list(map(lambda x: "", df.index))
    df["IE_EMPRESA"] = list(map(lambda x: "", df.index))


    obj_rename_cols = {
        "CPF/CNPJ": "CNPJ",
        "Vencimento": "DATA_VENC",
        "Pagamento": "DATA_PAG",
        "Nome Cliente": "NOME_CLIENTE",
        "Valor pago": "VALOR",
        "Valor": "VALOR_ORIGINAL",
    }

    df = df.rename(columns=obj_rename_cols)

    for i in df.index:
        if df["TIPO_REGISTRO"][i] == "C":
            df["VALOR"][i] = df["VALOR_ORIGINAL"][i]

    df.sort_values(by=["COMPLEM_HIST", "VALOR"], inplace=True)

    df = df[ df["VALOR_ORIGINAL"] > 0.0 ]

    df.index = list(range(0, len(df.index)))
    # df.to_excel("data_temp_cobrancas.xlsx")

    df_json = json.loads(df.to_json(orient="table"))

    return df_json

if __name__ == "__main__":
    create_base_contas_pagas("MODELO Cobrancas pagas 09-2023.xlsx")