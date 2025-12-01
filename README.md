# Sistema de Gestão de Estoque com IA

Sistema inteligente de gestão de estoque usando LLaMA 3 com histórico de vendas para análises robustas.

## 🚀 Instalação Rápida (Windows - Sem Admin)

```bash
# 1. Criar ambiente virtual
python -m venv .venv
.venv\Scripts\activate

# 2. Instalar dependências
pip install -r requirements.txt

# 3. Iniciar interface
python interface.py
```

📖 **Guia Completo**: [INSTALACAO_WINDOWS.md](INSTALACAO_WINDOWS.md) - Passo a passo detalhado para Windows sem permissão de administrador

## ⭐ Arquivos Principais (Raiz)

### 1. **analista.py** - Sistema Mestre
```bash
python analista.py
```
Executa todo o processo automaticamente:
- Calcula sugestões com balanceamento inteligente
- Gera análises de estratégias  
- Inicia sistema interativo com agente LLaMA 3

**Pré-requisitos:**
- `data/banco.db` (7.835 produtos)
- `data/vendas_historico.parquet` (opcional, mas recomendado)

### 2. **tratamento_abc.py** - Processar Vendas
```bash
python tratamento_abc.py
```
Processa vendas diárias e atualiza histórico:
- Lê CSV de vendas do dia
- Aplica filtros (seções: 10, 13, 14, 16, 17, 23)
- Remove produtos inválidos (ponto_pedido=0 ou embalagem=0)
- Salva Excel + atualiza banco Parquet
- Sugere data do dia anterior automaticamente

## 🎯 Funcionalidades

### Balanceamento Inteligente
- ✅ Respeita valores do comprador quando adequados (4-6 dias)
- ⚙️ Ajusta valores anti-econômicos automaticamente
- 📈 Aprende com padrões de exposição visual

### Histórico de Vendas
- 📊 Médias de vendas por produto/loja
- 📈 Detecção de tendências (crescimento/queda)
- 🎯 Cálculo preciso de cobertura
- 🤖 Agente IA com contexto histórico

## 📁 Estrutura

```
📂 slave/
│
├── analista.py                       ⭐ SISTEMA MESTRE
├── tratamento_abc.py                 ⭐ PROCESSAR VENDAS
├── README.md
├── requirements.txt
│
├── 📂 data/                          Dados do sistema
│   ├── banco.db                      SQLite: produtos, lojas
│   ├── vendas_historico.parquet      Histórico de vendas
│   ├── sugestao_ia.xlsx              Sugestões geradas
│   ├── resultado_abc.xlsx            Vendas processadas
│   ├── mix.xlsx                      Base de produtos
│   ├── grid_tmp_abcmerc.csv         Vendas brutas (input)
│   └── colunas.txt                   Definição de colunas
│
├── 📂 src/                           Código-fonte
│   ├── agente_estoque.py            Agente LLaMA 3
│   ├── analise_historico.py         ⭐ Análise de vendas
│   ├── calculador_pedido.py         Cálculo de sugestões
│   ├── regras_negocio.py            Regras configuráveis
│   ├── database.py                  SQLite
│   ├── modelos.py                   Classes de dados
│   ├── gerenciador.py               Gerenciamento
│   ├── analisador.py                Análise de estoque
│   ├── api.py                       API REST
│   └── cli.py                       Interface CLI
│
├── 📂 scripts/                      Scripts auxiliares
│   ├── atualizar_simples.py         Atualização rápida
│   ├── analisar_estrategias.py      Análise de estratégias
│   ├── criar_banco.py               Criar banco
│   └── ...                          Outros scripts
│
├── 📂 utilitarios/                  Ferramentas utilitárias
│   ├── consultar_vendas.py          Menu consultas históricas
│   └── testar_agente_historico.py   Teste de integração IA
│
├── 📂 docs/                         Documentação
│   ├── GUIA_INTERFACE.md            ⭐ Guia da interface gráfica
│   └── ...                          Outros guias
│
├── interface.py                      ⭐ INTERFACE GRÁFICA
├── criar_executavel.py              Criar .exe do sistema
├── iniciar_interface.bat            Launcher Windows
│
├── 📂 utilitarios/                  ⭐ Ferramentas
│   ├── consultar_vendas.py          Consultar histórico
│   └── testar_agente_historico.py   Testar integração IA
│
├── 📂 launchers/                    Launchers individuais
│   ├── criar_db.py
│   ├── calcular_pedidos.py
│   ├── iniciar_api.py
│   └── iniciar_cli.py
│
├── 📂 docs/                         Documentação completa
│   ├── BANCO_VENDAS_PARQUET.md      ⭐ Banco histórico
│   ├── INTEGRACAO_AGENTE_HISTORICO.md ⭐ Integração IA
│   ├── ESTRATEGIA_BALANCEAMENTO.md  Estratégias
│   ├── GUIA_AGENTE_IA.md           Como o agente aprende
│   ├── TRATAMENTO_ABC.md           Processamento vendas
│   ├── BANCO_DADOS.md              Estrutura do banco
│   └── CALCULADOR_PEDIDO.md        Lógica de cálculo
│
└── 📂 exemplos/                     Exemplos de uso
```

## 🚀 Workflow Completo

### Opção 1: Interface Gráfica (Recomendado) 🖥️

```bash
# Iniciar interface
python interface.py

# Ou use o launcher batch (Windows)
iniciar_interface.bat
```

**Vantagens**:
- ✅ Importação visual de arquivos
- ✅ Todas as funcionalidades com um clique
- ✅ Log em tempo real
- ✅ Consultas ao agente IA facilitadas
- ✅ Não precisa conhecer comandos

📖 **Guia Completo**: [docs/GUIA_INTERFACE.md](docs/GUIA_INTERFACE.md)

---

### Opção 2: Linha de Comando

#### 1. Configuração Inicial (Uma vez)
```bash
# Instalar dependências
pip install -r requirements.txt

# Criar banco de dados
python launchers/criar_db.py
```

#### 2. Rotina Diária
```bash
# Processar vendas do dia anterior
python tratamento_abc.py
# (Confirmar data ou pressionar ENTER)

# Executar análise e gerar pedidos
python analista.py
```

#### 3. Consultas e Análises
```bash
# Consultar histórico de vendas
python utilitarios/consultar_vendas.py

# Testar agente IA com histórico
python utilitarios/testar_agente_historico.py
```

## 📊 Estratégias de Pedido

### 1. "Comprador" ✅
- **Quando:** Valores resultam em 4-6 dias de cobertura
- **Ação:** Respeita ponto_pedido e estoque_ideal
- **Razão:** Comprador otimizou para exposição visual

### 2. "Giro Otimizado" ⚙️
- **Quando:** Valores resultam em <4 ou >6 dias
- **Ação:** Ajusta para range de 4-6 dias
- **Razão:** Evita capital parado ou rupturas

### 3. "Giro Saudável" 📈
- **Quando:** Sem valores do comprador
- **Ação:** Aplica padrão de 4 dias
- **Razão:** Melhores práticas de gestão

## 📈 Exemplo de Análise com Histórico

```
LEITE UHT STA CLARA INTEGRAL 1L (Loja 11)

Histórico (2 dias):
- Média: 735 un/dia
- Tendência: QUEDA (-17.4%)
- Total vendido: 1,470 unidades

Situação Atual:
- Estoque: 100 unidades
- Cobertura: 0.1 dias (CRÍTICO!)
- Status: Necessidade urgente

Recomendação IA:
- Pedir: 2,840 unidades (240 embalagens)
- Estratégia: "giro_otimizado"
- Cobertura desejada: 4 dias
- Justificativa: Baseado em média real + ajuste por tendência
```

## 🔧 Requisitos

- Python 3.11+
- Ollama com modelo LLaMA 3
- Bibliotecas: pandas, numpy, pyarrow, ollama, fastapi, uvicorn, openpyxl

## 📖 Documentação

Consulte `docs/` para documentação detalhada:
- **BANCO_VENDAS_PARQUET.md** - Banco de histórico de vendas
- **INTEGRACAO_AGENTE_HISTORICO.md** - Integração IA + histórico
- **ESTRATEGIA_BALANCEAMENTO.md** - Estratégias de balanceamento
- **GUIA_AGENTE_IA.md** - Como o agente LLaMA 3 aprende

## 💡 Comandos Rápidos

```bash
# Sistema completo
python analista.py

# Processar vendas
python tratamento_abc.py

# Consultar histórico
python utilitarios/consultar_vendas.py

# Testar IA
python utilitarios/testar_agente_historico.py

# Criar banco (primeira vez)
python launchers/criar_db.py

# API REST
python launchers/iniciar_api.py

# CLI interativo
python launchers/iniciar_cli.py
```

## 📊 Dados Atuais

- **Produtos:** 7.835
- **Lojas:** 14
- **Fornecedores:** 2
- **Histórico:** 53.769 registros (2 dias)
- **Produtos com histórico:** 5.545
- **Seções ativas:** 6 (10, 13, 14, 16, 17, 23)

## 🎯 Benefícios

### Antes (sem histórico):
- ❌ Decisões baseadas apenas em valores estáticos
- ❌ Sem considerar tendências
- ❌ Estoque de segurança genérico

### Agora (com histórico):
- ✅ Decisões baseadas em vendas reais
- ✅ Detecta produtos em crescimento/queda
- ✅ Ajusta automaticamente para tendências
- ✅ Estoque de segurança calculado por produto
- ✅ Redução de rupturas e excessos
- ✅ Previsões mais precisas

## 🤝 Suporte

Para dúvidas ou sugestões, consulte a documentação em `docs/` ou entre em contato com a equipe de desenvolvimento.
