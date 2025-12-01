"""
Sistema de análise de estoque e geração de alertas
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
from collections import defaultdict

from .modelos import Loja, CentroDistribuicao, ItemEstoque, VendaDiaria, Produto


class AnalisadorEstoque:
    """Classe para análise de estoque e geração de métricas"""
    
    def __init__(self):
        self.alertas = []
    
    def calcular_giro_estoque(
        self, 
        item: ItemEstoque, 
        vendas_periodo: List[VendaDiaria],
        dias: int = 30
    ) -> float:
        """
        Calcula o giro de estoque (quantas vezes o estoque é renovado)
        
        Args:
            item: Item de estoque
            vendas_periodo: Vendas do período
            dias: Período de análise
            
        Returns:
            Giro de estoque
        """
        total_vendido = sum(v.quantidade_vendida for v in vendas_periodo)
        estoque_medio = item.quantidade_atual  # Simplificado
        
        if estoque_medio == 0:
            return 0
        
        # Giro = Vendas / Estoque Médio
        giro = total_vendido / estoque_medio
        return round(giro, 2)
    
    def calcular_cobertura_estoque(
        self,
        item: ItemEstoque,
        vendas_periodo: List[VendaDiaria],
        dias: int = 30
    ) -> float:
        """
        Calcula por quantos dias o estoque atual é suficiente
        
        Args:
            item: Item de estoque
            vendas_periodo: Vendas do período
            dias: Período de análise
            
        Returns:
            Dias de cobertura
        """
        if not vendas_periodo:
            return 0
        
        total_vendido = sum(v.quantidade_vendida for v in vendas_periodo)
        media_diaria = total_vendido / dias
        
        if media_diaria == 0:
            return float('inf')
        
        cobertura = item.quantidade_atual / media_diaria
        return round(cobertura, 1)
    
    def calcular_ponto_pedido(
        self,
        item: ItemEstoque,
        vendas_periodo: List[VendaDiaria],
        dias: int = 30
    ) -> int:
        """
        Calcula o ponto de pedido (quando fazer nova reposição)
        PP = (Demanda média diária × Tempo de reposição) + Estoque de segurança
        
        Args:
            item: Item de estoque
            vendas_periodo: Vendas do período
            dias: Período de análise
            
        Returns:
            Quantidade do ponto de pedido
        """
        if not vendas_periodo:
            return item.produto.estoque_minimo
        
        total_vendido = sum(v.quantidade_vendida for v in vendas_periodo)
        demanda_media_diaria = total_vendido / dias
        
        tempo_reposicao = item.produto.tempo_reposicao_dias
        estoque_seguranca = item.produto.estoque_seguranca
        
        ponto_pedido = (demanda_media_diaria * tempo_reposicao) + estoque_seguranca
        return int(np.ceil(ponto_pedido))
    
    def calcular_lote_economico(
        self,
        produto: Produto,
        demanda_anual: int,
        custo_pedido: float = 50.0,
        taxa_armazenagem: float = 0.2
    ) -> int:
        """
        Calcula o Lote Econômico de Compra (LEC)
        LEC = √(2 × D × S / H)
        onde: D = demanda anual, S = custo por pedido, H = custo de manter estoque
        
        Args:
            produto: Produto
            demanda_anual: Demanda anual estimada
            custo_pedido: Custo fixo por pedido
            taxa_armazenagem: Taxa de custo de armazenagem (% do valor)
            
        Returns:
            Quantidade do lote econômico
        """
        if demanda_anual == 0:
            return produto.estoque_minimo
        
        custo_manutencao = produto.preco_custo * taxa_armazenagem
        
        if custo_manutencao == 0:
            return produto.estoque_minimo
        
        lec = np.sqrt((2 * demanda_anual * custo_pedido) / custo_manutencao)
        return int(np.ceil(lec))
    
    def prever_demanda_simples(
        self,
        vendas_periodo: List[VendaDiaria],
        dias_previsao: int = 7
    ) -> Dict[str, float]:
        """
        Previsão de demanda usando média móvel simples
        
        Args:
            vendas_periodo: Histórico de vendas
            dias_previsao: Dias para prever
            
        Returns:
            Dicionário com previsões
        """
        if not vendas_periodo:
            return {"previsao": 0, "min": 0, "max": 0}
        
        # Agrupa vendas por dia
        vendas_por_dia = defaultdict(int)
        for venda in vendas_periodo:
            data_str = venda.data.strftime("%Y-%m-%d")
            vendas_por_dia[data_str] += venda.quantidade_vendida
        
        quantidades = list(vendas_por_dia.values())
        
        # Média móvel simples
        media = np.mean(quantidades)
        desvio = np.std(quantidades)
        
        previsao_total = media * dias_previsao
        
        return {
            "previsao_total": round(previsao_total, 1),
            "media_diaria": round(media, 1),
            "previsao_min": round((media - desvio) * dias_previsao, 1),
            "previsao_max": round((media + desvio) * dias_previsao, 1),
            "confianca": "baixa" if len(quantidades) < 7 else "média" if len(quantidades) < 30 else "alta"
        }
    
    def analisar_tendencia(
        self,
        vendas_periodo: List[VendaDiaria]
    ) -> Dict[str, any]:
        """
        Analisa tendência de vendas (crescimento, estável, queda)
        
        Args:
            vendas_periodo: Histórico de vendas
            
        Returns:
            Dicionário com análise de tendência
        """
        if len(vendas_periodo) < 7:
            return {"tendencia": "dados_insuficientes", "percentual": 0}
        
        # Ordena por data
        vendas_ordenadas = sorted(vendas_periodo, key=lambda x: x.data)
        
        # Divide em duas metades
        meio = len(vendas_ordenadas) // 2
        primeira_metade = vendas_ordenadas[:meio]
        segunda_metade = vendas_ordenadas[meio:]
        
        media_primeira = np.mean([v.quantidade_vendida for v in primeira_metade])
        media_segunda = np.mean([v.quantidade_vendida for v in segunda_metade])
        
        if media_primeira == 0:
            return {"tendencia": "indefinida", "percentual": 0}
        
        variacao_percentual = ((media_segunda - media_primeira) / media_primeira) * 100
        
        if variacao_percentual > 10:
            tendencia = "crescimento"
        elif variacao_percentual < -10:
            tendencia = "queda"
        else:
            tendencia = "estável"
        
        return {
            "tendencia": tendencia,
            "percentual": round(variacao_percentual, 1),
            "media_inicial": round(media_primeira, 1),
            "media_recente": round(media_segunda, 1)
        }
    
    def gerar_alertas_loja(
        self,
        loja: Loja,
        cd: CentroDistribuicao,
        vendas: Dict[str, List[VendaDiaria]] = None
    ) -> List[Dict]:
        """
        Gera alertas para uma loja
        
        Args:
            loja: Loja a ser analisada
            cd: Centro de distribuição
            vendas: Histórico de vendas por produto
            
        Returns:
            Lista de alertas
        """
        alertas = []
        vendas = vendas or {}
        
        for produto_id, item in loja.estoque.items():
            # Alerta de estoque crítico
            if item.status == "CRÍTICO":
                item_cd = cd.obter_produto(produto_id)
                disponivel_cd = item_cd.quantidade_disponivel if item_cd else 0
                
                alertas.append({
                    "tipo": "ESTOQUE_CRITICO",
                    "prioridade": "ALTA",
                    "loja": loja.nome,
                    "produto": item.produto.nome,
                    "estoque_atual": item.quantidade_atual,
                    "estoque_minimo": item.produto.estoque_minimo,
                    "disponivel_cd": disponivel_cd,
                    "mensagem": f"Estoque crítico de {item.produto.nome}: apenas {item.quantidade_atual} unidades"
                })
            
            # Alerta de produto esgotado
            if item.quantidade_atual == 0:
                alertas.append({
                    "tipo": "ESTOQUE_ESGOTADO",
                    "prioridade": "URGENTE",
                    "loja": loja.nome,
                    "produto": item.produto.nome,
                    "mensagem": f"Produto {item.produto.nome} ESGOTADO na loja"
                })
            
            # Alerta baseado em vendas
            if produto_id in vendas and vendas[produto_id]:
                cobertura = self.calcular_cobertura_estoque(item, vendas[produto_id])
                
                if cobertura < item.produto.tempo_reposicao_dias:
                    alertas.append({
                        "tipo": "COBERTURA_INSUFICIENTE",
                        "prioridade": "ALTA",
                        "loja": loja.nome,
                        "produto": item.produto.nome,
                        "dias_cobertura": cobertura,
                        "tempo_reposicao": item.produto.tempo_reposicao_dias,
                        "mensagem": f"Cobertura de apenas {cobertura} dias para {item.produto.nome}"
                    })
        
        # Alerta de capacidade
        ocupacao = loja.calcular_ocupacao_volume()
        if ocupacao > 90:
            alertas.append({
                "tipo": "CAPACIDADE_ALTA",
                "prioridade": "MÉDIA",
                "loja": loja.nome,
                "ocupacao": ocupacao,
                "mensagem": f"Loja com {ocupacao:.1f}% de ocupação - próximo do limite"
            })
        
        self.alertas.extend(alertas)
        return alertas
    
    def relatorio_detalhado(
        self,
        loja: Loja,
        vendas: Dict[str, List[VendaDiaria]],
        dias: int = 30
    ) -> Dict:
        """
        Gera relatório detalhado de uma loja
        
        Args:
            loja: Loja para análise
            vendas: Histórico de vendas por produto
            dias: Período de análise
            
        Returns:
            Relatório completo
        """
        relatorio = {
            "loja": loja.nome,
            "data_relatorio": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "periodo_analise": f"{dias} dias",
            "resumo": {
                "total_produtos": len(loja.estoque),
                "produtos_criticos": len(loja.listar_produtos_criticos()),
                "ocupacao_volume": round(loja.calcular_ocupacao_volume(), 2)
            },
            "produtos": []
        }
        
        for produto_id, item in loja.estoque.items():
            info_produto = {
                "nome": item.produto.nome,
                "estoque_atual": item.quantidade_atual,
                "status": item.status
            }
            
            if produto_id in vendas and vendas[produto_id]:
                vendas_produto = vendas[produto_id]
                info_produto.update({
                    "giro": self.calcular_giro_estoque(item, vendas_produto, dias),
                    "cobertura_dias": self.calcular_cobertura_estoque(item, vendas_produto, dias),
                    "ponto_pedido": self.calcular_ponto_pedido(item, vendas_produto, dias),
                    "previsao_7dias": self.prever_demanda_simples(vendas_produto, 7),
                    "tendencia": self.analisar_tendencia(vendas_produto)
                })
            
            relatorio["produtos"].append(info_produto)
        
        return relatorio
