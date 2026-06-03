# Runbook — Troubleshooting de Pipeline CI/CD

**Categoria:** Engenharia de Plataforma  
**Produto:** TechCorp ERP — GitHub Actions  
**Versão:** 1.2  
**Última revisão:** 2026-05-20

---

## Sintomas

- Pipeline falha no step de `install dependencies`
- Erro `ModuleNotFoundError` no step de testes
- GitHub Actions mostra status vermelho após merge
- Pipeline fica em estado `queued` indefinidamente

---

## Causas Comuns

### 1. Pacote ausente no `requirements.txt`
O erro mais comum. O `ci.yml` instala dependências do `requirements.txt`, mas um módulo referenciado no código não foi adicionado ao arquivo.

**Log esperado:**
```
ModuleNotFoundError: No module named 'techcorp_core'
```
ou
```
ERROR: Could not find a version that satisfies the requirement techcorp_core
```

**Onde verificar:**
- `requirements.txt` na raiz do repositório
- Todos os `import` no código Python (`src/`)

### 2. Import de módulo interno usando nome errado
Módulos internos devem ser importados pelo caminho relativo. Imports absolutos sem o pacote instalado falham no CI.

**Exemplo de import problemático:**
```python
# ERRADO — funciona localmente mas quebra no CI
import techcorp_core

# CORRETO — caminho relativo dentro do projeto
from src.pedidos import processador
```

### 3. Versão de Python incompatível no `ci.yml`
O workflow especifica `python-version: 3.9` mas o código usa sintaxe de versão posterior.

### 4. Segredo (secret) não configurado no repositório
Actions que precisam de `secrets.GITHUB_TOKEN` ou similares falham silenciosamente se o secret não estiver configurado em Settings > Secrets.

---

## Diagnóstico

### Passo 1 — Ler o log completo do step com falha
No GitHub Actions, clicar no step vermelho e expandir o log completo. Procurar pela primeira linha de erro.

### Passo 2 — Verificar todos os imports do projeto
```bash
# Listar todos os módulos importados no código
grep -r "^import\|^from" src/ | grep -v "__pycache__"
```

### Passo 3 — Comparar com o `requirements.txt`
```bash
cat requirements.txt
```

Qualquer pacote que aparece nos imports mas não está no `requirements.txt` é a causa do erro.

### Passo 4 — Testar instalação localmente
```bash
python -m venv venv-test
venv-test\Scripts\activate  # Windows
pip install -r requirements.txt
python -m pytest tests/
```

---

## Resolução

### Caso 1 — Pacote ausente no `requirements.txt`
Adicionar o pacote na versão correta:
```bash
# Verificar a versão instalada localmente
pip show nome-do-pacote

# Adicionar ao requirements.txt
echo "nome-do-pacote==X.Y.Z" >> requirements.txt
```

### Caso 2 — Módulo interno com import errado
Corrigir o import no arquivo Python e garantir que o módulo seja importado pelo caminho correto.

### Caso 3 — Reprocessar o pipeline após o fix
Após commitar a correção:
1. O pipeline rodará automaticamente no push
2. Ou acionar manualmente: Actions > selecionar o workflow > `Run workflow`

---

## Padrão de `requirements.txt` na TechCorp

O arquivo deve listar **todas** as dependências com versão fixada:
```
flask==3.0.3
pyjwt==2.8.0
pytest==8.2.0
pytest-cov==5.0.0
```

Nunca usar `>=` sem limite superior em produção. Consultar `docs/pipelines/padrao-ci.md` para o padrão completo.

---

## Escalação

Se o pipeline continuar falhando após os passos acima:
1. Verificar se o repositório atingiu o limite de minutos gratuitos do GitHub Actions
2. Acionar o Tech Lead de Plataforma via `#devops`
3. Abrir issue com label `ci/pipeline` e anexar o log completo
