# Arquitetura — Visão Geral do Sistema TechCorp ERP

**Versão:** 3.0  
**Última revisão:** 2026-04-15  
**Responsável:** Time de Plataforma

---

## Visão Geral

O TechCorp ERP é um sistema de gestão de pedidos voltado para pequenas e médias empresas do varejo farmacêutico. Roda 100% local (on-premises), sem dependências de nuvem.

---

## Componentes Principais

```
┌─────────────────────────────────────────────────────────┐
│                    TechCorp ERP                         │
│                                                         │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────┐  │
│  │  API de      │    │  Módulo de   │    │  Auth    │  │
│  │  Pedidos     │───▶│  Processador │    │  Service │  │
│  │  (pedidos.py)│    │  (processad) │    │ (auth_s) │  │
│  └──────┬───────┘    └──────┬───────┘    └────┬─────┘  │
│         │                  │                  │        │
│         └──────────────────┴──────────────────┘        │
│                            │                           │
│                    ┌───────▼──────┐                    │
│                    │  SQLite DB   │                    │
│                    │ techcorp.db  │                    │
│                    └──────────────┘                    │
└─────────────────────────────────────────────────────────┘
```

---

## Módulos e Responsabilidades

### `src/api/pedidos.py`
- Recebe requisições de novos pedidos
- Valida campos obrigatórios (`cliente_id`, `produto_id`, `quantidade`)
- Encaminha para o processador após validação

**Regras de negócio:**
- `quantidade` deve ser inteiro positivo (nunca nulo)
- `cliente_id` deve referenciar um cliente ativo no banco
- Pedidos duplicados (mesmo `cliente_id` + `produto_id` nos últimos 60s) são bloqueados

### `src/pedidos/processador.py`
- Processa pedidos validados
- Calcula `valor_total = quantidade × preco_unitario`
- Persiste no banco com status `processado`
- Emite evento para notificação ao cliente

**SLA:** processamento em até 2 segundos por pedido.

### `src/auth/auth_service.py`
- Emite tokens JWT com validade de 8 horas
- Valida tokens em todas as requisições protegidas
- Gerencia perfis: `admin`, `suporte`, `dev`

**Regras de segurança:**
- Tokens devem ter expiração verificada obrigatoriamente
- `SECRET_KEY` nunca deve ser commitada — usar variável de ambiente em produção
- Tokens expirados devem ser rejeitados com `401`

---

## Banco de Dados — `db/techcorp.db`

SQLite local. Tabelas principais:

| Tabela | Descrição |
|--------|-----------|
| `pedidos` | Registros de pedidos com status e timestamps |
| `clientes` | Cadastro de clientes ativos |
| `produtos` | Catálogo de produtos com preços |
| `chamados` | Tickets de suporte abertos/fechados |
| `usuarios` | Usuários do sistema com perfis |

---

## Pipeline CI/CD

- **Ferramenta:** GitHub Actions
- **Arquivo:** `.github/workflows/ci.yml`
- **Trigger:** push e pull_request na branch `main`
- **Steps:** install deps → lint → testes unitários → cobertura mínima 80%

Consultar `docs/pipelines/padrao-ci.md` para o padrão completo.

---

## Padrões de Desenvolvimento

- **Linguagem:** Python 3.11+
- **Testes:** pytest com cobertura mínima de 80%
- **Linting:** flake8 + black
- **Commits:** Conventional Commits (`feat:`, `fix:`, `docs:`, `test:`)
- **PRs:** obrigatório revisão de 1 peer + pipeline verde antes do merge

---

## Integrações Externas

O sistema **não possui** integrações com serviços externos em produção. Toda comunicação é local:
- Banco de dados SQLite local
- Logs em arquivo (`logs/`)
- Notificações via fila interna (não persistente)
