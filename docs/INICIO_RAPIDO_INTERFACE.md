# Início Rápido - Interface Gráfica

## 🚀 3 Passos para Começar

### 1️⃣ Iniciar a Interface
```bash
python interface.py
```

### 2️⃣ Importar Arquivo de Vendas
1. Clique em **"Selecionar..."** ao lado de "Arquivo de Vendas"
2. Escolha o arquivo `grid_tmp_abcmerc.csv`
3. Clique em **"Importar para data/"**

### 3️⃣ Processar e Analisar
1. Confirme a data (dia anterior aparece automaticamente)
2. Clique em **"Processar Vendas"**
3. Aguarde conclusão (acompanhe no log)
4. Clique em **"Apenas Calcular Sugestões"**
5. Clique em **"Abrir Arquivo Sugestões"**

✅ **Pronto!** Seu arquivo `sugestao_ia.xlsx` está pronto para uso.

---

## 📋 Checklist Diário

- [ ] Recebeu arquivo `grid_tmp_abcmerc.csv`?
- [ ] Iniciou a interface: `python interface.py`
- [ ] Importou o arquivo de vendas
- [ ] Processou as vendas (confirme a data)
- [ ] Gerou as sugestões
- [ ] Abriu e verificou `sugestao_ia.xlsx`

---

## 🎯 Atalhos Úteis

### Barra de Botões
- **F5**: Atualizar log
- **Ctrl+L**: Limpar log
- **Alt+F4**: Fechar interface

### Área de Texto do Agente
- **Ctrl+A**: Selecionar tudo
- **Ctrl+C**: Copiar
- **Ctrl+V**: Colar

---

## 🆘 Problemas Comuns

### "Arquivo não encontrado"
➡️ Verifique se importou o arquivo para `data/` primeiro

### "Banco de dados não encontrado"
➡️ Execute uma vez: `python launchers/criar_db.py`

### "Agente IA não responde"
➡️ Verifique se Ollama está rodando:
```bash
ollama serve
ollama pull llama3
```

### Interface não abre
➡️ Verifique Python e tkinter:
```bash
python --version
python -c "import tkinter"
```

---

## 🎓 Próximos Passos

1. **Explore o Agente IA**
   - Digite perguntas na área de texto
   - Peça análises de produtos específicos
   - Consulte tendências de vendas

2. **Veja o Histórico**
   - Clique em "Ver Histórico de Vendas"
   - Explore diferentes consultas
   - Analise padrões ao longo do tempo

3. **Crie o Executável**
   - Para distribuir sem precisar Python
   - Execute: `python criar_executavel.py`
   - Escolha opção 2 (executável + pacote)

---

## 📚 Documentação Completa

- [GUIA_INTERFACE.md](GUIA_INTERFACE.md) - Guia completo da interface
- [README.md](../README.md) - Documentação geral do sistema
- [GUIA_RAPIDO.md](../GUIA_RAPIDO.md) - Comandos essenciais CLI

---

**Dúvidas?** Use o agente IA na própria interface! 🤖
