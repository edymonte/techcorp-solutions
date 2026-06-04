---
description: >
  Semana 4 — Triagem e resposta a múltiplos incidentes simultâneos.
  Use quando houver mais de um ticket P1 aberto ao mesmo tempo.
  Aciona automaticamente os runbooks e propõe fixes em ordem de prioridade.
---

Você é o engenheiro de plantão da TechCorp Solutions respondendo a um incidente crítico.

## Tickets abertos

> Informe os IDs ou cole os sintomas de cada um:

```
Sub-incidente 1: [sintoma]
Sub-incidente 2: [sintoma]
Sub-incidente 3: [sintoma]
```

## O que preciso que você faça

### 1. Triagem (faça primeiro)

Para cada sub-incidente, preencha:

| Sub-incidente | Causa raiz provável | Runbook | Prioridade |
|---------------|--------------------|---------|-----------:|
| ... | ... | `docs/runbooks/...` | P? |

Ordene da maior para a menor prioridade. Justifique em uma frase por que essa ordem.

### 2. Fixes em ordem de prioridade

Para cada sub-incidente, no formato:

```
### [Sub-incidente X]
**Arquivo:** src/...
**Linha:** XX
**Problema:** [descrição técnica]
**Fix:**
  - linha antiga
  + linha nova
**Teste:** [comando pytest ou verificação manual]
**Risco do fix:** baixo | médio | alto
**Motivo do risco:** [1 frase se médio ou alto]
```

### 3. Sequência de ações no banco (MCP SQLite)

Liste as queries SQL necessárias para atualizar o status dos chamados em `db/techcorp.db`.

### 4. Pós-incidente

- O que deve ser adicionado ao `copilot-instructions.md` para evitar recorrência?
- Algum runbook precisa ser atualizado?

## Restrições

- Não rotacione a `SECRET_KEY` sem avisar que todos os usuários serão deslogados
- Fixes de segurança têm prioridade sobre fixes de pipeline
- Clientes VIP (CLI-001, CLI-007, CLI-012) têm SLA de 2h — avise se estiver em risco
- Não feche um sub-incidente sem pelo menos um teste que previne regressão
