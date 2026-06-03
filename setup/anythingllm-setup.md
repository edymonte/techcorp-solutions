# Guia de Instalação — AnythingLLM (Windows)

**Tempo estimado:** 10 minutos

---

## O que é o AnythingLLM?

O AnythingLLM é uma interface visual que conecta ao Ollama e permite fazer **RAG (Retrieval-Augmented Generation)** — ou seja, o modelo responde perguntas com base em documentos que você indexar. No workshop ele é o **N1 da TechCorp**: indexa a pasta `docs/` e responde perguntas dos analistas com base nos runbooks.

---

## Instalação

### 1. Baixar o instalador

Acessar: **https://anythingllm.com/**

Clicar em **"Download for Windows"** e executar o `.exe`.

### 2. Abrir o AnythingLLM

Após instalação, abrir o app. Na primeira execução ele vai pedir para configurar o LLM.

---

## Configuração

### Passo 1 — Conectar ao Ollama

Na tela inicial ou em **Settings > LLM Preference**:

- **LLM Provider:** Ollama
- **Ollama Base URL:** `http://localhost:11434`
- **Model:** `llama3.2`
- Clicar em **Save**

> O Ollama precisa estar rodando. Se não estiver, abrir o terminal e digitar `ollama serve`.

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
