# TechCorp Solutions — ERP System

Sistema de gestão de pedidos para o varejo farmacêutico.  
Repositório oficial usado no **GitHub Copilot Workshop**.

---

## Para participantes do Workshop

**Primeiro acesso:**
1. Faça um **Fork** deste repositório para sua conta
2. Clone sua fork localmente
3. Siga o guia completo em [setup/SETUP.md](setup/SETUP.md)

---

## Estrutura do Projeto

```
techcorp-solutions/
├── .github/
│   ├── copilot-instructions.md   ← padrões do time
│   ├── agents/
│   │   └── incident-responder.agent.md
│   ├── prompts/
│   │   ├── close-ticket.prompt.md
│   │   └── troubleshoot-pipeline.prompt.md
│   └── workflows/
│       └── ci.yml
├── docs/                         ← base de conhecimento (RAG)
│   ├── runbooks/
│   ├── arquitetura/
│   ├── suporte/
│   └── pipelines/
├── src/
│   ├── api/pedidos.py
│   ├── auth/auth_service.py
│   └── pedidos/processador.py
├── tickets/
│   ├── ticket-001.md
│   ├── ticket-002.md
│   └── ticket-003.md
├── db/
│   ├── init_db.py
│   └── techcorp.db              ← gerado pelo init_db.py
├── setup/
│   ├── SETUP.md
│   ├── ollama-setup.md
│   ├── anythingllm-setup.md
│   └── mcp-setup.md
├── .vscode/mcp.json
├── requirements.txt
└── requirements-dev.txt
```

---

## Semanas do Workshop

| Semana | Tema | Papel | Ferramentas |
|--------|------|-------|-------------|
| 2 (08–12/06) | "O chamado chegou" | Analista N2 | Copilot inline + AnythingLLM |
| 3 (15–19/06) | "O pipeline quebrou" | Dev de plataforma | `@workspace` + MCP GitHub |
| 4 (22–26/06) | "Tudo caiu ao mesmo tempo" | Dev + Suporte | Agent Mode + MCP GitHub + MCP SQLite |

---

## Requisitos do Ambiente

- Windows 10/11
- Python 3.11+
- Node.js LTS (para MCP)
- VS Code + GitHub Copilot
- Ollama + llama3.2
- AnythingLLM

Ver instruções completas em [setup/SETUP.md](setup/SETUP.md).

---

## Executar os testes

```bash
pip install -r requirements-dev.txt
pytest tests/ -v --cov=src
```

---

*TechCorp Solutions é uma empresa fictícia criada exclusivamente para fins educacionais.*
