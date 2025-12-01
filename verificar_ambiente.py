# -*- coding: utf-8 -*-
"""
Script de Verificação do Ambiente

Verifica se todas as dependências estão instaladas corretamente
e se o sistema está pronto para uso.
"""

import sys
import os
from pathlib import Path

def verificar_python():
    """Verifica versão do Python"""
    print("\n" + "="*60)
    print("VERIFICANDO PYTHON")
    print("="*60)
    
    versao = sys.version_info
    print(f"Versão Python: {versao.major}.{versao.minor}.{versao.micro}")
    
    if versao.major >= 3 and versao.minor >= 11:
        print("[OK] Python 3.11+ detectado")
        return True
    else:
        print("[ERRO] Python 3.11+ necessário")
        print(f"Versão atual: {versao.major}.{versao.minor}.{versao.micro}")
        return False

def verificar_venv():
    """Verifica se está em ambiente virtual"""
    print("\n" + "="*60)
    print("VERIFICANDO AMBIENTE VIRTUAL")
    print("="*60)
    
    in_venv = hasattr(sys, 'real_prefix') or (
        hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix
    )
    
    if in_venv:
        print("[OK] Ambiente virtual ativado")
        print(f"Path: {sys.prefix}")
        return True
    else:
        print("[AVISO] Ambiente virtual nao detectado")
        print("Recomendado: python -m venv .venv")
        print("             .venv\\Scripts\\activate")
        return False

def verificar_modulos():
    """Verifica se módulos necessários estão instalados"""
    print("\n" + "="*60)
    print("VERIFICANDO MODULOS PYTHON")
    print("="*60)
    
    modulos_obrigatorios = {
        'pandas': 'Manipulacao de dados',
        'numpy': 'Computacao numerica',
        'openpyxl': 'Arquivos Excel',
        'pyarrow': 'Arquivos Parquet',
        'ollama': 'Cliente Ollama (IA)',
    }
    
    modulos_opcionais = {
        'fastapi': 'API REST',
        'uvicorn': 'Servidor ASGI',
        'pydantic': 'Validacao de dados',
        'pyinstaller': 'Criar executavel',
    }
    
    todos_ok = True
    
    print("\nMódulos Obrigatórios:")
    for modulo, descricao in modulos_obrigatorios.items():
        try:
            __import__(modulo)
            print(f"  [OK] {modulo:12} - {descricao}")
        except ImportError:
            print(f"  [ERRO] {modulo:12} - {descricao} (NAO INSTALADO)")
            todos_ok = False
    
    print("\nMódulos Opcionais:")
    for modulo, descricao in modulos_opcionais.items():
        try:
            __import__(modulo)
            print(f"  [OK] {modulo:12} - {descricao}")
        except ImportError:
            print(f"  [AVISO] {modulo:12} - {descricao} (nao instalado)")
    
    # Verificar tkinter (especial - vem com Python)
    print("\nInterface Gráfica:")
    try:
        import tkinter
        print(f"  [OK] tkinter      - Interface grafica")
    except ImportError:
        print(f"  [ERRO] tkinter    - Interface grafica (NAO DISPONIVEL)")
        print("         Reinstale Python com tkinter incluido")
        todos_ok = False
    
    return todos_ok

def verificar_ollama():
    """Verifica se Ollama está instalado e rodando"""
    print("\n" + "="*60)
    print("VERIFICANDO OLLAMA (AGENTE IA)")
    print("="*60)
    
    import subprocess
    
    # Verificar se ollama está instalado
    try:
        result = subprocess.run(
            ['ollama', '--version'],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            versao = result.stdout.strip()
            print(f"[OK] Ollama instalado: {versao}")
        else:
            print("[AVISO] Ollama instalado mas não respondeu")
    except FileNotFoundError:
        print("[ERRO] Ollama NAO INSTALADO")
        print("       Download: https://ollama.ai/download")
        return False
    except Exception as e:
        print(f"[ERRO] Erro ao verificar Ollama: {e}")
        return False
    
    # Verificar se está rodando
    try:
        import requests
        response = requests.get('http://localhost:11434/api/tags', timeout=2)
        if response.status_code == 200:
            print("[OK] Ollama está rodando")
            
            # Verificar modelo llama3
            data = response.json()
            modelos = [m['name'] for m in data.get('models', [])]
            if any('llama3' in m.lower() for m in modelos):
                print("[OK] Modelo LLaMA 3 instalado")
                return True
            else:
                print("[AVISO] Modelo LLaMA 3 nao encontrado")
                print("        Instale: ollama pull llama3")
                return False
        else:
            print("[AVISO] Ollama instalado mas nao esta rodando")
            print("        Execute: ollama serve")
            return False
    except requests.exceptions.ConnectionError:
        print("[AVISO] Ollama instalado mas nao esta rodando")
        print("        Execute: ollama serve")
        return False
    except Exception as e:
        print(f"[AVISO] Nao foi possivel verificar status: {e}")
        return False

def verificar_arquivos():
    """Verifica estrutura de arquivos do projeto"""
    print("\n" + "="*60)
    print("VERIFICANDO ESTRUTURA DO PROJETO")
    print("="*60)
    
    arquivos_essenciais = [
        'interface.py',
        'analista.py',
        'tratamento_abc.py',
        'requirements.txt',
        'src/agente_estoque.py',
        'src/analise_historico.py',
        'scripts/atualizar_simples.py',
    ]
    
    todos_ok = True
    
    for arquivo in arquivos_essenciais:
        caminho = Path(arquivo)
        if caminho.exists():
            print(f"  [OK] {arquivo}")
        else:
            print(f"  [ERRO] {arquivo} (NAO ENCONTRADO)")
            todos_ok = False
    
    # Verificar pastas
    print("\nPastas:")
    pastas = ['data', 'src', 'scripts', 'docs']
    for pasta in pastas:
        caminho = Path(pasta)
        if caminho.exists() and caminho.is_dir():
            print(f"  [OK] {pasta}/")
        else:
            print(f"  [AVISO] {pasta}/ (nao existe - sera criada)")
    
    return todos_ok

def verificar_dados():
    """Verifica se dados necessários existem"""
    print("\n" + "="*60)
    print("VERIFICANDO DADOS")
    print("="*60)
    
    banco = Path('data/banco.db')
    if banco.exists():
        print(f"[OK] Banco de dados encontrado ({banco.stat().st_size // 1024} KB)")
    else:
        print("[AVISO] Banco de dados nao encontrado")
        print("        Execute: python launchers/criar_db.py")
    
    historico = Path('data/vendas_historico.parquet')
    if historico.exists():
        print(f"[OK] Historico de vendas encontrado ({historico.stat().st_size // 1024} KB)")
    else:
        print("[AVISO] Historico de vendas nao encontrado")
        print("        Sera criado ao processar primeira venda")
    
    return True

def verificar_permissoes():
    """Verifica se tem permissões necessárias"""
    print("\n" + "="*60)
    print("VERIFICANDO PERMISSOES")
    print("="*60)
    
    # Verificar se pode criar arquivos em data/
    data_dir = Path('data')
    data_dir.mkdir(exist_ok=True)
    
    teste = data_dir / 'teste_permissao.tmp'
    try:
        teste.write_text('teste')
        teste.unlink()
        print("[OK] Permissao de escrita em data/")
        return True
    except Exception as e:
        print(f"[ERRO] Sem permissao de escrita em data/: {e}")
        return False

def gerar_relatorio():
    """Gera relatório completo"""
    print("\n" + "="*60)
    print("RELATORIO FINAL")
    print("="*60)
    
    resultados = {
        'Python': verificar_python(),
        'Ambiente Virtual': verificar_venv(),
        'Modulos': verificar_modulos(),
        'Ollama': verificar_ollama(),
        'Arquivos': verificar_arquivos(),
        'Dados': verificar_dados(),
        'Permissoes': verificar_permissoes(),
    }
    
    print("\n" + "="*60)
    print("RESUMO")
    print("="*60)
    
    for item, status in resultados.items():
        if status:
            print(f"[OK] {item}")
        else:
            print(f"[PROBLEMA] {item}")
    
    # Status geral
    obrigatorios = ['Python', 'Modulos', 'Arquivos', 'Permissoes']
    ok_obrigatorios = all(resultados[k] for k in obrigatorios)
    
    print("\n" + "="*60)
    if ok_obrigatorios:
        print("[OK] SISTEMA PRONTO PARA USO!")
        print("="*60)
        print("\nPróximos passos:")
        print("1. Iniciar interface: python interface.py")
        if not resultados['Ollama']:
            print("2. Para usar IA: Instalar Ollama e modelo LLaMA 3")
        if not resultados['Dados']:
            print("3. Criar banco: python launchers/criar_db.py")
    else:
        print("[ERRO] SISTEMA COM PROBLEMAS")
        print("="*60)
        print("\nResolva os problemas acima antes de usar o sistema.")
        print("Consulte: INSTALACAO_WINDOWS.md")
    
    return ok_obrigatorios

def main():
    """Função principal"""
    print("\n" + "="*60)
    print("VERIFICACAO DO AMBIENTE")
    print("Sistema de Gestao de Estoque com IA")
    print("="*60)
    
    sucesso = gerar_relatorio()
    
    input("\nPressione ENTER para sair...")
    return 0 if sucesso else 1

if __name__ == "__main__":
    sys.exit(main())
