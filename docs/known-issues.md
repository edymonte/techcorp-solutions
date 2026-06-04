# TechCorp Solutions — Problemas Conhecidos

> Documento interno de engenharia. Mantido pelo time de plataforma.  
> Última atualização: 2026-06-01

---

## Sobre este documento

Registro de comportamentos anômalos identificados no ambiente de produção da TechCorp Solutions.  
**Nem todos os itens abaixo representam bugs abertos** — alguns são limitações conhecidas com workaround documentado.

---

## KI-001 — Integração PDV: campo `quantidade` pode chegar nulo

**Componente:** `src/api/pedidos.py` — função `validar_pedido()`  
**Severidade:** Alta  
**Status:** Aguardando correção  
**Identificado em:** 2026-05-28

**Contexto:**  
PDVs da versão 3.x em diante passaram a enviar `"quantidade": null` quando o produto não tem estoque cadastrado, em vez de `"quantidade": 0`.  
A função `validar_pedido()` faz comparação direta com `<= 0` sem verificar `None` antes — isso causa `TypeError` em runtime.

**Sintoma em produção:**  
Clientes que usam PDV 3.x relatam erro silencioso ao finalizar pedido. O pedido não é confirmado e não há mensagem de erro para o usuário.

**Workaround atual:**  
Nenhum. O N1 orienta o cliente a reiniciar o PDV — o que não resolve o problema.

**Fix esperado:**  
Tratar `None` antes de qualquer comparação numérica em `validar_pedido()`.

---

## KI-002 — Import absoluto de módulo interno introduzido no PR #12

**Componente:** `src/pedidos/processador.py`  
**Severidade:** Média  
**Status:** Aguardando revisão  
**Identificado em:** 2026-05-30

**Contexto:**  
O padrão do time exige imports relativos para módulos internos (documentado em `docs/pipelines/padrao-ci.md`).  
O PR #12 introduziu um import absoluto que não causa problema em desenvolvimento local — mas falha no CI porque o módulo `techcorp_core` não existe como pacote instalável.

**Sintoma em produção:**  
O pipeline de CI passa localmente e quebra no GitHub Actions com `ModuleNotFoundError`.

**Workaround atual:**  
Nenhum — o deploy está bloqueado.

**Fix esperado:**  
Substituir import absoluto por caminho relativo conforme padrão do time.

---

## KI-003 — `verify_exp: False` em `auth_service.py`

**Componente:** `src/auth/auth_service.py` — função `validar_token()`  
**Severidade:** Crítica — impacto de segurança  
**Status:** Aberto — prioridade máxima  
**Identificado em:** 2026-06-01

**Contexto:**  
Durante uma refatoração emergencial em fevereiro, a opção `verify_exp: False` foi adicionada ao decoder JWT para contornar um problema de clock skew entre servidores.  
O problema de clock foi resolvido, mas a flag nunca foi removida.

**Sintoma em produção:**  
Tokens expirados estão sendo aceitos pela API. Clientes VIP com sessões longas (>8h) estão sendo autenticados com tokens que deveriam ter expirado — comportamento intermitente dependendo de qual instância processa a requisição.

**Risco de segurança:**  
Um token comprometido com validade expirada continua funcional indefinidamente enquanto a flag estiver ativa.

**Restrição crítica:**  
⚠️ **NÃO rotacionar a `SECRET_KEY` sem aprovação do CTO** — isso invalidaria todas as sessões ativas de produção simultaneamente.

**Fix esperado:**  
Remover `verify_exp: False`. A verificação de expiração padrão do PyJWT deve ser usada.

---

## KI-004 — `pyjwt` ausente no `requirements.txt`

**Componente:** `requirements.txt`  
**Severidade:** Alta  
**Status:** Aguardando correção  
**Identificado em:** 2026-06-20

**Contexto:**  
O módulo `pyjwt` é usado em `src/auth/auth_service.py` mas não foi adicionado ao `requirements.txt` quando o auth service foi implementado.  
Em ambientes limpos (CI, novas máquinas de dev) o import falha com `ModuleNotFoundError: No module named 'jwt'`.

**Sintoma:**  
Pipeline quebra com erro de import. Funciona localmente apenas porque `pyjwt` está instalado como dependência transitiva de outro pacote.

---

## Notas gerais de arquitetura

- **Clock skew tolerado:** 30 segundos (configurado no load balancer, não no código)
- **Timeout de sessão de UI:** 4 horas (configurado no frontend, independente do JWT)
- **Ambientes:** `dev` e `staging` compartilham o mesmo banco — não fazer testes destrutivos em `staging`
