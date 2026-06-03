# Runbook — Reset e Diagnóstico de Autenticação

**Categoria:** Suporte N1/N2  
**Produto:** TechCorp ERP — Módulo de Auth  
**Versão:** 1.4  
**Última revisão:** 2026-05-18

---

## Sintomas

- Usuários não conseguem fazer login
- Token JWT rejeitado mesmo recém-emitido
- Erro `401 Unauthorized` em endpoints protegidos
- Usuários conseguem acessar o sistema com tokens visivelmente antigos (> 8h)

---

## Causas Comuns

### 1. Validação de expiração desabilitada (vulnerabilidade crítica)
A função `validar_token()` em `src/auth/auth_service.py` usa `options={"verify_exp": False}`, aceitando tokens expirados como válidos.

**Risco:** Usuários desligados ou com permissões revogadas continuam acessando o sistema.

**Log esperado quando ocorre acesso com token expirado:**
```
INFO - Token validado para usuário: user-123
# Nenhum erro — o sistema aceita silenciosamente
```

### 2. SECRET_KEY comprometida ou rotacionada
Se a `SECRET_KEY` for alterada no servidor, todos os tokens existentes ficam inválidos.

### 3. Diferença de horário entre servidores
Tokens com `iat` no futuro são rejeitados pelo algoritmo JWT padrão.

### 4. Usuário sem perfil cadastrado
Token gerado sem o campo `perfil` causa erro ao tentar acessar recursos restritos.

---

## Diagnóstico

### Passo 1 — Verificar se o token está expirado
```python
import jwt

token = "<token do usuário>"
# Decodificar sem verificar assinatura para inspeção
payload = jwt.decode(token, options={"verify_signature": False})
print(payload)
# Verificar campo "exp" — timestamp Unix
```

### Passo 2 — Verificar logs de autenticação
```bash
grep -i "token\|auth\|401\|403" logs/auth.log | tail -50
```

### Passo 3 — Testar geração de novo token
```python
from src.auth.auth_service import gerar_token
token = gerar_token("user-teste", "suporte")
print(token)
```

---

## Resolução

### Caso 1 — Corrigir validação de expiração (CRÍTICO)
Remover `options={"verify_exp": False}` da função `validar_token()`:

```python
# ANTES (com bug — aceita tokens expirados)
payload = jwt.decode(
    token,
    SECRET_KEY,
    algorithms=[ALGORITHM],
    options={"verify_exp": False},
)

# DEPOIS (corrigido — rejeita tokens expirados)
payload = jwt.decode(
    token,
    SECRET_KEY,
    algorithms=[ALGORITHM],
)
```

### Caso 2 — Forçar re-login de todos os usuários
Rotacionar a `SECRET_KEY` no arquivo de configuração — invalida todos os tokens ativos:
```bash
# Gerar nova chave
python -c "import secrets; print(secrets.token_hex(32))"
# Atualizar SECRET_KEY em src/auth/auth_service.py
```

### Caso 3 — Reset de senha manual
```sql
UPDATE usuarios
SET senha_hash = NULL, force_reset = 1
WHERE usuario_id = '<id>';
```

---

## Prevenção

- Nunca usar `verify_exp: False` em ambiente de produção
- Implementar blacklist de tokens revogados (Redis ou tabela dedicada)
- Configurar alerta para tokens com mais de 12h ainda em uso
- Revisar mensalmente usuários com acesso ativo que foram desligados

---

## Escalação

Se o problema for o Caso 1 em produção:
1. **URGENTE** — acionar o Tech Lead imediatamente via `#incidentes`
2. Revogar todos os tokens ativos rotacionando a `SECRET_KEY`
3. Notificar a equipe de segurança
4. Consultar `docs/suporte/escalation-policy.md`
