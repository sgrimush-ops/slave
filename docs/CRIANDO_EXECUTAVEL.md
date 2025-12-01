# Criando Executável do Sistema

## 📦 Sobre o Executável

O sistema pode ser convertido em um arquivo `.exe` standalone para distribuição, permitindo que usuários sem Python instalado possam usar o sistema.

---

## 🎯 Vantagens do Executável

✅ **Facilidade de Distribuição**
- Não requer Python instalado
- Não precisa configurar ambiente virtual
- Instalação simplificada

✅ **Uso Profissional**
- Interface limpa e profissional
- Ícone personalizado (opcional)
- Executável único

✅ **Segurança**
- Código compilado
- Não expõe código-fonte diretamente
- Versionamento controlado

---

## 🛠️ Preparação

### 1. Instalar PyInstaller
```bash
pip install pyinstaller
```

### 2. Testar Interface
```bash
python interface.py
```
Certifique-se de que tudo funciona corretamente antes de criar o executável.

---

## 🚀 Criando o Executável

### Método Automatizado (Recomendado)

```bash
python criar_executavel.py
```

**Opções disponíveis:**
1. Criar apenas executável
2. Criar executável + pacote de distribuição ⭐
3. Apenas pacote (executável já existe)

**Recomendação:** Use opção 2 para criar tudo automaticamente.

---

## 📋 O que é Criado

### Opção 1: Apenas Executável
```
dist/
└── SistemaEstoque.exe    (~50-100 MB)
```

**Nota:** Ainda precisa das pastas `src/`, `scripts/`, `data/` no mesmo diretório.

### Opção 2: Pacote Completo ⭐
```
dist/SistemaEstoque_Completo/
├── SistemaEstoque.exe
├── data/
├── src/
├── scripts/
├── utilitarios/
├── launchers/
├── README.md
├── GUIA_RAPIDO.md
└── LEIA-ME.txt
```

**Este pacote está pronto para distribuir!**

---

## ⚙️ Método Manual (Avançado)

### Comando Básico
```bash
pyinstaller --onefile --windowed interface.py
```

### Comando Completo (com dependências)
```bash
pyinstaller ^
    --name=SistemaEstoque ^
    --onefile ^
    --windowed ^
    --add-data="src;src" ^
    --add-data="scripts;scripts" ^
    --add-data="data;data" ^
    --hidden-import=tkinter ^
    --hidden-import=pandas ^
    --hidden-import=pyarrow ^
    --hidden-import=ollama ^
    interface.py
```

### Parâmetros Explicados
- `--onefile`: Cria um único arquivo .exe
- `--windowed`: Não mostra console (apenas interface)
- `--name`: Nome do executável
- `--add-data`: Inclui pastas necessárias
- `--hidden-import`: Força inclusão de módulos

---

## 🎨 Personalizações

### Adicionar Ícone
```bash
pyinstaller --icon=icone.ico interface.py
```

### Adicionar Informações de Versão
Crie `version_info.txt`:
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
        StringStruct(u'FileDescription', u'Sistema de Gestão de Estoque'),
        StringStruct(u'FileVersion', u'1.0.0.0'),
        StringStruct(u'ProductName', u'Sistema Estoque IA'),
        StringStruct(u'ProductVersion', u'1.0.0.0')])
      ]), 
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)
```

Depois:
```bash
pyinstaller --version-file=version_info.txt interface.py
```

---

## 📊 Tamanho do Executável

### Fatores que Afetam o Tamanho
- **Pandas/NumPy**: ~40-50 MB
- **Tkinter**: ~10-15 MB
- **PyArrow**: ~20-30 MB
- **Ollama client**: ~5 MB
- **Python runtime**: ~15-20 MB

**Total esperado:** 90-130 MB

### Reduzir Tamanho

#### 1. Usar UPX (Compressor)
```bash
pip install pyinstaller[compression]
pyinstaller --upx-dir=caminho\para\upx interface.py
```

#### 2. Excluir Módulos Não Usados
```bash
pyinstaller --exclude-module=matplotlib interface.py
```

---

## 🧪 Testando o Executável

### 1. Testar Localmente
```bash
cd dist
SistemaEstoque.exe
```

### 2. Testar em Máquina Limpa
- VM sem Python
- Computador de usuário final
- Diferentes versões do Windows

### 3. Checklist de Testes
- [ ] Interface abre corretamente
- [ ] Importação de arquivos funciona
- [ ] Processamento de vendas executa
- [ ] Cálculo de sugestões funciona
- [ ] Agente IA responde (com Ollama)
- [ ] Arquivos são salvos corretamente
- [ ] Log mostra mensagens

---

## 📦 Distribuindo

### Método 1: ZIP
```bash
# Comprimir pasta completa
Compress-Archive -Path dist\SistemaEstoque_Completo -DestinationPath SistemaEstoque_v1.0.zip
```

### Método 2: Instalador
Use ferramentas como:
- **Inno Setup** (gratuito)
- **NSIS** (gratuito)
- **Advanced Installer** (pago)

Exemplo Inno Setup:
```iss
[Setup]
AppName=Sistema Estoque IA
AppVersion=1.0
DefaultDirName={pf}\SistemaEstoque
DefaultGroupName=Sistema Estoque
OutputBaseFilename=SistemaEstoque_Setup

[Files]
Source: "dist\SistemaEstoque_Completo\*"; DestDir: "{app}"; Flags: recursesubdirs

[Icons]
Name: "{group}\Sistema Estoque"; Filename: "{app}\SistemaEstoque.exe"
```

---

## 🔧 Problemas Comuns

### Executável não inicia
**Causa:** Falta de dependências
**Solução:** Use `--hidden-import` para módulos problemáticos

### Erro "Failed to execute script"
**Causa:** Caminho de dados incorreto
**Solução:** Use caminhos relativos ou `sys._MEIPASS`

### Interface não aparece
**Causa:** Erro no modo `--windowed`
**Solução:** Remova `--windowed` temporariamente para ver erros

### Lentidão ao iniciar
**Causa:** Normal na primeira execução
**Solução:** Executável descompacta arquivos na primeira vez

---

## 📝 Boas Práticas

### 1. Versionamento
```
SistemaEstoque_v1.0.exe
SistemaEstoque_v1.1.exe
```

### 2. Changelog
Mantenha arquivo `CHANGELOG.md`:
```markdown
## v1.0 (30/11/2024)
- Lançamento inicial
- Interface gráfica completa
- Integração com agente IA

## v1.1 (planejado)
- Melhorias de performance
- Novos relatórios
```

### 3. Documentação
Inclua sempre:
- `README.md` ou `LEIA-ME.txt`
- Requisitos do sistema
- Como usar
- Contato para suporte

---

## 🎯 Requisitos do Sistema

### Mínimo
- Windows 10 ou superior
- 4 GB RAM
- 500 MB espaço em disco
- Processador dual-core

### Recomendado
- Windows 10/11 (64-bit)
- 8 GB RAM
- 1 GB espaço em disco
- Processador quad-core
- **Ollama instalado** (para agente IA)

---

## 📞 Suporte

### Para Desenvolvedores
1. Verifique logs em `build/`
2. Use modo debug: `pyinstaller --debug=all`
3. Consulte: https://pyinstaller.org/

### Para Usuários
1. Inclua instruções claras no `LEIA-ME.txt`
2. Forneça canal de suporte
3. Documente requisitos claramente

---

## ✅ Checklist Final

Antes de distribuir:
- [ ] Testado em máquina limpa (sem Python)
- [ ] Todas as funcionalidades verificadas
- [ ] Documentação incluída
- [ ] Versão claramente identificada
- [ ] Requisitos documentados
- [ ] Instruções de instalação do Ollama
- [ ] Arquivo LEIA-ME.txt presente
- [ ] Licença de software (se aplicável)

---

**Sistema de Gestão de Estoque com IA**
*Guia de Criação de Executável - v1.0*
