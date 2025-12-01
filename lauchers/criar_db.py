#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Launcher: Criar Banco de Dados

Cria o banco de dados SQLite a partir do arquivo data/mix.xlsx.
"""

import sys
import os

# Adiciona o diretório scripts ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'scripts'))

# Importa e executa o script de criação
from criar_banco import main

if __name__ == "__main__":
    print("=" * 60)
    print("CRIAÇÃO DO BANCO DE DADOS")
    print("=" * 60)
    print()
    
    main()
    
    print()
    print("=" * 60)
    print("Processo concluído!")
    print("=" * 60)
