# 📦 Calculador de Sugestões de Pedido

## Visão Geral

Sistema inteligente para calcular sugestões de pedido baseado em:
- Vendas históricas (7, 14, 30 e 60 dias)
- Estoque atual
- Venda média diária
- Tamanho da embalagem (caixas fechadas)
- Tendência de vendas

## 🎯 Regras de Negócio

### 1. **Cobertura de Estoque**
- **Meta**: 4 dias de cobertura
- **Motivo**: Prazo de entrega de 2-4 dias + margem de segurança
- **Cálculo**: `Necessidade = Venda Média Dia × 4 dias × 1.2 (margem 20%)`

### 2. **Múltiplos de Embalagem**
- Pedidos sempre em **caixas fechadas**
- Arredondamento para cima
- Exemplo: Se precisa 25 unidades e a embalagem tem 12, pede 3 caixas (36 unidades)

### 3. **Análise de Tendência**
O sistema analisa tendências comparando períodos:
- **Crescimento Forte** (>20%): Adiciona 1 caixa extra
- **Crescimento Moderado** (5-20%): Mantém cálculo padrão
- **Estável** (-5% a 5%): Mantém cálculo padrão
- **Queda Moderada** (-20% a -5%): Mantém cálculo padrão
- **Queda Forte** (<-20%): Reduz 1 caixa (mínimo 1)

### 4. **Estoque Suficiente**
Se o estoque atual já cobre 4+ dias: **Sugestão = 0**

## 📊 Como Usar

### Método 1: Script Python

```bash
python calcular_sugestoes.py
```

### Método 2: Código Python

```python
from src.calculador_pedido import CalculadorPedido

# Inicializar
calculador = CalculadorPedido(
    dias_cobertura=4,      # Meta de dias de estoque
    margem_seguranca=1.2   # 20% extra
)

# Processar arquivo
df = calculador.processar_arquivo(
    arquivo_entrada="data/gerado.xlsx",
    arquivo_saida="data/gerado_com_sugestao.xlsx"
)
```

### Método 3: Cálculo Individual

```python
resultado = calculador.calcular_sugestao_pedido(
    estoque_atual=9,
    venda_media_dia=2.77,
    embalagem=12,
    venda_7dias=14,
    venda_14dias=45,
    venda_30dias=83,
    venda_60dias=118
)

print(f"Sugestão: {resultado['sugestao_caixas']} caixas")
print(f"Motivo: {resultado['motivo']}")
```

## 📁 Arquivos de Entrada/Saída

### Entrada: `data/gerado.xlsx`

Colunas obrigatórias:
- `codigo_interno`: Código do produto
- `loja`: Código da loja
- `estoque_atual`: Estoque atual em unidades
- `venda_media_dia`: Venda média diária
- `venda_acumulada_7dias`: Vendas dos últimos 7 dias
- `venda_acumulada_14dias`: Vendas dos últimos 14 dias
- `venda_acumulada_30dias`: Vendas dos últimos 30 dias
- `venda_acumulada_60dias`: Vendas dos últimos 60 dias
- `embalagem`: Unidades por caixa
- `sugestao`: (será preenchida)

### Saída: `data/gerado_com_sugestao.xlsx`

Colunas adicionadas:
- `sugestao`: Quantidade em unidades a pedir
- `sugestao_caixas`: Quantidade em caixas a pedir
- `dias_cobertura_atual`: Dias de cobertura com estoque atual
- `dias_cobertura_apos`: Dias de cobertura após o pedido
- `tendencia`: Análise de tendência de vendas
- `motivo_sugestao`: Justificativa da sugestão

### Relatório: `data/relatorio_sugestoes.txt`

Relatório detalhado em texto com:
- Análise produto por produto
- Dados de vendas
- Justificativa da sugestão
- Cobertura antes e depois

## 📈 Exemplos de Cálculo

### Exemplo 1: Produto com Estoque Baixo

**Dados:**
- Estoque atual: 2 unidades
- Venda média dia: 8 un/dia
- Embalagem: 30 un/caixa
- Tendência: Queda forte (-85%)

**Cálculo:**
1. Necessidade mínima: 8 × 4 = 32 unidades
2. Com margem segurança: 32 × 1.2 = 38.4 unidades
3. Faltando: 38.4 - 2 = 36.4 unidades
4. Caixas necessárias: ⌈36.4 / 30⌉ = 2 caixas
5. Ajuste por queda forte: 2 - 1 = 1 caixa
6. **Sugestão: 1 caixa (30 unidades)**

### Exemplo 2: Produto com Estoque Suficiente

**Dados:**
- Estoque atual: 162 unidades
- Venda média dia: 1.6 un/dia
- Embalagem: 15 un/caixa

**Cálculo:**
1. Necessidade mínima: 1.6 × 4 = 6.4 unidades
2. Com margem segurança: 6.4 × 1.2 = 7.68 unidades
3. Estoque atual (162) > Necessidade (7.68)
4. **Sugestão: 0 caixas**
5. Cobertura atual: 162 / 1.6 = 101 dias

### Exemplo 3: Produto com Crescimento Forte

**Dados:**
- Estoque atual: 10 unidades
- Venda média dia: 5 un/dia
- Embalagem: 12 un/caixa
- Tendência: Crescimento forte (+25%)

**Cálculo:**
1. Necessidade mínima: 5 × 4 = 20 unidades
2. Com margem segurança: 20 × 1.2 = 24 unidades
3. Faltando: 24 - 10 = 14 unidades
4. Caixas necessárias: ⌈14 / 12⌉ = 2 caixas
5. Ajuste por crescimento forte: 2 + 1 = 3 caixas
6. **Sugestão: 3 caixas (36 unidades)**

## 🔧 Configurações Avançadas

### Ajustar Dias de Cobertura

```python
# Para 5 dias de cobertura
calculador = CalculadorPedido(dias_cobertura=5)
```

### Ajustar Margem de Segurança

```python
# Margem de 30%
calculador = CalculadorPedido(margem_seguranca=1.3)

# Sem margem extra
calculador = CalculadorPedido(margem_seguranca=1.0)
```

### Processamento Personalizado

```python
# Diferentes arquivos
calculador.processar_arquivo(
    arquivo_entrada="data/pedidos_loja_02.xlsx",
    arquivo_saida="data/sugestoes_loja_02.xlsx"
)
```

## 📊 Interpretação dos Resultados

### Status do Produto

| Dias de Cobertura | Status | Ação |
|-------------------|--------|------|
| 0-2 dias | 🔴 CRÍTICO | Pedido urgente |
| 2-4 dias | 🟡 BAIXO | Fazer pedido |
| 4-7 dias | 🟢 NORMAL | Considerar pedido |
| 7+ dias | ⚪ ALTO | Sem necessidade |

### Tendências

| Tendência | Variação | Ajuste |
|-----------|----------|--------|
| Crescimento Forte | >20% | +1 caixa |
| Crescimento Moderado | 5-20% | Nenhum |
| Estável | -5% a 5% | Nenhum |
| Queda Moderada | -20% a -5% | Nenhum |
| Queda Forte | <-20% | -1 caixa |

## 💡 Dicas

1. **Execute diariamente** para sugestões atualizadas
2. **Revise produtos críticos** (cobertura < 2 dias)
3. **Considere sazonalidade** em datas especiais
4. **Ajuste manualmente** se necessário (promoções, eventos)
5. **Monitore tendências** para antecipar mudanças

## 🔄 Integração com Sistema

O calculador pode ser integrado ao sistema principal:

```python
from src.database import BancoDadosMix
from src.calculador_pedido import CalculadorPedido

# Buscar produto no banco
db = BancoDadosMix()
produto = db.obter_produto_por_codigo_interno(1023328)

# Calcular sugestão
calculador = CalculadorPedido()
resultado = calculador.calcular_sugestao_pedido(
    estoque_atual=9,
    venda_media_dia=2.77,
    embalagem=produto['embalagem'],
    # ... outros parâmetros
)
```

## 🤖 Uso com Agente IA

O agente LLaMA 3 pode analisar as sugestões:

```python
from src.agente_estoque import AgenteEstoque

agente = AgenteEstoque()

# Contexto com sugestões
contexto = f"""
Sugestões de pedido calculadas:
{df.to_string()}
"""

resposta = agente.consulta_livre(
    "Analise as sugestões de pedido e identifique prioridades",
    contexto
)
```

## 📞 Suporte

Para ajustes nos parâmetros ou lógica de cálculo, edite:
- `src/calculador_pedido.py`: Lógica principal
- `calcular_sugestoes.py`: Script de execução

## ✅ Validações

O sistema valida:
- ✓ Valores numéricos válidos
- ✓ Embalagem > 0
- ✓ Venda média dia ≥ 0
- ✓ Estoque atual ≥ 0
- ✓ Múltiplos de embalagem
- ✓ Caixas mínimas = 1 (se necessário pedir)
