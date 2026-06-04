# SETUP — TechCorp Solutions Workshop

> Tempo estimado: **15 minutos**  
> Sistema operacional: **Windows 10/11**  
> Pré-requisito: conta no GitHub com GitHub Copilot ativo

---

## Visão Geral do que você vai instalar

| # | Ferramenta | Para que serve |
|---|-----------|----------------|
| 1 | Git + VS Code | Editor + controle de versão |
| 2 | Python 3.11+ | Executar o código da TechCorp |
| 3 | Docker Desktop | Roda Ollama e AnythingLLM em container |
| 4 | Node.js | Necessário para o MCP GitHub |

> **Ollama e AnythingLLM rodam via Docker** — não é necessário instalar nada separado para eles. O `setup.bat` cuida de tudo automaticamente.

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

## Passo 2 — Python 3.11+

1. Acessar https://www.python.org/downloads/
2. Baixar **Python 3.11.x** ou superior (Windows installer 64-bit)
3. Na instalação: **marcar "Add python.exe to PATH"** ← importante!
4. Clicar em "Install Now"

Verificar:
```
python --version
# deve exibir: Python 3.11.x ou superior
```

---

## Passo 3 — Docker Desktop

1. Acessar https://docker.com/products/docker-desktop
2. Baixar e instalar o **Docker Desktop for Windows**
3. Após instalar, **abrir o Docker Desktop** e aguardar a baleia aparecer na barra de tarefas
4. Verificar no terminal:

```
docker --version
```

> O Docker Desktop deve estar aberto e rodando **antes** de executar o `setup.bat`.

---

## Passo 4 — Node.js (para MCP GitHub)

1. Acessar https://nodejs.org/
2. Baixar **LTS version** (Windows Installer)
3. Instalar com opções padrão
4. Reiniciar o terminal

Verificar:
```
node --version
npx --version
```

Ver guia de configuração do MCP: [mcp-setup.md](mcp-setup.md)

---

## Passo 5 — Clonar o repositório

```bash
git clone https://github.com/[instrutor]/techcorp-workshop.git
cd techcorp-workshop
```

Abrir no VS Code:
```bash
code .
```

---

## Passo 6 — Executar o setup.bat

Dê duplo clique em **`setup.bat`** na raiz do projeto, ou execute no terminal:

```
setup.bat
```

O script realiza automaticamente:
1. Instala as dependências Python (`requirements.txt` e `requirements-dev.txt`)
2. Cria o banco de dados SQLite (`db/techcorp.db`) com os tickets do workshop
3. Inicia Ollama e AnythingLLM via Docker (`docker compose up -d`)
4. Baixa o modelo `llama3.2` no container Ollama (se ainda não estiver)
5. Executa `setup/verificar_ambiente.py` para validar tudo

> Na primeira execução pode levar **~5 minutos** devido ao download do modelo (~2GB).

---

## Passo 7 — Configurar MCP no VS Code

1. Abrir `.vscode/mcp.json` no VS Code
2. Criar um **Personal Access Token** no GitHub:
   - Acessar https://github.com/settings/tokens
   - "Generate new token (classic)"
   - Marcar: `repo`, `read:org`
   - Copiar o token
3. No VS Code, quando o MCP solicitar o token, colar o valor

---

## Passo 8 — Configurar o workspace no AnythingLLM

Após o `setup.bat` concluir, o AnythingLLM estará acessível em **http://localhost:3001**.

A pasta `docs/` do projeto já é montada automaticamente no container.
Ainda assim é necessário criar o workspace e indexar os documentos uma vez:

Ver guia completo: [anythingllm-setup.md](anythingllm-setup.md)

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

---

## Pronto!

Seu ambiente está configurado. Aguarde as instruções do facilitador para começar.
