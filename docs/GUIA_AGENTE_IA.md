# 🧠 Guia: Como o Agente LLaMA 3 Aprende e Como Adicionar Novas Regras

## 📚 Onde o Conhecimento Está Armazenado

O LLaMA 3 **não guarda** conversas ou aprendizados no aplicativo. Ele funciona assim:

### 1. System Prompt (Cérebro do Agente)
**Arquivo:** `src/regras_negocio.py`

Este é o **único lugar** onde você "treina" o agente. Todas as regras de negócio estão aqui:
- Giro saudável (4-6 dias)
- Estratégias de balanceamento
- Regras por categoria (perecíveis, promoções, etc.)
- Alertas e prioridades
- Instruções personalizadas

### 2. Modelo Base (Ollama)
O LLaMA 3 original está instalado no Ollama. O aplicativo **não modifica** este modelo, apenas envia instruções através do system prompt.

### 3. Contexto da Conversa (Temporário)
Cada consulta envia dados atuais (estoque, vendas, etc.). O agente analisa e responde no momento, mas **não persiste** entre execuções.

---

## 🎯 Como Adicionar Novas Regras de Negócio

### Opção 1: Editar Arquivo de Regras (Recomendado)

**Arquivo:** `src/regras_negocio.py`

#### Exemplo 1: Adicionar Regra para Nova Categoria

```python
# No arquivo src/regras_negocio.py

REGRAS_CATEGORIAS["bebidas"] = {
    "dias_giro_maximo": 5,
    "prioridade": "MÉDIA",
    "observacao": "Bebidas têm demanda estável"
}
```

E adicione em `INSTRUCOES_EXTRAS`:

```python
INSTRUCOES_EXTRAS = """
...

   f) Produtos de Bebidas:
      - Máximo 5 dias de giro
      - Demanda geralmente estável
      - Atenção especial em datas comemorativas
"""
```

#### Exemplo 2: Adicionar Novo Alerta

```python
ALERTAS["venda_acelerando"] = {
    "condicao": "venda_7dias > venda_30dias * 0.5",
    "nivel": "OPORTUNIDADE",
    "acao": "Aumentar estoque - demanda crescendo"
}
```

#### Exemplo 3: Modificar Parâmetros de Giro

```python
GIRO_ESTOQUE = {
    "dias_minimo": 3,  # Mudou de 4 para 3
    "dias_maximo": 7,  # Mudou de 6 para 7
    "margem_seguranca": 1.3,  # 30% em vez de 20%
    "descricao": "Giro mais conservador"
}
```

### Opção 2: Interagir com o Agente via Sistema

Execute:
```bash
python iniciar_sistema.py
```

No menu, escolha a opção de consultar o agente e faça perguntas como:

```
"Como devo calcular o pedido para produtos em promoção?"

"Qual a melhor estratégia para produtos perecíveis?"

"Analise o produto X considerando que ele está em promoção"
```

O agente responderá baseado nas regras em `regras_negocio.py`.

---

## 📊 Atualização Diária do gerado.xlsx

### Como o Sistema Funciona com Dados Diários

1. **Arquivo Atualizado Diariamente:** `data/gerado.xlsx`
   - Novas vendas
   - Estoque atualizado
   - Tendências recentes

2. **Sistema Lê Dados Frescos:**
   ```bash
   python iniciar_sistema.py
   ```
   - Lê o arquivo atualizado
   - Aplica regras de `regras_negocio.py`
   - Calcula novas sugestões

3. **Agente Analisa Novos Dados:**
   - Compara tendências
   - Detecta mudanças
   - Ajusta recomendações

### Fluxo Diário Recomendado

```bash
# 1. Sistema atualiza gerado.xlsx (automaticamente ou manualmente)

# 2. Execute o sistema mestre
python iniciar_sistema.py

# 3. O sistema:
#    - Lê dados atualizados
#    - Calcula novas sugestões
#    - Gera sugestao_ia.xlsx
#    - Inicia agente para consultas
```

---

## 🔄 Exemplos de Variantes para Adicionar

### Variante 1: Sazonalidade

```python
# Em regras_negocio.py

REGRAS_SAZONALIDADE = {
    "natal": {
        "meses": [11, 12],  # Novembro e Dezembro
        "multiplicador_demanda": 2.0,  # Dobrar previsão
        "dias_giro_maximo": 10,  # Mais estoque permitido
        "observacao": "Período de alta demanda"
    },
    "verao": {
        "meses": [1, 2, 3],
        "categorias_afetadas": ["bebidas", "sorvetes"],
        "multiplicador_demanda": 1.5,
        "observacao": "Bebidas e sorvetes vendem mais"
    }
}
```

Adicione em `INSTRUCOES_EXTRAS`:
```python
   g) Sazonalidade:
      - Natal (Nov-Dez): Dobrar previsão de demanda
      - Verão (Jan-Mar): Bebidas +50% de demanda
      - Ajustar estoque_ideal temporariamente
```

### Variante 2: Fornecedores

```python
FORNECEDORES["Fornecedor_Novo"] = {
    "lead_time_dias": 5,
    "pedido_minimo_valor": 800,
    "confiabilidade": 0.95,  # 95% de entregas no prazo
    "observacao": "Novo fornecedor - monitorar desempenho"
}
```

### Variante 3: Dias da Semana

```python
REGRAS_DIA_SEMANA = {
    "sexta_sabado": {
        "multiplicador": 1.3,  # 30% mais vendas
        "observacao": "Final de semana vende mais"
    },
    "segunda": {
        "multiplicador": 0.8,  # 20% menos vendas
        "observacao": "Segunda geralmente mais fraca"
    }
}
```

---

## 💡 Perguntas Frequentes

### P: As mudanças em regras_negocio.py são aplicadas imediatamente?
**R:** Sim! Na próxima execução de `iniciar_sistema.py`, as novas regras serão usadas.

### P: Preciso reiniciar o Ollama?
**R:** Não! O Ollama continua rodando. Apenas o system prompt muda.

### P: O agente "esquece" as conversas anteriores?
**R:** Sim. Cada execução é independente. O agente não tem memória entre sessões.

### P: Como posso ver quais regras o agente está usando?
**R:** Abra `src/regras_negocio.py` e veja todas as regras configuradas.

### P: Posso ter múltiplos arquivos de regras?
**R:** Sim! Crie `regras_negocio_promocao.py`, `regras_negocio_natal.py`, etc. e importe conforme necessário.

---

## 🚀 Exemplo Prático: Adicionar Regra de Promoção

### Passo 1: Editar regras_negocio.py

```python
# Adicionar nova categoria
REGRAS_CATEGORIAS["promocao_black_friday"] = {
    "dias_giro_maximo": 3,  # Giro rápido
    "margem_seguranca": 2.0,  # Dobrar estoque
    "prioridade": "CRÍTICA",
    "observacao": "Black Friday - demanda explosiva"
}
```

### Passo 2: Adicionar instrução em INSTRUCOES_EXTRAS

```python
INSTRUCOES_EXTRAS = """
...
   h) Produtos em Black Friday:
      - Máximo 3 dias de giro (vende muito rápido)
      - DOBRAR margem de segurança (200%)
      - Prioridade CRÍTICA em pedidos
      - Monitorar estoque a cada 4 horas
      - Não deixar faltar em hipótese alguma
"""
```

### Passo 3: Executar o sistema

```bash
python iniciar_sistema.py
```

### Passo 4: Consultar o agente

```
"Como devo calcular o pedido para produtos na Black Friday?"
```

Resposta esperada:
```
Para produtos na Black Friday:

1. Giro máximo: 3 dias (demanda explosiva)
2. Margem de segurança: DOBRAR estoque normal
3. Prioridade: CRÍTICA - não pode faltar
4. Monitoramento: A cada 4 horas
5. Sugestão: Pedir 2x o normal + acompanhar de perto

Exemplo prático:
- Venda normal: 10 un/dia
- Black Friday: 40 un/dia (estimativa)
- Pedido: 40 * 3 * 2.0 = 240 unidades
```

---

## 📝 Resumo

| O Que | Onde | Como Atualizar |
|-------|------|----------------|
| Regras de Negócio | `src/regras_negocio.py` | Editar arquivo |
| System Prompt | Gerado de `regras_negocio.py` | Automático |
| Modelo Base | Ollama | Não modifica |
| Dados Diários | `data/gerado.xlsx` | Atualização externa |
| Sugestões IA | `data/sugestao_ia.xlsx` | Gerado pelo sistema |

---

**🎯 Dica Final:** Sempre que o arquivo `gerado.xlsx` for atualizado, execute `python iniciar_sistema.py` para recalcular as sugestões com as regras mais recentes!
