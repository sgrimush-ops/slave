# MANUAL DO USUÁRIO - SISTEMA DE GESTÃO DE ESTOQUE
==================================================

## Requisitos do Sistema

- **Sistema Operacional**: Windows 10 ou 11 (64-bit)
- **Memória RAM**: Mínimo 4GB (recomendado 8GB)
- **Espaço em Disco**: 500MB livres
- **Ollama** (opcional, para Agente IA): https://ollama.ai

## Instalação

1. **Download**: Baixe o arquivo `GestaoEstoque.zip`
2. **Extrair**: Descompacte em uma pasta de sua escolha
3. **Executar**: Dê duplo clique em `GestaoEstoque.exe`

**Primeira Execução**:
- O Windows pode mostrar aviso de segurança
- Clique em "Mais informações" → "Executar assim mesmo"
- Isso é normal para programas não assinados digitalmente

## Guia de Uso Passo a Passo

### 1️⃣ Importar Arquivos

**O que fazer**:
1. Clique em **"Selecionar..."** ao lado de "Arquivo de Vendas (CSV)"
2. Escolha seu arquivo de vendas diárias (formato CSV, separado por `;`)
3. Clique em **"Importar para data/"**
4. Repita para "Arquivo Gerado (Excel)"

**Importante**: 
- Os arquivos devem estar no formato correto
- CSV de vendas deve ter 31 colunas conforme layout padrão
- Excel gerado deve conter dados processados anteriormente

### 2️⃣ Processar Vendas Diárias

**O que fazer**:
1. Digite a data no formato `dd/mm/aa` (exemplo: `29/11/25`)
2. Clique em **"Processar Vendas"**
3. Aguarde o processamento (30 segundos a 2 minutos)

**O que acontece**:
- ✅ Filtra seções relevantes (10, 13, 14, 16, 17, 23)
- ✅ Remove produtos sem ponto de pedido ou embalagem
- ✅ Normaliza códigos e lojas com zeros à esquerda
- ✅ Converte valores do formato brasileiro (1.234,56)
- ✅ Salva em Excel: `data/resultado_abc.xlsx`
- ✅ Atualiza histórico: `data/vendas_historico.parquet`

**Resultado**: 
```
Total de linhas processadas: ~26.000-30.000
Arquivo Excel gerado com 13 colunas
Banco Parquet atualizado
```

### 3️⃣ Executar Análise Completa

**O que fazer**:
1. Clique em **"Executar Analista Completo"**
2. Aguarde (pode demorar 2-5 minutos)

**O que acontece**:
- ✅ Calcula sugestões de pedido por loja
- ✅ Aplica estratégias de balanceamento:
  - **Giro Saudável**: 4-6 dias de cobertura
  - **Comprador**: Respeita valores do comprador
  - **Giro Otimizado**: Ajusta para evitar excessos/rupturas
- ✅ Analisa cada produto individualmente
- ✅ Gera relatórios detalhados

**Arquivos gerados**:
- `data/sugestao_ia.xlsx` - Sugestões de pedido
- `data/analise_estrategias.xlsx` - Análise detalhada

### 4️⃣ Consultar Agente IA

**Requisitos**:
- Ollama instalado e rodando
- Modelo instalado: `ollama pull llama3.2` ou `ollama pull gemma3:4b`

**Como usar**:
1. Digite sua pergunta no campo de texto
2. Pressione **Enter** ou clique em **"Consultar Agente"**
3. Aguarde a resposta (10-30 segundos)

**Exemplos de perguntas**:
```
qual estoque do CD para o cod 21771?
qual foi a venda da loja 4 no dia 29?
qual estoque da loja 7 do produto 21771?
quantos dias de cobertura tem o produto 1023328?
qual a estratégia recomendada para o cod 149419?
```

**Dicas**:
- ✅ Mencione códigos de produtos (4-7 dígitos)
- ✅ Mencione lojas específicas se quiser filtrar
- ✅ Use "CD" para se referir ao Centro de Distribuição
- ✅ Pressione **Ctrl+Enter** para nova linha (Enter envia)
- ✅ Use **"Limpar Pergunta"** para começar nova consulta

### 5️⃣ Verificar Resultados

**Abrir arquivos Excel**:
- Clique em **"Abrir Arquivo Sugestões"** para ver pedidos sugeridos
- Abra manualmente os arquivos em `data/` com Excel

**Ver Histórico**:
- Clique em **"Ver Histórico de Vendas"** para análises temporais

## Estrutura de Pastas

```
GestaoEstoque/
│
├── GestaoEstoque.exe      # Executável principal
├── LEIA-ME.txt           # Instruções básicas
│
└── data/                 # Pasta de dados (criada automaticamente)
    ├── colunas.txt       # Mapeamento de colunas
    ├── grid_tmp_abcmerc.csv      # CSV importado
    ├── gerado.xlsx               # Excel importado
    ├── resultado_abc.xlsx        # Resultado processado
    ├── vendas_historico.parquet  # Banco histórico
    ├── sugestao_ia.xlsx          # Sugestões de pedido
    └── analise_estrategias.xlsx  # Análise detalhada
```

## Estratégias de Balanceamento

### 1. Giro Saudável
**Quando usar**: Produtos novos ou sem histórico confiável
**Lógica**: 4-6 dias de cobertura ideal
**Objetivo**: Evitar rupturas e capital parado

### 2. Valores do Comprador
**Quando usar**: Comprador definiu valores adequados
**Lógica**: Respeita ponto_pedido e estoque_ideal do comprador
**Objetivo**: Manter exposição visual ideal

### 3. Giro Otimizado
**Quando usar**: Valores do comprador geram giro inadequado
**Lógica**: Ajusta para 4-6 dias, mas mantém múltiplos de embalagem
**Objetivo**: Equilibrar exposição visual com giro saudável

## Interpretando Resultados

### Coluna "sugestao" (sugestao_ia.xlsx)
- **> 0**: Quantidade sugerida para pedir
- **0 ou vazio**: Estoque suficiente, não pedir

### Coluna "estrategia" (analise_estrategias.xlsx)
- **COMPRADOR**: Valores adequados, mantidos
- **GIRO_OTIMIZADO (↑)**: Ajustado para cima (evitar ruptura)
- **GIRO_OTIMIZADO (↓)**: Ajustado para baixo (evitar excesso)

### Dias de Cobertura
- **< 4 dias**: 🔴 Risco de ruptura
- **4-6 dias**: 🟢 Ideal
- **> 6 dias**: 🟡 Capital parado

## Solução de Problemas

### ❌ "Ollama não encontrado"
**Solução**:
1. Instale Ollama: https://ollama.ai
2. Abra CMD e execute: `ollama serve`
3. Em outro CMD: `ollama pull llama3.2`
4. Tente novamente no aplicativo

### ❌ "Arquivo CSV não encontrado"
**Solução**:
1. Verifique se selecionou o arquivo correto
2. Clique em "Importar para data/" após selecionar
3. Confirme que arquivo aparece em `data/`

### ❌ "Erro ao processar vendas"
**Causas comuns**:
- CSV não está no formato correto (31 colunas)
- Separador diferente de `;` (ponto e vírgula)
- Encoding incorreto (deve ser UTF-8 ou Latin-1)

**Solução**:
1. Abra o CSV no Excel
2. Salve como → CSV (delimitado por ponto e vírgula)
3. Tente novamente

### ❌ "Agente não responde"
**Verificar**:
1. Ollama está rodando? (CMD: `ollama list`)
2. Modelo instalado? (CMD: `ollama list`)
3. Internet necessária? (Não, Ollama roda local)

**Solução**:
```cmd
# Parar Ollama
Ctrl+C no terminal do ollama serve

# Reiniciar
ollama serve

# Testar
ollama run llama3.2 "teste"
```

### ❌ Aplicativo não abre
**Solução**:
1. Antivírus bloqueando? Adicione exceção
2. Windows Defender: "Mais informações" → "Executar"
3. Faltam arquivos? Re-extraia o ZIP completo
4. Execute como administrador (botão direito)

## Dicas de Performance

### ⚡ Processamento Rápido
- Feche programas pesados (Chrome, etc)
- Processe um dia por vez
- Limpe arquivos antigos de `data/` periodicamente

### ⚡ Agente IA Rápido
- Use modelos menores: `gemma3:4b` (3GB) é mais rápido que `llama3` (4.7GB)
- Feche outros programas ao usar o agente
- Faça perguntas específicas (evite "analise tudo")

### ⚡ Espaço em Disco
- Arquivo Parquet cresce com o tempo
- Recomendado: Limpar dados antigos a cada 3 meses
- Fazer backup antes de limpar

## Backup e Manutenção

### 📁 Fazer Backup
**Importante**: Faça backup regular da pasta `data/`

```powershell
# Criar backup manual
Compress-Archive -Path data\* -DestinationPath backup_2025-11-30.zip
```

**Arquivos críticos**:
- ✅ `vendas_historico.parquet` - Histórico completo
- ✅ `sugestao_ia.xlsx` - Última análise
- ⚠️ `grid_tmp_abcmerc.csv` - Pode re-importar
- ⚠️ `resultado_abc.xlsx` - Pode reprocessar

### 🔧 Limpeza
**Quando fazer**: A cada 3 meses ou se disco cheio

**O que limpar**:
```powershell
# Arquivos seguros para deletar
del data\grid_tmp_abcmerc.csv
del data\resultado_abc.xlsx
del data\analise_estrategias.xlsx

# CUIDADO: Não delete estes
# vendas_historico.parquet (histórico acumulado)
# sugestao_ia.xlsx (última análise)
```

## Suporte e Contato

Para dúvidas ou problemas:
1. Consulte este manual
2. Verifique `BUILD_GUIDE.md` (detalhes técnicos)
3. Entre em contato com suporte

**Versão**: 1.0  
**Data**: 30/11/2025  
**Sistema**: Gestão de Estoque ABC com IA
