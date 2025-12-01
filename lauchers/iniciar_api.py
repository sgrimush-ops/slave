#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Launcher: API REST

Inicia o servidor da API REST na porta 8000.
"""

import sys
import os

# Adiciona o diretório src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

import uvicorn

def main():
    """Inicia o servidor da API."""
    print("=" * 60)
    print("API REST - SISTEMA DE GESTÃO DE ESTOQUE")
    print("=" * 60)
    print()
    print("Iniciando servidor na porta 8000...")
    print("Acesse: http://localhost:8000")
    print("Documentação: http://localhost:8000/docs")
    print()
    print("Pressione Ctrl+C para encerrar.")
    print("=" * 60)
    print()
    
    try:
        uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
    except KeyboardInterrupt:
        print("\n\nServidor encerrado pelo usuário.")
    except Exception as e:
        print(f"\n\nErro ao iniciar servidor: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
