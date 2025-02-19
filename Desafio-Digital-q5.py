import pandas as pd
import dash
from dash import dcc, html
import plotly.graph_objects as go

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

app = dash.Dash(__name__)

fig = go.Figure()

for mes in maior_venda_por_unidade['Mes_Ano'].unique():
    subset = maior_venda_por_unidade[maior_venda_por_unidade['Mes_Ano'] == mes]
    fig.add_trace(go.Bar(
        x=subset['Unidade'],
        y=subset['Valor unitário'],
        name=str(mes), 
        text=subset['Valor unitário (R$)'],
        textposition='auto'
    ))

fig.update_layout(
    title='Maior Venda por Loja e Mês',
    xaxis_title='Unidade',
    yaxis_title='Valor de Vendas (R$)',
    barmode='group', 
    yaxis_tickprefix='R$ ',
    yaxis_tickformat=',.2f',
)

app.layout = html.Div(children=[
    html.Div(
        children=html.Img(src='https://upload.wikimedia.org/wikipedia/commons/thumb/2/22/Bemol.logo.png/320px-Bemol.logo.png', 
                          style={'width': '320px', 'height': '197px'}), 
        style={'textAlign': 'center', 'padding': '20px'} 
    ),
    html.H1(children='Período de Maior Venda por Loja'),
    html.Div(children='Aqui estão os meses em que cada loja teve as maiores vendas:'),

    dcc.Graph(
        id='bar-chart',
        figure=fig
    ),

    html.Div(children=[
        html.H2(children='Tabela de Vendas'),
        dcc.Markdown(maior_venda_por_unidade[['Unidade', 'Mes_Ano', 'Valor unitário (R$)', 'Produto Mais Vendido no Período']].to_markdown(index=False))
    ])
])

if __name__ == '__main__':
    app.run_server(debug=True)
