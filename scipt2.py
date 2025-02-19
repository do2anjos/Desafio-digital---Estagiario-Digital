import pandas as pd

set = pd.read_excel("C:\\Users\\anjos\\Downloads\\desafio_digital_-_base.xlsx", sheet_name="Dados - Questão 1")

set['Produto'] = set['Produto'].str.lower().str.replace('_', ' ').str.strip()
set['Produto'] = set['Produto'].replace({
    'ar_condicionado': 'ar condicionado', 
    'cadeira%gamer': 'cadeira gamer', 
    'fone d ouvido': 'fone de ouvido', 
    'samsung': 'samsungsamsung', 
    'xbox seriessss': 'xbox series s', 
    'iphone': 'iphone'
})

soma_por_produto = set.groupby('Produto')['Valor unitário'].sum().reset_index()
soma_total_vendas = soma_por_produto['Valor unitário'].sum()
soma_por_produto['Participacao'] = (soma_por_produto['Valor unitário'] / soma_total_vendas) * 100

soma_por_produto = soma_por_produto.sort_values(by='Participacao', ascending=True)
soma_por_produto['Participacao'] = soma_por_produto['Participacao'].apply(lambda x: round(x, 2))

print("Soma por Produto e Participação nas Vendas:")
print(soma_por_produto)
print("\nSoma Total de Vendas:", f"R$ {soma_total_vendas:,.2f}")
