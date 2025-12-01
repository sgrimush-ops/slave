"""
Módulo de análise de histórico de vendas usando banco Parquet
"""
import pandas as pd
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple


class AnalisadorHistorico:
    """
    Analisa histórico de vendas para fornecer insights ao agente IA
    """
    
    def __init__(self, arquivo_parquet: str = 'data/vendas_historico.parquet'):
        """
        Inicializa o analisador
        
        Args:
            arquivo_parquet: Caminho do arquivo Parquet com histórico
        """
        self.arquivo_parquet = arquivo_parquet
        self.df = None
        self._carregar_dados()
    
    def _carregar_dados(self):
        """Carrega dados do arquivo Parquet"""
        if os.path.exists(self.arquivo_parquet):
            self.df = pd.read_parquet(self.arquivo_parquet)
            print(f"[OK] Historico carregado: {len(self.df):,} registros")
        else:
            print(f"[AVISO] Arquivo {self.arquivo_parquet} nao encontrado")
            self.df = None
    
    def recarregar(self):
        """Recarrega dados do arquivo (útil após atualizações)"""
        self._carregar_dados()
    
    def consultar_produto(self, codigo_interno) -> pd.DataFrame:
        """
        Consulta todos os dados históricos de um produto
        
        Args:
            codigo_interno: Código do produto (int ou str, será padronizado)
            
        Returns:
            DataFrame com histórico do produto (vazio se não encontrado)
        """
        if self.df is None or len(self.df) == 0:
            return pd.DataFrame()
        
        # Normalizar código para string com padding de zeros (7 dígitos)
        codigo_padrao = str(codigo_interno).zfill(7)
        
        df_produto = self.df[self.df['codigo_interno'] == codigo_padrao].copy()
        
        # Ordenar por data para facilitar análise
        if not df_produto.empty:
            df_produto = df_produto.sort_values('data_venda')
        
        return df_produto
    
    def obter_estatisticas_gerais(self) -> Dict:
        """
        Retorna estatísticas gerais do histórico
        
        Returns:
            Dicionário com estatísticas
        """
        if self.df is None or len(self.df) == 0:
            return {"erro": "Sem dados disponíveis"}
        
        return {
            "total_registros": len(self.df),
            "datas_disponiveis": sorted(self.df['data_venda'].unique().tolist()),
            "periodo": {
                "inicio": self.df['data_venda'].min(),
                "fim": self.df['data_venda'].max()
            },
            "lojas": self.df['loja'].nunique(),
            "produtos_unicos": self.df['codigo_interno'].nunique(),
            "total_quantidade_vendida": float(self.df['quantidade_vendida'].sum()),
            "secoes": self.df['secao'].unique().tolist()
        }
    
    def calcular_media_vendas_produto(
        self,
        codigo_interno: int,
        loja: Optional[int] = None,
        dias: Optional[int] = None
    ) -> Dict:
        """
        Calcula média de vendas de um produto
        
        Args:
            codigo_interno: Código do produto
            loja: Filtrar por loja específica (opcional)
            dias: Considerar apenas últimos N dias (opcional)
            
        Returns:
            Dicionário com média e estatísticas
        """
        if self.df is None:
            return {"erro": "Sem dados disponíveis"}
        
        # Filtrar produto
        df_filtrado = self.df[self.df['codigo_interno'] == codigo_interno].copy()
        
        if len(df_filtrado) == 0:
            return {
                "erro": "Produto não encontrado no histórico",
                "codigo_interno": codigo_interno
            }
        
        # Filtrar por loja se especificado
        if loja is not None:
            df_filtrado = df_filtrado[df_filtrado['loja'] == loja]
            if len(df_filtrado) == 0:
                return {
                    "erro": "Produto não encontrado para esta loja",
                    "codigo_interno": codigo_interno,
                    "loja": loja
                }
        
        # Filtrar por período se especificado
        if dias is not None:
            datas_disponiveis = sorted(df_filtrado['data_venda'].unique())
            datas_recentes = datas_disponiveis[-dias:] if len(datas_disponiveis) >= dias else datas_disponiveis
            df_filtrado = df_filtrado[df_filtrado['data_venda'].isin(datas_recentes)]
        
        # Calcular estatísticas
        vendas_por_dia = df_filtrado.groupby('data_venda')['quantidade_vendida'].sum()
        
        resultado = {
            "codigo_interno": codigo_interno,
            "descricao": df_filtrado['descricao'].iloc[0],
            "secao": df_filtrado['secao'].iloc[0],
            "loja": loja if loja else "todas",
            "periodo_analisado": {
                "inicio": df_filtrado['data_venda'].min(),
                "fim": df_filtrado['data_venda'].max(),
                "dias_com_dados": len(vendas_por_dia)
            },
            "vendas": {
                "media_dia": float(vendas_por_dia.mean()),
                "total": float(df_filtrado['quantidade_vendida'].sum()),
                "minima_dia": float(vendas_por_dia.min()),
                "maxima_dia": float(vendas_por_dia.max()),
                "desvio_padrao": float(vendas_por_dia.std())
            },
            "detalhes_por_dia": vendas_por_dia.to_dict()
        }
        
        return resultado
    
    def calcular_cobertura_necessaria(
        self,
        codigo_interno: int,
        loja: int,
        estoque_atual: float,
        dias_cobertura: int = 4
    ) -> Dict:
        """
        Calcula quantidade necessária para cobertura baseado em histórico
        
        Args:
            codigo_interno: Código do produto
            loja: Loja
            estoque_atual: Estoque disponível atualmente
            dias_cobertura: Dias de cobertura desejados
            
        Returns:
            Dicionário com análise de cobertura
        """
        media_vendas = self.calcular_media_vendas_produto(codigo_interno, loja)
        
        if "erro" in media_vendas:
            return media_vendas
        
        media_dia = media_vendas['vendas']['media_dia']
        
        # Calcular necessidade
        necessidade_total = media_dia * dias_cobertura
        necessidade_pedido = max(0, necessidade_total - estoque_atual)
        
        # Cobertura atual
        cobertura_atual = estoque_atual / media_dia if media_dia > 0 else 999
        
        return {
            "codigo_interno": codigo_interno,
            "descricao": media_vendas['descricao'],
            "loja": loja,
            "estoque_atual": estoque_atual,
            "media_vendas_dia": round(media_dia, 2),
            "dias_cobertura_desejados": dias_cobertura,
            "dias_cobertura_atual": round(cobertura_atual, 2),
            "necessidade": {
                "total_para_cobertura": round(necessidade_total, 2),
                "quantidade_pedir": round(necessidade_pedido, 2)
            },
            "status": self._classificar_cobertura(cobertura_atual)
        }
    
    def _classificar_cobertura(self, dias: float) -> str:
        """Classifica status de cobertura"""
        if dias < 2:
            return "CRITICO"
        elif dias < 4:
            return "BAIXO"
        elif dias <= 6:
            return "IDEAL"
        elif dias <= 10:
            return "ALTO"
        else:
            return "EXCESSO"
    
    def analisar_tendencia_produto(
        self,
        codigo_interno: int,
        loja: Optional[int] = None
    ) -> Dict:
        """
        Analisa tendência de vendas de um produto
        
        Args:
            codigo_interno: Código do produto
            loja: Loja específica (opcional)
            
        Returns:
            Análise de tendência
        """
        media = self.calcular_media_vendas_produto(codigo_interno, loja)
        
        if "erro" in media:
            return media
        
        # Comparar primeiros 50% com últimos 50%
        vendas_por_dia = media['detalhes_por_dia']
        datas = sorted(vendas_por_dia.keys())
        
        if len(datas) < 2:
            return {
                "erro": "Dados insuficientes para análise de tendência",
                "codigo_interno": codigo_interno
            }
        
        meio = len(datas) // 2
        primeira_metade = [vendas_por_dia[d] for d in datas[:meio]]
        segunda_metade = [vendas_por_dia[d] for d in datas[meio:]]
        
        media_primeira = sum(primeira_metade) / len(primeira_metade)
        media_segunda = sum(segunda_metade) / len(segunda_metade)
        
        variacao_percentual = ((media_segunda - media_primeira) / media_primeira * 100) if media_primeira > 0 else 0
        
        # Classificar tendência
        if variacao_percentual > 10:
            tendencia = "CRESCIMENTO"
        elif variacao_percentual < -10:
            tendencia = "QUEDA"
        else:
            tendencia = "ESTAVEL"
        
        return {
            "codigo_interno": codigo_interno,
            "descricao": media['descricao'],
            "loja": loja if loja else "todas",
            "tendencia": tendencia,
            "variacao_percentual": round(variacao_percentual, 2),
            "periodo": {
                "primeira_metade": {
                    "media": round(media_primeira, 2),
                    "periodo": f"{datas[0]} a {datas[meio-1]}"
                },
                "segunda_metade": {
                    "media": round(media_segunda, 2),
                    "periodo": f"{datas[meio]} a {datas[-1]}"
                }
            }
        }
    
    def obter_top_produtos(
        self,
        loja: Optional[int] = None,
        top_n: int = 10,
        metrica: str = 'quantidade'
    ) -> List[Dict]:
        """
        Retorna produtos mais vendidos
        
        Args:
            loja: Filtrar por loja (opcional)
            top_n: Quantidade de produtos
            metrica: 'quantidade' ou 'valor'
            
        Returns:
            Lista de produtos
        """
        if self.df is None:
            return []
        
        df_filtrado = self.df.copy()
        
        if loja is not None:
            df_filtrado = df_filtrado[df_filtrado['loja'] == loja]
        
        # Agrupar por produto
        if metrica == 'quantidade':
            agrupado = df_filtrado.groupby(['codigo_interno', 'descricao', 'secao']).agg({
                'quantidade_vendida': 'sum'
            }).sort_values('quantidade_vendida', ascending=False).head(top_n)
            
            return [
                {
                    "posicao": i + 1,
                    "codigo_interno": int(idx[0]),
                    "descricao": idx[1],
                    "secao": idx[2],
                    "quantidade_total": float(row['quantidade_vendida'])
                }
                for i, (idx, row) in enumerate(agrupado.iterrows())
            ]
        else:
            agrupado = df_filtrado.groupby(['codigo_interno', 'descricao', 'secao']).agg({
                'valor_venda': 'sum'
            }).sort_values('valor_venda', ascending=False).head(top_n)
            
            return [
                {
                    "posicao": i + 1,
                    "codigo_interno": int(idx[0]),
                    "descricao": idx[1],
                    "secao": idx[2],
                    "valor_total": float(row['valor_venda'])
                }
                for i, (idx, row) in enumerate(agrupado.iterrows())
            ]
    
    def gerar_contexto_para_agente(
        self,
        codigo_interno: Optional[int] = None,
        loja: Optional[int] = None,
        incluir_tendencias: bool = True
    ) -> str:
        """
        Gera contexto formatado para o agente IA
        
        Args:
            codigo_interno: Produto específico (opcional)
            loja: Loja específica (opcional)
            incluir_tendencias: Incluir análise de tendências
            
        Returns:
            Texto formatado com contexto
        """
        if self.df is None:
            return "[AVISO] Sem dados historicos disponiveis no banco Parquet."
        
        contexto = ["="*60, "CONTEXTO: HISTORICO DE VENDAS", "="*60, ""]
        
        # Estatísticas gerais
        stats = self.obter_estatisticas_gerais()
        contexto.append(f"Periodo: {stats['periodo']['inicio']} a {stats['periodo']['fim']}")
        contexto.append(f"Produtos no historico: {stats['produtos_unicos']:,}")
        contexto.append(f"Lojas: {stats['lojas']}")
        contexto.append(f"Dias com dados: {len(stats['datas_disponiveis'])}")
        contexto.append("")
        
        # Se produto específico
        if codigo_interno:
            media = self.calcular_media_vendas_produto(codigo_interno, loja)
            if "erro" not in media:
                contexto.append(f"PRODUTO: {media['descricao']} (Cod: {codigo_interno})")
                contexto.append(f"   Secao: {media['secao']}")
                contexto.append(f"   Média de vendas/dia: {media['vendas']['media_dia']:.2f} unidades")
                contexto.append(f"   Total vendido no período: {media['vendas']['total']:.0f} unidades")
                contexto.append(f"   Variação: {media['vendas']['minima_dia']:.0f} - {media['vendas']['maxima_dia']:.0f} unidades/dia")
                contexto.append("")
                
                if incluir_tendencias:
                    tendencia = self.analisar_tendencia_produto(codigo_interno, loja)
                    if "erro" not in tendencia:
                        contexto.append(f"TENDENCIA: {tendencia['tendencia']} ({tendencia['variacao_percentual']:+.1f}%)")
                        contexto.append(f"   1a metade: {tendencia['periodo']['primeira_metade']['media']:.2f} un/dia")
                        contexto.append(f"   2a metade: {tendencia['periodo']['segunda_metade']['media']:.2f} un/dia")
                        contexto.append("")
        
        # Top produtos da loja
        if loja:
            contexto.append(f"TOP 5 PRODUTOS DA LOJA {loja}:")
            top = self.obter_top_produtos(loja, top_n=5)
            for item in top:
                contexto.append(f"   {item['posicao']}. {item['descricao'][:40]} - {item['quantidade_total']:.0f} unidades")
            contexto.append("")
        
        contexto.append("="*60)
        
        return "\n".join(contexto)
