# Banco de Dados de Vendas (Parquet)

## 📋 Visão Geral

Sistema de banco de dados histórico de vendas usando formato **Parquet**, otimizado para consultas rápidas e armazenamento eficiente.

## 🎯 Características

### ✅ Armazenamento Incremental
- Novos dias de vendas são **adicionados** ao banco (não substituem dados antigos)
- Se processar a mesma data novamente, os dados são **atualizados** (substitui apenas aquela data)
- Formato Parquet com compressão Snappy para otimização de espaço

### ✅ Sugestão Inteligente de Data
- Sistema sugere **dia anterior** como padrão
- Usuário pode aceitar (ENTER) ou digitar data diferente
- Formato: `dd/mm/yy` (exemplo: `29/11/25`)

### ✅ Filtros Aplicados
1. **Seções válidas**: 10, 13, 14, 16, 17, 23
2. **Produtos válidos**: `ponto_pedido != 0` E `embalagem != 0`
3. **Colunas essenciais**: 12 colunas mantidas + data_venda

## 📁 Estrutura do Banco

### Arquivo Principal
```
data/vendas_historico.parquet
```

### Colunas Armazenadas
1. `loja` - Código da loja (1-14)
2. `codigo_interno` - Código do produto
3. `descricao` - Nome do produto
4. `valor_venda` - Valor total vendido
5. `quantidade_vendida` - Unidades vendidas
6. `ponto_pedido` - Mínimo para reposição
7. `estoque_ideal` - Máximo de estoque
8. `embalagem` - Unidades por embalagem
9. `capacidade` - Capacidade de armazenamento
10. `estoque` - Estoque atual na loja
11. `estoque_cd` - Estoque no CD
12. `secao` - Seção do produto (ex: "10 MERCEARIA SECA")
13. `data_venda` - Data das vendas (dd/mm/yy)

## 🚀 Como Usar

### 1. Processar Vendas Diárias

```bash
python tratamento_abc.py
```

**Fluxo:**
1. Lê arquivo `data/grid_tmp_abcmerc.csv`
2. Aplica filtros (seções + zeros)
3. Sugere data do dia anterior
4. Usuário confirma ou digita data
5. Salva Excel: `data/resultado_abc.xlsx`
6. Atualiza banco: `data/vendas_historico.parquet`

**Exemplo de execução:**
```
💡 Data sugerida (ontem): 29/11/25
Digite a data de venda ou ENTER para usar 29/11/25: [ENTER]
✅ Usando data sugerida: 29/11/25

💾 Salvando no banco de dados Parquet...
   📝 Criando novo banco de dados...
   ✅ Banco atualizado com sucesso!
   📊 Total de registros no banco: 26,839

   📅 Registros por data:
      29/11/25: 26,839 registros
```

### 2. Consultar Histórico

```bash
python consultar_vendas.py
```

**Menu de opções:**
- **1.** Estatísticas gerais do banco
- **2.** Consultar vendas por data
- **3.** Consultar histórico de produto
- **4.** Exportar consulta para Excel
- **0.** Sair

### 3. Consultas Programáticas

```python
import pandas as pd

# Carregar todo o histórico
df = pd.read_parquet('data/vendas_historico.parquet')

# Filtrar por data
vendas_hoje = df[df['data_venda'] == '29/11/25']

# Filtrar por produto
produto = df[df['codigo_interno'] == 1402327]

# Filtrar por loja
loja = df[df['loja'] == 11]

# Análise por período
vendas_periodo = df[df['data_venda'].isin(['28/11/25', '29/11/25'])]
total_vendido = vendas_periodo.groupby('codigo_interno')['quantidade_vendida'].sum()
```

## 📊 Exemplos de Análises

### Produtos mais vendidos no período
```python
df = pd.read_parquet('data/vendas_historico.parquet')

top_produtos = df.groupby(['codigo_interno', 'descricao']).agg({
    'quantidade_vendida': 'sum',
    'valor_venda': lambda x: f"R$ {sum(x):,.2f}"
}).sort_values('quantidade_vendida', ascending=False).head(10)

print(top_produtos)
```

### Performance por loja
```python
df = pd.read_parquet('data/vendas_historico.parquet')

# Vendas por loja
vendas_loja = df.groupby('loja').agg({
    'valor_venda': lambda x: sum(x),
    'codigo_interno': 'nunique'  # Produtos diferentes
}).rename(columns={'codigo_interno': 'produtos_unicos'})

print(vendas_loja.sort_values('valor_venda', ascending=False))
```

### Tendência de vendas (dia a dia)
```python
df = pd.read_parquet('data/vendas_historico.parquet')

# Vendas totais por data
vendas_diarias = df.groupby('data_venda').agg({
    'valor_venda': lambda x: sum(x),
    'quantidade_vendida': 'sum'
}).sort_index()

print(vendas_diarias)
```

## 🔄 Comportamento Incremental

### Primeiro dia (29/11/25)
```
📊 Total de registros no banco: 26,839
📅 Registros por data:
   29/11/25: 26,839 registros
```

### Segundo dia (28/11/25)
```
📂 Banco existente encontrado, carregando...
📊 Registros existentes: 26,839
➕ Adicionando 26,839 novos registros
✅ Banco atualizado com sucesso!
📊 Total de registros no banco: 53,678

📅 Registros por data:
   28/11/25: 26,839 registros
   29/11/25: 26,839 registros
```

### Reprocessar data existente (29/11/25)
```
📂 Banco existente encontrado, carregando...
📊 Registros existentes: 53,678
⚠️  Encontrados 26,839 registros para 29/11/25
🔄 Removendo registros antigos dessa data...
✅ Registros removidos. Restam 26,839 registros
➕ Adicionando 26,839 novos registros
✅ Banco atualizado com sucesso!
📊 Total de registros no banco: 53,678
```

## 🎯 Integração com Sistema de Pedidos

O banco de vendas históricas será usado pelo **agente IA** para:

1. **Análise de tendências**
   - Comparar vendas dia a dia
   - Identificar produtos com crescimento/queda
   - Prever demanda futura

2. **Cálculo de pedidos inteligente**
   - Média de vendas dos últimos N dias
   - Sazonalidade por dia da semana
   - Ajuste de quantidades baseado em histórico

3. **Alertas e recomendações**
   - Produtos com vendas acima da média (risco de ruptura)
   - Produtos com vendas abaixo da média (risco de encalhe)
   - Lojas com performance atípica

## 📝 Exemplo de Uso pelo Sistema

```python
import pandas as pd
from datetime import datetime, timedelta

def calcular_pedido_inteligente(codigo_interno, loja, dias_historico=7):
    """
    Calcula quantidade de pedido baseado no histórico de vendas
    """
    df = pd.read_parquet('data/vendas_historico.parquet')
    
    # Últimos N dias
    datas = sorted(df['data_venda'].unique())[-dias_historico:]
    
    # Filtrar produto e loja
    historico = df[
        (df['codigo_interno'] == codigo_interno) &
        (df['loja'] == loja) &
        (df['data_venda'].isin(datas))
    ]
    
    if len(historico) == 0:
        return None
    
    # Média de vendas diárias
    media_vendas = historico['quantidade_vendida'].sum() / dias_historico
    
    # Cobertura de 4 dias + margem de segurança 20%
    quantidade_pedido = media_vendas * 4 * 1.2
    
    # Arredondar para múltiplo da embalagem
    embalagem = historico['embalagem'].iloc[0]
    quantidade_pedido = round(quantidade_pedido / embalagem) * embalagem
    
    return {
        'produto': codigo_interno,
        'loja': loja,
        'media_vendas_dia': media_vendas,
        'quantidade_pedido': quantidade_pedido,
        'embalagem': embalagem,
        'dias_analisados': len(historico)
    }
```

## 📊 Estatísticas Atuais do Banco

```
Total de registros: 53,678
Datas no banco: 28/11/25, 29/11/25
Lojas: 14
Produtos únicos: 5,046

Registros por data:
   28/11/25: 26,839 registros
   29/11/25: 26,839 registros

Top 5 seções:
   10 MERCEARIA SECA: 24,228 registros
   17 MAT LIMPEZA: 9,694 registros
   16 PERFUMARIA: 8,410 registros
   14 BEBIDAS: 8,156 registros
   23 OPLS: 1,630 registros
```

## 🔧 Manutenção

### Backup do Banco
```bash
# Windows PowerShell
Copy-Item data\vendas_historico.parquet data\backup\vendas_$(Get-Date -Format "yyyyMMdd").parquet
```

### Limpar dados antigos (manter últimos 30 dias)
```python
import pandas as pd
from datetime import datetime, timedelta

df = pd.read_parquet('data/vendas_historico.parquet')

# Converter datas para datetime
df['data_dt'] = pd.to_datetime(df['data_venda'], format='%d/%m/%y')

# Manter últimos 30 dias
data_corte = datetime.now() - timedelta(days=30)
df_recente = df[df['data_dt'] >= data_corte]

# Remover coluna temporária
df_recente = df_recente.drop(columns=['data_dt'])

# Salvar banco limpo
df_recente.to_parquet('data/vendas_historico.parquet', index=False)
print(f"Banco limpo: {len(df_recente)} registros mantidos")
```

## ✅ Próximos Passos

1. ✅ Banco Parquet implementado
2. ✅ Sistema incremental funcionando
3. ✅ Filtros de seção aplicados
4. ✅ Sugestão de data automática
5. 🔄 Integrar com sistema de pedidos
6. 🔄 Treinar agente IA com histórico
7. 🔄 Criar análises preditivas
