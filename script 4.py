import pandas as pd

set = pd.read_excel("C:\\Users\\anjos\\Downloads\\desafio_digital_-_base.xlsx", sheet_name="Dados - Questão 1")

set['Data_compra'] = pd.to_datetime(set['Data_compra'], errors='coerce')
set['Unidade'] = set['Unidade'].replace({'Ammazonas Shoping': 'Amazonas Shopping'})
set['Produto'] = set['Produto'].replace({
    'Ar_condicionado': 'Ar condicionado',
    'Cadeira%Gamer': 'Cadeira Gamer',
    'Fone d Ouvido': 'Fone de Ouvido',
    'SAMSUNG': 'samsungsamsung',
    'XBOX SERIESSSS': 'Xbox series s',
    'IPHOne': 'Iphone'
})

set['Mes_Ano'] = set['Data_compra'].dt.to_period('M')
vendas_por_periodo = set.groupby(['Unidade', 'Mes_Ano'])['Valor unitário'].sum().reset_index()

maior_venda_por_unidade = (
    vendas_por_periodo.loc[vendas_por_periodo.groupby('Unidade')['Valor unitário'].idxmax()]
    .reset_index(drop=True)
)

maior_venda_por_unidade['Valor unitário (R$)'] = maior_venda_por_unidade['Valor unitário'].apply(lambda x: f"R$ {x:,.2f}")
produto_mais_vendido = set.groupby(['Unidade', 'Mes_Ano', 'Produto'])['Valor unitário'].sum().reset_index()
produto_mais_vendido = produto_mais_vendido.loc[produto_mais_vendido.groupby(['Unidade', 'Mes_Ano'])['Valor unitário'].idxmax()]

maior_venda_por_unidade = maior_venda_por_unidade.merge(produto_mais_vendido[['Unidade', 'Mes_Ano', 'Produto']], on=['Unidade', 'Mes_Ano'], how='left')
maior_venda_por_unidade.rename(columns={'Produto': 'Produto Mais Vendido no Período'}, inplace=True)

print("Maior Venda por Unidade e Produto Mais Vendido:")
print(maior_venda_por_unidade)
