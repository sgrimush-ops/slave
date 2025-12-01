# Testando a Interface Gráfica

## 🧪 Plano de Testes

### Teste 1: Inicialização ✅
```bash
python interface.py
```

**Verificar:**
- [ ] Interface abre sem erros
- [ ] Título correto: "Sistema de Gestão de Estoque com IA"
- [ ] Todas as 5 seções visíveis
- [ ] Log vazio inicialmente
- [ ] Barra de status mostra "Pronto"
- [ ] Data sugerida é o dia anterior

---

### Teste 2: Detecção de Arquivos Existentes
**Pré-requisito:** Ter arquivos em `data/`

**Verificar:**
- [ ] Campo "Arquivo de Vendas" preenchido automaticamente se `data/grid_tmp_abcmerc.csv` existe
- [ ] Campo "Arquivo Gerado" preenchido automaticamente se `data/gerado.xlsx` existe
- [ ] Mensagens no log indicando arquivos encontrados

---

### Teste 3: Seleção de Arquivos
1. Clique em "Selecionar..." para vendas
2. Escolha um arquivo CSV qualquer

**Verificar:**
- [ ] Diálogo de arquivo abre
- [ ] Após seleção, caminho aparece no campo
- [ ] Log registra a seleção

Repita para arquivo gerado (Excel).

---

### Teste 4: Importação de Arquivos

**Preparação:**
```bash
# Criar arquivo de teste
echo "teste" > teste_vendas.csv
```

1. Selecione `teste_vendas.csv`
2. Clique "Importar para data/"

**Verificar:**
- [ ] Mensagem de sucesso
- [ ] Arquivo copiado para `data/grid_tmp_abcmerc.csv`
- [ ] Log mostra operação
- [ ] Barra de status atualizada

---

### Teste 5: Processar Vendas

**Pré-requisito:** 
- Arquivo `data/grid_tmp_abcmerc.csv` existe (pode ser arquivo real de vendas)

1. Confirme ou altere a data
2. Clique "Processar Vendas"

**Verificar:**
- [ ] Barra de status: "Processando vendas..."
- [ ] Log mostra saída do tratamento_abc.py
- [ ] Ao concluir, mensagem de sucesso
- [ ] Arquivos gerados:
  - [ ] `data/resultado_abc.xlsx`
  - [ ] `data/vendas_historico.parquet` (atualizado)

**Tempo esperado:** 10-30 segundos

---

### Teste 6: Calcular Sugestões

**Pré-requisito:** 
- `data/banco.db` existe
- `data/resultado_abc.xlsx` existe (do teste anterior)

1. Clique "Apenas Calcular Sugestões"

**Verificar:**
- [ ] Barra de status: "Calculando sugestões..."
- [ ] Log mostra progresso
- [ ] Mensagem de sucesso
- [ ] Arquivo gerado: `data/sugestao_ia.xlsx`

**Tempo esperado:** 5-15 segundos

---

### Teste 7: Abrir Arquivo de Sugestões

**Pré-requisito:** `data/sugestao_ia.xlsx` existe

1. Clique "Abrir Arquivo Sugestões"

**Verificar:**
- [ ] Excel abre automaticamente
- [ ] Arquivo correto (`sugestao_ia.xlsx`)
- [ ] Log registra abertura

---

### Teste 8: Executar Analista Completo

**Pré-requisito:** Todos os arquivos necessários

1. Clique "Executar Analista Completo"
2. Confirme na caixa de diálogo

**Verificar:**
- [ ] Diálogo de confirmação aparece
- [ ] Após confirmar, processamento inicia
- [ ] Log mostra todas as etapas:
  - [ ] Cálculo de sugestões
  - [ ] Análises
  - [ ] Inicialização do agente
- [ ] Mensagem final de sucesso

**Tempo esperado:** 30-60 segundos

---

### Teste 9: Consultar Agente IA

**Pré-requisito:** 
- Ollama rodando: `ollama serve`
- Modelo instalado: `ollama pull llama3`

1. Digite na área de texto: "Olá, você está funcionando?"
2. Clique "Consultar Agente"

**Verificar:**
- [ ] Barra de status: "Consultando agente IA..."
- [ ] Log mostra a pergunta
- [ ] Log mostra a resposta do agente
- [ ] Resposta faz sentido
- [ ] Status volta para "Consulta concluída"

**Tempo esperado:** 5-30 segundos (depende do hardware)

**Teste adicional - Pergunta com contexto:**
- Pergunta: "Qual o histórico de vendas do produto 12345 na loja 1?"
- Deve mostrar dados históricos (se existirem)

---

### Teste 10: Ver Histórico de Vendas

**Pré-requisito:** `data/vendas_historico.parquet` existe

1. Clique "Ver Histórico de Vendas"

**Verificar:**
- [ ] Nova janela abre com `consultar_vendas.py`
- [ ] Menu de consultas aparece
- [ ] Pode fazer consultas
- [ ] Log registra abertura

---

### Teste 11: Analisar Estratégias

1. Clique "Analisar Estratégias"

**Verificar:**
- [ ] Processamento inicia
- [ ] Log mostra análise
- [ ] Estatísticas de estratégias aparecem
- [ ] Mensagem de conclusão

---

### Teste 12: Limpar Log

1. Execute algumas operações (log fica cheio)
2. Clique "Limpar Log"

**Verificar:**
- [ ] Log é limpo completamente
- [ ] Status: "Log limpo"

---

### Teste 13: Tratamento de Erros

#### 13.1. Arquivo Não Encontrado
1. Tente processar vendas sem arquivo `grid_tmp_abcmerc.csv`

**Verificar:**
- [ ] Mensagem de erro clara
- [ ] Log registra o erro
- [ ] Interface não trava

#### 13.2. Banco Não Existe
1. Renomeie `data/banco.db` temporariamente
2. Tente calcular sugestões

**Verificar:**
- [ ] Mensagem de erro sobre banco
- [ ] Sugestão de executar `criar_db.py`
- [ ] Interface continua responsiva

#### 13.3. Ollama Não Rodando
1. Pare o Ollama
2. Tente consultar agente

**Verificar:**
- [ ] Erro detectado
- [ ] Mensagem sobre verificar Ollama
- [ ] Interface não trava

---

### Teste 14: Múltiplas Operações
1. Processe vendas
2. Imediatamente clique em outra operação

**Verificar:**
- [ ] Operação anterior continua (thread separada)
- [ ] Nova operação inicia normalmente
- [ ] Logs não se misturam
- [ ] Sem travamentos

---

### Teste 15: Interface Responsiva
Durante operações longas (processar vendas, analista completo):

**Verificar:**
- [ ] Interface não trava
- [ ] Pode rolar o log
- [ ] Pode clicar em outros elementos
- [ ] Botões respondem

---

## 🔧 Testes de Criação de Executável

### Teste 16: Criar Executável

```bash
python criar_executavel.py
```

1. Escolha opção 1 (apenas executável)

**Verificar:**
- [ ] PyInstaller instala se necessário
- [ ] Build completa sem erros
- [ ] Arquivo `dist/SistemaEstoque.exe` criado
- [ ] Tamanho razoável (90-130 MB)

---

### Teste 17: Testar Executável Localmente

```bash
cd dist
SistemaEstoque.exe
```

**Verificar:**
- [ ] Interface abre normalmente
- [ ] Todas as funcionalidades funcionam
- [ ] Arquivos são salvos em `data/`
- [ ] Log funciona

---

### Teste 18: Criar Pacote Completo

```bash
python criar_executavel.py
```

2. Escolha opção 2 (executável + pacote)

**Verificar:**
- [ ] Pasta `dist/SistemaEstoque_Completo/` criada
- [ ] Contém:
  - [ ] SistemaEstoque.exe
  - [ ] src/
  - [ ] scripts/
  - [ ] data/
  - [ ] utilitarios/
  - [ ] README.md
  - [ ] GUIA_RAPIDO.md
  - [ ] LEIA-ME.txt
- [ ] LEIA-ME.txt tem instruções corretas

---

### Teste 19: Pacote em Máquina Limpa (Opcional)

**Melhor teste:** VM ou PC sem Python

1. Copie pasta `SistemaEstoque_Completo/` para máquina limpa
2. Execute `SistemaEstoque.exe`

**Verificar:**
- [ ] Executa sem Python instalado
- [ ] Todas as funções básicas funcionam
- [ ] Arquivos são salvos
- [ ] (Agente IA só funciona se Ollama instalado)

---

## 📊 Checklist Geral

### Funcionalidades Básicas
- [ ] Interface abre
- [ ] Seleção de arquivos funciona
- [ ] Importação de arquivos funciona
- [ ] Processamento de vendas funciona
- [ ] Cálculo de sugestões funciona
- [ ] Abertura de arquivos funciona

### Funcionalidades Avançadas
- [ ] Analista completo funciona
- [ ] Agente IA responde (com Ollama)
- [ ] Histórico de vendas abre
- [ ] Análise de estratégias funciona

### Interface
- [ ] Log atualiza em tempo real
- [ ] Barra de status atualiza
- [ ] Botões respondem
- [ ] Não trava durante operações
- [ ] Erros são tratados adequadamente

### Executável
- [ ] Cria sem erros
- [ ] Funciona localmente
- [ ] Pacote completo gerado
- [ ] Documentação incluída

---

## 🐛 Problemas Conhecidos e Soluções

### Interface não abre
**Erro:** `ModuleNotFoundError: No module named 'tkinter'`

**Solução:**
- Windows: tkinter já vem com Python
- Linux: `sudo apt-get install python3-tk`
- Mac: `brew install python-tk`

---

### Executável muito lento para iniciar
**Comportamento:** Primeira execução demora 10-30 segundos

**Explicação:** Normal - descompacta arquivos na primeira vez
**Solução:** Próximas execuções serão mais rápidas

---

### Agente não responde
**Erro:** "Failed to connect to Ollama"

**Soluções:**
1. Verificar Ollama rodando: `ollama serve`
2. Verificar modelo: `ollama list`
3. Instalar se necessário: `ollama pull llama3`

---

### Erro ao processar vendas
**Erro:** "Arquivo não encontrado"

**Soluções:**
1. Importar arquivo primeiro
2. Verificar se arquivo está em `data/`
3. Verificar formato do arquivo (CSV)

---

### Erro "Banco de dados não encontrado"
**Erro:** `data/banco.db` não existe

**Solução:**
```bash
python launchers/criar_db.py
```

---

## ✅ Resultado Esperado

Após todos os testes:

✅ Interface 100% funcional  
✅ Todas as operações executam corretamente  
✅ Erros são tratados adequadamente  
✅ Executável pode ser criado  
✅ Executável funciona independentemente  
✅ Documentação completa e acessível  

**Sistema pronto para uso em produção!**

---

## 📝 Registro de Testes

### Tester: _______________
### Data: _______________
### Ambiente:
- [ ] Windows 10
- [ ] Windows 11
- [ ] Outro: _______________

### Versão Python: _______________
### Ollama Instalado: [ ] Sim [ ] Não

### Testes Aprovados: _____ / 19
### Observações:
```
_________________________________________________
_________________________________________________
_________________________________________________
```

---

**Sistema de Gestão de Estoque com IA**
*Plano de Testes - Interface Gráfica*
