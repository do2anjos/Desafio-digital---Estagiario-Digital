import pandas as pd
import dash
from dash import dcc, html
import plotly.express as px

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

grafico = dcc.Graph(
    figure=px.bar(soma_por_produto, x='Produto', y='Participacao',
                   title='Participação dos Produtos nas Vendas (%)',
                   text='Participacao',
                   labels={'Participacao': 'Participação (%)'},
                   )
)

app = dash.Dash(__name__)

app.layout = html.Div(children=[
    html.Div(
        children=html.Img(src='https://upload.wikimedia.org/wikipedia/commons/thumb/2/22/Bemol.logo.png/320px-Bemol.logo.png', 
                          style={'width': '320px', 'height': '197px'}), 
        style={'textAlign': 'center', 'padding': '20px'} 
    ),
    html.H1(children='Participação dos Produtos nas Vendas'),
    html.Div(children='Visualização da participação percentual de cada produto nas vendas.'),
    grafico
])

if __name__ == '__main__':
    app.run_server(debug=True)
