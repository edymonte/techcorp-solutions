# TechCorp Solutions — ERP System

Sistema de gestão de pedidos para o varejo farmacêutico.  
Repositório oficial usado no **GitHub Copilot Workshop**.

---

## Prepare seu ambiente em 3 passos

### Antes de começar — instale uma vez só

| # | O que instalar | Link | Observação |
|---|---------------|------|------------|
| 1 | **Python 3.11+** | https://python.org/downloads | Marque **"Add python.exe to PATH"** na instalação |
| 2 | **Docker Desktop** | https://docker.com/products/docker-desktop | Após instalar, **abra o Docker Desktop** e aguarde a baleia aparecer na barra de tarefas |

### Iniciar o workshop

```
1. Clone este repositório na sua máquina
2. Dê duplo clique em  setup.bat
3. Aguarde tudo ficar verde ✔  (pode levar ~5 min no primeiro uso)
```

> Dúvidas no setup? Consulte [setup/SETUP.md](setup/SETUP.md)

---

## Estrutura do Projeto

```
Workshop_validation/
├── .github/
│   ├── copilot-instructions.md        ← padrões do time
│   ├── agents/
│   │   └── incident-responder.agent.md
│   └── prompts/
│       ├── investigar-bug-ticket.prompt.md
│       ├── corrigir-pipeline.prompt.md
│       └── resposta-incidente-multiplo.prompt.md
├── docs/
│   ├── facilitador/
│   │   └── roteiro-facilitador.md     ← roteiro do facilitador
│   ├── prompts/
│   │   └── guia-prompts-profissionais.md
│   ├── runbooks/
│   ├── arquitetura/
│   ├── suporte/
│   └── pipelines/
├── evidencias/                        ← HTMLs gerados pelo script
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
│   └── techcorp.db                    ← gerado pelo setup.bat
├── setup/
│   ├── SETUP.md
│   ├── gerar_evidencia.py
│   ├── gerar_apresentacao.py
│   ├── verificar_ambiente.py
│   ├── ollama-setup.md
│   ├── anythingllm-setup.md
│   └── mcp-setup.md
├── docker-compose.yml                 ← Ollama + AnythingLLM em container
├── setup.bat                          ← setup com um clique
├── requirements.txt
└── requirements-dev.txt
```

---

## Semanas do Workshop

| Semana | Tema | Papel | Ferramentas |
|--------|------|-------|-------------|
| 2 | "O chamado chegou" | Analista N2 | Copilot inline + Chat + AnythingLLM |
| 3 | "O pipeline quebrou" | Dev de plataforma | `@workspace` + MCP GitHub |
| 4 | "Tudo caiu ao mesmo tempo" | Dev + Suporte | Agent Mode + MCP GitHub + MCP SQLite |

> **Antes de começar cada semana:** leia [docs/prompts/guia-prompts-profissionais.md](docs/prompts/guia-prompts-profissionais.md)  
> Os prompts prontos para cada semana estão em `.github/prompts/`

---

## Gerar evidência de conclusão

Ao terminar os objetivos de uma semana, gere a tela de evidência para a competição:

```bash
python setup/gerar_evidencia.py --semana 2 --nome "João Silva" --parceiro "Ana Lima"
python setup/gerar_evidencia.py --semana 3 --nome "João Silva" --parceiro "Ana Lima"
python setup/gerar_evidencia.py --semana 4 --nome "João Silva" --parceiro "Ana Lima"
```

O script valida automaticamente os critérios da semana, gera um HTML em `evidencias/` e abre no navegador.  
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
| Node.js LTS | MCP GitHub (Semana 3 e 4) |
| VS Code + GitHub Copilot | Editor + IA |
| Docker Desktop | Roda Ollama e AnythingLLM em container — sem instalação separada |

Ver instruções detalhadas em [setup/SETUP.md](setup/SETUP.md).

---

## Executar os testes

```bash
pip install -r requirements-dev.txt
pytest tests/ -v --cov=src
```

---

*TechCorp Solutions é uma empresa fictícia criada exclusivamente para fins educacionais.*
