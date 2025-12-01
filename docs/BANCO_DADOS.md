# 📊 Banco de Dados SQLite - Mix de Produtos

## Visão Geral

O sistema utiliza um banco de dados SQLite criado a partir da planilha `mix.xlsx`, contendo informações sobre os produtos ativos no mix de vendas.

### Estatísticas do Banco

- **Total de Produtos**: 7.835 itens
- **Origens/Fornecedores**: 2 principais (Baklizi, Nestlé)
- **Lojas Cadastradas**: 14 unidades
- **Arquivo**: `data/banco.db`

## 🗄️ Estrutura do Banco

### Tabela: `mix_produtos`

| Coluna | Tipo | Descrição |
|--------|------|-----------|
| `codigo_interno` | INTEGER | Código interno do produto |
| `codigo_ean` | INTEGER | Código de barras EAN |
| `descricao` | TEXT | Descrição completa do produto |
| `embalagem` | INTEGER | Quantidade de unidades por embalagem |
| `origem` | TEXT | Fornecedor/origem do produto |
| `loja_ativa_mix` | TEXT | Lojas onde o produto está ativo (formato: "002-003-004-...") |

### Tabela: `metadados`

Armazena informações sobre a importação e atualizações do banco.

## 🔍 Como Usar

### 1. Criar o Banco de Dados

```bash
python criar_banco.py
```

Este comando:
- Lê o arquivo `data/mix.xlsx`
- Cria o banco SQLite `data/banco.db`
- Importa todos os produtos
- Cria índices para otimização

### 2. Consultar o Banco

#### Via Python

```python
from src.database import BancoDadosMix

# Conectar
db = BancoDadosMix()

# Buscar produtos
produtos = db.buscar_produtos("ARROZ")
for prod in produtos:
    print(f"{prod['descricao']} - {prod['origem']}")

# Obter estatísticas
stats = db.obter_estatisticas()
print(f"Total: {stats['total_produtos']} produtos")

# Produtos por loja
produtos_loja = db.obter_produtos_por_loja("002")
print(f"Loja 002: {len(produtos_loja)} produtos")

# Fechar conexão
db.fechar()
```

#### Via Script de Consulta

```bash
python consultar_banco.py
```

Exibe:
- Estatísticas gerais
- Busca de produtos
- Produtos por origem
- Produtos por loja
- Exemplos de conversão

### 3. Integração com o Sistema

```bash
python demo_integracao.py
```

Demonstra:
- Conexão ao banco
- Criação de lojas baseadas no mix
- Importação de produtos
- Distribuição para lojas
- Relatórios integrados

## 📋 Consultas SQL Úteis

### Total de Produtos
```sql
SELECT COUNT(*) FROM mix_produtos;
```

### Produtos por Origem
```sql
SELECT origem, COUNT(*) as total 
FROM mix_produtos 
GROUP BY origem 
ORDER BY total DESC;
```

### Produtos de uma Loja Específica
```sql
SELECT * FROM mix_produtos 
WHERE loja_ativa_mix LIKE '%002%';
```

### Buscar por Descrição
```sql
SELECT * FROM mix_produtos 
WHERE descricao LIKE '%ARROZ%' 
LIMIT 10;
```

### Produtos por Código EAN
```sql
SELECT * FROM mix_produtos 
WHERE codigo_ean = 7891000113295;
```

## 🏪 Códigos das Lojas

As 14 lojas cadastradas no sistema:

- 001, 002, 003, 004, 005, 006, 007, 008
- 011, 012, 013, 014, 017, 018

**Nota**: Cada produto tem uma lista de lojas onde está ativo, armazenada no campo `loja_ativa_mix`.

## 📦 Principais Fornecedores

1. **Baklizi**: 7.540 produtos (~96%)
2. **Nestlé**: 295 produtos (~4%)

## 🔄 Conversão para o Sistema

O módulo `database.py` fornece o método `converter_para_produto()` que transforma registros do banco em objetos `Produto` do sistema:

```python
# Buscar produto no banco
produto_mix = db.obter_produto_por_codigo_interno(1012475)

# Converter para objeto Produto
produto = db.converter_para_produto(
    produto_mix,
    preco_custo=12.50,
    preco_venda=19.90
)

# Agora pode ser usado no sistema
gerenciador.adicionar_produto_catalogo(produto)
```

## 🛠️ Manutenção

### Atualizar o Banco

Quando o arquivo `mix.xlsx` for atualizado:

```bash
# Remove banco antigo
rm data/banco.db

# Cria novo banco
python criar_banco.py
```

### Backup

```bash
# Copiar banco de dados
copy data\banco.db data\banco_backup.db
```

### Verificar Integridade

```python
from src.database import BancoDadosMix

db = BancoDadosMix()
stats = db.obter_estatisticas()
print(f"Total de produtos: {stats['total_produtos']}")
print(f"Origens: {stats['total_origens']}")
```

## 🔌 API REST - Endpoints do Banco

Com a API REST rodando, você pode consultar o banco via HTTP:

```bash
# Iniciar API
python -m src.api

# Consultar via curl (exemplos futuros)
curl http://localhost:8000/produtos/buscar?termo=ARROZ
curl http://localhost:8000/lojas/002/produtos-mix
```

## 💡 Dicas de Uso

1. **Use índices**: O banco já tem índices criados para `codigo_interno`, `produto` e `categoria`
2. **Paginação**: Para grandes conjuntos, use `listar_produtos_paginado()`
3. **Context Manager**: Use `with BancoDadosMix() as db:` para garantir fechamento da conexão
4. **Cache**: Considere cachear consultas frequentes em memória
5. **Filtros**: Combine filtros (origem + loja) para buscas mais específicas

## 🚀 Exemplos Avançados

### Buscar produtos comuns entre duas lojas

```python
db = BancoDadosMix()

# Produtos da loja 002
loja_002 = set(p['codigo_interno'] for p in db.obter_produtos_por_loja("002"))

# Produtos da loja 003
loja_003 = set(p['codigo_interno'] for p in db.obter_produtos_por_loja("003"))

# Produtos comuns
comuns = loja_002 & loja_003
print(f"Produtos em ambas as lojas: {len(comuns)}")
```

### Importar todos os produtos para o sistema

```python
from src.database import BancoDadosMix
from src.gerenciador import GerenciadorEstoque

db = BancoDadosMix()
gerenciador = GerenciadorEstoque()

# Importar com preços fictícios
precos = {}  # Dict com preços reais se disponível

produtos_importados = db.importar_produtos_para_catalogo(
    gerenciador, 
    precos
)

print(f"Importados: {produtos_importados} produtos")
```

## 📞 Suporte

Para problemas com o banco de dados:

1. Verifique se `data/mix.xlsx` existe
2. Execute `python criar_banco.py` novamente
3. Verifique logs de erro no terminal
4. Consulte `data/banco.db` diretamente com ferramentas SQLite

## 🔗 Ferramentas Úteis

- **DB Browser for SQLite**: https://sqlitebrowser.org/
- **SQLite CLI**: Incluído no Python
- **VSCode Extension**: SQLite Viewer

```bash
# Abrir banco no SQLite CLI
sqlite3 data/banco.db

# Comandos úteis no CLI
.tables          # Listar tabelas
.schema          # Ver estrutura
.headers on      # Mostrar cabeçalhos
.mode column     # Modo coluna
```
