import random
from prepate_data.prepare_data_cobran_pagas import create_base_contas_pagas


def generate_unique_numbers():
    number = random.randint(10**17, 10**18 - 1)
    return number

unique_numbers = generate_unique_numbers()
print(unique_numbers)


# if __name__ == "__main__":
#     data = create_base_contas_pagas(file="MODELO Cobrancas pagas 09-2023.xlsx")
#     print(data)
#     # data.to_excel("data_temp_cobrancas.xlsx")
