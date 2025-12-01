# Configuração de Regras de Negócio para o Agente IA

"""
Este arquivo contém as regras de negócio que o agente LLaMA 3 usa para análise.
Edite este arquivo para adicionar novas regras ou modificar as existentes.

O agente lerá estas regras a cada execução e as aplicará nas análises.
"""

# ====================================================================
# REGRAS DE GIRO DE ESTOQUE
# ====================================================================

GIRO_ESTOQUE = {
    "dias_minimo": 4,
    "dias_maximo": 6,
    "margem_seguranca": 1.2,  # 20% adicional
    "descricao": "Giro saudável mantém estoque entre 4-6 dias"
}

# ====================================================================
# ESTRATÉGIAS DE BALANCEAMENTO
# ====================================================================

ESTRATEGIAS = {
    "comprador": {
        "quando_usar": "Valores do comprador resultam em cobertura de 4-6 dias",
        "acao": "Respeitar ponto_pedido e estoque_ideal",
        "razao": "Comprador já otimizou para exposição visual"
    },
    "giro_otimizado": {
        "quando_usar": "Valores do comprador resultam em < 4 ou > 6 dias",
        "acao": "Ajustar para range de 4-6 dias",
        "razao": "Evitar capital parado ou rupturas constantes"
    },
    "giro_saudavel": {
        "quando_usar": "Comprador não definiu valores",
        "acao": "Aplicar padrão de 4 dias de cobertura",
        "razao": "Melhores práticas de gestão de estoque"
    }
}

# ====================================================================
# ANÁLISE DE TENDÊNCIAS
# ====================================================================

TENDENCIAS = {
    "crescimento_forte": {
        "threshold": 0.20,  # 20% de crescimento
        "ajuste_caixas": +1,
        "descricao": "Aumentar pedido em 1 caixa"
    },
    "queda_forte": {
        "threshold": -0.20,  # 20% de queda
        "ajuste_caixas": -1,
        "descricao": "Reduzir pedido em 1 caixa"
    },
    "estavel": {
        "threshold_min": -0.05,
        "threshold_max": 0.05,
        "ajuste_caixas": 0,
        "descricao": "Manter pedido calculado"
    }
}

# ====================================================================
# REGRAS ESPECIAIS POR CATEGORIA (ADICIONE AQUI)
# ====================================================================

REGRAS_CATEGORIAS = {
    "pereciveis": {
        "dias_giro_maximo": 3,  # Máximo 3 dias para perecíveis
        "prioridade": "ALTA",
        "observacao": "Produtos com validade curta precisam giro mais rápido"
    },
    "promocao": {
        "margem_seguranca": 1.5,  # 50% adicional em promoções
        "prioridade": "ALTA",
        "observacao": "Promoções aumentam demanda significativamente"
    },
    "sazonal": {
        "ajuste_tendencia": 2.0,  # Dobrar sensibilidade a tendências
        "observacao": "Produtos sazonais precisam análise mais cuidadosa"
    }
}

# ====================================================================
# ALERTAS E PRIORIDADES
# ====================================================================

ALERTAS = {
    "ruptura_iminente": {
        "condicao": "dias_cobertura < 2",
        "nivel": "CRÍTICO",
        "acao": "Pedido urgente necessário"
    },
    "estoque_alto": {
        "condicao": "dias_cobertura > 10",
        "nivel": "ATENÇÃO",
        "acao": "Revisar necessidade de pedido"
    },
    "sem_vendas": {
        "condicao": "venda_media_dia == 0",
        "nivel": "ATENÇÃO",
        "acao": "Avaliar descontinuação do produto"
    }
}

# ====================================================================
# REGRAS DE EMBALAGEM
# ====================================================================

EMBALAGEM = {
    "sempre_caixa_fechada": True,
    "minimo_pedido_caixas": 1,
    "descricao": "Pedidos sempre em múltiplos de embalagem (caixas fechadas)"
}

# ====================================================================
# PARÂMETROS DE FORNECEDORES (ADICIONE AQUI)
# ====================================================================

FORNECEDORES = {
    "Baklizi": {
        "lead_time_dias": 3,
        "pedido_minimo_valor": 500,
        "observacao": "Fornecedor principal"
    },
    "Nestlé": {
        "lead_time_dias": 4,
        "pedido_minimo_valor": 1000,
        "observacao": "Produtos premium"
    }
}

# ====================================================================
# INSTRUÇÕES PERSONALIZADAS PARA O AGENTE
# ====================================================================

INSTRUCOES_EXTRAS = """

5. REGRAS ADICIONAIS PERSONALIZADAS:
   
   a) Produtos Perecíveis:
      - Máximo 3 dias de giro (mais rápido que o padrão)
      - Prioridade ALTA em pedidos
      - Nunca ultrapassar estoque ideal
   
   b) Produtos em Promoção:
      - Aumentar margem de segurança para 50%
      - Monitorar vendas diárias com atenção
      - Ajustar rapidamente se vendas explodirem
   
   c) Produtos Sazonais:
      - Sensibilidade dobrada a tendências
      - Considerar época do ano
      - Reduzir estoque fora de temporada
   
   d) Alertas Críticos:
      - Cobertura < 2 dias = PEDIDO URGENTE
      - Cobertura > 10 dias = REVISAR PEDIDO
      - Sem vendas = AVALIAR DESCONTINUAÇÃO
   
   e) Lead Time dos Fornecedores:
      - Baklizi: 3 dias de entrega
      - Nestlé: 4 dias de entrega
      - Considerar no cálculo de cobertura

6. ATUALIZAÇÃO DIÁRIA:
   - O arquivo gerado.xlsx é atualizado diariamente
   - Sempre use os dados mais recentes
   - Compare tendências com dias anteriores
   - Ajuste recomendações baseado em mudanças
"""

# ====================================================================
# FUNÇÃO PARA GERAR PROMPT COMPLETO
# ====================================================================

def obter_regras_completas():
    """
    Retorna todas as regras em formato texto para o agente IA
    """
    regras = f"""
CONHECIMENTO FUNDAMENTAL SOBRE GESTÃO DE ESTOQUE:

1. GIRO SAUDÁVEL DE ESTOQUE:
   - Ideal: {GIRO_ESTOQUE['dias_minimo']} a {GIRO_ESTOQUE['dias_maximo']} dias de cobertura
   - Menos de {GIRO_ESTOQUE['dias_minimo']} dias: Risco de ruptura, excesso de pedidos
   - Mais de {GIRO_ESTOQUE['dias_maximo']} dias: Capital parado, produtos podem vencer/deteriorar
   - Margem de segurança: {GIRO_ESTOQUE['margem_seguranca']} ({int((GIRO_ESTOQUE['margem_seguranca']-1)*100)}% adicional)

2. VALORES DO COMPRADOR (Ponto de Pedido / Estoque Ideal):
   - São baseados na EXPERIÊNCIA VISUAL e exposição do produto na prateleira
   - Refletem o conhecimento prático de como o produto deve ser apresentado
   - NÃO devem ser ignorados, mas devem ser EQUILIBRADOS com giro saudável

3. ESTRATÉGIA INTELIGENTE DE BALANCEAMENTO:
   a) {ESTRATEGIAS['comprador']['quando_usar']}:
      ✓ RESPEITAR os valores do comprador (ele entende a exposição visual)
   
   b) Se resultam em cobertura > {GIRO_ESTOQUE['dias_maximo']} dias:
      ⚠ AJUSTAR para máximo de {GIRO_ESTOQUE['dias_maximo']} dias (evitar estoque parado)
      → Explicar ao comprador: "Ajustado para giro mais saudável"
   
   c) Se resultam em cobertura < {GIRO_ESTOQUE['dias_minimo']} dias:
      ⚠ AJUSTAR para mínimo de {GIRO_ESTOQUE['dias_minimo']} dias (evitar rupturas constantes)
      → Explicar ao comprador: "Ajustado para evitar excesso de pedidos"

4. APRENDIZADO COM DADOS DO COMPRADOR:
   - Valores de ponto_pedido/estoque_ideal são "training data"
   - Mostram padrões de exposição que funcionam na prática
   - Use-os para entender necessidades visuais de cada categoria
   - Mas sempre corrija quando forem anti-econômicos

{INSTRUCOES_EXTRAS}

INSTRUÇÕES DE RESPOSTA:
- Seja direto e objetivo
- Use dados quantitativos quando disponíveis
- SEMPRE mencione a estratégia usada (giro_saudavel, comprador, giro_otimizado)
- Explique quando e por que ajusta valores do comprador
- Priorize ações urgentes
- Considere custos e eficiência logística
- Forneça justificativas claras para suas recomendações
"""
    return regras


# ====================================================================
# COMO USAR ESTE ARQUIVO
# ====================================================================

"""
PARA ADICIONAR NOVAS REGRAS:

1. Edite as seções acima (REGRAS_CATEGORIAS, ALERTAS, etc.)

2. Adicione instruções personalizadas em INSTRUCOES_EXTRAS

3. O agente lerá automaticamente na próxima execução

4. Não precisa reiniciar o Ollama ou recarregar o modelo


EXEMPLO - Adicionar nova regra:

REGRAS_CATEGORIAS["bebidas"] = {
    "dias_giro_maximo": 5,
    "prioridade": "MÉDIA",
    "observacao": "Bebidas têm demanda estável"
}

E adicione em INSTRUCOES_EXTRAS:

   f) Produtos de Bebidas:
      - Máximo 5 dias de giro
      - Demanda geralmente estável
      - Atenção especial em datas comemorativas


O agente usará estas regras na próxima análise!
"""
