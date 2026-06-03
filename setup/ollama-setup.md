# Guia de Instalação — Ollama (Windows)

**Tempo estimado:** 10 minutos (+ tempo de download do modelo ~2GB)

---

## O que é o Ollama?

O Ollama permite rodar modelos de linguagem (LLMs) **100% local**, sem internet e sem conta em nenhum serviço. No workshop ele faz o papel do **N1** — o agente de triagem automatizado da TechCorp.

---

## Instalação

### 1. Baixar o instalador

Acessar: **https://ollama.com/download**

Clicar em **"Download for Windows"** e executar o instalador `.exe`.

A instalação é simples: next → next → finish. O Ollama roda em background automaticamente.

### 2. Verificar que está rodando

Abrir o terminal e digitar:
```bash
ollama --version
```

Deve exibir algo como: `ollama version 0.5.x`

Se não reconhecer o comando, reiniciar o terminal ou o computador.

### 3. Baixar o modelo llama3.2

```bash
ollama pull llama3.2
```

> Download de ~2GB. Pode demorar dependendo da internet.

### 4. Testar o modelo

```bash
ollama run llama3.2
```

Digite uma pergunta, por exemplo:
```
O que causa ModuleNotFoundError em Python?
```

Deve responder em texto. Pressione `Ctrl+D` ou `Ctrl+C` para sair.

---

## Verificar se o servidor está ativo

O Ollama expõe uma API REST em `http://localhost:11434`. Para verificar:

```bash
curl http://localhost:11434
# deve retornar: Ollama is running
```

Ou abrir no navegador: http://localhost:11434

---

## Modelos disponíveis

Para o workshop usamos apenas `llama3.2`. Se quiser explorar outros:
```bash
ollama list          # modelos instalados
ollama pull phi4     # alternativa mais leve (3B parâmetros)
```

---

## Solução de problemas

**"ollama: command not found"**  
→ Reiniciar o terminal ou verificar se o Ollama está na bandeja do sistema (ícone próximo ao relógio).

**Download travado ou lento**  
→ O modelo é baixado em `C:\Users\<usuario>\.ollama\models`. Pode pausar e retomar.

**Porta 11434 em uso**  
→ Verificar se outro processo está usando a porta: `netstat -ano | findstr 11434`
