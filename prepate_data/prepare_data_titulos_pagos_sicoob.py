import json
import tabula
import random
import pandas as pd

def create_data_randomic():
    number = random.randint(10**17, 10**18 - 1)
    return number

def create_dataframe_debit(df, obj_new_cols):
    # print(obj_new_cols)
    for i in obj_new_cols:
        if len(obj_new_cols[i]) >= 1:
            df[i] = obj_new_cols[i]
    return df

def convert_PDF_to_DataFrame_SICOOB(file):
    list_df = list()
    try:
        dataframes = tabula.read_pdf(file, pages="all")
        for df in dataframes:
            list_df.append(df)
    except:
        pass
    df = pd.concat(list_df)
    df.index = list(range(0, len(df.index)))
    df = df.rename(columns={
        "Unnamed: 0": "COL1",
        "Sacado": "NOME",
        "Nosso Número": "NOSSO_NUMERO",
        "Seu Número": "SEU_NUMERO",
        "Entrada": "DATA_ENTRADA",
        "Vencimento": "DATA_VENCIMENTO",
        "Dt. Limite Pgto": "DT_LIMITE_PGTO",
        "Valor (R$)": "VALOR",
    })

    df["VALOR"] = list(map(lambda x: x.replace(".", "").replace(",", "."), df["VALOR"].values  ))

    obj_new_cols = {
        "TIPO_LANC" : list(),
        "COD_EMPRESA": list(),
        "FILIAL" : list(),
        "COD_ERP_CLIENTE" : list(),
        "TIPO_REGISTRO" : list(),
        "CONTA" : list(),
        "SUB_CONTA" : list(),
        "VALOR_LIQ" : list(),
        "ACAO_LANC" : list(),
        "PRIM_HIST_CONTA" : list(),
        "COD_HIST" : list(),
        "COMPLEM_HIST" : list(),
        "GRUPO_LANC" : list(),
        "CNPJ" : list(),
        "INSC_ESTADUAL" : list(),
        "TP_CNPJ" : list(),
        "CONTA_ORIGEM" : list(),
        "CNPJ_EMPRESA" : list(),
        "IE_EMPRESA" : list(),
    }

    # ---------------------------
    list_index = list(df.index)
    for i in list_index:
        obj_new_cols["TIPO_LANC"].append("00")
        obj_new_cols["COD_EMPRESA"].append("-")
        obj_new_cols["FILIAL"].append("-")
        obj_new_cols["TIPO_REGISTRO"].append("D")
        obj_new_cols["CONTA"].append("11")
        obj_new_cols["SUB_CONTA"].append("0")
        obj_new_cols["ACAO_LANC"].append("0")
        obj_new_cols["PRIM_HIST_CONTA"].append("2")
        obj_new_cols["COD_HIST"].append("")
        obj_new_cols["COMPLEM_HIST"].append(f'Desconto Dupl. {df["SEU_NUMERO"][i]} - {df["NOME"][i]} -  {df["DATA_VENCIMENTO"][i]}')

        cod_erp_client = f'G{df["NOSSO_NUMERO"][i]}{df["SEU_NUMERO"][i]}'.replace("-", "")
        obj_new_cols["COD_ERP_CLIENTE"].append(cod_erp_client)
        obj_new_cols["GRUPO_LANC"].append(create_data_randomic()) # CREATE RANDOMIC
        # ----
        obj_new_cols["CNPJ"].append("")
        obj_new_cols["INSC_ESTADUAL"].append("")
        obj_new_cols["TP_CNPJ"].append("")
        obj_new_cols["CONTA_ORIGEM"].append("")
        obj_new_cols["CNPJ_EMPRESA"].append("")
        obj_new_cols["IE_EMPRESA"].append("")

    df = create_dataframe_debit(df=df, obj_new_cols=obj_new_cols)
    df_debito = pd.DataFrame(df)
    df_credito = pd.DataFrame(df)

    df_credito["TIPO_REGISTRO"] = list(map(lambda x: "C", df_credito.index))
    df_credito["CONTA"] = list(map(lambda x: "524", df_credito.index))

    df = pd.concat([df_debito, df_credito])
    
    
    df.sort_values(by=["NOME", "COD_ERP_CLIENTE", "TIPO_REGISTRO"], inplace=True)
    df.index = list(range(0, len(df.index)))
    df = df[[
        "TIPO_LANC",
        "COD_EMPRESA",
        "NOME",
        "FILIAL",
        "DATA_ENTRADA",
        "COD_ERP_CLIENTE",
        "TIPO_REGISTRO",
        "CONTA",
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
    ]]

    cols_table = list(df.columns)
    df_json = json.loads(df.to_json(orient="table"))
    
    return {"df_json": df_json, "cols_table": cols_table}
   

if __name__ == "__main__":
    base = convert_PDF_to_DataFrame_SICOOB(file="../MODELO - Entrada Desconto.pdf")
    base.to_excel(r"I:\\1. Gaulke Contábil\\Administrativo\\9. TI\\1. Projetos\\3. Importação Dupl Descontada Sicoob\\Sabensulbase.xlsx")