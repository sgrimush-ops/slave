"""
Gerenciador central do sistema de estoque
"""
from typing import Dict, List, Optional
from datetime import datetime
import json
from pathlib import Path

from .modelos import (
    Produto, Loja, CentroDistribuicao, ItemEstoque, 
    Movimentacao, TipoMovimentacao, VendaDiaria
)


class GerenciadorEstoque:
    """Classe central para gerenciar todo o sistema de estoque"""
    
    def __init__(self, data_dir: str = "data"):
        """
        Inicializa o gerenciador
        
        Args:
            data_dir: Diretório para armazenar dados
        """
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        
        self.catalogo_produtos: Dict[str, Produto] = {}
        self.lojas: Dict[str, Loja] = {}
        self.centros_distribuicao: Dict[str, CentroDistribuicao] = {}
        self.historico_vendas: List[VendaDiaria] = []
        
        self.carregar_dados()
    
    def adicionar_produto_catalogo(self, produto: Produto):
        """Adiciona produto ao catálogo"""
        self.catalogo_produtos[produto.id] = produto
        self.salvar_produtos()
    
    def adicionar_loja(self, loja: Loja):
        """Adiciona uma loja ao sistema"""
        self.lojas[loja.id] = loja
        self.salvar_lojas()
    
    def adicionar_centro_distribuicao(self, cd: CentroDistribuicao):
        """Adiciona um centro de distribuição"""
        self.centros_distribuicao[cd.id] = cd
        self.salvar_centros()
    
    def adicionar_estoque_loja(
        self, 
        loja_id: str, 
        produto_id: str, 
        quantidade: int
    ) -> Dict:
        """
        Adiciona estoque a uma loja
        
        Args:
            loja_id: ID da loja
            produto_id: ID do produto
            quantidade: Quantidade a adicionar
            
        Returns:
            Dicionário com resultado da operação
        """
        loja = self.lojas.get(loja_id)
        if not loja:
            return {"sucesso": False, "mensagem": "Loja não encontrada"}
        
        produto = self.catalogo_produtos.get(produto_id)
        if not produto:
            return {"sucesso": False, "mensagem": "Produto não encontrado"}
        
        # Verifica se produto já existe no estoque
        item = loja.obter_produto(produto_id)
        if item:
            item.quantidade_atual += quantidade
        else:
            item = ItemEstoque(produto=produto, quantidade_atual=quantidade)
            loja.adicionar_produto(item)
        
        # Registra movimentação
        movimentacao = Movimentacao(
            id=f"mov_{datetime.now().timestamp()}",
            produto_id=produto_id,
            tipo=TipoMovimentacao.ENTRADA,
            quantidade=quantidade,
            data=datetime.now(),
            destino=loja_id,
            observacao="Entrada manual"
        )
        item.adicionar_movimentacao(movimentacao)
        
        self.salvar_lojas()
        
        return {
            "sucesso": True,
            "mensagem": f"Adicionado {quantidade} unidades de {produto.nome}",
            "estoque_atual": item.quantidade_atual
        }
    
    def adicionar_estoque_cd(
        self, 
        cd_id: str, 
        produto_id: str, 
        quantidade: int
    ) -> Dict:
        """Adiciona estoque a um CD"""
        cd = self.centros_distribuicao.get(cd_id)
        if not cd:
            return {"sucesso": False, "mensagem": "CD não encontrado"}
        
        produto = self.catalogo_produtos.get(produto_id)
        if not produto:
            return {"sucesso": False, "mensagem": "Produto não encontrado"}
        
        item = cd.obter_produto(produto_id)
        if item:
            item.quantidade_atual += quantidade
        else:
            item = ItemEstoque(produto=produto, quantidade_atual=quantidade)
            cd.adicionar_produto(item)
        
        movimentacao = Movimentacao(
            id=f"mov_{datetime.now().timestamp()}",
            produto_id=produto_id,
            tipo=TipoMovimentacao.ENTRADA,
            quantidade=quantidade,
            data=datetime.now(),
            destino=cd_id,
            observacao="Entrada no CD"
        )
        item.adicionar_movimentacao(movimentacao)
        
        self.salvar_centros()
        
        return {
            "sucesso": True,
            "mensagem": f"Adicionado {quantidade} unidades ao CD",
            "estoque_atual": item.quantidade_atual
        }
    
    def transferir_para_loja(
        self,
        cd_id: str,
        loja_id: str,
        produto_id: str,
        quantidade: int,
        observacao: str = ""
    ) -> Dict:
        """
        Transfere produtos do CD para uma loja
        
        Args:
            cd_id: ID do centro de distribuição
            loja_id: ID da loja destino
            produto_id: ID do produto
            quantidade: Quantidade a transferir
            observacao: Observação da transferência
            
        Returns:
            Dicionário com resultado da operação
        """
        cd = self.centros_distribuicao.get(cd_id)
        if not cd:
            return {"sucesso": False, "mensagem": "CD não encontrado"}
        
        loja = self.lojas.get(loja_id)
        if not loja:
            return {"sucesso": False, "mensagem": "Loja não encontrada"}
        
        produto = self.catalogo_produtos.get(produto_id)
        if not produto:
            return {"sucesso": False, "mensagem": "Produto não encontrado"}
        
        # Verifica disponibilidade no CD
        item_cd = cd.obter_produto(produto_id)
        if not item_cd or item_cd.quantidade_disponivel < quantidade:
            return {
                "sucesso": False,
                "mensagem": f"Estoque insuficiente no CD. Disponível: {item_cd.quantidade_disponivel if item_cd else 0}"
            }
        
        # Remove do CD
        item_cd.quantidade_atual -= quantidade
        mov_saida = Movimentacao(
            id=f"mov_{datetime.now().timestamp()}_saida",
            produto_id=produto_id,
            tipo=TipoMovimentacao.TRANSFERENCIA,
            quantidade=quantidade,
            data=datetime.now(),
            origem=cd_id,
            destino=loja_id,
            observacao=observacao
        )
        item_cd.adicionar_movimentacao(mov_saida)
        
        # Adiciona na loja
        item_loja = loja.obter_produto(produto_id)
        if item_loja:
            item_loja.quantidade_atual += quantidade
        else:
            item_loja = ItemEstoque(produto=produto, quantidade_atual=quantidade)
            loja.adicionar_produto(item_loja)
        
        mov_entrada = Movimentacao(
            id=f"mov_{datetime.now().timestamp()}_entrada",
            produto_id=produto_id,
            tipo=TipoMovimentacao.TRANSFERENCIA,
            quantidade=quantidade,
            data=datetime.now(),
            origem=cd_id,
            destino=loja_id,
            observacao=observacao
        )
        item_loja.adicionar_movimentacao(mov_entrada)
        
        self.salvar_centros()
        self.salvar_lojas()
        
        return {
            "sucesso": True,
            "mensagem": f"Transferido {quantidade} unidades de {produto.nome} para {loja.nome}",
            "estoque_cd": item_cd.quantidade_atual,
            "estoque_loja": item_loja.quantidade_atual
        }
    
    def registrar_venda(
        self,
        loja_id: str,
        produto_id: str,
        quantidade: int
    ) -> Dict:
        """Registra uma venda"""
        loja = self.lojas.get(loja_id)
        if not loja:
            return {"sucesso": False, "mensagem": "Loja não encontrada"}
        
        item = loja.obter_produto(produto_id)
        if not item:
            return {"sucesso": False, "mensagem": "Produto não encontrado na loja"}
        
        if item.quantidade_disponivel < quantidade:
            return {
                "sucesso": False,
                "mensagem": f"Estoque insuficiente. Disponível: {item.quantidade_disponivel}"
            }
        
        # Remove do estoque
        item.quantidade_atual -= quantidade
        
        # Registra movimentação
        movimentacao = Movimentacao(
            id=f"mov_{datetime.now().timestamp()}",
            produto_id=produto_id,
            tipo=TipoMovimentacao.SAIDA,
            quantidade=quantidade,
            data=datetime.now(),
            origem=loja_id,
            observacao="Venda"
        )
        item.adicionar_movimentacao(movimentacao)
        
        # Registra venda no histórico
        venda = VendaDiaria(
            produto_id=produto_id,
            loja_id=loja_id,
            data=datetime.now(),
            quantidade_vendida=quantidade,
            receita=quantidade * item.produto.preco_venda
        )
        self.historico_vendas.append(venda)
        
        self.salvar_lojas()
        self.salvar_vendas()
        
        return {
            "sucesso": True,
            "mensagem": f"Venda registrada: {quantidade} unidades",
            "estoque_restante": item.quantidade_atual,
            "receita": venda.receita
        }
    
    # Métodos de persistência
    
    def salvar_produtos(self):
        """Salva catálogo de produtos"""
        arquivo = self.data_dir / "produtos.json"
        dados = [
            {
                "id": p.id,
                "nome": p.nome,
                "categoria": p.categoria,
                "unidade": p.unidade,
                "preco_custo": p.preco_custo,
                "preco_venda": p.preco_venda,
                "peso": p.peso,
                "volume": p.volume,
                "estoque_minimo": p.estoque_minimo,
                "estoque_seguranca": p.estoque_seguranca,
                "tempo_reposicao_dias": p.tempo_reposicao_dias
            }
            for p in self.catalogo_produtos.values()
        ]
        arquivo.write_text(json.dumps(dados, indent=2, ensure_ascii=False))
    
    def salvar_lojas(self):
        """Salva dados das lojas"""
        arquivo = self.data_dir / "lojas.json"
        dados = []
        for loja in self.lojas.values():
            dados.append({
                "id": loja.id,
                "nome": loja.nome,
                "endereco": loja.endereco,
                "capacidade_m3": loja.capacidade_m3,
                "ativa": loja.ativa,
                "estoque": [
                    {
                        "produto_id": item.produto.id,
                        "quantidade_atual": item.quantidade_atual,
                        "quantidade_reservada": item.quantidade_reservada
                    }
                    for item in loja.estoque.values()
                ]
            })
        arquivo.write_text(json.dumps(dados, indent=2, ensure_ascii=False))
    
    def salvar_centros(self):
        """Salva dados dos centros de distribuição"""
        arquivo = self.data_dir / "centros.json"
        dados = []
        for cd in self.centros_distribuicao.values():
            dados.append({
                "id": cd.id,
                "nome": cd.nome,
                "endereco": cd.endereco,
                "capacidade_m3": cd.capacidade_m3,
                "lojas_atendidas": cd.lojas_atendidas,
                "estoque": [
                    {
                        "produto_id": item.produto.id,
                        "quantidade_atual": item.quantidade_atual,
                        "quantidade_reservada": item.quantidade_reservada
                    }
                    for item in cd.estoque.values()
                ]
            })
        arquivo.write_text(json.dumps(dados, indent=2, ensure_ascii=False))
    
    def salvar_vendas(self):
        """Salva histórico de vendas"""
        arquivo = self.data_dir / "vendas.json"
        dados = [
            {
                "produto_id": v.produto_id,
                "loja_id": v.loja_id,
                "data": v.data.isoformat(),
                "quantidade_vendida": v.quantidade_vendida,
                "receita": v.receita
            }
            for v in self.historico_vendas
        ]
        arquivo.write_text(json.dumps(dados, indent=2, ensure_ascii=False))
    
    def carregar_dados(self):
        """Carrega dados salvos"""
        # Carrega produtos
        arquivo_produtos = self.data_dir / "produtos.json"
        if arquivo_produtos.exists():
            dados = json.loads(arquivo_produtos.read_text())
            for d in dados:
                produto = Produto(**d)
                self.catalogo_produtos[produto.id] = produto
        
        # Carrega lojas (simplificado - em produção, carregar estoque completo)
        arquivo_lojas = self.data_dir / "lojas.json"
        if arquivo_lojas.exists():
            dados = json.loads(arquivo_lojas.read_text())
            for d in dados:
                estoque_data = d.pop("estoque", [])
                loja = Loja(**d)
                
                # Reconstrói estoque
                for item_data in estoque_data:
                    produto = self.catalogo_produtos.get(item_data["produto_id"])
                    if produto:
                        item = ItemEstoque(
                            produto=produto,
                            quantidade_atual=item_data["quantidade_atual"],
                            quantidade_reservada=item_data.get("quantidade_reservada", 0)
                        )
                        loja.adicionar_produto(item)
                
                self.lojas[loja.id] = loja
        
        # Carrega centros de distribuição
        arquivo_centros = self.data_dir / "centros.json"
        if arquivo_centros.exists():
            dados = json.loads(arquivo_centros.read_text())
            for d in dados:
                estoque_data = d.pop("estoque", [])
                cd = CentroDistribuicao(**d)
                
                for item_data in estoque_data:
                    produto = self.catalogo_produtos.get(item_data["produto_id"])
                    if produto:
                        item = ItemEstoque(
                            produto=produto,
                            quantidade_atual=item_data["quantidade_atual"],
                            quantidade_reservada=item_data.get("quantidade_reservada", 0)
                        )
                        cd.adicionar_produto(item)
                
                self.centros_distribuicao[cd.id] = cd
