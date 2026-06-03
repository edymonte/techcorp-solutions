# SETUP — TechCorp Solutions Workshop

> Tempo estimado: **30 minutos**  
> Sistema operacional: **Windows 10/11**  
> Pré-requisito: conta no GitHub com GitHub Copilot ativo

---

## Visão Geral do que você vai instalar

| # | Ferramenta | Para que serve |
|---|-----------|----------------|
| 1 | Git + VS Code | Editor + controle de versão |
| 2 | Python 3.11 | Executar o código da TechCorp |
| 3 | Ollama + llama3.2 | LLM local (N1 — sem internet) |
| 4 | AnythingLLM | Interface visual do N1 + RAG dos docs |
| 5 | Node.js | Necessário para o MCP GitHub |
| 6 | Fork do repositório | Sua cópia do projeto TechCorp |

---

## Passo 1 — Git e VS Code

Se ainda não tem instalados:

- **Git:** https://git-scm.com/download/win → instalar com opções padrão
- **VS Code:** https://code.visualstudio.com/ → instalar com opções padrão

No VS Code, instalar a extensão **GitHub Copilot**:
1. `Ctrl+Shift+X`
2. Buscar "GitHub Copilot"
3. Instalar e fazer login com sua conta GitHub

---

## Passo 2 — Python 3.11

1. Acessar https://www.python.org/downloads/
2. Baixar **Python 3.11.x** (Windows installer 64-bit)
3. Na instalação: **marcar "Add python.exe to PATH"** ← importante!
4. Clicar em "Install Now"

Verificar:
```
python --version
# deve exibir: Python 3.11.x
```

---

## Passo 3 — Ollama (LLM local)

Ver guia detalhado: [setup/ollama-setup.md](ollama-setup.md)

**Resumo rápido:**
```
# 1. Baixar em https://ollama.com/download → Windows
# 2. Instalar (next, next, finish)
# 3. No terminal:
ollama pull llama3.2
# aguardar download (~2GB)

# 4. Testar:
ollama run llama3.2
# digite "oi" e pressione Enter — deve responder
# Ctrl+D para sair
```

---

## Passo 4 — AnythingLLM

Ver guia detalhado: [setup/anythingllm-setup.md](anythingllm-setup.md)

**Resumo rápido:**
1. Baixar em https://anythingllm.com/ → Download for Windows
2. Instalar e abrir
3. Em **LLM Preference**: selecionar **Ollama** → URL: `http://localhost:11434` → Model: `llama3.2`
4. Criar um Workspace chamado **"TechCorp N1"**
5. Em **Document Settings**: apontar para a pasta `docs/` do repositório
6. Clicar em **"Sync"** para indexar os documentos

---

## Passo 5 — Node.js (para MCP GitHub)

1. Acessar https://nodejs.org/
2. Baixar **LTS version** (Windows Installer)
3. Instalar com opções padrão
4. Reiniciar o terminal

Verificar:
```
node --version
npx --version
```

Ver guia de configuração do MCP: [setup/mcp-setup.md](mcp-setup.md)

---

## Passo 6 — Fork e clone do repositório

1. Acessar **https://github.com/[instrutor]/techcorp-solutions**
2. Clicar em **Fork** → "Create fork"
3. Abrir o terminal no Windows e clonar **sua fork**:

```bash
git clone https://github.com/SEU-USUARIO/techcorp-solutions.git
cd techcorp-solutions
```

4. Abrir no VS Code:
```bash
code .
```

---

## Passo 7 — Instalar dependências Python

```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

---

## Passo 8 — Inicializar o banco de dados

```bash
python db/init_db.py
```

Deve exibir:
```
Banco criado em: db/techcorp.db
Chamados inseridos:
  TICKET-001 | Falha no Processamento de Pedidos | P1 | aberto
  TICKET-002 | Pipeline de Produção Bloqueado | P2 | aberto
  TICKET-003 | Incidente Crítico: Múltiplas Falhas Simultâneas | P1 | aberto
```

---

## Passo 9 — Configurar MCP no VS Code

1. Abrir `.vscode/mcp.json` no VS Code
2. Criar um **Personal Access Token** no GitHub:
   - Acessar https://github.com/settings/tokens
   - "Generate new token (classic)"
   - Marcar: `repo`, `read:org`
   - Copiar o token
3. No VS Code, quando o MCP solicitar o token, colar o valor

---

## Verificação Final

Execute o script de validação do ambiente:

```bash
python setup/verificar_ambiente.py
```

O script verifica automaticamente:

| # | O que checa | Esperado |
|---|-------------|----------|
| 1 | Python 3.11+ | `✔ Python 3.11.x` |
| 2 | flask, pyjwt, pytest instalados | `✔ ... instalado` |
| 3 | Testes da aplicação (pytest) | alguns falham — isso é intencional (bugs do workshop) |
| 4 | Banco `db/techcorp.db` existe | `✔ db/techcorp.db encontrado` |
| 5 | Node.js / npx | `✔ node v20.x.x` |
| 6 | Ollama rodando + modelo llama3.2 | `✔ Ollama está rodando` |
| 7 | AnythingLLM rodando | `✔ AnythingLLM está rodando` |
| 8 | `.vscode/mcp.json` presente | `✔ .vscode/mcp.json presente` |

**Saída esperada ao final:**
```
✔ 8 ok   ✘ 0 erro(s)   ⚠ 0 aviso(s)

  Ambiente pronto para o workshop!
```

> **Nota sobre os testes com falha:** `test_token_expirado_deve_ser_rejeitado` e `test_pedido_quantidade_none_deve_levantar_pedido_invalido_error` vão **falhar propositalmente** — esses são os bugs que você vai corrigir nas semanas 2 e 4.

Se algum item aparecer com `✘`, seguir a dica exibida pelo script.  
Se travar, consultar `docs/runbooks/pipeline-troubleshooting.md`.

---

## Pronto!

Seu ambiente está configurado. Aguarde as instruções do instrutor para começar o desafio.
