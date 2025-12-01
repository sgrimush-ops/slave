#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Launcher: Calcular Pedidos

Calcula as sugestões de pedido e atualiza o arquivo data/gerado.xlsx.
"""

import sys
import os

# Adiciona o diretório scripts ao path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), 'scripts'))

# Importa e executa o script de atualização
from atualizar_simples import main

if __name__ == "__main__":
    print("=" * 60)
    print("CÁLCULO DE SUGESTÕES DE PEDIDO")
    print("=" * 60)
    print()
    
    main()
    
    print()
    print("=" * 60)
    print("Processo concluído!")
    print("=" * 60)
