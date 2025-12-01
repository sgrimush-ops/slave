# Integração: Agente IA + Histórico de Vendas

## 🎯 Visão Geral

O sistema agora possui **inteligência ampliada** com acesso ao histórico de vendas armazenado em formato Parquet, permitindo análises muito mais robustas e precisas.

## ✅ O Que Foi Implementado

### 1. **Módulo de Análise de Histórico** (`src/analise_historico.py`)

Classe `AnalisadorHistorico` que fornece:

- ✅ Carregamento automático do banco Parquet
- ✅ Cálculo de média de vendas por produto/loja
- ✅ Análise de tendências (crescimento/queda/estável)
- ✅ Cálculo de cobertura de estoque
- ✅ Ranking de produtos mais vendidos
- ✅ Geração de contexto formatado para o agente IA

### 2. **Integração com Agente IA** (`src/agente_estoque.py`)

- ✅ Agente carrega automaticamente o analisador de histórico
- ✅ Novos métodos que usam dados históricos
- ✅ Contexto enriquecido em todas as análises

### 3. **Script de Teste** (`testar_agente_historico.py`)

Menu interativo para testar:
- Carregamento de histórico
- Análise detalhada de produtos
- Agente IA com histórico completo

## 📊 Exemplo de Análise

### Antes (sem histórico):
```
"Produto X está com estoque baixo. Recomendo repor."
```

### Agora (com histórico):
```
PRODUTO: LEITE UHT STA CLARA INTEGRAL 1L
Periodo: 28/11/25 a 29/11/25
Media vendas/dia: 735 unidades
Tendencia: QUEDA (-17.4%)

Com estoque de 100 unidades:
  Cobertura atual: 0.1 dias (CRITICO)
  Necessario pedir: 2,840 unidades para 4 dias
```

## 🚀 Como Usar

### 1. Análise Manual de Produto

```python
from src.analise_historico import AnalisadorHistorico

analisador = AnalisadorHistorico()

# Média de vendas
media = analisador.calcular_media_vendas_produto(
    codigo_interno=21771,
    loja=11
)
print(f"Média: {media['vendas']['media_dia']:.2f} unidades/dia")

# Tendência
tendencia = analisador.analisar_tendencia_produto(21771, loja=11)
print(f"Tendência: {tendencia['tendencia']}")

# Cobertura
cobertura = analisador.calcular_cobertura_necessaria(
    codigo_interno=21771,
    loja=11,
    estoque_atual=100,
    dias_cobertura=4
)
print(f"Status: {cobertura['status']}")
print(f"Pedir: {cobertura['necessidade']['quantidade_pedir']:.0f} unidades")
```

### 2. Agente IA com Histórico

```python
from src.agente_estoque import AgenteEstoque

# Inicializa com histórico ativado
agente = AgenteEstoque(usar_historico=True)

# Análise inteligente de pedido
resposta = agente.analisar_pedido_com_historico(
    codigo_interno=21771,
    loja_id=11,
    estoque_atual=50,
    ponto_pedido=100,
    estoque_ideal=200,
    embalagem=12
)

print(resposta)  # Análise completa do LLaMA 3
```

### 3. Teste Completo

```bash
python testar_agente_historico.py
```

Menu interativo com opções:
1. Testar carregamento de histórico
2. Testar análise detalhada de produto
3. Testar agente IA com histórico (LLaMA 3)
4. Executar todos os testes

## 📈 Métricas Disponíveis

### Estatísticas Gerais
- Total de registros no banco
- Período de dados (data início/fim)
- Quantidade de lojas
- Produtos únicos no histórico
- Seções disponíveis

### Por Produto
- **Média de vendas/dia**: Baseada em histórico real
- **Total vendido**: Soma de todas as vendas do período
- **Variação**: Min/max de vendas diárias
- **Desvio padrão**: Estabilidade das vendas
- **Tendência**: CRESCIMENTO / QUEDA / ESTAVEL
- **Variação %**: Comparação entre períodos

### Cobertura de Estoque
- **Dias de cobertura atual**: Quanto tempo o estoque dura
- **Status**: CRITICO / BAIXO / IDEAL / ALTO / EXCESSO
- **Quantidade necessária**: Para alcançar cobertura desejada

## 🎯 Casos de Uso

### 1. Produto com Alta Rotatividade
```python
# LEITE UHT STA CLARA INTEGRAL 1L (Loja 11)
# Media: 735 unidades/dia
# Estoque atual: 100 unidades
# Resultado: CRITICO (0.1 dias de cobertura)
# Ação: Pedir 2,840 unidades urgente
```

### 2. Produto em Crescimento
```python
# Tendência: CRESCIMENTO (+25%)
# 1ª metade: 45 un/dia
# 2ª metade: 56 un/dia
# Ação: Aumentar estoque de segurança
```

### 3. Produto em Queda
```python
# Tendência: QUEDA (-30%)
# 1ª metade: 100 un/dia
# 2ª metade: 70 un/dia
# Ação: Reduzir pedidos, evitar excesso
```

## 🔧 Métodos da Classe AnalisadorHistorico

### `calcular_media_vendas_produto(codigo_interno, loja, dias)`
Calcula média de vendas de um produto específico.

**Retorna:**
```python
{
    "codigo_interno": 21771,
    "descricao": "LEITE UHT...",
    "secao": "13 PRODUTOS ANIMAIS",
    "vendas": {
        "media_dia": 735.0,
        "total": 1470.0,
        "minima_dia": 600.0,
        "maxima_dia": 870.0,
        "desvio_padrao": 135.0
    },
    "periodo_analisado": {
        "inicio": "28/11/25",
        "fim": "29/11/25",
        "dias_com_dados": 2
    }
}
```

### `analisar_tendencia_produto(codigo_interno, loja)`
Analisa tendência de vendas comparando períodos.

**Retorna:**
```python
{
    "tendencia": "QUEDA",  # ou CRESCIMENTO / ESTAVEL
    "variacao_percentual": -17.4,
    "periodo": {
        "primeira_metade": {"media": 870.0},
        "segunda_metade": {"media": 600.0}
    }
}
```

### `calcular_cobertura_necessaria(codigo_interno, loja, estoque_atual, dias_cobertura)`
Calcula necessidade de pedido para cobertura desejada.

**Retorna:**
```python
{
    "estoque_atual": 100,
    "media_vendas_dia": 735.0,
    "dias_cobertura_atual": 0.1,
    "status": "CRITICO",
    "necessidade": {
        "total_para_cobertura": 2940.0,
        "quantidade_pedir": 2840.0
    }
}
```

### `obter_top_produtos(loja, top_n, metrica)`
Lista produtos mais vendidos.

**Retorna:**
```python
[
    {
        "posicao": 1,
        "codigo_interno": 21771,
        "descricao": "LEITE UHT STA CLARA INTEGRAL 1L",
        "secao": "13 PRODUTOS ANIMAIS",
        "quantidade_total": 11082.0
    },
    # ... mais produtos
]
```

### `gerar_contexto_para_agente(codigo_interno, loja, incluir_tendencias)`
Gera texto formatado para o agente IA com todas as informações relevantes.

## 🤖 Novos Métodos do Agente IA

### `analisar_pedido_com_historico()`
Análise completa de pedido usando LLaMA 3 + histórico de vendas.

**Exemplo de resposta:**
```
RECOMENDAÇÃO INTELIGENTE:

1. QUANTIDADE A PEDIR: 2,880 unidades (240 embalagens)
   
   Justificativa: Baseado na média de 735 un/dia, com tendência de 
   queda de 17.4%. Ajustado para 4 dias de cobertura = 2,940 unidades.
   Arredondado para múltiplo de embalagem (12 un) = 2,880 unidades.

2. ESTRATÉGIA: "giro_otimizado"
   
   O ponto_pedido do comprador (100) resulta em apenas 0.1 dias de 
   cobertura, muito abaixo do ideal. Ajustamos para giro saudável de 
   4 dias. Valores do comprador parecem desatualizados.

3. ALERTAS:
   - ⚠ SITUAÇÃO CRÍTICA: Estoque atual cobre apenas 0.1 dias
   - 📉 TENDÊNCIA DE QUEDA: Vendas caíram 17.4% no período
   - 🔄 REAVALIAR: Ponto de pedido do comprador precisa revisão
```

## 📊 Integração com Sistema Principal

O sistema mestre (`iniciar_sistema.py`) agora automaticamente:

1. ✅ Carrega histórico de vendas ao iniciar
2. ✅ Enriquece análises com dados históricos
3. ✅ Fornece recomendações baseadas em tendências
4. ✅ Calcula coberturas usando médias reais

## 🔄 Workflow Completo

```
1. Processar vendas diárias
   └─> python tratamento_abc.py
   
2. Dados salvos no Parquet
   └─> data/vendas_historico.parquet
   
3. Sistema principal carrega histórico
   └─> python iniciar_sistema.py
   
4. Agente IA analisa com contexto enriquecido
   └─> Recomendações baseadas em dados reais
   
5. Decisões mais assertivas
   └─> Redução de rupturas e excessos
```

## 📈 Benefícios da Integração

### Antes (sem histórico):
- ❌ Decisões baseadas apenas em valores estáticos
- ❌ Sem considerar sazonalidade
- ❌ Sem detectar tendências
- ❌ Estoque de segurança genérico

### Agora (com histórico):
- ✅ Decisões baseadas em vendas reais
- ✅ Detecta produtos em crescimento/queda
- ✅ Ajusta automaticamente para tendências
- ✅ Estoque de segurança calculado por produto
- ✅ Previsões mais precisas
- ✅ Redução de rupturas e excessos

## 🎓 Próximos Passos

1. ✅ Sistema básico funcionando
2. ✅ Histórico de vendas integrado
3. 🔄 Usar histórico nas sugestões de pedidos
4. 🔄 Dashboard de visualização de tendências
5. 🔄 Alertas automáticos de anomalias
6. 🔄 Previsão de demanda com ML

## 📝 Exemplo Real de Uso

```python
# Cenário: Analisar LEITE UHT na Loja 11
from src.agente_estoque import AgenteEstoque

agente = AgenteEstoque(usar_historico=True)

# O agente automaticamente:
# 1. Carrega histórico (53,769 registros)
# 2. Calcula média: 735 un/dia
# 3. Detecta tendência: QUEDA -17.4%
# 4. Avalia cobertura: 0.1 dias (CRÍTICO)
# 5. Recomenda: 2,880 unidades
# 6. Justifica: Com base em dados reais + tendência

resposta = agente.analisar_pedido_com_historico(
    codigo_interno=21771,
    loja_id=11,
    estoque_atual=100,
    ponto_pedido=100,
    estoque_ideal=200,
    embalagem=12
)
```

**Resultado:** Decisão fundamentada em dados reais, não em "achismos"! 🎯
