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

## Passo 1 — Verificar o arquivo `.vscode/mcp.json`

O arquivo já está configurado no repositório:

```json
{
  "servers": {
    "github": {
      "type": "http",
      "url": "https://api.githubcopilot.com/mcp/"
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

**GitHub MCP** usa o servidor remoto oficial do GitHub — não requer token separado, autentica automaticamente via sua conta do GitHub Copilot já configurada no VS Code.

**SQLite MCP** baixa o pacote `mcp-server-sqlite` via `npx` na primeira execução. A versão está fixada (`0.0.2`) para evitar breaking changes no dia do workshop.

---

## Passo 2 — Ativar os servidores MCP no VS Code

1. Abrir o VS Code no repositório (`code .`)
2. Pressionar `Ctrl+Shift+P`
3. Digitar: **"MCP: List Servers"**
4. Deve aparecer `github` e `sqlite`
5. O GitHub MCP autenticará automaticamente via sua conta Copilot já logada no VS Code

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
