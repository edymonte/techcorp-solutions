---
description: >
  Semana 2 — Investigar e corrigir um bug reportado em um ticket de suporte.
  Use quando tiver um ticket aberto e precisar diagnosticar a causa raiz no código.
---

Você é um desenvolvedor N2 da TechCorp Solutions.

## Ticket que estou investigando

> Cole aqui o conteúdo do ticket (ou informe o ID):

```
[TICKET-XXX]
```

## O que preciso que você faça

1. **Diagnóstico** — Identifique a causa raiz no código com base no sintoma relatado.
   Cite o arquivo e a linha exata.

2. **Fix mínimo** — Mostre apenas as linhas que mudam, em formato diff:
   ```diff
   - linha antiga
   + linha nova
   ```

3. **Teste** — Escreva um teste pytest que:
   - Reproduz o cenário que causou o bug (deve FALHAR antes do fix)
   - Passa depois do fix aplicado
   - Fica em `tests/test_<módulo>.py`

4. **Preenchimento do ticket** — Gere o texto para a seção "Ações do N2":
   - Diagnóstico (1 frase técnica)
   - Solução aplicada
   - Teste realizado

## Restrições

- Não altere assinaturas de funções existentes
- Siga os padrões em `.github/copilot-instructions.md`
- O fix deve ser o menor possível — não refatore o código ao redor
- Não adicione dependências externas
