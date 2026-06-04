# Ticket-003 — Incidente Crítico: Múltiplas Falhas Simultâneas

**ID:** TICKET-003  
**Prioridade:** P1 — Crítico  
**Status:** 🔴 Aberto  
**Aberto em:** 2026-06-20 17:03 (sexta-feira)  
**Responsável:** aguardando Dev + Suporte  
**SLA:** resolução até 2026-06-20 19:03 (2h — múltiplos VIPs afetados)

---

## ⚠️ ATENÇÃO — 3 CHAMADOS SIMULTÂNEOS

Este ticket agrupa 3 incidentes correlacionados abertos nos últimos 15 minutos.

---

### Sub-incidente A — Autenticação fora do ar
**Reportado por:** Rede Saúde+ (CLI-012) — ⭐ VIP Premium  
**Sintoma:** Todos os usuários da rede recebem `401 Unauthorized` ao tentar logar. O sistema passou a rejeitar os tokens emitidos hoje de manhã.

**Detalhe técnico suspeito:** tokens com mais de 8 horas continuam funcionando para alguns usuários (tokens de ontem). Tokens novos são aceitos e depois invalidados aleatoriamente.

---

### Sub-incidente B — Pipeline de produção bloqueado novamente
**Reportado por:** Time interno — Dev  
**Sintoma:** Após o hotfix do Ticket-002, um novo deploy foi tentado. O pipeline está vermelho em um step diferente: `ModuleNotFoundError: No module named 'jwt'`. O `pyjwt` não está no `requirements.txt`.

---

### Sub-incidente C — Cliente VIP sem acesso (relacionado a A)
**Reportado por:** Farmácia Boa Saúde (CLI-001) — ⭐ VIP Premium  
**Sintoma:** Gerente da farmácia não consegue acessar o painel administrativo. O token dele foi emitido há 10 horas — deveria ter expirado, mas o sistema ora aceita ora rejeita.

**Impacto financeiro estimado:** R$ 12.000/h de vendas paradas.

---

## 🤖 Triagem N1 — Bot de Suporte TechCorp

> *Nota gerada automaticamente em 2026-06-20 17:08*

**Análise correlacionada dos 3 sub-incidentes:**

Consultei `docs/runbooks/auth-reset.md` e `docs/runbooks/pipeline-troubleshooting.md`.

**Causa raiz provável (A e C):** A função `validar_token()` em `src/auth/auth_service.py` usa `options={"verify_exp": False}`, desabilitando a verificação de expiração. Tokens expirados são aceitos — mas o comportamento intermitente sugere que pode haver outra validação acontecendo em camada superior que rejeita tokens antigos de forma inconsistente.

**Causa raiz (B):** `pyjwt` não está no `requirements.txt`. Adicionado como dependência do auth_service mas nunca foi commitado.

**Ação recomendada (ordem de prioridade):**

1. **IMEDIATO** — Corrigir `auth_service.py`: remover `options={"verify_exp": False}`
2. **IMEDIATO** — Forçar re-login de todos: rotacionar `SECRET_KEY` para invalidar todos os tokens ativos
3. Adicionar `pyjwt==2.8.0` ao `requirements.txt`
4. Via MCP SQLite: atualizar status dos 3 chamados no banco
5. Via MCP GitHub: abrir PR com os fixes + fechar as issues
6. Criar `.agent.md` de resposta a incidentes para o time usar no futuro

---

## Ações do Time

> *[Preencher durante a resolução]*

**Sub-incidente A — auth_service.py corrigido?** ☐ Sim  
**Sub-incidente B — requirements.txt atualizado?** ☐ Sim  
**Sub-incidente C — clientes notificados?** ☐ Sim  

**SECRET_KEY rotacionada?** ☐ Sim  
**PR de fix:** #___  
**Pipeline verde?** ☐ Sim  

---

## Encerramento

**Todos os sub-incidentes resolvidos em:** _______________  
**Fechado por:** _______________  
**Resolução dentro do SLA?** ☐ Sim ☐ Não  

---

## Post-Mortem (obrigatório para P1)

> *Preencher em até 24h após resolução*

**Causa raiz confirmada:**

**Por que não foi detectado antes:**

**Ações preventivas:**

- [ ] Adicionar teste de segurança para validação de expiração JWT
- [ ] Criar `.agent.md` de resposta a incidentes
- [ ] Revisão completa do `requirements.txt`
