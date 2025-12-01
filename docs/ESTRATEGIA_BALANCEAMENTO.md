# Estratégia Inteligente de Balanceamento de Estoque

## 🎯 Objetivo

Equilibrar dois fatores importantes na gestão de estoque:

1. **Giro Saudável** (4-6 dias de cobertura) - Eficiência financeira
2. **Exposição Visual** (ponto_pedido/estoque_ideal) - Experiência do comprador

## 📊 Conceitos Fundamentais

### Giro de Estoque

O **giro de estoque** mede quantos dias o estoque atual duraria considerando a venda média diária.

**Fórmula:**
```
Dias de Cobertura = Estoque Atual ÷ Venda Média Diária
```

**Ranges Recomendados:**
- ✅ **4-6 dias**: Giro saudável
- ⚠️ **< 4 dias**: Risco de ruptura, excesso de pedidos
- ⚠️ **> 6 dias**: Capital parado, risco de vencimento

### Valores do Comprador

Os campos **ponto_pedido** (mínimo) e **estoque_ideal** (máximo) são definidos pelo comprador baseado em:

- Experiência prática de exposição do produto
- Como o produto deve ser apresentado na prateleira
- Quantidade que "fica bonita" visualmente
- Gatilho automático para sistemas auxiliares da loja

**Exemplo:**
```
Produto: Cereal Matinal
- Ponto de Pedido: 10 unidades (gatilho)
- Estoque Ideal: 22 unidades (exposição completa)
- Diferença: 12 unidades
```

## 🧠 Estratégia de Balanceamento

O sistema utiliza **3 estratégias** diferentes dependendo do contexto:

### 1. Estratégia "Comprador" ✅

**Quando usar:** Valores do comprador resultam em cobertura de 4-6 dias

**Lógica:**
```python
dias_cobertura = (estoque_ideal - ponto_pedido) / venda_media_dia

if 4 <= dias_cobertura <= 6:
    if estoque_atual < ponto_pedido:
        sugestao = estoque_ideal - estoque_atual
    estrategia = "comprador"
    observacao = "Respeitando valores do comprador"
```

**Razão:** O comprador definiu valores que já estão otimizados!

### 2. Estratégia "Giro Otimizado" ⚙️

**Quando usar:** Valores do comprador resultam em cobertura fora do range (< 4 ou > 6 dias)

**Lógica para cobertura > 6 dias:**
```python
if dias_cobertura > 6:
    # Ajusta para máximo de 6 dias
    quantidade_necessaria = (venda_media_dia * 6 * 1.2) - estoque_atual
    estrategia = "giro_otimizado"
    observacao = f"Ajustado de {dias_cobertura:.1f} para 6 dias (giro mais saudável)"
```

**Lógica para cobertura < 4 dias:**
```python
if dias_cobertura < 4:
    # Ajusta para mínimo de 4 dias
    quantidade_necessaria = (venda_media_dia * 4 * 1.2) - estoque_atual
    estrategia = "giro_otimizado"
    observacao = f"Ajustado de {dias_cobertura:.1f} para 4 dias (evitar excesso de pedidos)"
```

**Razão:** Corrigir valores anti-econômicos mantendo sustentabilidade financeira.

### 3. Estratégia "Giro Saudável" 📈

**Quando usar:** Comprador não definiu valores (ponto_pedido/estoque_ideal vazios)

**Lógica:**
```python
if not ponto_pedido or not estoque_ideal:
    # Usa apenas lógica de giro saudável (4 dias)
    quantidade_necessaria = (venda_media_dia * 4 * 1.2) - estoque_atual
    estrategia = "giro_saudavel"
    observacao = "Baseado em giro de 4 dias (padrão do sistema)"
```

**Razão:** Sem dados do comprador, aplicar melhores práticas padrão.

## 📝 Exemplos Práticos

### Exemplo 1: Respeitando o Comprador ✅

**Dados:**
- Estoque Atual: 9 unidades
- Ponto de Pedido: 10 unidades
- Estoque Ideal: 22 unidades
- Venda Média/Dia: 2.77 unidades/dia
- Embalagem: 12 unidades/caixa

**Cálculo:**
```
Dias de Cobertura = (22 - 10) / 2.77 = 4.33 dias ✅

Como está no range 4-6 dias:
- Estoque atual (9) < Ponto de pedido (10) → Precisa pedir!
- Quantidade necessária = 22 - 9 = 13 unidades
- Caixas = ceil(13 / 12) = 2 caixas = 24 unidades

Estratégia: "comprador"
Observação: "Respeitando valores do comprador (4.3 dias de cobertura)"
```

### Exemplo 2: Ajustando Excesso (> 6 dias) ⚙️

**Dados:**
- Estoque Atual: 50 unidades
- Ponto de Pedido: 100 unidades
- Estoque Ideal: 200 unidades
- Venda Média/Dia: 10 unidades/dia
- Embalagem: 24 unidades/caixa

**Cálculo:**
```
Dias de Cobertura = (200 - 100) / 10 = 10 dias ⚠️ (muito alto!)

Como está > 6 dias:
- Ajusta para 6 dias máximo
- Quantidade necessária = (10 * 6 * 1.2) - 50 = 22 unidades
- Caixas = ceil(22 / 24) = 1 caixa = 24 unidades

Estratégia: "giro_otimizado"
Observação: "Ajustado de 10.0 para 6 dias (giro mais saudável)"
```

### Exemplo 3: Ajustando Insuficiência (< 4 dias) ⚙️

**Dados:**
- Estoque Atual: 5 unidades
- Ponto de Pedido: 20 unidades
- Estoque Ideal: 30 unidades
- Venda Média/Dia: 8 unidades/dia
- Embalagem: 12 unidades/caixa

**Cálculo:**
```
Dias de Cobertura = (30 - 20) / 8 = 1.25 dias ⚠️ (muito baixo!)

Como está < 4 dias:
- Ajusta para 4 dias mínimo
- Quantidade necessária = (8 * 4 * 1.2) - 5 = 33.4 unidades
- Caixas = ceil(33.4 / 12) = 3 caixas = 36 unidades

Estratégia: "giro_otimizado"
Observação: "Ajustado de 1.2 para 4 dias (evitar excesso de pedidos)"
```

## 🤖 Treinamento do Agente LLaMA 3

O agente LLaMA 3 foi treinado para entender e aplicar essas estratégias através de um **system prompt** atualizado que inclui:

1. **Conhecimento sobre giro saudável** (4-6 dias)
2. **Respeito aos valores do comprador** quando adequados
3. **Lógica de ajuste** quando valores são anti-econômicos
4. **Explicações claras** sobre qual estratégia foi usada

### Exemplos de Prompts para o Agente

**Análise de produto:**
```
Produto X:
- Estoque: 50 un
- Ponto pedido: 80 un
- Estoque ideal: 150 un
- Venda média: 15 un/dia

O que fazer?
```

**Resposta esperada:**
```
Análise do Produto X:

Dias de cobertura atual: 3.3 dias
Dias de cobertura (valores comprador): 4.7 dias ✅

Estratégia: COMPRADOR
Recomendação: Respeitar valores do comprador

Ação:
- Estoque atual (50) abaixo do ponto de pedido (80)
- Pedir: 150 - 50 = 100 unidades
- Resultado: 4.7 dias de cobertura (ideal!)

Justificativa: Valores do comprador já estão otimizados 
para giro saudável (4-6 dias) e exposição visual adequada.
```

## 📈 Benefícios da Abordagem

### Para o Negócio
- ✅ Reduz capital imobilizado em estoque
- ✅ Diminui risco de vencimento/deterioração
- ✅ Mantém giro saudável (4-6 dias)
- ✅ Evita rupturas constantes

### Para o Comprador
- ✅ Respeita experiência e conhecimento prático
- ✅ Mantém padrões de exposição visual quando adequados
- ✅ Recebe feedback quando valores precisam ajuste
- ✅ Aprende com o sistema sobre giro otimizado

### Para o Sistema
- ✅ Combina IA (LLaMA 3) com regras de negócio
- ✅ Aprende com dados históricos do comprador
- ✅ Adapta-se a diferentes categorias de produtos
- ✅ Explica decisões de forma transparente

## 🔧 Configuração

### Parâmetros Ajustáveis

```python
calculador = CalculadorPedido(
    dias_cobertura=4,        # Dias mínimos de cobertura
    margem_seguranca=1.2     # 20% adicional de segurança
)

# Ranges de giro saudável
dias_giro_minimo = 4  # Mínimo recomendado
dias_giro_maximo = 6  # Máximo recomendado
```

### Campos Necessários no Arquivo

```
gerado.xlsx deve conter:
- codigo_interno
- loja
- estoque_atual
- ponto_pedido        ← Novo!
- estoque_ideal       ← Novo!
- venda_media_dia
- venda_acumulada_7dias
- venda_acumulada_14dias
- venda_acumulada_30dias
- venda_acumulada_60dias
- embalagem
```

## 📊 Análise de Resultados

O sistema gera colunas adicionais no arquivo de saída:

```
Colunas geradas:
- sugestao                  # Unidades sugeridas
- sugestao_caixas          # Caixas sugeridas
- dias_cobertura_atual     # Cobertura antes do pedido
- dias_cobertura_apos      # Cobertura após o pedido
- estrategia_usada         # "comprador", "giro_otimizado" ou "giro_saudavel"
- tendencia                # Análise de tendência de vendas
- motivo_sugestao          # Explicação detalhada
```

## 🎓 Conclusão

Esta abordagem **híbrida** combina:
- 🤖 **Machine Learning** (LLaMA 3) para análise inteligente
- 📊 **Regras de Negócio** para giro saudável
- 🧑‍💼 **Experiência Humana** (valores do comprador)

O resultado é um sistema que:
- Respeita conhecimento prático
- Otimiza financeiramente
- Explica decisões claramente
- Aprende continuamente

**"O melhor dos dois mundos: tecnologia + experiência humana!"**
