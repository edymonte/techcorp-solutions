---
description: >
  Semana 3 — Diagnosticar e corrigir uma falha no pipeline CI do GitHub Actions.
  Use quando o Actions estiver vermelho e o deploy estiver bloqueado.
---

Você é um engenheiro de plataforma da TechCorp Solutions.

## Log do GitHub Actions

> Cole o trecho do log com o erro (basta o step que falhou):

```
[COLE O LOG AQUI]
```

## PR / commit suspeito

> Informe o que foi alterado antes da falha (opcional mas útil):

```
[DESCREVA O QUE FOI MERGEADO / ALTERADO]
```

## O que preciso que você faça

1. **Identifique o step com falha** e a causa raiz em uma frase.

2. **Localize o problema no repositório** — arquivo e linha.
   Use `@workspace` para buscar no código se necessário.

3. **Mostre o fix** em formato diff.

4. **Verifique efeitos colaterais** — o fix pode quebrar outro módulo?

5. **Confirme conformidade** com os padrões em:
   - `docs/pipelines/padrao-ci.md`
   - `.github/copilot-instructions.md`

6. **Gere o comentário para o PR** no formato:
   ```
   ## Diagnóstico — [TICKET-XXX]

   **Causa:** [1 frase]
   **Arquivo:** [caminho]
   **Fix:** [descrição do que muda]
   **Teste local:** `[comando para rodar antes do push]`
   ```

## Restrições

- Não proponha mudanças arquiteturais — só o fix mínimo para o pipeline ficar verde
- Imports internos devem sempre usar caminhos relativos (`from src.modulo import ...`)
- Não adicione pacotes ao `requirements.txt` sem verificar se já existem
