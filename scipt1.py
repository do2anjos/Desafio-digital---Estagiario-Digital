import pandas as pd

set = pd.read_excel("C:\\Users\\anjos\\Downloads\\desafio_digital_-_base.xlsx", sheet_name="Dados - Questão 1")

def calcular_porcentagem(soma):
    if soma <= 2100000:
        return 0.05  # 5%
    elif soma <= 2400000:
        return 0.12  # 12%
    else:
        return 0.17  # 17%

set['Unidade'] = set['Unidade'].replace({'Ammazonas Shoping': 'Amazonas Shopping'})

soma_por_unidade = set.groupby('Unidade')['Valor unitário'].sum().reset_index()
soma_total_verificada = soma_por_unidade['Valor unitário'].sum()

porcentagem_imposto = calcular_porcentagem(soma_total_verificada)
imposto_total = soma_total_verificada * porcentagem_imposto

soma_por_unidade['Imposto_por_Unidade'] = soma_por_unidade['Valor unitário'].apply(lambda x: x * calcular_porcentagem(x))

soma_por_unidade_formatada = soma_por_unidade.copy()
soma_por_unidade_formatada['Valor unitário'] = soma_por_unidade['Valor unitário'].apply(lambda x: f"R$ {x:,.2f}")
soma_por_unidade_formatada['Imposto_por_Unidade'] = soma_por_unidade['Imposto_por_Unidade'].apply(lambda x: f"R$ {x:,.2f}")

imposto_total_formatado = f"R$ {imposto_total:,.2f}"

coluna_C = 'Produto'
valor_mais_repetido = set[coluna_C].value_counts().idxmax()
frequencia = set[coluna_C].value_counts().max()

print("Soma por Unidade:")
print(soma_por_unidade_formatada)
print("\nSoma Total Verificada:", f"R$ {soma_total_verificada:,.2f}")
print("Porcentagem de Imposto:", porcentagem_imposto * 100, "%")
print("Imposto Total:", imposto_total_formatado)
print("\nProduto mais repetido:", valor_mais_repetido)
print("Frequência:", frequencia)