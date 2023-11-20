import json
import pandas as pd
from datetime import datetime, timedelta

import holidays

# criar um objeto com os feriados do Brasil
br_holidays = holidays.Brazil()

# definir uma data para verificar
date = datetime(year=2023, month=12, day=25)

# verificar se a data é feriado
if date in br_holidays:
    print(f"{date} é feriado no Brasil: {br_holidays[date]}")
else:
    print(f"{date} não é feriado no Brasil")

# https://decorise.painel.magazord.com.br/
# contato@contabilgaulke.com.br
# Gaulke.7300

def get_all_data():
    data_init = 1
    list_df = list()
    while True:
        try:
            df = pd.read_csv(f"DECORISE/{data_init}.csv", encoding='latin-1', delimiter=";")
            print(f" ------------------------- FILE: {data_init}")
            print(df)
            list_df.append(df)
            data_init += 1
        except:
            break

    print( "\n\n\n  ---------------------  ")
    df = pd.concat(list_df)
    df.index = list(range(0, len(df.index)))
    print(df)
    df.to_excel("base_decorise.xlsx")

def adjust_date_decorise(file_name):
    # Data Esperada
    df = pd.read_excel(file_name)
    # df['Data Esperada'] = df['Data Esperada'].astype('datetime64[ns]')
    print(df.info())
    print(df)

    list_weekday = list()
    list_datetime_adjust = list()
    list_feridos = list()
    list_weekday_name = ["seg", "ter", "qua", "qui", "sex", "sab", "dom"]
    for i in df.index:
        adjust_dt = datetime.strptime(df["Data Esperada"][i], "%d/%m/%Y")
        wk = list_weekday_name[adjust_dt.weekday()]
        dt_adj = adjust_dt
        # ----
        if adjust_dt in br_holidays:
            print(f"{adjust_dt} é feriado no Brasil: {br_holidays[adjust_dt]}")
            dt_adj = dt_adj + timedelta(days=1)

            if list_weekday_name[dt_adj.weekday()] == "sab":
                dt_adj = dt_adj + timedelta(days=2)
            elif list_weekday_name[dt_adj.weekday()] == "dom":
                dt_adj = dt_adj + timedelta(days=1)


            if dt_adj not in list_feridos:
                list_feridos.append(f"{dt_adj} - { br_holidays[adjust_dt] }")
        else:
            if wk == "sab":
                dt_adj = dt_adj + timedelta(days=2)
            elif wk == "dom":
                dt_adj = dt_adj + timedelta(days=1)

        list_weekday.append( wk )
        list_datetime_adjust.append(dt_adj)
        df["Data Esperada"][i] = adjust_dt



    df['dia_da_semana'] = list_weekday
    df['data_ajustada'] = list_datetime_adjust
    df = df.sort_values(by=["Data Esperada"])
    print(df)


    for i in list_feridos:
        print(">>> ", i)


    df.to_excel("DECORISE/data_adjust/base.xlsx")

adjust_date_decorise(file_name="base_decorise.xlsx")
# get_all_data()