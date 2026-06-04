# Ticket-001 — Falha no Processamento de Pedidos

**ID:** TICKET-001  
**Cliente:** Farmácia Boa Saúde (CLI-001) — ⭐ VIP Premium  
**Prioridade:** P1 — Crítico  
**Status:** 🔴 Aberto  
**Aberto em:** 2026-06-03 14:12  
**Responsável:** aguardando N2  
**SLA:** resolução até 2026-06-03 16:12 (2h — cliente VIP)

---

## Relato do Cliente

> "Desde as 14h o sistema travou. Os pedidos não estão sendo confirmados. Quando a atendente tenta finalizar a compra, aparece uma tela de erro e o pedido some. Já reiniciamos o sistema e não resolveu. Estamos perdendo vendas."

**Canal:** Telefone  
**Contato:** Maria Silva — Supervisora de Loja  
**Fone:** (85) 9XXXX-XXXX

---

## 🤖 Triagem N1 — Bot de Suporte TechCorp

> *Nota gerada automaticamente em 2026-06-03 14:15*

**Diagnóstico provável:** Com base no sintoma relatado (pedidos não são confirmados + tela de erro), consultei o runbook `docs/runbooks/pedidos-falha.md`.

**Causa mais provável:** Campo `quantidade` nulo ou ausente no payload enviado pela integração do PDV. A função `validar_pedido()` em `src/api/pedidos.py` não trata `None` antes da comparação numérica, lançando `TypeError`.

**Evidência:** O sistema PDV da Farmácia Boa Saúde foi atualizado em 2026-06-02. Versões antigas deste PDV enviam `"quantidade": null` quando o produto não tem estoque cadastrado.

**Ação recomendada para N2:**
1. Verificar logs: `tail -50 logs/api.log | grep TypeError`
2. Abrir `src/api/pedidos.py` e localizar a função `validar_pedido()`
3. Corrigir o tratamento de `None` antes da comparação `<= 0`
4. Adicionar teste unitário cobrindo `quantidade = None`
5. Abrir PR com o fix e fechar este ticket com a solução

---

## Ações do N2

> *[Preencher durante a resolução]*

**Diagnóstico:**

**Solução aplicada:**

**Teste realizado:**

---

## Encerramento

**Fechado em:** _______________  
**Resolvido por:** _______________  
**Tempo de resolução:** _______________  
**Resolução dentro do SLA?** ☐ Sim ☐ Não

**Resumo da solução:**

---

## Lições Aprendidas / Prevenção

> *[Preencher após resolução — será usado para atualizar o runbook]*
