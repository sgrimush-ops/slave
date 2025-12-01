# -*- coding: utf-8 -*-
"""
Script para criar executável do Sistema de Gestão de Estoque

Gera um executável standalone usando PyInstaller
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def verificar_pyinstaller():
    """Verifica se PyInstaller está instalado"""
    try:
        import PyInstaller
        print("[OK] PyInstaller encontrado")
        return True
    except ImportError:
        print("[AVISO] PyInstaller nao encontrado")
        resposta = input("Deseja instalar PyInstaller? (s/n): ")
        if resposta.lower() == 's':
            subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
            return True
        return False

def limpar_builds_anteriores():
    """Remove builds anteriores"""
    dirs = ['build', 'dist', '__pycache__']
    for dir_name in dirs:
        if os.path.exists(dir_name):
            print(f"Removendo {dir_name}/")
            shutil.rmtree(dir_name)
    
    spec_file = 'interface.spec'
    if os.path.exists(spec_file):
        print(f"Removendo {spec_file}")
        os.remove(spec_file)

def criar_executavel():
    """Cria o executável"""
    print("\n" + "="*60)
    print("CRIANDO EXECUTAVEL DO SISTEMA DE GESTAO DE ESTOQUE")
    print("="*60 + "\n")
    
    # Verificar PyInstaller
    if not verificar_pyinstaller():
        print("[ERRO] PyInstaller necessario para criar executavel")
        return False
    
    # Limpar builds anteriores
    print("\nLimpando builds anteriores...")
    limpar_builds_anteriores()
    
    # Comando PyInstaller
    comando = [
        sys.executable,
        "-m", "PyInstaller",
        "--name=SistemaEstoque",
        "--onefile",
        "--windowed",
        "--icon=NONE",
        "--add-data=src;src",
        "--add-data=scripts;scripts",
        "--add-data=data;data",
        "--hidden-import=tkinter",
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=pyarrow",
        "--hidden-import=ollama",
        "--hidden-import=openpyxl",
        "--hidden-import=sqlite3",
        "interface.py"
    ]
    
    print("\nExecutando PyInstaller...")
    print(f"Comando: {' '.join(comando)}\n")
    
    try:
        resultado = subprocess.run(comando, check=True)
        
        print("\n" + "="*60)
        print("[OK] EXECUTAVEL CRIADO COM SUCESSO!")
        print("="*60)
        print(f"\nLocalização: {os.path.abspath('dist/SistemaEstoque.exe')}")
        print("\nPROXIMOS PASSOS:")
        print("1. Copie o arquivo dist/SistemaEstoque.exe para onde desejar")
        print("2. Certifique-se de que as pastas data/, src/ e scripts/ estejam no mesmo diretorio")
        print("3. Execute SistemaEstoque.exe")
        print("\nOBSERVACAO: O executável precisa dos arquivos de dados e scripts no mesmo diretório!")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"\n[ERRO] Falha ao criar executavel: {e}")
        return False
    except Exception as e:
        print(f"\n[ERRO] Erro inesperado: {e}")
        return False

def criar_pacote_distribuicao():
    """Cria um pacote completo para distribuição"""
    if not os.path.exists('dist/SistemaEstoque.exe'):
        print("[ERRO] Executavel não encontrado. Execute a criação primeiro.")
        return
    
    print("\n" + "="*60)
    print("CRIANDO PACOTE DE DISTRIBUICAO")
    print("="*60 + "\n")
    
    # Criar pasta de distribuição
    dist_folder = Path('dist/SistemaEstoque_Completo')
    if dist_folder.exists():
        shutil.rmtree(dist_folder)
    dist_folder.mkdir(parents=True)
    
    # Copiar executável
    shutil.copy2('dist/SistemaEstoque.exe', dist_folder / 'SistemaEstoque.exe')
    print("[OK] Executavel copiado")
    
    # Copiar pastas necessárias
    for pasta in ['src', 'scripts', 'utilitarios', 'launchers']:
        if os.path.exists(pasta):
            shutil.copytree(pasta, dist_folder / pasta)
            print(f"[OK] Pasta {pasta}/ copiada")
    
    # Criar pasta data vazia
    (dist_folder / 'data').mkdir(exist_ok=True)
    print("[OK] Pasta data/ criada")
    
    # Copiar documentação
    for doc in ['README.md', 'GUIA_RAPIDO.md']:
        if os.path.exists(doc):
            shutil.copy2(doc, dist_folder / doc)
            print(f"[OK] {doc} copiado")
    
    # Criar arquivo LEIA-ME
    with open(dist_folder / 'LEIA-ME.txt', 'w', encoding='utf-8') as f:
        f.write("""SISTEMA DE GESTAO DE ESTOQUE COM IA
=====================================

COMO USAR:
1. Execute SistemaEstoque.exe
2. Use a interface gráfica para importar arquivos
3. Processe as vendas diárias
4. Execute análises e consulte o agente IA

REQUISITOS:
- Ollama instalado (para agente IA com LLaMA 3)
- Modelo LLaMA 3 instalado: ollama pull llama3

ESTRUTURA:
- SistemaEstoque.exe: Interface gráfica principal
- src/: Módulos do sistema
- scripts/: Scripts de processamento
- data/: Dados e banco de dados
- utilitarios/: Ferramentas auxiliares

DOCUMENTACAO:
- README.md: Documentação completa
- GUIA_RAPIDO.md: Guia rápido de uso

SUPORTE:
Consulte a documentação ou use o agente IA para dúvidas.
""")
    print("[OK] LEIA-ME.txt criado")
    
    print("\n" + "="*60)
    print("[OK] PACOTE DE DISTRIBUICAO CRIADO!")
    print("="*60)
    print(f"\nLocalização: {os.path.abspath(dist_folder)}")
    print("\nConteúdo:")
    print("- SistemaEstoque.exe (executável)")
    print("- src/, scripts/, utilitarios/, launchers/ (código)")
    print("- data/ (pasta para dados)")
    print("- README.md e GUIA_RAPIDO.md (documentação)")
    print("- LEIA-ME.txt (instruções)")
    print("\nEste pacote pode ser distribuído completo!")

def main():
    """Função principal"""
    print("Sistema de Criação de Executável")
    print("="*60)
    print("\nOpções:")
    print("1. Criar apenas executável")
    print("2. Criar executável + pacote de distribuição")
    print("3. Apenas pacote (executável já existe)")
    
    opcao = input("\nEscolha uma opção (1-3): ").strip()
    
    if opcao == '1':
        criar_executavel()
    elif opcao == '2':
        if criar_executavel():
            input("\nPressione ENTER para criar pacote de distribuição...")
            criar_pacote_distribuicao()
    elif opcao == '3':
        criar_pacote_distribuicao()
    else:
        print("[ERRO] Opção inválida")
    
    input("\nPressione ENTER para sair...")

if __name__ == "__main__":
    main()
