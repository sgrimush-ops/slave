#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Consultar Vendas Históricas

Script para consultar o banco de dados de vendas em formato Parquet
"""

import pandas as pd
import os
from datetime import datetime


def consultar_vendas_por_data(data_venda=None, arquivo_parquet='data/vendas_historico.parquet'):
    """
    Consulta vendas por data específica
    
    Args:
        data_venda: Data no formato dd/mm/yy (None = todas as datas)
        arquivo_parquet: Caminho do arquivo Parquet
    """
    if not os.path.exists(arquivo_parquet):
        print(f"❌ Banco de dados não encontrado: {arquivo_parquet}")
        return None
    
    print("="*60)
    print("CONSULTA DE VENDAS HISTÓRICAS")
    print("="*60)
    
    # Carregar banco
    print(f"\n📂 Carregando banco de dados...")
    df = pd.read_parquet(arquivo_parquet)
    print(f"[OK] {len(df)} registros carregados")
    
    # Filtrar por data se especificado
    if data_venda:
        df_filtrado = df[df['data_venda'] == data_venda]
        print(f"\n🔍 Filtrando por data: {data_venda}")
        print(f"[OK] {len(df_filtrado)} registros encontrados")
        return df_filtrado
    
    return df


def estatisticas_vendas(arquivo_parquet='data/vendas_historico.parquet'):
    """
    Mostra estatísticas gerais do banco de vendas
    """
    if not os.path.exists(arquivo_parquet):
        print(f"❌ Banco de dados não encontrado: {arquivo_parquet}")
        return
    
    print("="*60)
    print("ESTATÍSTICAS DO BANCO DE VENDAS")
    print("="*60)
    
    df = pd.read_parquet(arquivo_parquet)
    
    print(f"\n📊 Total de registros: {len(df):,}")
    print(f"📅 Período: {df['data_venda'].min()} a {df['data_venda'].max()}")
    print(f"🏪 Lojas: {df['loja'].nunique()}")
    print(f"📦 Produtos únicos: {df['codigo_interno'].nunique()}")
    
    print(f"\n📅 Registros por data:")
    for data, count in df['data_venda'].value_counts().sort_index().items():
        print(f"   {data}: {count:,} registros")
    
    print(f"\n🏪 Registros por loja:")
    for loja, count in df['loja'].value_counts().sort_index().items():
        print(f"   Loja {loja}: {count:,} registros")
    
    print(f"\n📦 Top 10 produtos (por quantidade vendida total):")
    top_produtos = df.groupby(['codigo_interno', 'descricao'])['quantidade_vendida'].sum().sort_values(ascending=False).head(10)
    for (codigo, descricao), qtd in top_produtos.items():
        print(f"   {codigo} - {descricao[:40]}: {qtd:,.0f} unidades")
    
    print(f"\n🏬 Top 5 seções (por registros):")
    for secao, count in df['secao'].value_counts().head(5).items():
        print(f"   {secao}: {count:,} registros")


def consultar_produto(codigo_interno, arquivo_parquet='data/vendas_historico.parquet'):
    """
    Consulta histórico de vendas de um produto específico
    
    Args:
        codigo_interno: Código do produto
        arquivo_parquet: Caminho do arquivo Parquet
    """
    if not os.path.exists(arquivo_parquet):
        print(f"❌ Banco de dados não encontrado: {arquivo_parquet}")
        return None
    
    print("="*60)
    print(f"HISTÓRICO DO PRODUTO: {codigo_interno}")
    print("="*60)
    
    df = pd.read_parquet(arquivo_parquet)
    df_produto = df[df['codigo_interno'] == codigo_interno]
    
    if len(df_produto) == 0:
        print(f"\n[ERRO] Produto {codigo_interno} não encontrado no banco")
        return None
    
    print(f"\n📦 Descrição: {df_produto['descricao'].iloc[0]}")
    print(f"🏬 Seção: {df_produto['secao'].iloc[0]}")
    print(f"📊 Total de registros: {len(df_produto)}")
    
    print(f"\n📅 Vendas por data:")
    vendas_por_data = df_produto.groupby('data_venda').agg({
        'quantidade_vendida': 'sum',
        'valor_venda': lambda x: f"{sum(x):,.2f}",
        'loja': 'count'
    }).rename(columns={'loja': 'lojas_venderam'})
    
    for data, row in vendas_por_data.iterrows():
        print(f"   {data}: {row['quantidade_vendida']:,.0f} unidades, R$ {row['valor_venda']}, {row['lojas_venderam']} lojas")
    
    print(f"\n🏪 Vendas por loja:")
    vendas_por_loja = df_produto.groupby('loja').agg({
        'quantidade_vendida': 'sum',
        'valor_venda': lambda x: f"{sum(x):,.2f}"
    })
    
    for loja, row in vendas_por_loja.iterrows():
        print(f"   Loja {loja}: {row['quantidade_vendida']:,.0f} unidades, R$ {row['valor_venda']}")
    
    return df_produto


def menu():
    """Menu interativo"""
    while True:
        print("\n" + "="*60)
        print("MENU DE CONSULTAS")
        print("="*60)
        print("1. Estatísticas gerais do banco")
        print("2. Consultar vendas por data")
        print("3. Consultar histórico de produto")
        print("4. Exportar consulta para Excel")
        print("0. Sair")
        
        opcao = input("\nEscolha uma opção: ").strip()
        
        if opcao == "0":
            print("\n👋 Até logo!")
            break
        
        elif opcao == "1":
            estatisticas_vendas()
        
        elif opcao == "2":
            data = input("\nDigite a data (dd/mm/yy) ou ENTER para todas: ").strip()
            df = consultar_vendas_por_data(data if data else None)
            if df is not None and len(df) > 0:
                print("\n📊 Primeiras 10 linhas:")
                print(df.head(10))
        
        elif opcao == "3":
            codigo = input("\nDigite o código interno do produto: ").strip()
            try:
                codigo = int(codigo)
                consultar_produto(codigo)
            except ValueError:
                print("[ERRO] Código inválido! Digite apenas números.")
        
        elif opcao == "4":
            data = input("\nDigite a data (dd/mm/yy) ou ENTER para todas: ").strip()
            df = consultar_vendas_por_data(data if data else None)
            if df is not None and len(df) > 0:
                arquivo = f"data/consulta_vendas_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
                df.to_excel(arquivo, index=False)
                print(f"\n[OK] Consulta exportada para: {arquivo}")
        
        else:
            print("\n[ERRO] Opção inválida!")


if __name__ == "__main__":
    menu()
