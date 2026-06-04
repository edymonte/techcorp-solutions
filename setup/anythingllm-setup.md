# Guia do AnythingLLM — Workshop TechCorp

> O AnythingLLM **não precisa ser instalado** na máquina.  
> Ele roda via Docker, iniciado automaticamente pelo `setup.bat`.

---

## O que é o AnythingLLM?

O AnythingLLM é uma interface visual que conecta ao Ollama e permite fazer **RAG (Retrieval-Augmented Generation)** — o modelo responde perguntas com base em documentos indexados. No workshop ele é o **N1 da TechCorp**: consulta os runbooks e responde perguntas dos analistas.

---

## Como é iniciado

O `setup.bat` executa:

```bash
docker compose up -d
```

Isso sobe o container `techcorp-anythingllm` com a imagem `mintplexlabs/anythingllm:latest`.
A pasta `docs/` do projeto é montada automaticamente como diretório de documentos do container.

---

## Acessar a interface

Após o `setup.bat` concluir, abrir no navegador:

**http://localhost:3001**

---

## Configurar o workspace (feito uma vez)

Na primeira vez que acessar, configure o AnythingLLM para usar o Ollama do container:

### Passo 1 — Conectar ao Ollama

Em **Settings > LLM Preference**:

- **LLM Provider:** Ollama
- **Ollama Base URL:** `http://ollama:11434`  
  *(use `ollama` como hostname — é o nome do serviço Docker, não `localhost`)*
- **Model:** `llama3.2`
- Clicar em **Save**

### Passo 2 — Criar o Workspace do N1

1. Na tela principal, clicar em **"+ New Workspace"**
2. Nome: **TechCorp N1**
3. Clicar em **Create**

### Passo 3 — Indexar os documentos da TechCorp

1. Dentro do workspace **TechCorp N1**, clicar no ícone de documentos
2. Os arquivos da pasta `docs/` já aparecem listados (montagem automática do container)
3. Selecionar todos e clicar em **"Move to Workspace"**
4. Clicar em **"Save and Embed"** — aguardar o embedding

Documentos que devem aparecer:
- `runbooks/pedidos-falha.md`
- `runbooks/auth-reset.md`
- `runbooks/pipeline-troubleshooting.md`
- `arquitetura/visao-geral.md`
- `suporte/sla.md`
- `suporte/escalation-policy.md`
- `pipelines/padrao-ci.md`

---

## Testar o N1

No chat do workspace **TechCorp N1**, fazer uma pergunta de teste:

```
O que pode causar falha no processamento de pedidos?
```

O N1 deve responder citando o `runbook/pedidos-falha.md`. Se não mencionar o runbook, verificar se os documentos foram embedados corretamente.

---

## Parar / reiniciar

```bash
# parar
docker compose stop anythingllm

# reiniciar
docker compose start anythingllm

# ver logs
docker logs techcorp-anythingllm
```

---

## Solução de problemas

| Sintoma | O que fazer |
|---------|-------------|
| http://localhost:3001 não abre | Verifique se o Docker está rodando e execute `docker compose up -d` |
| Ollama não conecta no AnythingLLM | Confirme que a URL está como `http://ollama:11434` (não `localhost`) |
| Documentos não aparecem | Execute `docker logs techcorp-anythingllm` para verificar a montagem da pasta |
| Resposta não cita runbooks | Verifique se os documentos foram embedados (botão "Save and Embed") |

### Passo 2 — Criar o Workspace do N1

1. Na tela principal, clicar em **"+ New Workspace"**
2. Nome: **TechCorp N1**
3. Clicar em **Create**

### Passo 3 — Indexar os documentos da TechCorp

1. Dentro do workspace **TechCorp N1**, clicar no ícone de pasta/documentos
2. Clicar em **"Upload Documents"**
3. Selecionar **todos os arquivos** da pasta `docs/` do repositório:
   - `docs/runbooks/pedidos-falha.md`
   - `docs/runbooks/auth-reset.md`
   - `docs/runbooks/pipeline-troubleshooting.md`
   - `docs/arquitetura/visao-geral.md`
   - `docs/suporte/sla.md`
   - `docs/suporte/escalation-policy.md`
   - `docs/pipelines/padrao-ci.md`
4. Após o upload, selecionar todos e clicar em **"Move to Workspace"**
5. Clicar em **"Save and Embed"** — aguardar o embedding

---

## Testar o N1

No chat do workspace **TechCorp N1**, fazer uma pergunta de teste:

```
O que pode causar falha no processamento de pedidos?
```

O N1 deve responder citando o `runbook/pedidos-falha.md`. Se não mencionar o runbook, verificar se os documentos foram embedados corretamente.

---

## Dicas de uso no workshop

- Sempre perguntar em português
- O N1 responde com base apenas nos documentos indexados
- Se a resposta não vier do runbook, perguntar de forma mais específica: *"Qual runbook descreve o erro TypeError na API de pedidos?"*
- Para atualizar a base de conhecimento após editar um doc: re-upload do arquivo

---

## Solução de problemas

**"Cannot connect to Ollama"**  
→ Verificar se o Ollama está rodando: abrir terminal e digitar `ollama serve` ou verificar o ícone na bandeja do sistema.

**Respostas genéricas sem citar os runbooks**  
→ Verificar em Documents se todos os arquivos aparecem com status "embedded". Se não, re-fazer o upload.

**AnythingLLM não abre**  
→ Verificar se há uma instância já rodando na bandeja do sistema (ícone próximo ao relógio).
