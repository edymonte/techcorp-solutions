# Padrão de Pipeline CI — TechCorp Solutions

**Versão:** 1.1  
**Última revisão:** 2026-05-05  
**Responsável:** Time de Plataforma

---

## Visão Geral

Todo repositório Python da TechCorp deve ter um pipeline CI seguindo este padrão. O pipeline roda automaticamente em todo push e pull_request para a branch `main`.

---

## Estrutura do `ci.yml`

```yaml
name: CI — TechCorp Solutions

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Lint (flake8)
        run: flake8 src/ tests/

      - name: Run tests
        run: pytest tests/ --cov=src --cov-report=term-missing

      - name: Check coverage threshold
        run: pytest tests/ --cov=src --cov-fail-under=80
```

---

## Padrão do `requirements.txt`

- **Obrigatório:** listar todas as dependências com versão fixada
- **Proibido:** `>=` sem limite superior (`flask>=3.0` é inválido)
- **Obrigatório:** incluir dependências de desenvolvimento separadas em `requirements-dev.txt`

**Exemplo correto (`requirements.txt`):**
```
flask==3.0.3
pyjwt==2.8.0
```

**Exemplo correto (`requirements-dev.txt`):**
```
pytest==8.2.0
pytest-cov==5.0.0
flake8==7.0.0
black==24.4.2
```

---

## Regras de Import de Módulos Internos

Módulos do próprio projeto devem ser importados por caminho relativo:

```python
# CORRETO
from src.api.pedidos import validar_pedido
from src.pedidos.processador import processar_pedido

# ERRADO — quebra no CI
import techcorp_core
from techcorp_core import pedidos
```

**Por quê?** O projeto não é instalado como pacote no ambiente CI. Apenas o que está em `requirements.txt` é instalado. Imports absolutos de módulos internos sem o pacote devidamente publicado falharão com `ModuleNotFoundError`.

---

## Critérios para Merge

Um PR só pode ser mergeado quando:
- ✅ Pipeline verde (todos os steps passando)
- ✅ Cobertura de testes ≥ 80%
- ✅ Aprovação de pelo menos 1 revisor
- ✅ Sem conflitos com a branch `main`

---

## Troubleshooting

Para problemas comuns no pipeline, consultar `docs/runbooks/pipeline-troubleshooting.md`.
