import pandas as pd

soma_total_vendas = 1292291.00  # Exemplo
imposto_total = 64614.55  # Exemplo
produto_mais_vendido = Mi Band 6
quantidade_produto_mais_vendido = 48  # Exemplo

resultados = pd.DataFrame({
    'Descrição' [
        'Soma Total de Vendas',
        'Imposto Total',
        'Produto Mais Vendido',
        'Quantidade do Produto Mais Vendido'
    ],
    'Valor' [
        soma_total_vendas,
        imposto_total,
        produto_mais_vendido,
        quantidade_produto_mais_vendido
    ]
})

resultados.to_csv(CUsersanjosDownloadsresultados_vendas.csv, index=False)

print(Resultados salvos em 'resultados_vendas.csv'.)
