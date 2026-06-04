# TechCorp Solutions — ERP System

Sistema de gestão de pedidos para o varejo farmacêutico.  
Repositório oficial usado no **GitHub Copilot Workshop**.

---

## Prepare seu ambiente em 3 passos

### Antes de começar — instale uma vez só

| # | O que instalar | Link | Observação |
|---|---------------|------|------------|
| 1 | **Python 3.11+** | https://python.org/downloads | Marque **"Add python.exe to PATH"** na instalação |
| 2 | **VS Code** | https://code.visualstudio.com | Instale as extensões recomendadas ao abrir o projeto |
| 3 | **Node.js LTS** | https://nodejs.org | Necessário para os servidores MCP |
| 4 | **Git** | https://git-scm.com | Para clonar o repositório |

> **GitHub Copilot:** você precisa de uma licença ativa no VS Code.  
> Acesse [github.com/features/copilot](https://github.com/features/copilot) para verificar.

### Iniciar o workshop

```
1. Clone este repositório:
   git clone https://github.com/edymonte/techcorp-solutions.git

2. Abra a pasta no VS Code:
   code techcorp-solutions

3. Dê duplo clique em  setup.bat
4. Aguarde tudo ficar verde ✔  (menos de 1 minuto)
```

> Dúvidas no setup? Consulte [setup/SETUP.md](setup/SETUP.md)

---

## Estrutura do Projeto

```
techcorp-solutions/
├── .github/
│   ├── copilot-instructions.md        ← padrões do time TechCorp
│   └── prompts/
│       ├── investigar-bug-ticket.prompt.md
│       ├── corrigir-pipeline.prompt.md
│       └── resposta-incidente-multiplo.prompt.md
├── .vscode/
│   ├── extensions.json                ← extensões recomendadas (instale ao abrir)
│   ├── settings.json                  ← configurações do workshop
│   └── mcp.json                       ← MCP GitHub + MCP SQLite
├── docs/
│   ├── known-issues.md                ← problemas conhecidos (leia antes de começar!)
│   ├── runbooks/
│   ├── arquitetura/
│   ├── suporte/
│   └── pipelines/
├── evidencias/                        ← HTMLs gerados ao final de cada etapa
├── src/
│   ├── api/pedidos.py
│   ├── auth/auth_service.py
│   └── pedidos/processador.py
├── tickets/
│   ├── ticket-001.md                  ← Etapa 1 — ESSENCIAL
│   ├── ticket-002.md                  ← Etapa 2 — INTERMEDIÁRIO
│   └── ticket-003.md                  ← Etapa 3 — CHALLENGE
├── db/
│   ├── init_db.py
│   └── techcorp.db                    ← gerado automaticamente pelo setup.bat
├── setup/
│   ├── SETUP.md
│   ├── gerar_evidencia.py
│   ├── verificar_ambiente.py
│   └── mcp-setup.md
├── setup.bat                          ← setup com um clique
├── requirements.txt
└── requirements-dev.txt
```

---

## Etapas do Workshop

| Etapa | Nível | Tema | Ferramentas |
|-------|-------|------|-------------|
| 1 | 🟢 ESSENCIAL | "O chamado chegou" — debugging com Copilot | Copilot Chat + Inline |
| 2 | 🟡 INTERMEDIÁRIO | "O pipeline quebrou" — CI com Copilot | `@workspace` + MCP GitHub |
| 3 | 🔴 CHALLENGE | "Tudo caiu ao mesmo tempo" — Agent Mode | Agent Mode + MCP SQLite |

> **Antes de começar cada etapa:** leia o ticket correspondente em `tickets/`  
> Dica: confira `docs/known-issues.md` — pode ter pistas úteis!  
> Os prompts prontos estão em `.github/prompts/`

---

## Gerar evidência de conclusão

Ao terminar os objetivos de uma etapa, gere a tela de evidência para a competição:

```bash
python setup/gerar_evidencia.py --semana 1 --nome "João Silva" --parceiro "Ana Lima"
python setup/gerar_evidencia.py --semana 2 --nome "João Silva" --parceiro "Ana Lima"
python setup/gerar_evidencia.py --semana 3 --nome "João Silva" --parceiro "Ana Lima"
```

O script valida automaticamente os critérios da etapa, gera um HTML em `evidencias/` e abre no navegador.  
Use **Print → Salvar como PDF** ou **screenshot** para entregar na competição.

---

## Para o Facilitador

O roteiro completo de condução (blocos de tempo, falas sugeridas, perguntas de debrief) está em:

> [docs/facilitador/roteiro-facilitador.md](docs/facilitador/roteiro-facilitador.md)

---

## Requisitos do Ambiente

| Ferramenta | Para quê |
|-----------|----------|
| Windows 10/11 | Sistema operacional |
| Python 3.11+ | Rodar o código da TechCorp e os testes |
| Node.js LTS | Servidores MCP (GitHub e SQLite) |
| Git | Clonar o repositório |
| VS Code + GitHub Copilot | Editor + IA |

Ver instruções detalhadas em [setup/SETUP.md](setup/SETUP.md).

---

## Executar os testes

```bash
pip install -r requirements-dev.txt
pytest tests/ -v --cov=src
```

---

*TechCorp Solutions é uma empresa fictícia criada exclusivamente para fins educacionais.*
