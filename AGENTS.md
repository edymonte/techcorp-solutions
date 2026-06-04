# TechCorp Solutions — Instruções para Agentes de IA

> Este arquivo orienta o comportamento do GitHub Copilot (Chat, Inline e Agent Mode)
> no contexto do workshop. Complementa `.github/copilot-instructions.md`.

---

## Contexto do projeto

Este é um sistema ERP fictício para o varejo farmacêutico da **TechCorp Solutions**.
O repositório é usado em um **workshop de GitHub Copilot** onde os participantes
praticam debugging, diagnóstico de pipeline e resposta a incidentes com suporte de IA.

---

## Regras de geração de código

- **Fix mínimo sempre:** corrija apenas o que o ticket/prompt pede. Não refatore código adjacente.
- **Preserve assinaturas:** nunca altere a assinatura de funções públicas sem instrução explícita.
- **Português no output:** comentários, mensagens de erro e docstrings em português (pt-BR).
- **Sem dependências externas:** não sugira imports de pacotes que não estão em `requirements.txt`.
- **Segurança:** nunca desabilite verificações de segurança JWT (`verify_exp`, `verify_signature`).
  Nunca exponha `SECRET_KEY` em logs ou outputs.

---

## Fluxo de diagnóstico esperado

Quando o usuário descrever um bug ou incidente, siga esta ordem:

1. Identifique o arquivo e a função relevante
2. Mostre a linha exata do problema com contexto
3. Explique a causa raiz em uma frase
4. Proponha o fix mínimo em formato diff
5. Indique qual teste deve ser rodado para confirmar

---

## Arquivos-chave do projeto

| Arquivo | Papel |
|---------|-------|
| `src/api/pedidos.py` | API de pedidos — validação de entrada |
| `src/auth/auth_service.py` | Autenticação JWT |
| `src/pedidos/processador.py` | Processamento de pedidos |
| `tests/` | Testes automatizados — sempre rodar após qualquer fix |
| `tickets/` | Chamados do workshop — leia o ticket antes de propor soluções |
| `docs/runbooks/` | Runbooks de suporte — use como referência de diagnóstico |

---

## Restrições operacionais

- **NÃO rotacionar `SECRET_KEY`** sem aprovação explícita do CTO (causa logout em massa)
- **NÃO alterar o schema do banco** (`db/init_db.py`) durante o workshop
- **NÃO modificar arquivos de teste** para fazer os testes passarem — corrija o código de produção

---

## Ferramentas disponíveis no Agent Mode

- `@workspace` — analisa todos os arquivos do projeto
- MCP GitHub — ler issues, comentar em PRs (requer token configurado)
- MCP SQLite — consultar e atualizar `db/techcorp.db`
