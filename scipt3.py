import pandas as pd

set = pd.read_excel("C:\\Users\\anjos\\Downloads\\desafio_digital_-_base.xlsx", sheet_name="Dados - Questão 1")

set['Unidade'] = set['Unidade'].replace({'Ammazonas Shoping': 'Amazonas Shopping'})
soma_por_unidade = set.groupby('Unidade')['Valor unitário'].sum().reset_index()
soma_total_vendas = soma_por_unidade['Valor unitário'].sum()
soma_por_unidade['Participacao'] = (soma_por_unidade['Valor unitário'] / soma_total_vendas) * 100


def calcular_porcentagem(soma):
    if soma <= 2100000:
        return 0.05  # 5%
    elif soma <= 2400000:
        return 0.12  # 12%
    else:
        return 0.17  # 17%

porcentagem_imposto = calcular_porcentagem(soma_total_vendas)
soma_por_unidade['Imposto'] = soma_por_unidade['Valor unitário'] * porcentagem_imposto
soma_por_unidade['Lucro_Apos_Impostos'] = soma_por_unidade['Valor unitário'] - soma_por_unidade['Imposto']
soma_por_unidade['Lucro_Apos_Impostos'] = soma_por_unidade['Lucro_Apos_Impostos'].apply(lambda x: f"R$ {x:,.2f}")

# Print dos resultados
print("Soma por Unidade:")
print(soma_por_unidade)
print("\nSoma Total de Vendas:", f"R$ {soma_total_vendas:,.2f}")
print("Porcentagem de Imposto:", porcentagem_imposto * 100, "%")
