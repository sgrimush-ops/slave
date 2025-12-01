# GUIA RÁPIDO - Sistema de Gestão de Estoque

## 🖥️ INTERFACE GRÁFICA (Novo!)

```bash
# Iniciar interface
python interface.py

# Ou use o launcher (Windows)
iniciar_interface.bat
```

**Todas as funcionalidades com interface visual:**
- Importar arquivos
- Processar vendas
- Gerar sugestões
- Consultar agente IA
- Ver logs em tempo real

📖 [Guia Completo da Interface](docs/GUIA_INTERFACE.md)

---

## 📌 Arquivos Principais

### Na Raiz do Projeto (sempre visíveis):

1. **interface.py** ⭐ Interface Gráfica
   - Interface visual completa
   - Todas as funcionalidades integradas
   
2. **analista.py** ⭐ Sistema Mestre
   - Executa todo o processo automaticamente
   - Calcula sugestões + Análises + Agente IA
   
3. **tratamento_abc.py** ⭐ Processar Vendas Diárias
   - Processa vendas do dia anterior
   - Atualiza histórico no banco Parquet

---

## 🚀 Comandos Essenciais (Linha de Comando)

### Primeira Vez (Configuração)
```bash
# 0. Verificar ambiente (RECOMENDADO)
python verificar_ambiente.py

# 1. Criar ambiente virtual
python -m venv .venv
.venv\Scripts\activate

# 2. Instalar dependências
pip install -r requirements.txt

# 3. Criar banco de dados
python launchers/criar_db.py
```

📖 **Instalação Detalhada**: [INSTALACAO_WINDOWS.md](INSTALACAO_WINDOWS.md) - Guia completo para Windows sem admin

### Rotina Diária
```bash
# 1. Processar vendas (todos os dias)
python tratamento_abc.py

# 2. Executar análise e gerar pedidos
python analista.py
```

### Consultas
```bash
# Consultar histórico de vendas
python utilitarios/consultar_vendas.py

# Testar agente IA com histórico
python utilitarios/testar_agente_historico.py
```

---

## 📊 Pré-requisitos

✅ **Obrigatórios:**
- `data/banco.db` - Banco de produtos/lojas
  - Execute: `python launchers/criar_db.py`

⭐ **Recomendados:**
- `data/vendas_historico.parquet` - Histórico de vendas
  - Execute: `python tratamento_abc.py`
  - Melhora muito as análises do agente IA!

---

## 📁 Arquivos de Entrada/Saída

### Entrada (você fornece):
- `data/mix.xlsx` - Base de produtos
- `data/grid_tmp_abcmerc.csv` - Vendas brutas do dia

### Saída (sistema gera):
- `data/sugestao_ia.xlsx` - Sugestões de pedidos
- `data/resultado_abc.xlsx` - Vendas processadas
- `data/vendas_historico.parquet` - Histórico acumulado

---

## 🎯 Workflow Típico

```
1. Segunda-feira (início da semana):
   ├─> Baixar arquivo de vendas (grid_tmp_abcmerc.csv)
   ├─> python tratamento_abc.py
   │   └─> Confirma data: 29/11/25 (domingo)
   ├─> python analista.py
   │   └─> Gera sugestões de pedidos
   └─> Revisar: data/sugestao_ia.xlsx

2. Terça a Sexta (diariamente):
   └─> Repetir processo acima para cada dia

3. Consultas (quando necessário):
   ├─> python utilitarios/consultar_vendas.py
   │   └─> Ver histórico, tendências, top produtos
   └─> python utilitarios/testar_agente_historico.py
       └─> Testar análises da IA
```

---

## 💡 Dicas Importantes

### tratamento_abc.py
- ✅ Sugere automaticamente o dia anterior
- ✅ Pressione ENTER para aceitar ou digite data (dd/mm/yy)
- ✅ Se executar mesma data novamente, atualiza (não duplica)
- ✅ Filtra automaticamente seções: 10, 13, 14, 16, 17, 23
- ✅ Remove produtos com ponto_pedido=0 ou embalagem=0

### analista.py
- ✅ Verifica se banco de dados existe
- ✅ Avisa se histórico não existe (mas continua)
- ✅ Com histórico: análises muito mais precisas
- ✅ Sem histórico: usa apenas dados atuais

---

## 📈 Estratégias de Pedido

O sistema escolhe automaticamente entre:

1. **"comprador"** - Respeita valores quando adequados (4-6 dias)
2. **"giro_otimizado"** - Ajusta valores anti-econômicos
3. **"giro_saudavel"** - Padrão de 4 dias quando sem valores

---

## ❓ Problemas Comuns

### "Banco de dados não encontrado"
```bash
python launchers/criar_db.py
```

### "Histórico de vendas não encontrado"
```bash
python tratamento_abc.py
# (Execute pelo menos uma vez)
```

### "Ollama não está rodando"
- Inicie o Ollama
- Verifique se modelo LLaMA 3 está instalado
- Teste: `ollama run llama3`

### "Erro ao ler CSV de vendas"
- Verifique se `data/grid_tmp_abcmerc.csv` existe
- Arquivo usa encoding latin-1
- Separador: ponto-e-vírgula (;)

---

## 📚 Documentação Completa

Para mais detalhes, consulte:
- `README.md` - Documentação completa
- `docs/BANCO_VENDAS_PARQUET.md` - Banco histórico
- `docs/INTEGRACAO_AGENTE_HISTORICO.md` - Integração IA
- `docs/ESTRATEGIA_BALANCEAMENTO.md` - Estratégias

---

## 🎯 Resumo Ultra-Rápido

```bash
# Todos os dias:
python tratamento_abc.py    # Processar vendas
python analista.py          # Gerar pedidos

# Primeira vez:
python launchers/criar_db.py  # Criar banco

# Quando precisar:
python utilitarios/consultar_vendas.py  # Consultar histórico
```

**Pronto! Sistema organizado e fácil de usar! 🚀**
