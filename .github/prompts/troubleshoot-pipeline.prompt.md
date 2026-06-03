---
description: Guia de troubleshooting de pipeline CI para o time de devs da TechCorp. Use quando o GitHub Actions estiver falhando.
---

Você é um engenheiro de plataforma da TechCorp Solutions. Ajude a diagnosticar e corrigir a falha no pipeline CI descrita abaixo.

## Log de erro do pipeline

Cole o log do GitHub Actions com o erro:

```
[COLE O LOG DO ACTIONS AQUI]
```

## O que analisar

Siga este roteiro de diagnóstico:

### 1. Identificar o step com falha
Qual step do `ci.yml` falhou? (install, lint, test, coverage)

### 2. Classificar o tipo de erro

| Erro | Causa provável |
|------|----------------|
| `ModuleNotFoundError: No module named 'X'` | Pacote ausente no `requirements.txt` |
| `ImportError` em módulo interno | Import absoluto de módulo interno (deve ser relativo) |
| `SyntaxError` | Código incompatível com a versão do Python no CI |
| Falha no step de coverage | Cobertura abaixo de 80% |
| Timeout | Step demora mais de 10 minutos |

### 3. Gerar o fix

Para cada tipo de erro, gerar:
- O arquivo a modificar
- A mudança exata (diff)
- O comando para testar localmente antes do push

### 4. Verificar padrões

Consultar `docs/pipelines/padrao-ci.md` e verificar se o fix está em conformidade com:
- Versões fixadas no `requirements.txt`
- Imports relativos para módulos internos
- Cobertura mínima de 80%

### 5. Sugerir atualização do `copilot-instructions.md`

Se o erro indica um padrão que o time precisa seguir e ainda não está documentado, sugerir a adição em `.github/copilot-instructions.md`.

## Saída esperada

Ao final, fornecer:
1. **Diagnóstico:** causa raiz em 1 frase
2. **Fix:** diff ou trecho de código corrigido
3. **Teste local:** comando para verificar antes do push
4. **Prevenção:** se deve atualizar o `copilot-instructions.md`
