# Sistema de Gestão de Estoque com IA

Sistema inteligente para gestão de estoque e decisões de abastecimento de lojas a partir de um centro de distribuição, utilizando LLaMA 3 como modelo base.

## 🚀 Funcionalidades

- **Banco de Dados SQLite**: Base de dados com 7.835+ produtos do mix ativo
- **Gestão de Estoque**: Controle completo de produtos, quantidades e movimentações
- **Análise Inteligente**: Agente baseado em LLaMA 3 para análise e recomendações
- **Previsão de Demanda**: Análise de histórico e tendências de vendas
- **Alertas Automáticos**: Notificações de estoque baixo e necessidades de reposição
- **Otimização de Distribuição**: Sugestões inteligentes de abastecimento entre CD e lojas
- **Multi-Loja**: Suporte para 14 lojas com produtos específicos por unidade
- **API REST**: Interface para integração com outros sistemas
- **Dashboard CLI**: Interface de linha de comando para operações rápidas

## 📋 Requisitos

- Python 3.9+
- Ollama (para executar LLaMA 3 localmente)
- Bibliotecas: pandas, numpy, fastapi, uvicorn, requests

## 🔧 Instalação

```bash
# Instalar dependências
pip install -r requirements.txt

# Criar banco de dados SQLite a partir do mix.xlsx
python criar_banco.py

# Instalar Ollama (para LLaMA 3)
# Windows: Baixe de https://ollama.ai/download
# Após instalação, baixe o modelo LLaMA 3:
ollama pull llama3
```

## 💻 Uso Rápido

```python
from src.database import BancoDadosMix
from src.agente_estoque import AgenteEstoque

# Conectar ao banco de dados
db = BancoDadosMix()

# Buscar produtos
produtos = db.buscar_produtos("ARROZ")
print(f"Encontrados {len(produtos)} produtos")

# Consultar produtos de uma loja
produtos_loja = db.obter_produtos_por_loja("002")
print(f"Loja 002 tem {len(produtos_loja)} produtos ativos")

# Consultar agente IA
agente = AgenteEstoque()
# ... análises e recomendações
```

## 📊 Estrutura do Projeto

```
├── src/
│   ├── modelos.py          # Classes de dados (Produto, Estoque, Loja, CD)
│   ├── database.py         # Integração com SQLite
│   ├── agente_estoque.py   # Agente LLaMA 3
│   ├── analisador.py       # Análises e métricas
│   ├── gerenciador.py      # Gerenciamento central
│   ├── api.py              # API REST
│   └── cli.py              # Interface CLI
├── data/
│   ├── mix.xlsx            # Planilha original do mix
│   ├── banco.db            # Banco de dados SQLite (7.835 produtos)
│   ├── produtos.json       # Catálogo de produtos
│   ├── lojas.json          # Dados das lojas
│   └── centros.json        # Centros de distribuição
├── tests/
│   └── test_sistema.py     # Testes unitários
├── criar_banco.py          # Script para criar banco SQLite
├── consultar_banco.py      # Exemplos de consultas ao banco
├── exemplo.py              # Dados de exemplo
├── requirements.txt
└── README.md
```

## 🤖 Como Funciona o Agente

O agente utiliza LLaMA 3 para:
1. Analisar dados de estoque em tempo real
2. Considerar histórico de vendas e sazonalidade
3. Calcular ponto de reposição e estoque de segurança
4. Gerar recomendações personalizadas por loja
5. Priorizar transferências do CD

## 📝 Licença

MIT License
