# Guia de Instalação e Uso

## 🚀 Instalação Rápida

### 1. Pré-requisitos

- **Python 3.9 ou superior**
- **Ollama** (para executar LLaMA 3)

### 2. Instalar Ollama e LLaMA 3

#### Windows
```bash
# Baixe e instale o Ollama de: https://ollama.ai/download
# Após instalação, abra o terminal e execute:
ollama pull llama3
```

### 3. Instalar Dependências Python

```bash
# No diretório do projeto
pip install -r requirements.txt
```

## 📦 Inicialização com Dados de Exemplo

Para começar rapidamente com dados pré-configurados:

```bash
python exemplo.py
```

Este comando criará:
- 8 produtos de exemplo (arroz, feijão, óleo, etc.)
- 1 centro de distribuição com estoque
- 3 lojas com estoques variados
- 30 dias de histórico de vendas

## 💻 Formas de Uso

### 1. Interface CLI (Linha de Comando)

A forma mais fácil de interagir com o sistema:

```bash
python -m src.cli
```

Menu principal oferece:
- Gerenciar produtos
- Gerenciar lojas
- Consultar o agente IA
- Visualizar alertas
- Gerar relatórios

### 2. API REST

Inicie o servidor da API:

```bash
python -m src.api
```

A API estará disponível em: `http://localhost:8000`

Acesse a documentação interativa: `http://localhost:8000/docs`

#### Exemplos de requisições:

```bash
# Listar produtos
curl http://localhost:8000/produtos

# Obter alertas de uma loja
curl http://localhost:8000/lojas/loja001/alertas

# Consultar o agente IA
curl -X POST http://localhost:8000/agente/analise-abastecimento/loja001
```

### 3. Uso Programático

```python
from src.gerenciador import GerenciadorEstoque
from src.agente_estoque import AgenteEstoque

# Inicializar
gerenciador = GerenciadorEstoque()
agente = AgenteEstoque()

# Obter loja e CD
loja = gerenciador.lojas["loja001"]
cd = gerenciador.centros_distribuicao["cd001"]

# Consultar agente
resposta = agente.analisar_necessidade_abastecimento(loja, cd)
print(resposta)
```

## 🤖 Demonstrações do Agente IA

### Análise de Abastecimento

```bash
python exemplo.py agente
```

O agente LLaMA 3 analisará uma loja e recomendará:
- Produtos que precisam de reposição urgente
- Quantidades sugeridas
- Prioridades
- Justificativas baseadas em dados

### Análise de Estoque

```bash
python exemplo.py analise
```

Exibe alertas automáticos:
- Produtos em estoque crítico
- Produtos esgotados
- Cobertura insuficiente
- Capacidade das lojas

## 📊 Estrutura de Dados

### Produtos
```python
{
    "id": "prod001",
    "nome": "Arroz 5kg",
    "categoria": "Alimentos",
    "preco_venda": 24.90,
    "estoque_minimo": 20,
    "estoque_seguranca": 30
}
```

### Lojas
```python
{
    "id": "loja001",
    "nome": "Loja Centro",
    "endereco": "Rua Principal, 100",
    "capacidade_m3": 80.0
}
```

## 🔧 Configuração Avançada

### Mudar Modelo de IA

Por padrão, usa `llama3`. Para usar outro modelo:

```python
agente = AgenteEstoque(modelo="llama3.1:70b")
```

Modelos disponíveis no Ollama:
- `llama3` (padrão, 8B parâmetros)
- `llama3.1:70b` (mais poderoso)
- `llama2`

### Ajustar Parâmetros de Estoque

Edite os valores ao criar produtos:

```python
produto = Produto(
    # ...
    estoque_minimo=50,        # Nível mínimo antes de alertas
    estoque_seguranca=80,     # Nível de segurança recomendado
    tempo_reposicao_dias=7    # Tempo para reposição
)
```

## 🧪 Executar Testes

```bash
python -m unittest tests.test_sistema
```

## ⚠️ Solução de Problemas

### Erro: "Não foi possível conectar ao Ollama"

1. Verifique se o Ollama está rodando:
```bash
ollama list
```

2. Se não estiver instalado, instale de: https://ollama.ai/download

3. Baixe o modelo:
```bash
ollama pull llama3
```

### Erro: "Módulo não encontrado"

```bash
pip install -r requirements.txt
```

### Lentidão do Agente IA

O LLaMA 3 pode ser lento em hardware limitado. Considere:
- Usar um modelo menor: `llama2`
- Executar com GPU se disponível
- Aumentar recursos do sistema

## 📝 Próximos Passos

1. **Personalize os produtos**: Adicione produtos do seu negócio
2. **Configure suas lojas**: Crie lojas com endereços reais
3. **Importe dados reais**: Use o gerenciador para importar seu estoque
4. **Consulte o agente**: Pergunte sobre estratégias de abastecimento
5. **Automatize**: Use a API para integrar com outros sistemas

## 🔗 Recursos Adicionais

- **Documentação da API**: `http://localhost:8000/docs` (quando rodando)
- **Ollama**: https://ollama.ai
- **LLaMA 3**: https://llama.meta.com

## 💡 Dicas de Uso

1. **Mantenha histórico de vendas atualizado** para previsões mais precisas
2. **Configure alertas** com níveis adequados ao seu negócio
3. **Consulte o agente regularmente** para decisões estratégicas
4. **Use a API** para integrar com ERPs existentes
5. **Ajuste parâmetros** conforme aprende sobre seu negócio
