#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Launcher: Interface de Linha de Comando

Inicia a CLI interativa do sistema de gestão de estoque.
"""

import sys
import os

# Adiciona o diretório src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from cli import main as cli_main

def main():
    """Inicia a interface de linha de comando."""
    print("=" * 60)
    print("CLI - SISTEMA DE GESTÃO DE ESTOQUE")
    print("=" * 60)
    print()
    print("Inicializando interface...")
    print()
    
    try:
        cli_main()
    except KeyboardInterrupt:
        print("\n\nCLI encerrada pelo usuário.")
    except Exception as e:
        print(f"\n\nErro ao executar CLI: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
