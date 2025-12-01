import pandas as pd

# Ler arquivo com sugestões
df = pd.read_excel('data/gerado.xlsx')

print("="*70)
print("  RESUMO DAS SUGESTÕES DE PEDIDO")
print("="*70)
print()

# Análise geral
print("📊 VISÃO GERAL")
print(f"  Total de produtos: {len(df)}")
print(f"  Produtos que precisam pedido: {len(df[df['sugestao'] > 0])}")
print(f"  Produtos com estoque suficiente: {len(df[df['sugestao'] == 0])}")
print()

# Total de pedidos
total_unidades = df['sugestao'].sum()
print(f"📦 TOTAL A PEDIR")
print(f"  Total de unidades: {total_unidades:.0f}")
print()

# Por loja
print("🏪 POR LOJA")
por_loja = df.groupby('loja').agg({
    'sugestao': ['sum', 'count'],
    'codigo_interno': 'count'
}).round(0)
por_loja.columns = ['Total Unidades', 'Itens com Pedido', 'Total Itens']
print(por_loja)
print()

# Produtos com pedido
print("📋 DETALHAMENTO DOS PEDIDOS")
print("-"*70)
pedidos = df[df['sugestao'] > 0][['codigo_interno', 'loja', 'estoque_atual', 'venda_media_dia', 'embalagem', 'sugestao']]
for idx, row in pedidos.iterrows():
    caixas = row['sugestao'] / row['embalagem']
    print(f"Produto {row['codigo_interno']} | Loja {row['loja']}")
    print(f"  Estoque atual: {row['estoque_atual']} un | Venda/dia: {row['venda_media_dia']:.2f} un")
    print(f"  ➜ Pedir: {caixas:.0f} caixas ({row['sugestao']:.0f} unidades)")
    print()

print("="*70)
