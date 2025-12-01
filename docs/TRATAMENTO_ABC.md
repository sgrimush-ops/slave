# Instruções de Uso - tratamento_abc.py

## 📋 Pré-requisitos

1. **Arquivos necessários:**
   - `data/grid_tmp_abcmerc.csv` - Arquivo CSV com dados ABC
   - `data/colunas.txt` - Definição dos nomes das colunas (já existe)

2. **Formato do CSV:**
   - Separador: `;` (ponto e vírgula)
   - Sem cabeçalho (primeira linha já é dado)
   - Número de colunas deve corresponder ao colunas.txt

## 🚀 Como Usar

```bash
python tratamento_abc.py
```

O sistema irá:
1. ✅ Ler nomes das colunas de `data/colunas.txt`
2. ✅ Ler dados de `data/grid_tmp_abcmerc.csv`
3. ✅ Nomear as colunas
4. ✅ Remover colunas desnecessárias
5. ❓ Solicitar a data de venda (formato: dd/mm/yy)
6. ✅ Adicionar coluna data_venda
7. ✅ Gerar `data/resultado_abc.xlsx`

## 📊 Colunas Removidas

As seguintes colunas serão removidas do resultado final:
- percentual_venda
- posicao_venda
- percentual_acumulado
- valor_margem
- percentual_margem
- participacao
- posicao_margem
- acumulo_margem
- ranking_margem
- cmv_bruto
- cmv_liquido
- fornecedor_principal
- tributação
- usuario
- departamento
- grupo
- subgrupo
- secao
- tipo_comercial
- rankin_venda

## 📈 Colunas Mantidas

- loja
- codigo_interno
- descricao
- valor_venda
- quantidade_vendida
- ponto_pedido
- estoque_ideal
- embalagem
- capacidade
- estoque
- estoque_cd
- **data_venda** (adicionada pelo sistema)

## 💡 Exemplo de Uso

```
$ python tratamento_abc.py

============================================================
TRATAMENTO DE DADOS ABC
============================================================

📂 Lendo nomes das colunas de: data/colunas.txt
✅ 32 colunas encontradas

📂 Lendo arquivo CSV: data/grid_tmp_abcmerc.csv
✅ Arquivo lido: 1000 linhas, 32 colunas

✅ Colunas nomeadas: ['loja', 'codigo_interno', ...]

🗑️  Removendo 19 colunas:
   - percentual_venda
   - posicao_venda
   ...

✅ Colunas removidas. Restaram 13 colunas

============================================================
INFORMAR DATA DE VENDA
============================================================

Digite a data de venda (formato dd/mm/yy): 30/11/25
✅ Data válida: 30/11/25

✅ Coluna 'data_venda' adicionada com valor: 30/11/25

============================================================
PREVIEW DOS DADOS (primeiras 5 linhas)
============================================================
   loja  codigo_interno     descricao  ...  data_venda
0     1         1234567  Produto Teste  ...   30/11/25

💾 Salvando arquivo Excel: data/resultado_abc.xlsx
✅ Arquivo salvo com sucesso!
   Total de linhas: 1000
   Total de colunas: 14

============================================================
ESTATÍSTICAS
============================================================
Linhas processadas: 1000
Colunas finais: 14
Data de venda: 30/11/25

Colunas mantidas:
  1. loja
  2. codigo_interno
  3. descricao
  4. valor_venda
  5. quantidade_vendida
  6. ponto_pedido
  7. estoque_ideal
  8. embalagem
  9. capacidade
  10. estoque
  11. estoque_cd
  12. data_venda

============================================================
PROCESSAMENTO CONCLUÍDO!
============================================================
```

## ⚠️ Possíveis Erros

### Arquivo não encontrado
```
❌ Arquivo grid_tmp_abcmerc.csv não encontrado!
```
**Solução:** Coloque o arquivo na pasta `data/`

### Data inválida
```
❌ Data inválida! Use o formato dd/mm/yy (exemplo: 30/11/25)
```
**Solução:** Digite a data no formato correto: dd/mm/yy

### Número de colunas diferente
```
⚠️  ATENÇÃO: CSV tem 30 colunas, mas colunas.txt tem 32 nomes
```
**Solução:** O sistema usará apenas as colunas disponíveis

## 🔍 Próximos Passos

Após gerar o `resultado_abc.xlsx`, você pode:
1. Abrir o arquivo no Excel para revisar
2. Integrar com o sistema principal
3. Processar os dados adicionais conforme necessário
