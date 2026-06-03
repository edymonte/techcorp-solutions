# TechCorp Solutions — Copilot Instructions

> Padrões do time de engenharia. O Copilot deve seguir estas regras ao gerar código neste repositório.

---

## Linguagem e Stack

- **Linguagem:** Python 3.11+
- **Testes:** pytest com cobertura mínima de 80%
- **Linting:** flake8 + black (linha máxima: 88 caracteres)
- **Commits:** Conventional Commits (`feat:`, `fix:`, `docs:`, `test:`, `refactor:`)

---

## Regra de Imports (CRÍTICO)

Módulos internos do projeto **sempre** devem ser importados por caminho relativo:

```python
# CORRETO
from src.api.pedidos import validar_pedido
from src.pedidos.processador import processar_pedido
from src.auth.auth_service import validar_token

# ERRADO — quebra o pipeline CI
import techcorp_core
from techcorp_core import pedidos
```

Nunca gerar imports absolutos de módulos que não estão no `requirements.txt`.

---

## Tratamento de Valores Nulos

Sempre verificar `None` antes de comparações numéricas ou de string:

```python
# CORRETO
if valor is None:
    raise ValueError("Campo obrigatório não pode ser nulo")
if valor <= 0:
    raise ValueError("Valor deve ser positivo")

# ERRADO — lança TypeError se valor for None
if valor <= 0:
    raise ValueError("Valor deve ser positivo")
```

---

## Segurança — JWT

Nunca desabilitar a verificação de expiração de tokens:

```python
# CORRETO
payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])

# ERRADO — vulnerabilidade de segurança
payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"],
                     options={"verify_exp": False})
```

---

## Padrão de Funções

```python
def nome_da_funcao(param: tipo) -> tipo_retorno:
    """
    Descrição em uma linha.

    Args:
        param: descrição do parâmetro

    Returns:
        descrição do retorno

    Raises:
        NomeDoErro: quando ocorre X
    """
```

---

## Padrão de Testes

```python
def test_nome_descritivo():
    # Arrange
    ...
    # Act
    ...
    # Assert
    ...

# Sempre testar os casos de borda: None, 0, string vazia, lista vazia
```

---

## `requirements.txt`

- Sempre fixar versões: `flask==3.0.3` (nunca `flask>=3.0`)
- Dependências de dev ficam em `requirements-dev.txt`
- Nunca adicionar pacotes internos ao `requirements.txt`
