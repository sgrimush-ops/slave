"""
Modelos de dados para o sistema de gestão de estoque
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Optional
from enum import Enum


class TipoMovimentacao(Enum):
    """Tipos de movimentação de estoque"""
    ENTRADA = "entrada"
    SAIDA = "saida"
    TRANSFERENCIA = "transferencia"
    AJUSTE = "ajuste"
    DEVOLUCAO = "devolucao"


@dataclass
class Produto:
    """Representa um produto no catálogo"""
    id: str
    nome: str
    categoria: str
    unidade: str  # kg, un, cx, etc
    preco_custo: float
    preco_venda: float
    peso: float = 0.0  # em kg
    volume: float = 0.0  # em m³
    estoque_minimo: int = 10
    estoque_seguranca: int = 20
    tempo_reposicao_dias: int = 7
    # Valores definidos pelo comprador para exposição visual
    ponto_pedido: Optional[int] = None  # Mínimo para disparar pedido automático
    estoque_ideal: Optional[int] = None  # Máximo desejado para exposição bonita
    
    def __str__(self):
        return f"{self.nome} (ID: {self.id})"


@dataclass
class Movimentacao:
    """Registro de movimentação de estoque"""
    id: str
    produto_id: str
    tipo: TipoMovimentacao
    quantidade: int
    data: datetime
    origem: Optional[str] = None
    destino: Optional[str] = None
    observacao: str = ""
    usuario: str = "sistema"
    
    def __post_init__(self):
        if isinstance(self.tipo, str):
            self.tipo = TipoMovimentacao(self.tipo)


@dataclass
class ItemEstoque:
    """Item de estoque com informações detalhadas"""
    produto: Produto
    quantidade_atual: int
    quantidade_reservada: int = 0
    ultima_atualizacao: datetime = field(default_factory=datetime.now)
    historico_movimentacoes: List[Movimentacao] = field(default_factory=list)
    
    @property
    def quantidade_disponivel(self) -> int:
        """Quantidade disponível para venda/transferência"""
        return max(0, self.quantidade_atual - self.quantidade_reservada)
    
    @property
    def precisa_reposicao(self) -> bool:
        """Verifica se precisa reposição"""
        return self.quantidade_atual <= self.produto.estoque_minimo
    
    @property
    def status(self) -> str:
        """Status do estoque"""
        if self.quantidade_atual == 0:
            return "ESGOTADO"
        elif self.quantidade_atual <= self.produto.estoque_minimo:
            return "CRÍTICO"
        elif self.quantidade_atual <= self.produto.estoque_seguranca:
            return "BAIXO"
        else:
            return "NORMAL"
    
    def adicionar_movimentacao(self, movimentacao: Movimentacao):
        """Registra uma movimentação"""
        self.historico_movimentacoes.append(movimentacao)
        self.ultima_atualizacao = datetime.now()


@dataclass
class Loja:
    """Representa uma loja"""
    id: str
    nome: str
    endereco: str
    capacidade_m3: float
    estoque: Dict[str, ItemEstoque] = field(default_factory=dict)
    ativa: bool = True
    
    def adicionar_produto(self, item: ItemEstoque):
        """Adiciona um produto ao estoque da loja"""
        self.estoque[item.produto.id] = item
    
    def obter_produto(self, produto_id: str) -> Optional[ItemEstoque]:
        """Obtém um item do estoque"""
        return self.estoque.get(produto_id)
    
    def listar_produtos_criticos(self) -> List[ItemEstoque]:
        """Lista produtos com estoque crítico"""
        return [item for item in self.estoque.values() 
                if item.precisa_reposicao]
    
    def calcular_ocupacao_volume(self) -> float:
        """Calcula percentual de ocupação por volume"""
        volume_ocupado = sum(
            item.quantidade_atual * item.produto.volume 
            for item in self.estoque.values()
        )
        return (volume_ocupado / self.capacidade_m3) * 100 if self.capacidade_m3 > 0 else 0
    
    def __str__(self):
        return f"Loja {self.nome} (ID: {self.id})"


@dataclass
class CentroDistribuicao:
    """Representa um centro de distribuição"""
    id: str
    nome: str
    endereco: str
    capacidade_m3: float
    estoque: Dict[str, ItemEstoque] = field(default_factory=dict)
    lojas_atendidas: List[str] = field(default_factory=list)
    
    def adicionar_produto(self, item: ItemEstoque):
        """Adiciona um produto ao estoque do CD"""
        self.estoque[item.produto.id] = item
    
    def obter_produto(self, produto_id: str) -> Optional[ItemEstoque]:
        """Obtém um item do estoque"""
        return self.estoque.get(produto_id)
    
    def verificar_disponibilidade(self, produto_id: str, quantidade: int) -> bool:
        """Verifica se há quantidade disponível para transferência"""
        item = self.obter_produto(produto_id)
        if not item:
            return False
        return item.quantidade_disponivel >= quantidade
    
    def calcular_ocupacao_volume(self) -> float:
        """Calcula percentual de ocupação por volume"""
        volume_ocupado = sum(
            item.quantidade_atual * item.produto.volume 
            for item in self.estoque.values()
        )
        return (volume_ocupado / self.capacidade_m3) * 100 if self.capacidade_m3 > 0 else 0
    
    def relatorio_geral(self) -> Dict:
        """Gera relatório geral do CD"""
        return {
            "nome": self.nome,
            "total_produtos": len(self.estoque),
            "ocupacao_percentual": round(self.calcular_ocupacao_volume(), 2),
            "lojas_atendidas": len(self.lojas_atendidas),
            "produtos_criticos": len([i for i in self.estoque.values() if i.precisa_reposicao])
        }
    
    def __str__(self):
        return f"CD {self.nome} (ID: {self.id})"


@dataclass
class VendaDiaria:
    """Registro de vendas diárias por produto"""
    produto_id: str
    loja_id: str
    data: datetime
    quantidade_vendida: int
    receita: float
    
    def __post_init__(self):
        if isinstance(self.data, str):
            self.data = datetime.fromisoformat(self.data)
