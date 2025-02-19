import pandas as pd
import dash
from dash import dcc, html
from dash import dash_table
import plotly.express as px

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

app = dash.Dash(__name__)

soma_por_unidade['Participacao_text'] = soma_por_unidade['Participacao'].apply(lambda x: f"{x:.2f}%")
grafico = dcc.Graph(
    figure=px.bar(soma_por_unidade, x='Unidade', y='Participacao',
                   title='Participação das Lojas nas Vendas (%)',
                   text='Participacao_text',
                   labels={'Participacao': 'Participação (%)'},
                   )
)

tabela_lucro = dash_table.DataTable(
    data=soma_por_unidade.to_dict('records'),
    columns=[{"name": "Unidade", "id": "Unidade"},
             {"name": "Lucro Após Impostos", "id": "Lucro_Apos_Impostos", "type": "text"}],
    style_data={'textAlign': 'left'},
)

app.layout = html.Div(children=[
    html.Div(
        children=html.Img(src='https://upload.wikimedia.org/wikipedia/commons/thumb/2/22/Bemol.logo.png/320px-Bemol.logo.png',
                          style={'width': '320px', 'height': '197px'}),
        style={'textAlign': 'center', 'padding': '20px'}
    ),
    html.H1(children='Participação das Lojas nas Vendas'),
    html.Div(children='Visualização da participação percentual de cada loja nas vendas.'),
    grafico,
    html.H2(children='Lucro de Cada Loja Após Desconto de Impostos'),
    tabela_lucro
])

if __name__ == '__main__':
    app.run_server(debug=True)
