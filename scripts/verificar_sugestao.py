import pandas as pd

df = pd.read_excel('data/gerado.xlsx')
print('Colunas:', list(df.columns))
print('\nSugestoes:')
print(df[['codigo_interno', 'loja', 'estoque_atual', 'venda_media_dia', 'sugestao']].to_string())
print(f'\nTotal com sugestao > 0: {len(df[df["sugestao"] > 0])}')
print(f'Total de sugestoes NaN: {df["sugestao"].isna().sum()}')
