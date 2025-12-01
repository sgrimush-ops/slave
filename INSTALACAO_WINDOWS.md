# Instalação em Windows - Sem Permissão de Administrador

## 📋 Requisitos Mínimos

- Windows 10 ou superior (64-bit)
- 4 GB RAM (8 GB recomendado)
- 2 GB espaço em disco
- Acesso à internet (para download)

---

## 🚀 Passo a Passo - Instalação Completa

### 1️⃣ Instalar Python 3.11+

#### Opção A: Instalação da Microsoft Store (Recomendado - Não Requer Admin)
```
1. Abra a Microsoft Store
2. Busque "Python 3.11" ou "Python 3.12"
3. Clique em "Obter" / "Instalar"
4. Aguarde instalação
```

✅ **Vantagens:**
- Não requer permissão de administrador
- Atualizações automáticas
- PATH configurado automaticamente
- tkinter incluído

#### Opção B: Instalador Oficial (Requer Download)
```
1. Baixe Python em: https://www.python.org/downloads/
2. Execute o instalador
3. ⚠️ MARQUE: "Add Python to PATH"
4. Escolha "Install for current user only" (se sem admin)
5. Conclua instalação
```

#### Verificar Instalação:
```bash
python --version
# Deve mostrar: Python 3.11.x ou superior
```

---

### 2️⃣ Baixar o Projeto

#### Opção A: Download ZIP
```
1. Baixe o arquivo .zip do projeto
2. Extraia para: C:\Users\SeuUsuario\Documents\slave
```

#### Opção B: Git Clone (se tiver Git)
```bash
cd C:\Users\SeuUsuario\Documents
git clone [url-do-repositorio] slave
cd slave
```

---

### 3️⃣ Criar Ambiente Virtual

```bash
# Navegar até pasta do projeto
cd C:\Users\SeuUsuario\Documents\slave

# Criar ambiente virtual
python -m venv .venv

# Ativar ambiente virtual
.venv\Scripts\activate

# Verificar ativação (deve aparecer (.venv) no prompt)
```

✅ **Vantagens do Ambiente Virtual:**
- Isola dependências do sistema
- Não requer permissão de admin
- Evita conflitos de versões
- Fácil de recriar se necessário

---

### 4️⃣ Instalar Dependências Python

```bash
# Com ambiente virtual ativado:
pip install -r requirements.txt

# Aguarde instalação (2-5 minutos)
```

**O que será instalado:**
- pandas (manipulação de dados)
- numpy (computação numérica)
- openpyxl (arquivos Excel)
- pyarrow (arquivos Parquet)
- ollama (cliente para IA)
- fastapi, uvicorn (API - opcional)
- pyinstaller (criar executável)

---

### 5️⃣ Instalar Ollama (Agente IA)

#### Download e Instalação:
```
1. Acesse: https://ollama.ai/download
2. Baixe "Ollama for Windows"
3. Execute o instalador
4. ⚠️ Escolha instalação para usuário atual (se sem admin)
5. Aguarde conclusão
```

#### Instalar Modelo LLaMA 3:
```bash
# Após instalar Ollama, em um terminal:
ollama pull llama3

# Aguarde download (~4 GB)
```

#### Iniciar Ollama:
```bash
# Em um terminal separado, deixe rodando:
ollama serve

# OU simplesmente inicie o aplicativo Ollama da bandeja do sistema
```

✅ **Verificar Ollama:**
```bash
ollama list
# Deve mostrar: llama3
```

---

### 6️⃣ Criar Banco de Dados

```bash
# Com ambiente virtual ativado:
python launchers/criar_db.py

# Siga instruções na tela para importar:
# - mix.xlsx (produtos)
# - lojas.csv ou similar
```

---

### 7️⃣ Testar Instalação

#### Teste 1: Interface Gráfica
```bash
python interface.py
```

**Deve abrir:** Interface gráfica do sistema

#### Teste 2: Processar Vendas
```bash
python tratamento_abc.py
```

**Deve:** Pedir arquivo CSV e processar

#### Teste 3: Agente IA
```bash
# Certifique-se que Ollama está rodando
python utilitarios/testar_agente_historico.py
```

**Deve:** Responder perguntas sobre estoque

---

## 🔧 Solução de Problemas

### Problema: "Python não é reconhecido"

**Causa:** Python não está no PATH

**Solução:**
```bash
# Opção 1: Use caminho completo
C:\Users\SeuUsuario\AppData\Local\Programs\Python\Python311\python.exe --version

# Opção 2: Adicione ao PATH manualmente
# 1. Abra Variáveis de Ambiente do USUÁRIO (não requer admin)
# 2. Edite "Path"
# 3. Adicione: C:\Users\SeuUsuario\AppData\Local\Programs\Python\Python311
# 4. Adicione: C:\Users\SeuUsuario\AppData\Local\Programs\Python\Python311\Scripts
```

---

### Problema: "pip não funciona"

**Causa:** pip não instalado ou PATH incorreto

**Solução:**
```bash
# Reinstalar pip
python -m ensurepip --upgrade

# Usar pip como módulo
python -m pip install -r requirements.txt
```

---

### Problema: "tkinter não encontrado"

**Causa:** Python instalado sem tkinter

**Solução:**
```bash
# Verificar se tkinter está disponível
python -c "import tkinter; print('OK')"

# Se erro: Reinstale Python da Microsoft Store (inclui tkinter)
```

---

### Problema: "Erro ao instalar pyarrow"

**Causa:** Versão incompatível do numpy

**Solução:**
```bash
# Instalar na ordem correta
pip install numpy==1.26.3
pip install pyarrow==15.0.0
```

---

### Problema: "Ollama não conecta"

**Causa:** Ollama não está rodando

**Solução:**
```bash
# Opção 1: Iniciar manualmente
ollama serve

# Opção 2: Verificar se está rodando
curl http://localhost:11434/api/tags

# Opção 3: Verificar serviço
Get-Service -Name *ollama*
```

---

### Problema: "Acesso negado ao instalar"

**Causa:** Tentando instalar em local protegido

**Solução:**
```bash
# Sempre use ambiente virtual
python -m venv .venv
.venv\Scripts\activate

# OU instale para usuário
pip install --user -r requirements.txt
```

---

## 📁 Estrutura de Pastas (Após Instalação)

```
C:\Users\SeuUsuario\Documents\slave\
│
├── .venv\                    # Ambiente virtual (criado)
│   ├── Scripts\
│   │   ├── python.exe
│   │   ├── pip.exe
│   │   └── activate.bat
│   └── Lib\
│
├── data\                     # Dados (criado após uso)
│   ├── banco.db
│   ├── vendas_historico.parquet
│   └── sugestao_ia.xlsx
│
├── interface.py              # Interface gráfica
├── tratamento_abc.py         # Processar vendas
├── analista.py               # Sistema completo
├── requirements.txt          # Dependências
└── ...
```

---

## 🎯 Workflow Diário (Após Instalação)

### Início do Dia:
```bash
# 1. Navegar até pasta
cd C:\Users\SeuUsuario\Documents\slave

# 2. Ativar ambiente virtual
.venv\Scripts\activate

# 3. Iniciar interface
python interface.py
```

### Durante o Dia:
1. Importar arquivo de vendas (CSV)
2. Processar vendas
3. Gerar sugestões de pedido
4. Consultar agente IA quando necessário

### Fim do Dia:
- Fechar interface
- Ollama pode continuar rodando (não afeta)

---

## 🔐 Permissões Necessárias

### ✅ NÃO Requer Admin:
- Instalação Python (Microsoft Store ou para usuário)
- Criar ambiente virtual
- Instalar pacotes Python (em venv ou --user)
- Instalar Ollama (para usuário atual)
- Executar scripts
- Interface gráfica
- Criar executável com PyInstaller
- Ler/escrever arquivos em Documents

### ⚠️ Pode Requerer Admin:
- Nenhuma operação do sistema requer admin!
- Tudo pode ser feito como usuário normal

---

## 💡 Dicas de Otimização

### 1. Criar Atalho para Interface
```
1. Clique direito na área de trabalho
2. Novo → Atalho
3. Destino: C:\Users\SeuUsuario\Documents\slave\.venv\Scripts\python.exe C:\Users\SeuUsuario\Documents\slave\interface.py
4. Nome: Sistema de Estoque
```

### 2. Script Batch de Inicialização
Crie `iniciar.bat` na pasta do projeto:
```batch
@echo off
cd /d "%~dp0"
call .venv\Scripts\activate.bat
python interface.py
```

### 3. Manter Ollama Rodando
```
1. Ollama geralmente fica na bandeja do sistema
2. Inicia automaticamente com Windows
3. Não precisa rodar "ollama serve" manualmente
```

### 4. Backup Automático
```
- Pasta data\ contém todos os dados importantes
- Faça backup regular de data\banco.db
- vendas_historico.parquet cresce com o tempo
```

---

## 📊 Consumo de Recursos

### Espaço em Disco:
- Python 3.11: ~100 MB
- Ambiente virtual + dependências: ~500 MB
- Ollama: ~1 GB
- Modelo LLaMA 3: ~4 GB
- Dados do sistema: ~50-200 MB (cresce com uso)
- **Total:** ~6 GB

### Memória RAM (durante uso):
- Interface: ~100-200 MB
- Python + dependências: ~300-500 MB
- Ollama + LLaMA 3: ~2-4 GB
- **Total:** ~3-5 GB

### CPU:
- Interface: Baixo (1-5%)
- Processamento vendas: Médio (20-50% por ~10s)
- Agente IA (LLaMA 3): Alto (50-100% por ~5-30s)

---

## ✅ Checklist de Instalação

- [ ] Python 3.11+ instalado
- [ ] Comando `python --version` funciona
- [ ] Projeto baixado/extraído
- [ ] Ambiente virtual criado (`.venv`)
- [ ] Ambiente virtual ativado (aparece `(.venv)` no prompt)
- [ ] Dependências instaladas (`pip install -r requirements.txt`)
- [ ] Ollama instalado
- [ ] Modelo llama3 baixado (`ollama pull llama3`)
- [ ] Banco criado (`python launchers/criar_db.py`)
- [ ] Interface abre (`python interface.py`)
- [ ] Agente IA responde (Ollama rodando)

---

## 🆘 Suporte

### Documentação:
- `README.md` - Visão geral do sistema
- `GUIA_RAPIDO.md` - Comandos essenciais
- `docs/GUIA_INTERFACE.md` - Guia da interface
- `docs/TESTES_INTERFACE.md` - Testes

### Problemas Comuns:
- Consulte seção "Solução de Problemas" acima
- Use o agente IA na própria interface para dúvidas
- Verifique logs na interface (seção Log de Execução)

---

**Sistema de Gestão de Estoque com IA**  
**Guia de Instalação - Windows sem Admin**  
**Versão: 1.0**
