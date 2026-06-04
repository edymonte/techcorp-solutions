# Guia do Participante — TechCorp Solutions Workshop

> Mantenha este guia aberto ao lado do ticket da semana.  
> A cada passo: **leia → escreva o prompt → valide → avance.**

---

## Antes de cada semana — faça sempre

```bash
# 1. Confirme que o ambiente está ok
python setup/verificar_ambiente.py

# 2. Confirme os bugs intencionais (saída esperada: 3 ⚠ avisos, 0 ✘ erros)
python -m pytest tests/ --tb=no -q
```

Se aparecer ✘ erro (não ⚠ aviso), chame o facilitador antes de continuar.

---

## Regra de ouro — válida em todas as etapas

> Se o Copilot te deu uma resposta genérica, o problema está no prompt — não no Copilot.

Um prompt profissional tem 5 elementos:

| Elemento | O que é |
|---|---|
| **Papel** | Quem o Copilot deve ser nesta resposta |
| **Contexto** | O que ele precisa saber sobre o sistema |
| **Tarefa** | O que você quer que ele faça (uma coisa só) |
| **Restrições** | O que ele não pode fazer ou deve respeitar |
| **Formato** | Como a resposta deve ser estruturada |

---

---

## ETAPA 1 — "O chamado chegou" 🟢 ESSENCIAL

**Seu papel:** Analista N2 de suporte  
**Arquivo-alvo:** `src/api/pedidos.py`  
**Meta:** Fazer o teste `test_pedido_quantidade_none_deve_levantar_pedido_invalido_error` passar  
**Tempo:** ~1h30

---

### PASSO 1 — Leia o ticket completo

Abra `tickets/ticket-001.md`. Leia tudo — especialmente:
- O relato da Maria Silva (supervisora da Farmácia Boa Saúde)
- A seção **"Triagem N1 — Bot de Suporte TechCorp"**
- A lista de ações recomendadas para o N2

> ⚠️ Não abra `src/api/pedidos.py` ainda. Deixe o Copilot te mostrar onde está o problema.

---

### PASSO 2 — Abra o template de prompt

Abra `.github/prompts/investigar-bug-ticket.prompt.md`.  
Este é o template oficial da TechCorp — **use como base, não invente do zero**.

---

### PASSO 3 — Monte seu prompt no Copilot Chat

Abra o Copilot Chat (`Ctrl+Shift+I`) e preencha o template com os dados do ticket:

```
Você é um desenvolvedor N2 da TechCorp Solutions, responsável por
resolver o TICKET-001.

Sintoma reportado: pedidos com quantidade=None travam o sistema com
TypeError. O N1 indicou que o problema está em validar_pedido() em
src/api/pedidos.py.

O que preciso:
1. Identifique a linha exata do TypeError e explique por quê ocorre
2. Mostre o fix mínimo em formato diff
3. Escreva um teste pytest para o caso quantidade=None em tests/test_pedidos.py

Restrições:
- Não altere a assinatura da função validar_pedido()
- Fix mínimo — não refatore o código ao redor
- Siga os padrões de .github/copilot-instructions.md
```

**Avalie a resposta recebida:**

| O Copilot entregou | O que fazer |
|---|---|
| Diff + teste prontos | Vá para o Passo 4 |
| Explicação genérica sem linha específica | Adicione `#file:src/api/pedidos.py` antes do prompt e reenvie |
| Proposta de refatoração grande | Reforce a restrição: *"apenas o fix mínimo, nada mais"* |

---

### PASSO 4 — Aplique o fix

Abra `src/api/pedidos.py` e aplique **exatamente** o diff sugerido. Não adicione nada além do necessário.

---

### PASSO 5 — Valide com pytest

```bash
pytest tests/test_pedidos.py -v
```

Resultado esperado: **14 passed**. Se falhar mais do que o bug intencional, volte ao Passo 3.

---

### PASSO 6 — Preencha o ticket

Em `tickets/ticket-001.md`, seção "Ações do N2", peça ao Copilot:

```
Gere o texto para preencher a seção "Ações do N2" do TICKET-001
com base no diagnóstico e fix que aplicamos. Siga o formato do ticket.
```

---

### PASSO 7 — Gere a evidência

```bash
python setup/gerar_evidencia.py --semana 1 --nome "Seu Nome" --parceiro "Nome do Parceiro"
```

Um HTML abrirá no navegador. Print da tela = entrega da etapa. ✅

---

---

## ETAPA 2 — "O pipeline quebrou" 🟡 INTERMEDIÁRIO

**Seu papel:** Dev de Plataforma  
**Arquivo-alvo:** `.github/workflows/ci.yml`  
**Meta:** Entender a causa do erro no CI e corrigir o workflow  
**Tempo:** ~1h30

---

### PASSO 1 — Leia o ticket e o log de erro

Abra `tickets/ticket-002.md`. Identifique:
- O PR que causou a falha (`#14 — dev-carlos`)
- O log exato do Actions (seção "Erro no log do Actions")
- O padrão de CI da empresa: `docs/pipelines/padrao-ci.md`

---

### PASSO 2 — Consulte o N1 antes de abrir qualquer código

No chat do N1 (AnythingLLM), pergunte:

```
O pipeline de CI falhou com o erro:
ERROR: No matching distribution found for techcorp_core

O que pode estar causando isso e qual runbook devo seguir?
```

O N1 deve citar `docs/runbooks/pipeline-troubleshooting.md` e indicar o arquivo problemático.

---

### PASSO 3 — Use @workspace para mapear o impacto

No Copilot Chat, use `@workspace` para entender o escopo antes de mexer em qualquer coisa:

```
@workspace Onde o pacote techcorp_core é referenciado no projeto?
Liste todos os arquivos e linhas.
```

---

### PASSO 4 — Monte o prompt usando #file

Abra `.github/prompts/corrigir-pipeline.prompt.md` como base e envie:

```
#file:.github/workflows/ci.yml #file:docs/pipelines/padrao-ci.md

Log de erro do Actions:
ERROR: Could not find a version that satisfies the requirement techcorp_core
ERROR: No matching distribution found for techcorp_core
[exit code 1]

PR suspeito: #14 — "feat: adicionar validação de estoque no processador" (autor: dev-carlos)

1. Identifique o step com falha e a causa raiz em uma frase
2. Localize o problema no arquivo ci.yml com a linha exata
3. Mostre o fix em formato diff
4. Verifique se o fix está em conformidade com docs/pipelines/padrao-ci.md
5. Gere o comentário de diagnóstico para o PR no formato definido no template
```

**Avalie a resposta recebida:**

| O Copilot entregou | O que fazer |
|---|---|
| Linha exata no ci.yml + diff | Vá para o Passo 5 |
| "Adicione o pacote ao requirements.txt" | Errado — reforce que o problema está no ci.yml, não no requirements |
| Análise sem citar arquivo específico | Adicione o conteúdo do ci.yml diretamente no prompt |

---

### PASSO 5 — Aplique o fix no ci.yml

Abra `.github/workflows/ci.yml` e aplique o diff sugerido.

---

### PASSO 6 — Valide localmente

```bash
# Confirme que os testes ainda passam após a mudança no ci.yml
pytest tests/ --tb=no -q
```

Resultado esperado: mesmas 3 falhas intencionais (⚠) e zero falhas inesperadas.

---

### PASSO 7 — Gere o comentário do PR

Peça ao Copilot para gerar o texto do comentário no formato definido no template:

```
Gere o comentário de diagnóstico para o PR #14 no formato:
## Diagnóstico — TICKET-002
**Causa:** ...
**Arquivo:** ...
**Fix:** ...
**Teste local:** ...
```

---

### PASSO 8 — Gere a evidência

```bash
python setup/gerar_evidencia.py --semana 2 --nome "Seu Nome" --parceiro "Nome do Parceiro"
```

---

---

## ETAPA 3 — "Tudo caiu ao mesmo tempo" 🔴 CHALLENGE

**Seu papel:** Engenheiro de plantão (Dev + Suporte simultaneamente)  
**Arquivos-alvo:** `src/auth/auth_service.py` + `requirements.txt` + `db/techcorp.db`  
**Meta:** Triagear e resolver 3 sub-incidentes simultâneos em ordem de prioridade  
**Tempo:** ~1h30

> ⚠️ Esta etapa usa **Agent Mode**. Ative-o no Copilot Chat antes de começar.  
> O ícone de agente fica no seletor de modo no topo do chat.

---

### PASSO 1 — Consulte o banco de chamados (MCP SQLite)

No Copilot Chat (modo Agent), consulte o banco:

```
Use o MCP do SQLite para listar todos os chamados abertos em db/techcorp.db,
ordenados por prioridade. Mostre: ID, título, prioridade e status.
```

---

### PASSO 2 — Consulte o N1 para triagem

No AnythingLLM:

```
Temos 3 chamados P1 simultâneos:
A) autenticação fora do ar — tokens expirados sendo aceitos como válidos
B) pipeline bloqueado — ModuleNotFoundError: No module named 'jwt'
C) cliente VIP CLI-001 sem acesso ao painel há 40 minutos

Qual a ordem de prioridade pelo SLA da TechCorp e qual runbook para cada um?
```

---

### PASSO 3 — Monte o prompt de incidente múltiplo

Abra `.github/prompts/resposta-incidente-multiplo.prompt.md` como base:

```
#file:docs/runbooks/auth-reset.md
#file:src/auth/auth_service.py
#file:requirements.txt

Sub-incidente A: autenticação JWT — tokens expirados aceitos como válidos
Sub-incidente B: pipeline bloqueado — ModuleNotFoundError: No module named 'jwt'
Sub-incidente C: cliente VIP CLI-001 sem acesso ao painel

Faça a triagem dos 3 sub-incidentes em ordem de prioridade.
Para cada um: causa raiz, arquivo, linha, fix mínimo em diff, teste de validação.

Restrições:
- Fixes de segurança têm prioridade absoluta
- NÃO rotacione SECRET_KEY sem avisar explicitamente
- Não feche um sub-incidente sem teste que previne regressão
- Clientes CLI-001 e CLI-012 têm SLA de 2h — sinalize se estiver em risco
```

**Avalie a triagem proposta:**

| A triagem propõe | O que esperar |
|---|---|
| Segurança (auth) → Pipeline → Acesso | ✅ Ordem correta |
| Pipeline antes de auth | ❌ Errado — refaça o prompt enfatizando a restrição de segurança |

---

### PASSO 4 — Aplique os fixes em ordem

Para **cada sub-incidente**, repita:
1. Leia o diff proposto
2. Entenda o que muda **antes** de aceitar
3. Aplique o fix
4. Rode o teste correspondente:

```bash
# Sub-incidente A (auth — valida os 2 testes que estavam falhando)
pytest tests/test_auth.py -v

# Sub-incidente B (pipeline — verifique requirements.txt)
# Confirme que pyjwt==2.8.0 está presente no requirements.txt

# Sub-incidente C (valida após A estar resolvido — mesmo teste)
pytest tests/test_auth.py -v
```

---

### PASSO 5 — Atualize o banco via MCP SQLite

No Copilot Chat (Agent Mode):

```
Use o MCP do SQLite para atualizar o status dos 3 chamados
em db/techcorp.db para 'resolvido'.
Mostre o SQL que vai executar antes de aplicar.
```

---

### PASSO 6 — Atualize o copilot-instructions.md

Peça ao Copilot para sugerir uma regra de prevenção:

```
Com base nos 3 problemas que resolvemos hoje, sugira uma regra para adicionar
em .github/copilot-instructions.md que previna regressão de cada um.
```

---

### PASSO 7 — Valide o ambiente completo

```bash
pytest tests/ -v
python setup/verificar_ambiente.py
```

Resultado esperado: **39 passed**, zero falhas inesperadas, 9 ✔ no verificador.

---

### PASSO 8 — Gere a evidência final

```bash
python setup/gerar_evidencia.py --semana 3 --nome "Seu Nome" --parceiro "Nome do Parceiro"
```

---

---

## Sinais de que seu prompt precisa melhorar

| Sinal na resposta do Copilot | O que está faltando no prompt |
|---|---|
| Explicação genérica sem citar arquivo/linha | Adicione `#file:` com o arquivo relevante |
| Sugestão de refatoração grande | Adicione: *"fix mínimo, não refatore o código ao redor"* |
| Resposta ignorou as restrições | Mova as restrições para o **início** do prompt |
| Não seguiu o formato pedido | Seja explícito: *"responda APENAS neste formato: ..."* |
| Inventou um pacote que não existe | Adicione: *"use apenas pacotes listados em requirements.txt"* |
| Proposta certa mas sem teste | Adicione: *"inclua o teste pytest que valida o fix"* |

---

## Atalhos úteis no VS Code

| Ação | Atalho |
|---|---|
| Abrir Copilot Chat | `Ctrl+Shift+I` |
| Sugestão inline | `Alt+\` |
| Aceitar sugestão inline | `Tab` |
| Abrir terminal integrado | `` Ctrl+` `` |
| Buscar em todos os arquivos | `Ctrl+Shift+F` |
