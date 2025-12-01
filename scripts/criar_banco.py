"""
Script para criar banco de dados SQLite a partir da planilha mix.xlsx
"""
import sqlite3
import pandas as pd
from pathlib import Path
from datetime import datetime


def criar_banco_dados():
    """Cria banco de dados SQLite a partir do mix.xlsx"""
    
    # Caminhos
    data_dir = Path("data")
    arquivo_excel = data_dir / "mix.xlsx"
    arquivo_db = data_dir / "banco.db"
    
    # Verifica se o arquivo Excel existe
    if not arquivo_excel.exists():
        print(f"❌ Arquivo {arquivo_excel} não encontrado!")
        return False
    
    print(f"📂 Lendo arquivo: {arquivo_excel}")
    
    try:
        # Lê a planilha Excel
        df = pd.read_excel(arquivo_excel)
        
        print(f"✓ Planilha carregada com sucesso!")
        print(f"  - Total de linhas: {len(df)}")
        print(f"  - Colunas encontradas: {list(df.columns)}")
        
        # Mostra primeiras linhas
        print(f"\n📊 Primeiras linhas do arquivo:")
        print(df.head())
        print(f"\n📋 Informações do DataFrame:")
        print(df.info())
        
        # Conecta ao banco SQLite
        print(f"\n💾 Criando banco de dados: {arquivo_db}")
        conn = sqlite3.connect(arquivo_db)
        
        # Remove tabela se já existir
        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS mix_produtos")
        
        # Cria tabela com os dados
        df.to_sql('mix_produtos', conn, if_exists='replace', index=False)
        
        # Cria índices para melhorar performance
        print("🔧 Criando índices...")
        
        # Tenta criar índices nas colunas mais comuns
        # (ajustar conforme as colunas reais da planilha)
        try:
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_codigo ON mix_produtos(codigo)")
        except:
            pass
        
        try:
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_produto ON mix_produtos(produto)")
        except:
            pass
        
        try:
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_categoria ON mix_produtos(categoria)")
        except:
            pass
        
        # Adiciona metadados
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS metadados (
                chave TEXT PRIMARY KEY,
                valor TEXT,
                data_atualizacao TEXT
            )
        """)
        
        cursor.execute("""
            INSERT OR REPLACE INTO metadados (chave, valor, data_atualizacao)
            VALUES (?, ?, ?)
        """, ('data_importacao', arquivo_excel.name, datetime.now().isoformat()))
        
        cursor.execute("""
            INSERT OR REPLACE INTO metadados (chave, valor, data_atualizacao)
            VALUES (?, ?, ?)
        """, ('total_produtos', str(len(df)), datetime.now().isoformat()))
        
        conn.commit()
        
        # Estatísticas
        total_registros = cursor.execute("SELECT COUNT(*) FROM mix_produtos").fetchone()[0]
        
        print(f"\n✅ Banco de dados criado com sucesso!")
        print(f"  - Arquivo: {arquivo_db}")
        print(f"  - Tabela: mix_produtos")
        print(f"  - Total de registros: {total_registros}")
        print(f"  - Colunas: {', '.join(df.columns)}")
        
        # Mostra amostra dos dados
        print(f"\n📊 Amostra dos dados no banco:")
        amostra = pd.read_sql("SELECT * FROM mix_produtos LIMIT 5", conn)
        print(amostra)
        
        conn.close()
        
        print(f"\n💡 Para consultar o banco, use:")
        print(f"   import sqlite3")
        print(f"   conn = sqlite3.connect('{arquivo_db}')")
        print(f"   cursor = conn.cursor()")
        print(f"   cursor.execute('SELECT * FROM mix_produtos LIMIT 10')")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Erro ao processar arquivo: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("="*70)
    print("  CRIAÇÃO DE BANCO DE DADOS SQLITE - MIX DE PRODUTOS")
    print("="*70)
    print()
    
    sucesso = criar_banco_dados()
    
    if sucesso:
        print("\n" + "="*70)
        print("  ✅ PROCESSO CONCLUÍDO COM SUCESSO!")
        print("="*70)
    else:
        print("\n" + "="*70)
        print("  ❌ PROCESSO CONCLUÍDO COM ERROS")
        print("="*70)
