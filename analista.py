#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
ANALISTA - Sistema Mestre de Gestão de Estoque com IA

Sistema principal integrado que:
1. Calcula sugestões de pedido com balanceamento inteligente
2. Usa histórico de vendas para análises robustas
3. Gera análises e relatórios
4. Inicia agente LLaMA 3 para recomendações avançadas

Pré-requisitos:
- Banco de dados: data/banco.db (execute: python launchers/criar_db.py)
- Histórico de vendas: data/vendas_historico.parquet (execute: python tratamento_abc.py)

Execute este arquivo para rodar todo o sistema!
"""

import sys
import os
import subprocess
from pathlib import Path

# Adiciona diretórios ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'scripts'))

def print_header(titulo):
    """Imprime cabeçalho formatado"""
    print("\n" + "=" * 70)
    print(f"  {titulo}")
    print("=" * 70 + "\n")

def executar_etapa(descricao, comando, args=None):
    """Executa uma etapa do processo"""
    print(f"> {descricao}...")
    try:
        if args:
            resultado = comando(*args)
        else:
            resultado = comando()
        print(f"[OK] {descricao} - Concluido!\n")
        return resultado
    except Exception as e:
        print(f"[AVISO] {descricao} - Erro: {e}\n")
        return None

def verificar_banco_dados():
    """Verifica se o banco de dados existe"""
    banco_path = Path("data/banco.db")
    return banco_path.exists()

def criar_banco_dados():
    """Cria o banco de dados a partir do mix.xlsx"""
    from criar_banco import main as criar_banco_main
    criar_banco_main()

def calcular_sugestoes():
    """Calcula sugestões de pedido com balanceamento inteligente"""
    from atualizar_simples import main as calcular_main
    calcular_main()

def gerar_analise():
    """Gera análise das estratégias aplicadas"""
    print("Gerando analise detalhada das estrategias...\n")
    try:
        subprocess.run([sys.executable, "scripts/analisar_estrategias.py"], check=True)
    except Exception as e:
        print(f"[AVISO] Analise nao pode ser gerada: {e}\n")

def iniciar_sistema_completo():
    """Inicia o sistema completo com menu interativo"""
    from gerenciador import GerenciadorEstoque
    
    print_header("SISTEMA INTERATIVO COM AGENTE IA")
    print("Iniciando sistema completo com agente LLaMA 3...")
    print("(Use Ctrl+C para sair)\n")
    
    try:
        gerenciador = GerenciadorEstoque()
        gerenciador.executar()
    except KeyboardInterrupt:
        print("\n\nSistema encerrado pelo usuario.")
    except Exception as e:
        print(f"\n\n[ERRO] Erro ao executar o sistema: {e}")
        import traceback
        traceback.print_exc()

def verificar_historico_vendas():
    """Verifica se existe histórico de vendas"""
    historico_path = Path("data/vendas_historico.parquet")
    return historico_path.exists()

def main():
    """Função principal que executa todo o processo"""
    
    print_header("ANALISTA - Sistema Mestre de Gestao de Estoque com IA")
    
    print("Este sistema executa automaticamente:")
    print("  1. Calculo de sugestoes com balanceamento inteligente")
    print("  2. Analise de estrategias aplicadas")
    print("  3. Sistema interativo com agente LLaMA 3 + Historico")
    print()
    
    # Verifica se o banco existe
    if not verificar_banco_dados():
        print("[ERRO] Banco de dados nao encontrado!")
        print("   Execute: python launchers/criar_db.py")
        print()
        input("Pressione ENTER para sair...")
        return
    
    print("[OK] Banco de dados encontrado: data/banco.db")
    
    # Verifica histórico de vendas
    if verificar_historico_vendas():
        print("[OK] Historico de vendas encontrado: data/vendas_historico.parquet")
        print("     O agente IA tera acesso a dados historicos!")
    else:
        print("[AVISO] Historico de vendas nao encontrado")
        print("        Execute: python tratamento_abc.py")
        print("        O sistema funcionara com analise basica")
    
    print()
    input("Pressione ENTER para iniciar o processo completo...")
    
    # ETAPA 1: Cálculo de Sugestões
    print_header("ETAPA 1: CALCULO DE SUGESTOES DE PEDIDO")
    print("Aplicando estrategia de balanceamento inteligente:")
    print("  - Comprador: Respeita valores adequados (4-6 dias)")
    print("  - Giro Otimizado: Ajusta valores anti-economicos")
    print("  - Giro Saudavel: Padrao quando nao ha valores\n")
    
    executar_etapa("Calculando sugestoes", calcular_sugestoes)
    
    # ETAPA 2: Análise de Estratégias
    print_header("ETAPA 2: ANALISE DE ESTRATEGIAS")
    executar_etapa("Gerando analise detalhada", gerar_analise)
    
    # ETAPA 3: Sistema Completo
    input("\nPressione ENTER para iniciar o sistema interativo com IA...")
    iniciar_sistema_completo()
    
    # Finalização
    print_header("PROCESSO COMPLETO FINALIZADO")
    print("Obrigado por usar o Sistema de Gestao de Estoque com IA!")

if __name__ == "__main__":
    main()
