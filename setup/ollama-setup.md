# Guia do Ollama — Workshop TechCorp

> O Ollama **não precisa ser instalado** na máquina.  
> Ele roda via Docker, iniciado automaticamente pelo `setup.bat`.

---

## Como o Ollama é iniciado

O `setup.bat` executa:

```bash
docker compose up -d
```

Isso sobe o container `techcorp-ollama` com a imagem `ollama/ollama:latest`.
Na primeira execução, o script também baixa o modelo `llama3.2` automaticamente (~2GB).

---

## Verificar se está rodando

A API do Ollama fica acessível em `http://localhost:11434`.

Via terminal:
```bash
curl http://localhost:11434
# deve retornar: Ollama is running
```

Ou acessar no navegador: http://localhost:11434

Verificar o modelo instalado:
```bash
docker exec techcorp-ollama ollama list
```

Deve listar `llama3.2`.

---

## Parar / reiniciar

```bash
# parar
docker compose stop ollama

# reiniciar
docker compose start ollama

# ver logs
docker logs techcorp-ollama
```

---

## Baixar o modelo manualmente (se necessário)

Se o modelo não foi baixado automaticamente:

```bash
docker exec techcorp-ollama ollama pull llama3.2
```

---

## Solução de problemas

| Sintoma | O que fazer |
|---------|-------------|
| `curl` não responde | Verifique se o Docker Desktop está aberto e rode `docker compose up -d` |
| Container não sobe | Rode `docker logs techcorp-ollama` para ver o erro |
| Modelo não encontrado | Execute `docker exec techcorp-ollama ollama pull llama3.2` |
| Porta 11434 em uso | Pare qualquer instalação local do Ollama antes de usar o container |

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
