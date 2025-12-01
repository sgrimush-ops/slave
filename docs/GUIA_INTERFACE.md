# Guia da Interface Gráfica

## Sistema de Gestão de Estoque com IA

### Iniciando a Interface

#### Opção 1: Script Python
```bash
python interface.py
```

#### Opção 2: Arquivo Batch (Windows)
```bash
iniciar_interface.bat
```

#### Opção 3: Executável (após criação)
```bash
dist\SistemaEstoque.exe
```

---

## Seções da Interface

### 1. Importar Arquivos

**Objetivo**: Copiar arquivos de vendas e gerados para a pasta `data/`

**Arquivos necessários**:
- `grid_tmp_abcmerc.csv` - Arquivo de vendas diárias
- `gerado.xlsx` - Arquivo Excel gerado (opcional)

**Como usar**:
1. Clique em "Selecionar..." para escolher o arquivo
2. Clique em "Importar para data/" para copiar

**Nota**: A interface detecta automaticamente se os arquivos já existem na pasta `data/`

---

### 2. Processar Vendas Diárias

**Objetivo**: Executar o tratamento ABC e atualizar histórico

**Como usar**:
1. Verifique a data sugerida (dia anterior)
2. Ajuste se necessário (formato: dd/mm/yy)
3. Clique em "Processar Vendas"

**O que acontece**:
- Executa `tratamento_abc.py`
- Filtra dados (seções 10, 13, 14, 16, 17, 23)
- Remove produtos com ponto_pedido=0 ou embalagem=0
- Gera `resultado_abc.xlsx`
- Atualiza `vendas_historico.parquet`

**Saída**:
- `data/resultado_abc.xlsx` - Dados tratados
- `data/vendas_historico.parquet` - Histórico atualizado

---

### 3. Análise e Geração de Pedidos

**Botões disponíveis**:

#### Executar Analista Completo
- Executa todo o fluxo de análise
- Calcula sugestões
- Gera análises
- Inicia agente IA
- **Arquivo**: `analista.py`

#### Apenas Calcular Sugestões
- Calcula apenas as sugestões de pedido
- Mais rápido que análise completa
- **Arquivo**: `scripts/atualizar_simples.py`
- **Saída**: `data/sugestao_ia.xlsx`

#### Analisar Estratégias
- Analisa estratégias aplicadas no sistema
- Mostra distribuição ABC, rotatividade, etc.
- **Arquivo**: `scripts/analisar_estrategias.py`

#### Abrir Arquivo Sugestões
- Abre `data/sugestao_ia.xlsx` no Excel
- Facilita visualização dos resultados

---

### 4. Agente IA (LLaMA 3)

**Objetivo**: Consultar o agente de IA para análises personalizadas

**Requisitos**:
- Ollama instalado e rodando
- Modelo LLaMA 3 instalado: `ollama pull llama3`

**Como usar**:
1. Digite sua pergunta na área de texto
2. Clique em "Consultar Agente"
3. Aguarde a resposta no log

**Exemplos de perguntas**:
- "Qual produto teve maior queda nas vendas?"
- "Analise o produto 12345 na loja 1"
- "Quais produtos estão com cobertura crítica?"
- "Explique a estratégia de balanceamento"

**Botão "Ver Histórico de Vendas"**:
- Abre `utilitarios/consultar_vendas.py`
- Menu com consultas ao histórico Parquet

---

### 5. Log de Execução

**Objetivo**: Acompanhar todas as operações em tempo real

**Recursos**:
- Mostra saída de todos os scripts
- Registra erros e sucessos
- Scroll automático
- Botão "Limpar Log" para reiniciar

---

## Barra de Status

Localizada na parte inferior, mostra:
- Estado atual do sistema
- Última operação realizada
- Mensagens de erro ou sucesso

---

## Fluxo de Trabalho Diário

### 1. Manhã - Importar Vendas
```
1. Receba o arquivo grid_tmp_abcmerc.csv
2. Abra a interface
3. Vá em "1. Importar Arquivos"
4. Selecione o arquivo CSV
5. Clique "Importar para data/"
```

### 2. Processar Vendas
```
1. Vá em "2. Processar Vendas Diárias"
2. Confirme a data (normalmente dia anterior)
3. Clique "Processar Vendas"
4. Aguarde conclusão (log mostra progresso)
```

### 3. Gerar Sugestões
```
1. Vá em "3. Análise e Geração de Pedidos"
2. Clique "Apenas Calcular Sugestões"
3. Aguarde processamento
4. Clique "Abrir Arquivo Sugestões"
```

### 4. Análise Detalhada (Opcional)
```
1. Para análise completa, clique "Executar Analista Completo"
2. Para consultas específicas, use "4. Agente IA"
3. Digite perguntas personalizadas ao agente
```

---

## Criando o Executável

### Passo 1: Instalar PyInstaller
```bash
pip install pyinstaller
```

### Passo 2: Executar Script de Criação
```bash
python criar_executavel.py
```

### Opções disponíveis:
1. **Criar apenas executável**
   - Gera `dist/SistemaEstoque.exe`
   - ~50-100 MB
   - Requer pasta `src/`, `scripts/`, `data/` no mesmo diretório

2. **Criar executável + pacote de distribuição**
   - Cria pasta `dist/SistemaEstoque_Completo/`
   - Inclui executável + todos os arquivos necessários
   - Pronto para distribuir

3. **Apenas pacote (executável já existe)**
   - Reorganiza arquivos existentes
   - Cria documentação

---

## Estrutura do Pacote de Distribuição

```
SistemaEstoque_Completo/
│
├── SistemaEstoque.exe          # Executável principal
│
├── data/                        # Dados (inicialmente vazio)
│   └── (arquivos serão criados aqui)
│
├── src/                         # Código fonte
│   ├── agente_estoque.py
│   ├── analise_historico.py
│   └── gerenciador.py
│
├── scripts/                     # Scripts de processamento
│   ├── atualizar_simples.py
│   └── analisar_estrategias.py
│
├── utilitarios/                 # Ferramentas auxiliares
│   ├── consultar_vendas.py
│   └── testar_agente_historico.py
│
├── launchers/                   # Lançadores de setup
│   └── criar_db.py
│
├── README.md                    # Documentação completa
├── GUIA_RAPIDO.md              # Guia rápido
└── LEIA-ME.txt                 # Instruções de uso
```

---

## Requisitos do Executável

### Sistema Operacional
- Windows 10 ou superior
- 64-bit

### Software Necessário
- **Ollama** (para agente IA)
  - Download: https://ollama.ai
  - Instalar modelo: `ollama pull llama3`

### Hardware Recomendado
- RAM: 8 GB mínimo (16 GB recomendado)
- Disco: 1 GB livre
- Processador: Intel i5 ou equivalente

---

## Solução de Problemas

### Interface não abre
```
1. Verifique se Python está instalado: python --version
2. Ative o ambiente virtual: .venv\Scripts\activate
3. Instale dependências: pip install -r requirements.txt
4. Execute novamente: python interface.py
```

### Erro ao processar vendas
```
1. Verifique se grid_tmp_abcmerc.csv existe em data/
2. Confirme formato do arquivo (CSV com encoding correto)
3. Verifique data no formato dd/mm/yy
```

### Agente IA não responde
```
1. Verifique se Ollama está rodando:
   - Windows: Abra Task Manager, procure por "ollama"
   - Ou execute: ollama serve

2. Verifique modelo LLaMA 3:
   ollama list
   
3. Se não aparecer, instale:
   ollama pull llama3
```

### Erro "Banco de dados não encontrado"
```
1. Execute o criador de banco:
   python launchers/criar_db.py

2. Importe os arquivos necessários (produtos, lojas, fornecedores)
```

### Executável muito lento
```
1. Primeira execução é sempre mais lenta (carrega bibliotecas)
2. Próximas execuções serão mais rápidas
3. Para melhor performance, use script Python diretamente
```

---

## Dicas de Uso

### Performance
- Use "Apenas Calcular Sugestões" para operações rápidas
- "Executar Analista Completo" é mais lento mas mais completo
- Agente IA depende da velocidade do Ollama

### Segurança
- Faça backup da pasta `data/` regularmente
- `vendas_historico.parquet` contém todo o histórico
- `banco.db` contém cadastros de produtos e lojas

### Manutenção
- Limpe o log periodicamente para melhor visualização
- Monitore tamanho do arquivo `vendas_historico.parquet`
- Verifique atualizações de dependências

### Produtividade
- Use atalhos de teclado (Tab para navegar)
- Mantenha arquivos CSV atualizados em local fixo
- Configure path padrão para importação

---

## Vantagens da Interface Gráfica

✅ **Facilidade de Uso**
- Não precisa digitar comandos
- Visual intuitivo
- Feedback imediato

✅ **Integração Completa**
- Todas as funcionalidades em um lugar
- Fluxo de trabalho guiado
- Log centralizado

✅ **Produtividade**
- Importação rápida de arquivos
- Execução com um clique
- Consultas ao agente facilitadas

✅ **Distribuição**
- Pode ser transformado em executável
- Não requer conhecimento técnico
- Pronto para uso por qualquer usuário

---

## Próximos Passos

1. **Teste a interface**:
   ```bash
   python interface.py
   ```

2. **Execute fluxo completo**:
   - Importe arquivo de vendas
   - Processe as vendas
   - Gere sugestões
   - Consulte o agente

3. **Crie o executável**:
   ```bash
   python criar_executavel.py
   ```

4. **Distribua**:
   - Copie pasta `SistemaEstoque_Completo/`
   - Envie para outros usuários
   - Inclua instruções do `LEIA-ME.txt`

---

## Suporte

Para dúvidas ou problemas:
1. Consulte README.md
2. Consulte GUIA_RAPIDO.md
3. Use o agente IA na própria interface
4. Verifique logs de execução

---

**Sistema de Gestão de Estoque com IA**
*Interface Gráfica - Versão 1.0*
