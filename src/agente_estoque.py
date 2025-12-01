"""
Agente inteligente baseado em LLaMA 3 para gestão de estoque
"""
import json
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import ollama
import os
import sys

from .modelos import CentroDistribuicao, Loja, Produto, ItemEstoque

# Importa regras de negócio configuráveis
try:
    from .regras_negocio import obter_regras_completas
    USAR_REGRAS_CUSTOMIZADAS = True
except ImportError:
    USAR_REGRAS_CUSTOMIZADAS = False

# Importa analisador de histórico
try:
    from .analise_historico import AnalisadorHistorico
    USAR_HISTORICO = True
except ImportError:
    USAR_HISTORICO = False


class AgenteEstoque:
    """
    Agente inteligente que utiliza LLaMA 3 para análise e recomendações
    sobre gestão de estoque e abastecimento de lojas
    """
    
    def __init__(self, modelo: str = "llama3", usar_historico: bool = True):
        """
        Inicializa o agente
        
        Args:
            modelo: Nome do modelo Ollama a ser utilizado (padrão: llama3)
            usar_historico: Usar dados históricos de vendas do Parquet
        """
        # Detectar modelos disponíveis e usar o primeiro se modelo padrão não existir
        self.modelo = self._detectar_modelo(modelo)
        self.historico_conversas = []
        
        # Inicializa analisador de histórico se disponível
        self.analisador = None
        if usar_historico and USAR_HISTORICO:
            try:
                self.analisador = AnalisadorHistorico()
                print("[OK] Analisador de historico ativado")
            except Exception as e:
                print(f"[AVISO] Erro ao carregar historico: {e}")
                self.analisador = None
    
    def _detectar_modelo(self, modelo_preferido: str) -> str:
        """
        Detecta modelos Ollama instalados e retorna o melhor disponível
        
        Args:
            modelo_preferido: Modelo que o usuário quer usar
            
        Returns:
            Nome do modelo a ser usado (com versão completa se necessário)
        """
        try:
            import requests
            response = requests.get('http://localhost:11434/api/tags', timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                modelos = [m['name'] for m in data.get('models', [])]
                
                if not modelos:
                    raise Exception("Nenhum modelo instalado no Ollama")
                
                print(f"[INFO] Modelos disponíveis: {', '.join(modelos)}")
                
                # 1. Verificar se o modelo preferido existe exatamente (com ou sem versão)
                if modelo_preferido in modelos:
                    print(f"[OK] Usando modelo: {modelo_preferido}")
                    return modelo_preferido
                
                # 2. Procurar por modelo preferido com qualquer versão
                for modelo in modelos:
                    if modelo.startswith(modelo_preferido + ':'):
                        print(f"[OK] Usando modelo: {modelo}")
                        return modelo
                
                # 3. Procurar por variações (ex: llama3 pode estar como llama3:latest)
                modelos_base = {m.split(':')[0]: m for m in modelos}
                if modelo_preferido in modelos_base:
                    modelo_escolhido = modelos_base[modelo_preferido]
                    print(f"[OK] Usando modelo: {modelo_escolhido}")
                    return modelo_escolhido
                
                # 4. Buscar por substring (gemma pode encontrar gemma3:4b)
                for modelo in modelos:
                    if modelo_preferido.lower() in modelo.lower():
                        print(f"[OK] Modelo '{modelo_preferido}' não encontrado, usando: {modelo}")
                        return modelo
                
                # 5. Se não encontrou nada, usar o primeiro disponível
                modelo_escolhido = modelos[0]
                print(f"[AVISO] Modelo '{modelo_preferido}' não encontrado")
                print(f"[OK] Usando primeiro modelo disponível: {modelo_escolhido}")
                return modelo_escolhido
                
        except Exception as e:
            print(f"[AVISO] Não foi possível detectar modelos: {e}")
            print(f"[INFO] Tentando usar modelo padrão: {modelo_preferido}")
            
        return modelo_preferido
        
    def _chamar_llm(self, prompt: str, contexto: Optional[str] = None) -> str:
        """
        Chama o modelo LLaMA 3 via Ollama
        
        Args:
            prompt: Pergunta ou solicitação
            contexto: Contexto adicional para a análise
            
        Returns:
            Resposta do modelo
        """
        try:
            mensagens = []
            
            # Sistema prompt com contexto do domínio
            # Usa regras customizadas se disponíveis, senão usa padrão
            if USAR_REGRAS_CUSTOMIZADAS:
                regras_negocio = obter_regras_completas()
                system_prompt = f"""Você é um especialista em gestão de estoque e supply chain.
Sua função é analisar dados de estoque, prever demandas e recomendar ações de 
abastecimento para lojas a partir de um centro de distribuição.

{regras_negocio}
"""
            else:
                system_prompt = """Você é um especialista em gestão de estoque e supply chain.
Sua função é analisar dados de estoque, prever demandas e recomendar ações de 
abastecimento para lojas a partir de um centro de distribuição.

CONHECIMENTO FUNDAMENTAL SOBRE GESTÃO DE ESTOQUE:

1. GIRO SAUDÁVEL DE ESTOQUE:
   - Ideal: 4 a 6 dias de cobertura
   - Menos de 4 dias: Risco de ruptura, excesso de pedidos
   - Mais de 6 dias: Capital parado, produtos podem vencer/deteriorar
   
2. VALORES DO COMPRADOR (Ponto de Pedido / Estoque Ideal):
   - São baseados na EXPERIÊNCIA VISUAL e exposição do produto na prateleira
   - Refletem o conhecimento prático de como o produto deve ser apresentado
   - NÃO devem ser ignorados, mas devem ser EQUILIBRADOS com giro saudável
   
3. ESTRATÉGIA INTELIGENTE DE BALANCEAMENTO:
   a) Se ponto_pedido/estoque_ideal resultam em cobertura de 4-6 dias:
      ✓ RESPEITAR os valores do comprador (ele entende a exposição visual)
   
   b) Se resultam em cobertura > 6 dias:
      ⚠ AJUSTAR para máximo de 6 dias (evitar estoque parado)
      → Explicar ao comprador: "Ajustado para giro mais saudável"
   
   c) Se resultam em cobertura < 4 dias:
      ⚠ AJUSTAR para mínimo de 4 dias (evitar rupturas constantes)
      → Explicar ao comprador: "Ajustado para evitar excesso de pedidos"

4. APRENDIZADO COM DADOS DO COMPRADOR:
   - Valores de ponto_pedido/estoque_ideal são "training data"
   - Mostram padrões de exposição que funcionam na prática
   - Use-os para entender necessidades visuais de cada categoria
   - Mas sempre corrija quando forem anti-econômicos

5. ENTENDENDO ESTOQUE CD vs ESTOQUE LOJA:
   - ESTOQUE CD (estoque_cd): É o Centro de Distribuição, estoque CENTRAL
     * Abastece TODAS as lojas
     * Valor ÚNICO para o produto (não varia por loja)
     * Quando perguntarem "estoque do CD", refira-se a este valor
   
   - ESTOQUE LOJA (estoque): É o estoque INDIVIDUAL de cada loja
     * Cada loja tem seu próprio estoque
     * Soma dos estoques das lojas ≠ estoque do CD
     * Quando perguntarem "estoque da loja X", refira-se ao estoque daquela loja específica

IMPORTANTE: Perguntas sobre "CD", "centro de distribuição" ou "estoque do CD" 
devem ser respondidas com o valor de estoque_cd, NÃO com a soma das lojas!

Ao responder:
- Seja direto e objetivo
- Use dados quantitativos quando disponíveis
- SEMPRE mencione a estratégia usada (giro_saudavel, comprador, giro_otimizado)
- Explique quando e por que ajusta valores do comprador
- Priorize ações urgentes
- Considere custos e eficiência logística
- Diferencie claramente entre estoque do CD e estoque das lojas
- Forneça justificativas claras para suas recomendações"""
            
            mensagens.append({
                "role": "system",
                "content": system_prompt
            })
            
            # Adiciona contexto se fornecido
            if contexto:
                mensagens.append({
                    "role": "user",
                    "content": f"CONTEXTO:\n{contexto}"
                })
            
            # Adiciona a pergunta principal
            mensagens.append({
                "role": "user",
                "content": prompt
            })
            
            # Chama o modelo
            resposta = ollama.chat(
                model=self.modelo,
                messages=mensagens
            )
            
            return resposta['message']['content']
            
        except Exception as e:
            return f"Erro ao consultar o modelo: {str(e)}\nVerifique se o Ollama está rodando e o modelo {self.modelo} está instalado."
    
    def analisar_necessidade_abastecimento(
        self, 
        loja: Loja, 
        cd: CentroDistribuicao,
        dias_analise: int = 30
    ) -> str:
        """
        Analisa necessidade de abastecimento de uma loja
        
        Args:
            loja: Loja a ser analisada
            cd: Centro de distribuição
            dias_analise: Período de análise histórica
            
        Returns:
            Recomendações do agente
        """
        # Prepara contexto com dados da loja
        contexto = self._preparar_contexto_loja(loja, cd)
        
        # Adiciona contexto de histórico de vendas se disponível
        if self.analisador:
            try:
                contexto_historico = self.analisador.gerar_contexto_para_agente(loja=loja.id)
                contexto = f"{contexto}\n\n{contexto_historico}"
            except Exception as e:
                print(f"[AVISO] Erro ao carregar historico: {e}")
        
        prompt = f"""Analise o estoque da {loja.nome} e recomende quais produtos precisam 
de reposição URGENTE do centro de distribuição.

Para cada produto crítico, informe:
1. Quantidade sugerida para transferência
2. Prioridade (ALTA/MÉDIA/BAIXA)
3. Justificativa baseada nos dados (USE O HISTÓRICO DE VENDAS quando disponível)

Considere:
- Estoque atual vs estoque mínimo
- Disponibilidade no CD
- Capacidade da loja
- Histórico de vendas (média diária, tendências)
- Cobertura atual vs ideal (4-6 dias)"""
        
        resposta = self._chamar_llm(prompt, contexto)
        
        # Registra no histórico
        self.historico_conversas.append({
            "timestamp": datetime.now(),
            "tipo": "analise_abastecimento",
            "loja_id": loja.id,
            "resposta": resposta
        })
        
        return resposta
    
    def prever_demanda(
        self, 
        produto_id: str,
        loja: Loja,
        historico_vendas: List[Dict]
    ) -> str:
        """
        Prevê demanda futura de um produto
        
        Args:
            produto_id: ID do produto
            loja: Loja para análise
            historico_vendas: Histórico de vendas
            
        Returns:
            Previsão e recomendações
        """
        item = loja.obter_produto(produto_id)
        if not item:
            return "Produto não encontrado no estoque da loja."
        
        # Prepara dados de vendas
        contexto_vendas = self._preparar_contexto_vendas(
            item.produto, 
            historico_vendas
        )
        
        prompt = f"""Com base no histórico de vendas do produto {item.produto.nome}, 
faça uma previsão de demanda para os próximos 7, 15 e 30 dias.

Considere:
- Tendências de vendas
- Sazonalidade
- Estoque atual: {item.quantidade_atual} {item.produto.unidade}
- Tempo de reposição: {item.produto.tempo_reposicao_dias} dias

Recomende:
1. Quantidade ideal de reposição
2. Momento ideal para solicitar (em dias)
3. Estoque de segurança sugerido"""
        
        resposta = self._chamar_llm(prompt, contexto_vendas)
        return resposta
    
    def otimizar_distribuicao(
        self,
        cd: CentroDistribuicao,
        lojas: List[Loja]
    ) -> str:
        """
        Otimiza distribuição de produtos entre múltiplas lojas
        
        Args:
            cd: Centro de distribuição
            lojas: Lista de lojas a serem abastecidas
            
        Returns:
            Plano de distribuição otimizado
        """
        # Prepara contexto com todas as lojas
        contexto_lojas = []
        for loja in lojas:
            criticos = loja.listar_produtos_criticos()
            if criticos:
                contexto_lojas.append({
                    "loja": loja.nome,
                    "produtos_criticos": len(criticos),
                    "ocupacao": round(loja.calcular_ocupacao_volume(), 2),
                    "itens": [
                        {
                            "produto": item.produto.nome,
                            "atual": item.quantidade_atual,
                            "minimo": item.produto.estoque_minimo,
                            "status": item.status
                        }
                        for item in criticos[:5]  # Top 5 críticos
                    ]
                })
        
        contexto = f"""
CENTRO DE DISTRIBUIÇÃO:
{cd.relatorio_geral()}

LOJAS COM NECESSIDADES:
{json.dumps(contexto_lojas, indent=2, ensure_ascii=False)}
"""
        
        prompt = """Crie um plano de distribuição otimizado para abastecer todas as lojas.

Priorize:
1. Produtos em situação CRÍTICA ou ESGOTADO
2. Lojas com maior número de produtos críticos
3. Eficiência logística (agrupar transferências)

Para cada loja, liste:
- Prioridade de atendimento (1 a N)
- Produtos e quantidades a transferir
- Justificativa da priorização"""
        
        resposta = self._chamar_llm(prompt, contexto)
        return resposta
    
    def analisar_pedido_com_historico(
        self,
        codigo_interno: int,
        loja_id: int,
        estoque_atual: float,
        ponto_pedido: float,
        estoque_ideal: float,
        embalagem: float
    ) -> str:
        """
        Analisa necessidade de pedido usando histórico de vendas
        
        Args:
            codigo_interno: Código do produto
            loja_id: ID da loja
            estoque_atual: Estoque disponível
            ponto_pedido: Ponto de pedido do comprador
            estoque_ideal: Estoque ideal do comprador
            embalagem: Unidades por embalagem
            
        Returns:
            Análise e recomendação
        """
        if not self.analisador:
            return "[AVISO] Analisador de historico nao disponivel. Analise limitada a dados atuais."
        
        # Buscar dados históricos
        try:
            media_vendas = self.analisador.calcular_media_vendas_produto(codigo_interno, loja_id)
            if "erro" in media_vendas:
                return f"[AVISO] Produto sem historico de vendas: {media_vendas['erro']}"
            
            cobertura = self.analisador.calcular_cobertura_necessaria(
                codigo_interno, loja_id, estoque_atual, dias_cobertura=4
            )
            
            tendencia = self.analisador.analisar_tendencia_produto(codigo_interno, loja_id)
            
            # Preparar contexto rico
            contexto = f"""
ANÁLISE DE PEDIDO - PRODUTO {codigo_interno}

DADOS ATUAIS:
- Descrição: {media_vendas['descricao']}
- Seção: {media_vendas['secao']}
- Loja: {loja_id}
- Estoque atual: {estoque_atual} unidades
- Ponto de pedido (comprador): {ponto_pedido}
- Estoque ideal (comprador): {estoque_ideal}
- Embalagem: {embalagem} unidades

HISTÓRICO DE VENDAS:
- Período: {media_vendas['periodo_analisado']['inicio']} a {media_vendas['periodo_analisado']['fim']}
- Dias com dados: {media_vendas['periodo_analisado']['dias_com_dados']}
- Média vendas/dia: {media_vendas['vendas']['media_dia']:.2f} unidades
- Total vendido: {media_vendas['vendas']['total']:.0f} unidades
- Variação: {media_vendas['vendas']['minima_dia']:.0f} - {media_vendas['vendas']['maxima_dia']:.0f} unidades/dia
- Desvio padrão: {media_vendas['vendas']['desvio_padrao']:.2f}

ANÁLISE DE COBERTURA:
- Cobertura atual: {cobertura['dias_cobertura_atual']:.1f} dias
- Cobertura desejada: {cobertura['dias_cobertura_desejados']} dias
- Status: {cobertura['status']}
- Necessidade calculada: {cobertura['necessidade']['quantidade_pedir']:.0f} unidades

TENDÊNCIA:
- Classificação: {tendencia.get('tendencia', 'N/A')}
- Variação: {tendencia.get('variacao_percentual', 0):+.1f}%
"""
            
            prompt = """Com base nos dados históricos e situação atual, faça uma RECOMENDAÇÃO INTELIGENTE:

1. QUANTIDADE A PEDIR:
   - Justifique usando média de vendas histórica
   - Ajuste para múltiplos da embalagem
   - Considere tendência (crescimento/queda)
   - Balance entre valores do comprador e giro saudável

2. ESTRATÉGIA:
   - Qual usar: "comprador", "giro_otimizado" ou "giro_saudavel"?
   - Por que esta é a melhor escolha?

3. ALERTAS:
   - Produto com alta variabilidade de vendas?
   - Tendência preocupante?
   - Estoque atual suficiente ou crítico?

Seja objetivo e direto nas recomendações."""
            
            resposta = self._chamar_llm(prompt, contexto)
            return resposta
            
        except Exception as e:
            return f"[ERRO] Erro ao analisar historico: {str(e)}"
    
    def consulta_livre(self, pergunta: str, contexto_adicional: str = "") -> str:
        """
        Permite consultas livres ao agente
        
        Args:
            pergunta: Pergunta sobre gestão de estoque
            contexto_adicional: Contexto opcional
            
        Returns:
            Resposta do agente
        """
        contexto_completo = contexto_adicional
        
        # Se tiver analisador de histórico, tentar extrair código do produto da pergunta
        if self.analisador:
            import re
            print("[INFO] Analisador de histórico ativo, buscando códigos na pergunta...")
            
            # Detectar códigos numéricos na pergunta (4-7 dígitos)
            codigos = re.findall(r'\b(\d{4,7})\b', pergunta)
            
            # Detectar lojas mencionadas na pergunta (1-3 dígitos)
            # Busca por padrões: "loja 4", "loja 04", "loja 004", "lojas 4 e 7", etc
            lojas_detectadas = re.findall(r'loja[s]?\s+(\d{1,3})', pergunta.lower())
            lojas_normalizadas = None
            if lojas_detectadas:
                # Normalizar lojas com padding de zeros (3 dígitos)
                lojas_normalizadas = [str(int(loja)).zfill(3) for loja in lojas_detectadas]
                print(f"[INFO] Lojas detectadas na pergunta: {lojas_normalizadas}")
            
            if codigos:
                print(f"[INFO] Códigos detectados: {codigos}")
                
                try:
                    # Para cada código encontrado, buscar dados do histórico
                    for codigo in codigos[:3]:  # Limitar a 3 códigos para não sobrecarregar
                        codigo_int = int(codigo)
                        print(f"[INFO] Buscando histórico do produto {codigo_int}...")
                        
                        dados_produto = self.analisador.consultar_produto(codigo_int)
                        
                        if dados_produto is not None and not dados_produto.empty:
                            print(f"[OK] Encontrados {len(dados_produto)} registros para produto {codigo_int}")
                            
                            # Converter quantidade para numérico
                            import pandas as pd
                            dados_produto['quantidade_vendida_num'] = pd.to_numeric(
                                dados_produto['quantidade_vendida'], errors='coerce'
                            ).fillna(0)
                            
                            # AGREGAR VENDAS POR DATA (somar todas as lojas)
                            vendas_por_data = dados_produto.groupby('data_venda').agg({
                                'quantidade_vendida_num': 'sum',
                                'loja': lambda x: ', '.join(map(str, sorted(x.unique())))
                            }).reset_index()
                            vendas_por_data = vendas_por_data.sort_values('data_venda')
                            
                            contexto_produto = f"\n\n{'='*60}\n"
                            contexto_produto += f"DADOS REAIS DO HISTÓRICO - PRODUTO {codigo}\n"
                            contexto_produto += f"{'='*60}\n"
                            contexto_produto += f"FONTE: data/vendas_historico.parquet\n"
                            contexto_produto += f"Total de registros encontrados: {len(dados_produto)}\n"
                            contexto_produto += f"IMPORTANTE: Dados agregados por data (somando todas as lojas)\n"
                            
                            # Descrição do produto
                            if 'descricao' in dados_produto.columns:
                                contexto_produto += f"Descrição: {dados_produto['descricao'].iloc[0]}\n"
                            
                            # ÚLTIMA VENDA (dados agregados)
                            ultima_data = vendas_por_data.iloc[-1]
                            contexto_produto += f"\n*** ÚLTIMA VENDA REGISTRADA (AGREGADA) ***\n"
                            contexto_produto += f"Data: {ultima_data['data_venda']}\n"
                            contexto_produto += f"Quantidade TOTAL vendida (todas as lojas): {ultima_data['quantidade_vendida_num']:.0f} unidades\n"
                            contexto_produto += f"Lojas que venderam: {ultima_data['loja']}\n"
                            
                            # Mostrar detalhamento por loja na última data COM ESTOQUE
                            dados_ultima_data = dados_produto[
                                dados_produto['data_venda'] == ultima_data['data_venda']
                            ]
                            
                            # Se lojas específicas foram mencionadas, filtrar por elas
                            if lojas_normalizadas:
                                dados_filtrados = dados_ultima_data[dados_ultima_data['loja'].isin(lojas_normalizadas)]
                                if len(dados_filtrados) > 0:
                                    contexto_produto += f"\n*** DADOS DAS LOJAS SOLICITADAS ({', '.join(lojas_normalizadas)}) ***\n"
                                    contexto_produto += f"Data: {ultima_data['data_venda']}\n"
                                    for _, row in dados_filtrados.iterrows():
                                        estoque_txt = ""
                                        if 'estoque' in row and pd.notna(row['estoque']):
                                            try:
                                                estoque_val = float(row['estoque'])
                                                estoque_txt = f" | ESTOQUE: {estoque_val:.0f} un"
                                            except:
                                                estoque_txt = f" | ESTOQUE: {row['estoque']}"
                                        contexto_produto += f"  - Loja {row['loja']}: {row['quantidade_vendida_num']:.0f} un vendidas{estoque_txt}\n"
                                else:
                                    contexto_produto += f"\n⚠️  ATENÇÃO: Lojas {', '.join(lojas_normalizadas)} não encontradas para este produto na última data.\n"
                            
                            # Mostrar todas as lojas (resumido ou completo)
                            if len(dados_ultima_data) > 1:
                                if lojas_normalizadas:
                                    contexto_produto += f"\nTodas as lojas (resumo) na data {ultima_data['data_venda']}:\n"
                                else:
                                    contexto_produto += f"\nDetalhamento por loja na data {ultima_data['data_venda']}:\n"
                                for _, row in dados_ultima_data.iterrows():
                                    estoque_txt = ""
                                    if 'estoque' in row and pd.notna(row['estoque']):
                                        try:
                                            estoque_val = float(row['estoque'])
                                            estoque_txt = f" | ESTOQUE: {estoque_val:.0f} un"
                                        except:
                                            estoque_txt = f" | ESTOQUE: {row['estoque']}"
                                    contexto_produto += f"  - Loja {row['loja']}: {row['quantidade_vendida_num']:.0f} un vendidas{estoque_txt}\n"
                            
                            # Estatísticas gerais
                            contexto_produto += f"\n*** ESTATÍSTICAS DO HISTÓRICO ***\n"
                            contexto_produto += f"Total vendido (TODAS as datas e lojas): {dados_produto['quantidade_vendida_num'].sum():.0f} unidades\n"
                            contexto_produto += f"Número de datas com vendas: {dados_produto['data_venda'].nunique()}\n"
                            contexto_produto += f"Número de lojas que venderam: {dados_produto['loja'].nunique()}\n"
                            contexto_produto += f"Período: {dados_produto['data_venda'].min()} a {dados_produto['data_venda'].max()}\n"
                            
                            # Média diária (considerando agregação por data)
                            media_diaria = vendas_por_data['quantidade_vendida_num'].mean()
                            contexto_produto += f"Média de venda por DIA (agregada): {media_diaria:.2f} unidades/dia\n"
                            
                            # ESTOQUE DO CD (CENTRO DE DISTRIBUIÇÃO) - DESTACADO
                            if 'estoque_cd' in dados_produto.columns:
                                estoque_cd_valor = dados_ultima_data['estoque_cd'].iloc[0]
                                try:
                                    estoque_cd_num = float(estoque_cd_valor)
                                    contexto_produto += f"\n{'='*60}\n"
                                    contexto_produto += f"*** ESTOQUE DO CD (CENTRO DE DISTRIBUIÇÃO) ***\n"
                                    contexto_produto += f"Data: {ultima_data['data_venda']}\n"
                                    contexto_produto += f"ESTOQUE CD: {estoque_cd_num:.0f} unidades\n"
                                    contexto_produto += f"\nO CD (Centro de Distribuição) é o estoque central que\n"
                                    contexto_produto += f"abastece todas as lojas. Este valor é DIFERENTE do estoque\n"
                                    contexto_produto += f"individual de cada loja mostrado abaixo.\n"
                                    contexto_produto += f"{'='*60}\n"
                                except:
                                    pass
                            
                            # ESTOQUE ATUAL POR LOJA (última data disponível)
                            if 'estoque' in dados_produto.columns:
                                contexto_produto += f"\n*** ESTOQUE POR LOJA (última data: {ultima_data['data_venda']}) ***\n"
                                estoque_por_loja = dados_ultima_data[['loja', 'estoque']].copy()
                                
                                # DEBUG: Mostrar valores originais
                                print(f"[DEBUG] Valores de estoque originais no Parquet:")
                                for idx, row in dados_ultima_data.iterrows():
                                    print(f"  Loja {row['loja']}: estoque={row['estoque']} (tipo: {type(row['estoque'])})")
                                
                                estoque_por_loja['estoque_num'] = pd.to_numeric(
                                    estoque_por_loja['estoque'], errors='coerce'
                                ).fillna(0)
                                
                                estoque_total = 0
                                for _, row in estoque_por_loja.iterrows():
                                    contexto_produto += f"  Loja {row['loja']}: {row['estoque_num']:.0f} unidades em estoque\n"
                                    estoque_total += row['estoque_num']
                                
                                contexto_produto += f"\nESTOQUE TOTAL (todas as lojas): {estoque_total:.0f} unidades\n"
                                
                                # Calcular dias de cobertura
                                if media_diaria > 0:
                                    dias_cobertura = estoque_total / media_diaria
                                    contexto_produto += f"COBERTURA: {dias_cobertura:.1f} dias (estoque/média diária)\n"
                                    
                                    if dias_cobertura < 4:
                                        contexto_produto += "⚠️  ALERTA: Cobertura abaixo de 4 dias - RISCO DE RUPTURA!\n"
                                    elif dias_cobertura > 6:
                                        contexto_produto += "ℹ️  INFO: Cobertura acima de 6 dias - considerar ajuste\n"
                                    else:
                                        contexto_produto += "✓ OK: Cobertura saudável (4-6 dias)\n"
                            
                            # VENDAS AGREGADAS POR DATA (últimas datas)
                            num_datas_unicas = len(vendas_por_data)
                            contexto_produto += f"\n*** VENDAS AGREGADAS POR DATA ***\n"
                            contexto_produto += f"Total de datas diferentes: {num_datas_unicas}\n\n"
                            
                            if num_datas_unicas <= 10:
                                contexto_produto += "Todas as vendas agregadas:\n"
                                for _, row in vendas_por_data.iterrows():
                                    contexto_produto += f"  {row['data_venda']}: {row['quantidade_vendida_num']:.0f} un TOTAL (lojas: {row['loja']})\n"
                            else:
                                contexto_produto += f"Últimas 10 datas (de {num_datas_unicas} datas):\n"
                                ultimas = vendas_por_data.tail(10)
                                for _, row in ultimas.iterrows():
                                    contexto_produto += f"  {row['data_venda']}: {row['quantidade_vendida_num']:.0f} un TOTAL (lojas: {row['loja']})\n"
                            
                            contexto_produto += f"{'='*60}\n"
                            contexto_produto += "IMPORTANTE: Use APENAS estes dados reais do histórico para responder.\n"
                            contexto_produto += "NÃO use dados do arquivo gerado.xlsx que são estimativas.\n"
                            contexto_produto += f"{'='*60}\n"
                            
                            contexto_completo += contexto_produto
                        else:
                            print(f"[AVISO] Nenhum registro encontrado para produto {codigo_int}")
                            contexto_completo += f"\n\n[AVISO] Produto {codigo_int} não encontrado no histórico de vendas.\n"
                            
                except Exception as e:
                    # Se der erro, continua sem o contexto histórico
                    print(f"[ERRO] Erro ao buscar histórico para código {codigo}: {e}")
                    import traceback
                    traceback.print_exc()
                    contexto_completo += f"\n\n[ERRO] Não foi possível buscar histórico: {e}\n"
            else:
                print("[INFO] Nenhum código de produto detectado na pergunta")
        else:
            print("[AVISO] Analisador de histórico NÃO está ativo (histórico não disponível)")
            contexto_completo += "\n\n[AVISO] Histórico de vendas não está disponível. Execute 'tratamento_abc.py' primeiro.\n"
        
        return self._chamar_llm(pergunta, contexto_completo)
    
    def _preparar_contexto_loja(
        self, 
        loja: Loja, 
        cd: CentroDistribuicao
    ) -> str:
        """Prepara contexto detalhado da loja para o LLM"""
        produtos_info = []
        
        for item in loja.estoque.values():
            item_cd = cd.obter_produto(item.produto.id)
            disponivel_cd = item_cd.quantidade_disponivel if item_cd else 0
            
            produtos_info.append({
                "produto": item.produto.nome,
                "categoria": item.produto.categoria,
                "estoque_loja": item.quantidade_atual,
                "estoque_minimo": item.produto.estoque_minimo,
                "estoque_seguranca": item.produto.estoque_seguranca,
                "disponivel_cd": disponivel_cd,
                "status": item.status,
                "ultima_atualizacao": item.ultima_atualizacao.strftime("%Y-%m-%d %H:%M")
            })
        
        contexto = f"""
LOJA: {loja.nome}
Endereço: {loja.endereco}
Capacidade: {loja.capacidade_m3} m³
Ocupação atual: {loja.calcular_ocupacao_volume():.1f}%

PRODUTOS NO ESTOQUE:
{json.dumps(produtos_info, indent=2, ensure_ascii=False)}

CENTRO DE DISTRIBUIÇÃO:
{json.dumps(cd.relatorio_geral(), indent=2, ensure_ascii=False)}
"""
        return contexto
    
    def _preparar_contexto_vendas(
        self, 
        produto: Produto, 
        historico: List[Dict]
    ) -> str:
        """Prepara contexto de histórico de vendas"""
        contexto = f"""
PRODUTO: {produto.nome}
Categoria: {produto.categoria}
Preço: R$ {produto.preco_venda:.2f}

HISTÓRICO DE VENDAS (últimos registros):
{json.dumps(historico[-30:], indent=2, default=str, ensure_ascii=False)}
"""
        return contexto
    
    def obter_historico(self) -> List[Dict]:
        """Retorna histórico de consultas ao agente"""
        return self.historico_conversas
