#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import io
import pandas as pd

# Configurar stdout para UTF-8 no Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Carrega dados do arquivo de sugestões gerado
df = pd.read_excel('data/sugestao_ia.xlsx')

print("="*70)
print("ANÁLISE DETALHADA - ESTRATÉGIA DE BALANCEAMENTO")
print("="*70)
print()

for idx, row in df.iterrows():
    print(f"[{idx+1}] Produto: {row['codigo_interno']} | Loja: {row['loja']}")
    print(f"    Estoque atual: {row['estoque']} un")
    print(f"    Ponto de pedido: {row['ponto_pedido']} un")
    print(f"    Estoque ideal: {row['estoque_ideal']} un")
    
    # Calcular venda média com base na quantidade vendida
    quantidade_vendida = float(row['quantidade_vendida']) if pd.notna(row['quantidade_vendida']) else 0
    venda_media_dia = quantidade_vendida / 1  # Dados de 1 dia
    print(f"    Venda média/dia: {venda_media_dia:.2f} un/dia")
    
    # Calcula dias de cobertura dos valores do comprador
    if pd.notna(row['ponto_pedido']) and pd.notna(row['estoque_ideal']):
        if venda_media_dia > 0:
            dias_cobertura_comprador = (row['estoque_ideal'] - row['ponto_pedido']) / venda_media_dia
            print(f"    Dias cobertura (valores comprador): {dias_cobertura_comprador:.1f} dias")
        else:
            dias_cobertura_comprador = float('inf')
            print(f"    Dias cobertura (valores comprador): infinito (sem vendas)")
        
        # Avalia estratégia
        if 4 <= dias_cobertura_comprador <= 6:
            estrategia = "[OK] COMPRADOR (valores adequados)"
        elif dias_cobertura_comprador > 6:
            estrategia = "[AJUSTE] GIRO_OTIMIZADO (ajustado para baixo)"
        else:
            estrategia = "[AJUSTE] GIRO_OTIMIZADO (ajustado para cima)"
    else:
        estrategia = "[PADRÃO] GIRO_SAUDAVEL (sem valores do comprador)"
    
    print(f"    Estratégia: {estrategia}")
    print(f"    -> Sugestão: {row['sugestao']:.0f} unidades")
    print()

print("="*70)
print("RESUMO GERAL")
print("="*70)
print(f"Total de produtos analisados: {len(df)}")
print(f"Produtos com sugestão > 0: {len(df[df['sugestao'] > 0])}")
print(f"Produtos com estoque suficiente: {len(df[df['sugestao'] == 0])}")
print(f"\nTotal de unidades sugeridas: {df['sugestao'].sum():.0f}")

# Calcular média de venda diária total
venda_total = df['quantidade_vendida'].sum()
print(f"Média de venda diária total: {venda_total:.2f} un/dia")
print("="*70)

# Salvar análise em Excel
print("\nGerando arquivo de análise...")
try:
    # Adicionar coluna de estratégia ao DataFrame
    estrategias = []
    for idx, row in df.iterrows():
        if pd.notna(row['ponto_pedido']) and pd.notna(row['estoque_ideal']):
            quantidade_vendida = float(row['quantidade_vendida']) if pd.notna(row['quantidade_vendida']) else 0
            venda_media = quantidade_vendida / 1
            if venda_media > 0:
                dias = (row['estoque_ideal'] - row['ponto_pedido']) / venda_media
                if 4 <= dias <= 6:
                    estrategias.append('COMPRADOR')
                elif dias > 6:
                    estrategias.append('GIRO_OTIMIZADO_BAIXO')
                else:
                    estrategias.append('GIRO_OTIMIZADO_ALTO')
            else:
                estrategias.append('SEM_VENDAS')
        else:
            estrategias.append('GIRO_SAUDAVEL')
    
    df['estrategia_aplicada'] = estrategias
    df.to_excel('data/analise_estrategias.xlsx', index=False)
    print("[OK] Arquivo salvo: data/analise_estrategias.xlsx")
except Exception as e:
    print(f"[ERRO] Não foi possível salvar análise: {e}")
