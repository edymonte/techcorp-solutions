# Política de Escalação — TechCorp Solutions

**Versão:** 1.3  
**Última revisão:** 2026-04-02  
**Responsável:** Gerência de Suporte

---

## Quando Escalar

Escale o chamado imediatamente quando:

1. O tempo de diagnóstico do SLA for atingido sem resolução
2. O problema afetar múltiplos clientes simultaneamente
3. Houver suspeita de vulnerabilidade de segurança
4. O N1 não encontrar runbook correspondente ao sintoma
5. O cliente solicitar explicitamente falar com engenharia

---

## Níveis de Escalação

### N1 — Bot de Suporte TechCorp
- Triagem inicial baseada nos runbooks de `docs/runbooks/`
- Responde perguntas frequentes automaticamente via GitHub Copilot
- Se não encontrar solução: marca o ticket como `aguardando-N2`

### N2 — Analistas de Suporte
- Diagnóstico e resolução de problemas conhecidos
- Executa procedimentos dos runbooks
- Escalação para N3 se não resolver em 2h (P1) ou 8h (P2)

### N3 — Time de Engenharia
- Bugs no código ou infraestrutura
- Acionado via issue no GitHub com label `escalation/n3`
- Obrigatório: PR com fix + teste unitário cobrindo o cenário

### N4 — Tech Lead / CTO
- Incidentes críticos com impacto financeiro
- Decisões arquiteturais urgentes
- Acionado apenas quando N3 não consegue resolver em 4h

---

## Canais de Comunicação

| Nível | Canal | Urgência |
|-------|-------|----------|
| N2 → N3 | `#suporte-n3` no Slack | Normal |
| P1 qualquer nível | `#incidentes` no Slack | Imediata |
| N3 → N4 | Ligação direta + `#incidentes` | Crítica |

---

## Informações Obrigatórias na Escalação

Ao escalar, sempre incluir:

```
TICKET: [número]
CLIENTE: [nome] — [prioridade contratual]
SINTOMA: [descrição em 1 linha]
JÁ TENTEI: [o que foi feito]
LOGS: [trecho relevante do log]
IMPACTO: [número de usuários afetados]
```

---

## Pós-Incidente (P1 e P2)

- Dentro de 24h após resolução: preencher o template de post-mortem
- Atualizar o runbook correspondente se o problema não estava documentado
- Abrir issue de dívida técnica se o fix for paliativo
