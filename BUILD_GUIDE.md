# GUIA DE GERAÇÃO DO EXECUTÁVEL
================================

## Passo a Passo para Criar o Executável

### 1. Preparação do Ambiente

Execute no PowerShell ou CMD:

```powershell
# Instalar PyInstaller se ainda não tiver
python -m pip install pyinstaller

# Verificar instalação
python -m pip show pyinstaller
```

### 2. Gerar o Executável

Execute o script de build:

```powershell
python build_exe.py
```

O script irá:
- ✅ Limpar builds anteriores
- ✅ Verificar/instalar PyInstaller
- ✅ Criar configuração otimizada
- ✅ Compilar o executável (demora alguns minutos)
- ✅ Organizar arquivos para distribuição

### 3. Resultado

Será criado em `dist/`:

```
dist/
├── GestaoEstoque.exe          # Executável principal (40-60 MB)
└── GestaoEstoque/             # Pasta para distribuição
    ├── data/                  # Pasta de dados
    │   └── colunas.txt       # Mapeamento de colunas
    └── LEIA-ME.txt           # Instruções para o usuário
```

### 4. Distribuir

**Opção 1: Pasta completa**
- Copie toda a pasta `dist/GestaoEstoque/`
- Usuário executa `GestaoEstoque.exe`

**Opção 2: ZIP**
```powershell
# Criar ZIP para distribuição
Compress-Archive -Path dist\GestaoEstoque\* -DestinationPath GestaoEstoque_v1.0.zip
```

### 5. Requisitos no PC do Usuário

O executável é **standalone**, mas o usuário precisa:

✅ **Windows 10/11** (64-bit)
✅ **Ollama instalado** (para usar Agente IA)
   - Download: https://ollama.ai
   - Instalar modelo: `ollama pull llama3.2` ou `ollama pull gemma3:4b`

❌ **NÃO precisa**:
   - Python instalado
   - Instalar bibliotecas
   - Permissões de administrador

### 6. Primeira Execução

O usuário deve:
1. Extrair o ZIP (se distribuído assim)
2. Executar `GestaoEstoque.exe`
3. Importar arquivos CSV pela interface
4. Começar a usar

A pasta `data/` será criada automaticamente se não existir.

## Solução de Problemas

### Erro: "PyInstaller não encontrado"
```powershell
python -m pip install --upgrade pyinstaller
```

### Erro: "Módulo XXX não encontrado"
Adicione o módulo em `hiddenimports` no arquivo `GestaoEstoque.spec`:
```python
hiddenimports=[
    'pandas',
    'openpyxl',
    'pyarrow',
    'requests',
    'seu_modulo_aqui',  # Adicione aqui
],
```

Depois execute:
```powershell
python -m PyInstaller GestaoEstoque.spec --clean
```

### Executável muito grande

Tamanho esperado: **40-70 MB**

Se estiver maior que 100 MB, adicione mais exclusões em `GestaoEstoque.spec`:
```python
excludes=[
    'matplotlib',
    'numpy.testing',
    'IPython',
    'jupyter',
    'scipy',  # Se não usar
    'PIL',    # Se não usar
],
```

### Executável não abre

1. **Teste no terminal primeiro**:
```cmd
cd dist
GestaoEstoque.exe
```

2. **Verifique logs**:
   - O PyInstaller pode criar logs em `%TEMP%`
   - Procure por erros de importação

3. **Teste com console ativado**:
   Edite `GestaoEstoque.spec`:
```python
exe = EXE(
    ...
    console=True,  # Mude de False para True
    ...
)
```

Rebuild e veja os erros no console.

## Customizações

### Adicionar Ícone

1. Crie ou obtenha um arquivo `.ico` (256x256 ou 48x48)
2. Coloque na raiz do projeto: `icone.ico`
3. Edite `GestaoEstoque.spec`:
```python
exe = EXE(
    ...
    icon='icone.ico',  # Adicione esta linha
    ...
)
```

### Adicionar Informações de Versão (Windows)

Crie `file_version_info.txt`:
```
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=(1, 0, 0, 0),
    prodvers=(1, 0, 0, 0),
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
  ),
  kids=[
    StringFileInfo(
      [
      StringTable(
        u'040904B0',
        [StringStruct(u'CompanyName', u'Sua Empresa'),
        StringStruct(u'FileDescription', u'Sistema de Gestão de Estoque ABC'),
        StringStruct(u'FileVersion', u'1.0.0.0'),
        StringStruct(u'InternalName', u'GestaoEstoque'),
        StringStruct(u'LegalCopyright', u'Copyright 2025'),
        StringStruct(u'OriginalFilename', u'GestaoEstoque.exe'),
        StringStruct(u'ProductName', u'Gestão de Estoque'),
        StringStruct(u'ProductVersion', u'1.0.0.0')])
      ]), 
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)
```

Edite `GestaoEstoque.spec`:
```python
exe = EXE(
    ...
    version='file_version_info.txt',  # Adicione
    ...
)
```

## Versões Futuras

Para criar nova versão:
1. Atualize o código
2. Execute `python build_exe.py` novamente
3. Renomeie o ZIP: `GestaoEstoque_v1.1.zip`
4. Distribua

## Checklist Final

Antes de distribuir, teste:
- [ ] Executável abre sem erros
- [ ] Interface gráfica carrega corretamente
- [ ] Importação de CSV funciona
- [ ] Processamento de vendas funciona
- [ ] Análise completa funciona
- [ ] Agente IA funciona (com Ollama rodando)
- [ ] Arquivos são salvos em data/
- [ ] Logs aparecem corretamente
- [ ] Botões respondem adequadamente
- [ ] Não há erros no console

## Notas Importantes

⚠️ **Antivírus**: Alguns antivírus podem bloquear executáveis PyInstaller
   - É um falso positivo comum
   - Adicione exceção se necessário
   - Considere assinar digitalmente o executável para produção

⚠️ **Windows Defender**: Pode exigir permissão na primeira execução
   - É normal para executáveis não assinados
   - Clique em "Mais informações" → "Executar assim mesmo"

⚠️ **Tamanho**: O executável inclui todo o Python + bibliotecas
   - Primeira vez parece grande (~50MB)
   - É normal para aplicações Python empacotadas
   - Alternativa: Criar instalador com NSIS/Inno Setup
