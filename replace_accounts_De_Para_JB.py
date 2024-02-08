import io
import os
import pandas as pd
import pandas as pd
from django.db import connections
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "automations_gaulke_contabil.settings")

# file_dir = r"I:\1. Gaulke Contábil\Administrativo\9. TI\1. Projetos\16. Importação saldos contabeis\Contab 01122023 - 31122023.txt"




class ReplaceValues:
    def __init__(self, file_dir_text):
        self.file_dir_text = file_dir_text
    
    def read_text(self):
        file_dir = r"{file}".format(file=self.file_dir_text)
        names=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17]
        df = pd.read_csv(file_dir,  encoding='ISO-8859-1', delimiter=";", names=names, dtype="str")
        print(df)
        return df

    def query_company_De_Para_JB(self, company_code):

        list_de_para = list()
        all_companies = connections["default"]
        with all_companies.cursor() as cursor:
            cursor.execute(f"""
                SELECT
                    id, pc_old, pc_new, code_old, code_new, username, created_at, update_at, company_code, insert_JB, update_at_JB
                FROM app_payroll_relation_model_plano_contas_de_para_antigo_x_novo
                WHERE company_code = "{company_code}";
            """)
            rows = cursor.fetchall()

            for result in rows:
                list_de_para.append({
                    "id":           result[0],
                    "pc_old":       result[1],
                    "pc_new":       result[2],
                    "code_old":     result[3],
                    "code_new":     result[4],
                    "username":     result[5],
                    "created_at":   result[6],
                    "update_at":    result[7],
                    "company_code": result[8],
                    "insert_JB":    result[9],
                    "update_at_JB": result[10],
                })

            # print(list_de_para)
        df_de_para = pd.DataFrame.from_dict(data=list_de_para, orient="columns")
        return df_de_para

    def replace_values(self, df_text, df_de_para):


        # df_text[15] = df_text[15].astype(int)
        df_text.index = list(range(0, len(df_text.index)))
        print(" ------------------- df_text -------------------")
        print(df_text)
        print(" ------------------- df_de_para -------------------")
        print(df_de_para)
        # return
        print("\n substituido valores...")
        for i in df_de_para.index:
            code_old = df_de_para["code_old"][i]
            code_new = df_de_para["code_new"][i]

            for j in df_text.index:
                if str(df_text[6][j]) == str(code_old):
                    print(f">> code_old: {code_old} | code_new: {code_new} | {df_text[6][j]}")
                    df_text[6][j] = str(code_new)
        
        print("\n valores substituidos com sucesso!")
        print(df_text)

        return df_text




file_dir = str(input("Informe o caminho do arquivo (.txt): "))
company_code = str(input("Informe o código da empresa (JB): "))

APP = ReplaceValues(file_dir_text=file_dir)
df_text = APP.read_text()
df_de_para = APP.query_company_De_Para_JB(company_code=company_code)
df_new_text = APP.replace_values(df_text=df_text,df_de_para=df_de_para)

print(f"\n ----> caminho informado: {file_dir}\n ")
print(f" ----> código da empresa informado: {company_code}\n\n ")

print("\n\n ------------------ df_new_text ------------------")
print(df_new_text)


file_dir_save = str(input("Informe o caminho para salvar o arquivo (.txt): "))
file_dir_save = r"{file}".format(file=file_dir_save) + f"\de-para-substituido - {company_code}.txt"
print(file_dir_save)
df_new_text.to_csv(file_dir_save, sep=';', header=False, index=False)
