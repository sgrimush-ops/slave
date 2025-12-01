"""
Módulo para integração com o banco de dados SQLite
"""
import sqlite3
from typing import List, Dict, Optional, Tuple
from pathlib import Path
from datetime import datetime

from .modelos import Produto


class BancoDadosMix:
    """Classe para gerenciar o banco de dados SQLite com o mix de produtos"""
    
    def __init__(self, db_path: str = "data/banco.db"):
        """
        Inicializa conexão com o banco de dados
        
        Args:
            db_path: Caminho para o arquivo do banco de dados
        """
        self.db_path = Path(db_path)
        if not self.db_path.exists():
            raise FileNotFoundError(
                f"Banco de dados não encontrado: {db_path}\n"
                f"Execute: python criar_banco.py"
            )
        
        self.conn = None
        self._conectar()
    
    def _conectar(self):
        """Estabelece conexão com o banco"""
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row  # Permite acesso por nome de coluna
    
    def _executar_query(self, query: str, params: tuple = ()) -> List[sqlite3.Row]:
        """
        Executa query e retorna resultados
        
        Args:
            query: Query SQL
            params: Parâmetros da query
            
        Returns:
            Lista de resultados
        """
        cursor = self.conn.cursor()
        cursor.execute(query, params)
        return cursor.fetchall()
    
    def obter_total_produtos(self) -> int:
        """Retorna total de produtos no banco"""
        result = self._executar_query("SELECT COUNT(*) as total FROM mix_produtos")
        return result[0]['total']
    
    def obter_produto_por_codigo_interno(self, codigo: int) -> Optional[Dict]:
        """
        Busca produto por código interno
        
        Args:
            codigo: Código interno do produto
            
        Returns:
            Dicionário com dados do produto ou None
        """
        query = "SELECT * FROM mix_produtos WHERE codigo_interno = ?"
        results = self._executar_query(query, (codigo,))
        
        if results:
            return dict(results[0])
        return None
    
    def obter_produto_por_ean(self, ean: int) -> Optional[Dict]:
        """
        Busca produto por código EAN
        
        Args:
            ean: Código EAN/código de barras
            
        Returns:
            Dicionário com dados do produto ou None
        """
        query = "SELECT * FROM mix_produtos WHERE codigo_ean = ?"
        results = self._executar_query(query, (ean,))
        
        if results:
            return dict(results[0])
        return None
    
    def buscar_produtos(
        self, 
        termo: str, 
        limite: int = 50
    ) -> List[Dict]:
        """
        Busca produtos por termo na descrição
        
        Args:
            termo: Termo de busca
            limite: Número máximo de resultados
            
        Returns:
            Lista de produtos encontrados
        """
        query = """
            SELECT * FROM mix_produtos 
            WHERE descricao LIKE ? 
            ORDER BY descricao 
            LIMIT ?
        """
        results = self._executar_query(query, (f"%{termo}%", limite))
        return [dict(row) for row in results]
    
    def obter_produtos_por_origem(self, origem: str) -> List[Dict]:
        """
        Retorna produtos de uma determinada origem/fornecedor
        
        Args:
            origem: Nome da origem/fornecedor
            
        Returns:
            Lista de produtos
        """
        query = "SELECT * FROM mix_produtos WHERE origem = ? ORDER BY descricao"
        results = self._executar_query(query, (origem,))
        return [dict(row) for row in results]
    
    def obter_produtos_por_loja(self, codigo_loja: str) -> List[Dict]:
        """
        Retorna produtos ativos para uma loja específica
        
        Args:
            codigo_loja: Código da loja (ex: '002', '003')
            
        Returns:
            Lista de produtos ativos na loja
        """
        query = """
            SELECT * FROM mix_produtos 
            WHERE loja_ativa_mix LIKE ? 
            ORDER BY descricao
        """
        # Busca o código da loja no campo loja_ativa_mix
        results = self._executar_query(query, (f"%{codigo_loja}%",))
        return [dict(row) for row in results]
    
    def obter_origens(self) -> List[str]:
        """Retorna lista de todas as origens/fornecedores"""
        query = "SELECT DISTINCT origem FROM mix_produtos ORDER BY origem"
        results = self._executar_query(query)
        return [row['origem'] for row in results]
    
    def obter_lojas_ativas(self) -> List[str]:
        """Extrai lista de códigos de lojas do campo loja_ativa_mix"""
        query = "SELECT DISTINCT loja_ativa_mix FROM mix_produtos"
        results = self._executar_query(query)
        
        # Extrai todos os códigos de loja únicos
        lojas = set()
        for row in results:
            codigos = row['loja_ativa_mix'].split('-')
            lojas.update(codigos)
        
        return sorted(list(lojas))
    
    def obter_estatisticas(self) -> Dict:
        """Retorna estatísticas do banco de dados"""
        stats = {
            'total_produtos': self.obter_total_produtos(),
            'total_origens': len(self.obter_origens()),
            'lojas_cadastradas': self.obter_lojas_ativas(),
            'origens': self.obter_origens()[:10]  # Top 10 origens
        }
        
        # Produtos por origem
        query = """
            SELECT origem, COUNT(*) as total 
            FROM mix_produtos 
            GROUP BY origem 
            ORDER BY total DESC 
            LIMIT 10
        """
        results = self._executar_query(query)
        stats['produtos_por_origem'] = [
            {'origem': row['origem'], 'total': row['total']} 
            for row in results
        ]
        
        return stats
    
    def converter_para_produto(
        self, 
        dados_mix: Dict,
        preco_custo: float = 0.0,
        preco_venda: float = 0.0
    ) -> Produto:
        """
        Converte dados do mix para objeto Produto
        
        Args:
            dados_mix: Dicionário com dados do mix_produtos
            preco_custo: Preço de custo (precisa ser fornecido)
            preco_venda: Preço de venda (precisa ser fornecido)
            
        Returns:
            Objeto Produto
        """
        # Tenta extrair categoria da descrição (primeira palavra geralmente)
        descricao = dados_mix['descricao']
        categoria = descricao.split()[0] if descricao else "Geral"
        
        produto = Produto(
            id=str(dados_mix['codigo_interno']),
            nome=dados_mix['descricao'],
            categoria=categoria,
            unidade="un",  # Padrão unidade
            preco_custo=preco_custo,
            preco_venda=preco_venda,
            peso=1.0,  # Peso padrão
            volume=0.001,  # Volume padrão
            estoque_minimo=10,  # Valores padrão - ajustar conforme necessário
            estoque_seguranca=20,
            tempo_reposicao_dias=5
        )
        
        return produto
    
    def importar_produtos_para_catalogo(
        self,
        gerenciador,
        precos: Dict[str, Tuple[float, float]] = None
    ) -> int:
        """
        Importa produtos do mix para o catálogo do gerenciador
        
        Args:
            gerenciador: Instância do GerenciadorEstoque
            precos: Dicionário {codigo_interno: (preco_custo, preco_venda)}
            
        Returns:
            Número de produtos importados
        """
        query = "SELECT * FROM mix_produtos"
        results = self._executar_query(query)
        
        importados = 0
        precos = precos or {}
        
        for row in results:
            dados = dict(row)
            codigo = str(dados['codigo_interno'])
            
            # Obtém preços ou usa valores padrão
            preco_custo, preco_venda = precos.get(codigo, (10.0, 15.0))
            
            try:
                produto = self.converter_para_produto(
                    dados, 
                    preco_custo, 
                    preco_venda
                )
                gerenciador.adicionar_produto_catalogo(produto)
                importados += 1
            except Exception as e:
                print(f"Erro ao importar produto {codigo}: {e}")
        
        return importados
    
    def listar_produtos_paginado(
        self,
        pagina: int = 1,
        itens_por_pagina: int = 50,
        origem: Optional[str] = None
    ) -> Tuple[List[Dict], int]:
        """
        Lista produtos com paginação
        
        Args:
            pagina: Número da página (começa em 1)
            itens_por_pagina: Itens por página
            origem: Filtro por origem (opcional)
            
        Returns:
            Tupla (lista de produtos, total de páginas)
        """
        offset = (pagina - 1) * itens_por_pagina
        
        if origem:
            query = """
                SELECT * FROM mix_produtos 
                WHERE origem = ?
                ORDER BY descricao 
                LIMIT ? OFFSET ?
            """
            results = self._executar_query(query, (origem, itens_por_pagina, offset))
            
            count_query = "SELECT COUNT(*) as total FROM mix_produtos WHERE origem = ?"
            total = self._executar_query(count_query, (origem,))[0]['total']
        else:
            query = """
                SELECT * FROM mix_produtos 
                ORDER BY descricao 
                LIMIT ? OFFSET ?
            """
            results = self._executar_query(query, (itens_por_pagina, offset))
            
            total = self.obter_total_produtos()
        
        total_paginas = (total + itens_por_pagina - 1) // itens_por_pagina
        
        return [dict(row) for row in results], total_paginas
    
    def fechar(self):
        """Fecha conexão com o banco"""
        if self.conn:
            self.conn.close()
    
    def __enter__(self):
        """Suporte para context manager"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Suporte para context manager"""
        self.fechar()
