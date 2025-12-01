"""
Script para gerar executável do sistema de gestão de estoque
Usa PyInstaller para criar um executável standalone
"""

import sys
import os
import subprocess
import shutil
from pathlib import Path

def limpar_builds_anteriores():
    """Remove builds anteriores"""
    print("\n[1/5] Limpando builds anteriores...")
    
    dirs_remover = ['build', 'dist', '__pycache__']
    for dir_name in dirs_remover:
        if os.path.exists(dir_name):
            print(f"  Removendo: {dir_name}/")
            shutil.rmtree(dir_name)
    
    # Remover spec file se existir
    spec_file = 'interface.spec'
    if os.path.exists(spec_file):
        print(f"  Removendo: {spec_file}")
        os.remove(spec_file)
    
    print("  [OK] Limpeza concluída")

def verificar_pyinstaller():
    """Verifica se PyInstaller está instalado"""
    print("\n[2/5] Verificando PyInstaller...")
    
    try:
        result = subprocess.run(
            [sys.executable, '-m', 'pip', 'show', 'pyinstaller'],
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            print("  [AVISO] PyInstaller não encontrado")
            print("  Instalando PyInstaller...")
            subprocess.run(
                [sys.executable, '-m', 'pip', 'install', 'pyinstaller'],
                check=True
            )
            print("  [OK] PyInstaller instalado")
        else:
            print("  [OK] PyInstaller já instalado")
        return True
    except Exception as e:
        print(f"  [ERRO] Falha ao verificar/instalar PyInstaller: {e}")
        return False

def criar_spec_customizado():
    """Cria arquivo .spec customizado para o build"""
    print("\n[3/5] Criando configuração de build...")
    
    spec_content = """# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['interface.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('src', 'src'),
        ('scripts', 'scripts'),
        ('data/colunas.txt', 'data'),
    ],
    hiddenimports=[
        'pandas',
        'openpyxl',
        'pyarrow',
        'requests',
        'tkinter',
        'tkinter.scrolledtext',
        'tkinter.ttk',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib',
        'numpy.testing',
        'IPython',
        'jupyter',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='GestaoEstoque',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Sem console extra
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # Adicione um ícone .ico se tiver
)
"""
    
    with open('GestaoEstoque.spec', 'w', encoding='utf-8') as f:
        f.write(spec_content)
    
    print("  [OK] Arquivo GestaoEstoque.spec criado")

def executar_build():
    """Executa o PyInstaller"""
    print("\n[4/5] Gerando executável...")
    print("  [INFO] Isso pode levar alguns minutos...")
    print("  [INFO] Aguarde enquanto o PyInstaller compila o aplicativo...\n")
    
    try:
        resultado = subprocess.run(
            [sys.executable, '-m', 'PyInstaller', 'GestaoEstoque.spec', '--clean'],
            check=True,
            text=True
        )
        
        print("\n  [OK] Build concluído com sucesso!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n  [ERRO] Falha no build: {e}")
        return False

def organizar_distribuicao():
    """Organiza arquivos para distribuição"""
    print("\n[5/5] Organizando distribuição...")
    
    # Criar estrutura de pastas
    dist_dir = Path('dist/GestaoEstoque')
    if not dist_dir.exists():
        dist_dir.mkdir(parents=True)
    
    # Copiar pasta data (se não existir)
    data_src = Path('data')
    data_dst = dist_dir / 'data'
    if not data_dst.exists():
        data_dst.mkdir()
        print("  Criando pasta data/")
        
        # Copiar apenas colunas.txt
        if (data_src / 'colunas.txt').exists():
            shutil.copy(data_src / 'colunas.txt', data_dst / 'colunas.txt')
            print("  [OK] colunas.txt copiado")
    
    # Criar arquivo README
    readme_content = """SISTEMA DE GESTÃO DE ESTOQUE - ABC
====================================

COMO USAR:
----------
1. Execute GestaoEstoque.exe
2. Importe os arquivos CSV necessários
3. Processe as vendas diárias
4. Execute análises e consulte o agente IA

REQUISITOS:
-----------
- Ollama instalado (para usar o Agente IA)
  Baixe em: https://ollama.ai
  Instale um modelo: ollama pull llama3.2

ESTRUTURA DE PASTAS:
--------------------
data/           - Arquivos de dados (CSV, Excel, Parquet)
scripts/        - Scripts auxiliares (incluídos no executável)
src/            - Código fonte (incluído no executável)

SUPORTE:
--------
Para problemas ou dúvidas, consulte a documentação do sistema.

Versão: 1.0
Data: 30/11/2025
"""
    
    readme_path = dist_dir / 'LEIA-ME.txt'
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print("  [OK] LEIA-ME.txt criado")
    
    # Verificar se executável foi criado
    exe_path = Path('dist/GestaoEstoque.exe')
    if exe_path.exists():
        tamanho_mb = exe_path.stat().st_size / (1024 * 1024)
        print(f"\n  [OK] Executável criado: dist/GestaoEstoque.exe ({tamanho_mb:.1f} MB)")
        return True
    else:
        print("\n  [ERRO] Executável não encontrado!")
        return False

def main():
    """Função principal"""
    print("="*60)
    print("GERADOR DE EXECUTÁVEL - SISTEMA DE GESTÃO DE ESTOQUE")
    print("="*60)
    
    # Verificar se estamos no diretório correto
    if not os.path.exists('interface.py'):
        print("\n[ERRO] Arquivo interface.py não encontrado!")
        print("Execute este script na pasta raiz do projeto.")
        return False
    
    # Etapas do build
    limpar_builds_anteriores()
    
    if not verificar_pyinstaller():
        print("\n[ERRO] Não foi possível instalar PyInstaller")
        return False
    
    criar_spec_customizado()
    
    if not executar_build():
        print("\n[ERRO] Build falhou")
        return False
    
    if not organizar_distribuicao():
        print("\n[ERRO] Falha ao organizar distribuição")
        return False
    
    # Resumo final
    print("\n" + "="*60)
    print("BUILD CONCLUÍDO COM SUCESSO!")
    print("="*60)
    print("\nArquivos gerados:")
    print("  • dist/GestaoEstoque.exe - Executável principal")
    print("  • dist/GestaoEstoque/data/ - Pasta de dados")
    print("  • dist/GestaoEstoque/LEIA-ME.txt - Instruções")
    print("\nPara distribuir:")
    print("  1. Copie a pasta dist/GestaoEstoque/ completa")
    print("  2. Ou crie um ZIP com todo o conteúdo")
    print("  3. O usuário precisa apenas executar GestaoEstoque.exe")
    print("\nOBSERVAÇÕES:")
    print("  • Ollama deve ser instalado separadamente")
    print("  • Arquivos CSV devem ser importados pelo usuário")
    print("  • A pasta data/ será criada automaticamente se não existir")
    print("="*60)
    
    return True

if __name__ == '__main__':
    try:
        sucesso = main()
        sys.exit(0 if sucesso else 1)
    except KeyboardInterrupt:
        print("\n\n[CANCELADO] Build interrompido pelo usuário")
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERRO FATAL] {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
