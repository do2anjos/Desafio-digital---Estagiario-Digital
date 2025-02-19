import pandas as pd
import dash
from dash import dcc, html
from dash import dash_table 
import plotly.express as px

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

app = dash.Dash(__name__)

tabela = dash_table.DataTable(
    data=soma_por_unidade_formatada.to_dict('records'),
    columns=[{"name": i, "id": i} for i in soma_por_unidade_formatada.columns],
)

soma_por_unidade['Valor unitario_formatado'] = soma_por_unidade['Valor unitário'].apply(lambda x: f"R$ {x:,.2f}")
grafico = dcc.Graph(
    figure=px.bar(soma_por_unidade, x='Unidade', y='Valor unitário',
                   title='Valores por Unidade', text='Valor unitario_formatado')
)

app.layout = html.Div(children=[
     html.Div(
        children=html.Img(src='https://upload.wikimedia.org/wikipedia/commons/thumb/2/22/Bemol.logo.png/320px-Bemol.logo.png', style={'width': '320px', 'height': '197px'}), 
        style={'textAlign': 'center', 'padding': '20px'} 
    ),
    html.H1(children='Dashboard de Vendas'),
    html.Div(children='Visualização dos dados de vendas e impostos.'),
    html.H2(children=f"A soma total de todas as vendas é: R$ {soma_total_verificada:,.2f}"),  
    html.H2(children=f"O imposto total a ser pago pela empresa é: {imposto_total_formatado}"), 
    html.H2(children=f"O Produto que mais vende é: {valor_mais_repetido} com {frequencia} vendas."),
    tabela,
    grafico
])

if __name__ == '__main__':
    app.run_server(debug=True)
