# Runbook — Falha no Processamento de Pedidos

**Categoria:** Suporte N1/N2  
**Produto:** TechCorp ERP — Módulo de Pedidos  
**Versão:** 2.1  
**Última revisão:** 2026-05-10

---

## Sintomas

- Pedidos não aparecem na fila de processamento
- Erro `TypeError` ou `PedidoInvalidoError` nos logs da API
- Clientes relatam que o carrinho trava ao confirmar compra
- Status do pedido permanece `pendente` indefinidamente

---

## Causas Comuns

### 1. Campo `quantidade` nulo ou ausente
Sistemas legados de integração (ex: PDV antigo) podem enviar o campo `quantidade` como `null` no JSON. A API não trata esse caso e lança exceção.

**Log esperado:**
```
TypeError: '<=' not supported between instances of 'NoneType' and 'int'
```

**Localização do código:** `src/api/pedidos.py` → função `validar_pedido()`

### 2. Produto sem preço cadastrado
Pedidos com `preco_unitario` zerado ou ausente são processados mas geram `valor_total = 0`.

### 3. Timeout na fila de processamento
A fila interna tem timeout de 30s. Pedidos acima desse tempo são descartados silenciosamente.

### 4. Banco de dados indisponível
Verificar `db/techcorp.db` — se o arquivo estiver corrompido ou bloqueado, nenhum pedido é persistido.

---

## Diagnóstico

### Passo 1 — Verificar os logs da API
```bash
tail -100 logs/api.log | grep -i "pedido\|error\|TypeError"
```

### Passo 2 — Consultar os últimos pedidos com erro
```sql
SELECT id, status, erro, criado_em
FROM pedidos
WHERE status = 'erro'
ORDER BY criado_em DESC
LIMIT 10;
```

### Passo 3 — Reproduzir o erro localmente
```python
from src.api.pedidos import validar_pedido

# Simular payload com quantidade nula (caso mais comum)
pedido_teste = {
    "cliente_id": "CLI-001",
    "produto_id": "PROD-042",
    "quantidade": None  # <- causa do problema
}

validar_pedido(pedido_teste)
```

---

## Resolução

### Caso 1 — Quantidade nula
Corrigir a função `validar_pedido()` em `src/api/pedidos.py` para tratar `None` antes da comparação:

```python
# ANTES (com bug)
if pedido["quantidade"] <= 0:
    raise PedidoInvalidoError("Quantidade deve ser maior que zero")

# DEPOIS (corrigido)
if pedido["quantidade"] is None:
    raise PedidoInvalidoError("Campo 'quantidade' não pode ser nulo")
if pedido["quantidade"] <= 0:
    raise PedidoInvalidoError("Quantidade deve ser maior que zero")
```

### Caso 2 — Reprocessar pedidos pendentes
```sql
-- Identificar pedidos travados há mais de 1 hora
SELECT id FROM pedidos
WHERE status = 'pendente'
AND criado_em < datetime('now', '-1 hour');
```

Após corrigir o código, reprocessar via endpoint:
```
POST /api/pedidos/{id}/reprocessar
```

---

## Prevenção

- Adicionar testes unitários para `quantidade = None`, `quantidade = 0`, `quantidade = -1`
- Validar schema do payload na camada de entrada (antes de chegar na função de negócio)
- Configurar alerta no Grafana para `status = 'erro'` acima de 5/min

---

## Escalação

Se o problema persistir após os passos acima:
1. Acionar o Tech Lead de Plataforma via canal `#suporte-critico`
2. Abrir issue no repositório com label `bug/pedidos`
3. Consultar `docs/suporte/escalation-policy.md`
