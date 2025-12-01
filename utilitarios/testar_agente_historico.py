#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Teste de integração: Agente IA + Histórico de Vendas

Demonstra como o agente usa dados históricos para análises mais robustas
"""

import sys
import os

# Adiciona diretório raiz ao path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.agente_estoque import AgenteEstoque
from src.analise_historico import AnalisadorHistorico


def testar_historico():
    """Testa carregamento e análise de histórico"""
    print("="*60)
    print("TESTE 1: ANALISADOR DE HISTÓRICO")
    print("="*60)
    
    analisador = AnalisadorHistorico()
    
    if analisador.df is None:
        print("❌ Sem dados históricos disponíveis")
        print("   Execute 'python tratamento_abc.py' primeiro")
        return False
    
    # Estatísticas gerais
    stats = analisador.obter_estatisticas_gerais()
    print(f"\n📊 Estatísticas Gerais:")
    print(f"   Total registros: {stats['total_registros']:,}")
    print(f"   Período: {stats['periodo']['inicio']} a {stats['periodo']['fim']}")
    print(f"   Lojas: {stats['lojas']}")
    print(f"   Produtos: {stats['produtos_unicos']:,}")
    
    # Top 5 produtos
    print(f"\n🏆 Top 5 Produtos (todas as lojas):")
    top = analisador.obter_top_produtos(top_n=5)
    for item in top:
        print(f"   {item['posicao']}. {item['descricao'][:50]} - {item['quantidade_total']:.0f} unidades")
    
    return True


def testar_analise_produto():
    """Testa análise detalhada de um produto"""
    print("\n" + "="*60)
    print("TESTE 2: ANÁLISE DE PRODUTO ESPECÍFICO")
    print("="*60)
    
    analisador = AnalisadorHistorico()
    
    if analisador.df is None:
        return
    
    # Pegar um produto do top 5
    top = analisador.obter_top_produtos(top_n=1)
    if not top:
        print("❌ Sem produtos no histórico")
        return
    
    codigo = top[0]['codigo_interno']
    loja = 11  # Testar para loja 11
    
    print(f"\n🎯 Analisando produto {codigo} na loja {loja}...")
    
    # Média de vendas
    media = analisador.calcular_media_vendas_produto(codigo, loja)
    if "erro" not in media:
        print(f"\n📊 Vendas Históricas:")
        print(f"   Produto: {media['descricao']}")
        print(f"   Seção: {media['secao']}")
        print(f"   Média/dia: {media['vendas']['media_dia']:.2f} unidades")
        print(f"   Total no período: {media['vendas']['total']:.0f} unidades")
        print(f"   Variação: {media['vendas']['minima_dia']:.0f} - {media['vendas']['maxima_dia']:.0f}")
    
    # Tendência
    tendencia = analisador.analisar_tendencia_produto(codigo, loja)
    if "erro" not in tendencia:
        print(f"\n📈 Tendência:")
        print(f"   Classificação: {tendencia['tendencia']}")
        print(f"   Variação: {tendencia['variacao_percentual']:+.1f}%")
        print(f"   1ª metade: {tendencia['periodo']['primeira_metade']['media']:.2f} un/dia")
        print(f"   2ª metade: {tendencia['periodo']['segunda_metade']['media']:.2f} un/dia")
    
    # Cobertura (simulando estoque de 100 unidades)
    estoque_simulado = 100
    cobertura = analisador.calcular_cobertura_necessaria(codigo, loja, estoque_simulado, dias_cobertura=4)
    if "erro" not in cobertura:
        print(f"\n🔍 Análise de Cobertura (estoque simulado: {estoque_simulado}):")
        print(f"   Cobertura atual: {cobertura['dias_cobertura_atual']:.1f} dias")
        print(f"   Status: {cobertura['status']}")
        print(f"   Necessário para 4 dias: {cobertura['necessidade']['total_para_cobertura']:.0f} unidades")
        print(f"   Quantidade a pedir: {cobertura['necessidade']['quantidade_pedir']:.0f} unidades")


def testar_agente_com_historico():
    """Testa agente IA usando histórico"""
    print("\n" + "="*60)
    print("TESTE 3: AGENTE IA COM HISTÓRICO")
    print("="*60)
    
    print("\n⏳ Inicializando agente LLaMA 3 com histórico...")
    agente = AgenteEstoque(usar_historico=True)
    
    if not agente.analisador:
        print("⚠️  Agente sem histórico - análise limitada")
        return
    
    # Pegar produto para análise
    top = agente.analisador.obter_top_produtos(top_n=1)
    if not top:
        print("❌ Sem produtos para análise")
        return
    
    codigo = top[0]['codigo_interno']
    loja = 11
    
    print(f"\n🤖 Analisando pedido do produto {codigo} (loja {loja}) com IA...")
    print(f"   Produto: {top[0]['descricao']}")
    print("\n⏳ Consultando LLaMA 3 (isso pode levar alguns segundos)...\n")
    
    # Simular dados de estoque
    resposta = agente.analisar_pedido_com_historico(
        codigo_interno=codigo,
        loja_id=loja,
        estoque_atual=50,
        ponto_pedido=100,
        estoque_ideal=200,
        embalagem=12
    )
    
    print("="*60)
    print("RESPOSTA DO AGENTE:")
    print("="*60)
    print(resposta)
    print("="*60)


def menu():
    """Menu de testes"""
    print("\n" + "="*60)
    print("SISTEMA DE TESTES - AGENTE IA + HISTÓRICO")
    print("="*60)
    print("\n1. Testar carregamento de histórico")
    print("2. Testar análise detalhada de produto")
    print("3. Testar agente IA com histórico (LLaMA 3)")
    print("4. Executar todos os testes")
    print("0. Sair")
    
    opcao = input("\nEscolha uma opção: ").strip()
    
    if opcao == "0":
        print("\n👋 Até logo!")
        return False
    
    elif opcao == "1":
        testar_historico()
    
    elif opcao == "2":
        testar_analise_produto()
    
    elif opcao == "3":
        testar_agente_com_historico()
    
    elif opcao == "4":
        if testar_historico():
            testar_analise_produto()
            print("\n" + "="*60)
            resposta = input("\nDeseja testar o agente IA? (s/n): ").strip().lower()
            if resposta == 's':
                testar_agente_com_historico()
    
    else:
        print("❌ Opção inválida!")
    
    return True


def main():
    """Função principal"""
    
    # Verificar se há histórico
    if not os.path.exists('data/vendas_historico.parquet'):
        print("="*60)
        print("⚠️  ATENÇÃO: BANCO DE HISTÓRICO NÃO ENCONTRADO")
        print("="*60)
        print("\nPara usar este sistema, você precisa primeiro processar")
        print("os dados de vendas executando:")
        print("\n  python tratamento_abc.py")
        print("\nDepois volte e execute este teste novamente.")
        print("="*60)
        return
    
    # Menu interativo
    while menu():
        input("\nPressione ENTER para continuar...")


if __name__ == "__main__":
    main()
