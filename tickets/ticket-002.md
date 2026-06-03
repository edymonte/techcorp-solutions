# Ticket-002 — Pipeline de Produção Bloqueado

**ID:** TICKET-002  
**Afetado:** Time de Desenvolvimento — TechCorp interno  
**Prioridade:** P2 — Alto  
**Status:** 🔴 Aberto  
**Aberto em:** 2026-06-10 09:47  
**Responsável:** aguardando Dev de Plataforma  
**SLA:** resolução até 2026-06-11 09:47 (1 dia útil)

---

## Descrição do Incidente

Um PR foi aprovado e mergeado na `main` às 09:40. O GitHub Actions disparou automaticamente e falhou no step **"Install dependencies"**. O deploy está bloqueado.

**Erro no log do Actions:**
```
Step: Install dependencies
Run pip install -r requirements.txt

Collecting flask==3.0.3
  Downloading Flask-3.0.3...
Collecting pyjwt==2.8.0
  Downloading PyJWT-2.8.0...
Collecting techcorp_core
  ERROR: Could not find a version that satisfies the requirement techcorp_core
  ERROR: No matching distribution found for techcorp_core

[exit code 1]
```

**PR que causou a falha:** #14 — "feat: adicionar validação de estoque no processador"  
**Autor do PR:** dev-carlos  
**Revisores que aprovaram:** dev-ana

---

## 🤖 Triagem N1 — AnythingLLM

> *Nota gerada automaticamente em 2026-06-10 09:52*

**Diagnóstico:** Consultei o runbook `docs/runbooks/pipeline-troubleshooting.md`.

**Causa identificada:** O arquivo `requirements.txt` não contém o pacote `techcorp_core`, mas o código o importa diretamente. Isso viola o padrão documentado em `docs/pipelines/padrao-ci.md` — módulos internos não devem ser importados como pacotes externos.

**Ação recomendada para N2/Dev:**
1. Executar `grep -r "techcorp_core" src/` para localizar o import problemático
2. Corrigir o import para usar o caminho relativo (`from src.pedidos import processador`)
3. Verificar se há outros imports absolutos de módulos internos
4. Atualizar o `requirements.txt` removendo referências a módulos internos
5. Criar ou atualizar o `.github/copilot-instructions.md` com a regra de imports
6. Via MCP GitHub: comentar no PR #14 com o diagnóstico
7. Abrir PR com o fix — verificar que o pipeline fica verde

---

## Ações do Dev

> *[Preencher durante a resolução]*

**Localização do import problemático:**

**Correção aplicada:**

**`copilot-instructions.md` atualizado?** ☐ Sim ☐ Não

**PR de fix:** #___

---

## Encerramento

**Pipeline verde em:** _______________  
**Fechado em:** _______________  
**Resolvido por:** _______________  
**Resolução dentro do SLA?** ☐ Sim ☐ Não

---

## Dívida Técnica Identificada

- [ ] Adicionar lint rule para detectar imports absolutos de módulos internos
- [ ] Criar `copilot-instructions.md` com o padrão para o time não repetir o erro
