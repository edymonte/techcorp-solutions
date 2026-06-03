# Guia de Configuração — MCP (Model Context Protocol)

**Tempo estimado:** 10 minutos  
**Pré-requisito:** Node.js instalado (`node --version` deve funcionar)

---

## O que é MCP?

O MCP (Model Context Protocol) permite que o GitHub Copilot no VS Code **execute ações reais** além de gerar código — como ler issues, comentar em PRs, criar branches e consultar bancos de dados, tudo via chat.

No workshop usamos dois servidores MCP:

| Servidor | Função |
|----------|--------|
| **MCP GitHub** | Ler issues, comentar em PRs, criar branches, fechar tickets |
| **MCP SQLite** | Consultar e atualizar os chamados no banco `techcorp.db` |

---

## Passo 1 — Criar o Personal Access Token do GitHub

1. Acessar: https://github.com/settings/tokens
2. Clicar em **"Generate new token"** → "Generate new token (classic)"
3. Nome: `techcorp-workshop-mcp`
4. Expiração: 30 dias
5. Marcar os escopos:
   - ✅ `repo` (acesso completo ao repositório)
   - ✅ `read:org` (ler organização, se aplicável)
6. Clicar em **"Generate token"**
7. **Copiar o token** — ele só aparece uma vez!

---

## Passo 2 — Verificar o arquivo `.vscode/mcp.json`

O arquivo já está configurado no repositório:

```json
{
  "servers": {
    "github": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github@2025.4.8"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "${input:githubToken}"
      }
    },
    "sqlite": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "mcp-server-sqlite@0.0.2", "--db-path",
               "${workspaceFolder}/db/techcorp.db"]
    }
  }
}
```

Ambos os servidores rodam **localmente** — nenhuma dependência de serviços externos.

- **GitHub MCP** usa `@modelcontextprotocol/server-github@2025.4.8` via `npx`. A versão está fixada para garantir comportamento estável no dia do workshop.
- **SQLite MCP** usa `mcp-server-sqlite@0.0.2` e lê diretamente o `techcorp.db` local.

O `${input:githubToken}` faz o VS Code pedir o token na primeira vez — você não precisa colocar o token no arquivo.

---

## Passo 3 — Ativar os servidores MCP no VS Code

1. Abrir o VS Code no repositório (`code .`)
2. Pressionar `Ctrl+Shift+P`
3. Digitar: **"MCP: List Servers"**
4. Deve aparecer `github` e `sqlite`
5. Ao usar o MCP pela primeira vez no chat, o VS Code pedirá o token — colar o token gerado no Passo 1

---

## Testando o MCP GitHub

No chat do Copilot (`Ctrl+Shift+I`), perguntar:

```
@github liste as issues abertas neste repositório
```

Deve listar as issues da sua fork.

---

## Testando o MCP SQLite

No chat do Copilot:

```
Quais chamados estão com status 'aberto' no banco de dados?
```

Deve retornar os 3 tickets do workshop.

---

## Comandos úteis no workshop

### MCP GitHub
```
@github leia a issue #1 e me dê um resumo
@github crie uma branch chamada fix/ticket-001
@github comente no PR #2: "diagnóstico concluído, fix em andamento"
@github abra um PR de fix/ticket-001 para main com título "fix: corrige tratamento de None em validar_pedido"
```

### MCP SQLite
```
Quais chamados estão abertos?
Atualize o status do TICKET-001 para 'resolvido'
Mostre todos os clientes Premium
```

---

## Solução de problemas

**"npx: command not found"**  
→ Node.js não está instalado. Ver Passo 5 do SETUP.md.

**"Error: GITHUB_PERSONAL_ACCESS_TOKEN not set"**  
→ Reiniciar o VS Code e tentar novamente. O VS Code pedirá o token.

**MCP SQLite não encontra o banco**  
→ Verificar se o arquivo `db/techcorp.db` existe. Se não, executar `python db/init_db.py`.
