# Política de SLA — TechCorp Solutions

**Versão:** 2.0  
**Última revisão:** 2026-03-01  
**Responsável:** Gerência de Suporte

---

## Definições de Prioridade

| Prioridade | Critério | Exemplo |
|------------|----------|---------|
| **P1 — Crítico** | Sistema indisponível para o cliente | Login fora do ar, sem processar pedidos |
| **P2 — Alto** | Funcionalidade principal degradada | Pedidos lentos, erros intermitentes |
| **P3 — Médio** | Funcionalidade secundária com problema | Relatório com dado errado |
| **P4 — Baixo** | Melhoria ou dúvida de uso | "Como exportar em Excel?" |

---

## Tempos de Atendimento

| Prioridade | Primeiro Contato | Diagnóstico | Resolução |
|------------|-----------------|-------------|-----------|
| P1 | 15 minutos | 1 hora | 4 horas |
| P2 | 1 hora | 4 horas | 1 dia útil |
| P3 | 4 horas | 1 dia útil | 3 dias úteis |
| P4 | 1 dia útil | — | 10 dias úteis |

---

## Horário de Atendimento

- **N1 (bot/runbook):** 24h × 7 dias
- **N2 (analistas):** Segunda a sexta, 08h às 18h (horário de Brasília)
- **Plantão P1:** Segunda a sexta, 18h às 22h + finais de semana 09h às 17h

---

## Clientes VIP

Clientes com contrato **Premium** têm SLA reduzido em 50%:

| Prioridade | Resolução Standard | Resolução VIP |
|------------|-------------------|---------------|
| P1 | 4 horas | 2 horas |
| P2 | 1 dia útil | 4 horas |

Clientes VIP ativos: Farmácia Boa Saúde (CLI-001), Drogaria Central (CLI-007), Rede Saúde+ (CLI-012)

---

## Penalidades por SLA Vencido

- P1 não resolvido no prazo: desconto de 10% na próxima mensalidade
- Reincidência em 30 dias: reunião de análise de causa raiz obrigatória
- 3 P1s no mesmo mês: revisão contratual

---

## Comunicação com o Cliente

- **Abertura:** confirmação automática por email em até 5 minutos
- **Updates:** a cada hora para P1, a cada 4h para P2
- **Fechamento:** email com resumo da solução + orientações preventivas

Usar template padrão do `.github/prompts/close-ticket.prompt.md`.
