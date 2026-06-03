"""
Testes unitários — Serviço de Autenticação
Semana 4: encontre e corrija o bug que faz test_token_expirado_deve_ser_rejeitado falhar.
"""

import pytest
from datetime import datetime, timedelta

import jwt as pyjwt

from src.auth.auth_service import (
    SECRET_KEY,
    ALGORITHM,
    gerar_token,
    obter_perfil_usuario,
    validar_token,
)


# ---------------------------------------------------------------------------
# Helpers de teste
# ---------------------------------------------------------------------------


def _criar_token_expirado(usuario_id: str, perfil: str) -> str:
    """Cria um token com expiração no passado para simular token expirado."""
    payload = {
        "sub": usuario_id,
        "perfil": perfil,
        "iat": datetime.utcnow() - timedelta(hours=10),
        "exp": datetime.utcnow() - timedelta(hours=2),  # expirou 2h atrás
    }
    return pyjwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


# ---------------------------------------------------------------------------
# Testes de geração de token — devem PASSAR
# ---------------------------------------------------------------------------


def test_gerar_token_retorna_string():
    token = gerar_token("USER-001", "admin")
    assert isinstance(token, str)
    assert len(token) > 0


def test_gerar_token_contem_payload_correto():
    token = gerar_token("USER-002", "suporte")
    payload = pyjwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

    assert payload["sub"] == "USER-002"
    assert payload["perfil"] == "suporte"
    assert "exp" in payload
    assert "iat" in payload


def test_gerar_token_expira_em_8_horas():
    token = gerar_token("USER-003", "dev")
    payload = pyjwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

    exp = datetime.utcfromtimestamp(payload["exp"])
    iat = datetime.utcfromtimestamp(payload["iat"])
    diferenca = exp - iat

    assert abs(diferenca.total_seconds() - 8 * 3600) < 5  # margem de 5s


# ---------------------------------------------------------------------------
# Testes de validação de token — devem PASSAR
# ---------------------------------------------------------------------------


def test_validar_token_valido_retorna_payload():
    token = gerar_token("USER-001", "admin")
    payload = validar_token(token)

    assert payload["sub"] == "USER-001"
    assert payload["perfil"] == "admin"


def test_token_com_assinatura_invalida_levanta_erro():
    token = gerar_token("USER-001", "admin")
    token_adulterado = token[:-5] + "XXXXX"  # corrompe os últimos bytes

    with pytest.raises(pyjwt.InvalidTokenError):
        validar_token(token_adulterado)


# ---------------------------------------------------------------------------
# ⚠️  BUG — Este teste FALHA antes da correção
#
# Tokens expirados estão sendo aceitos porque `validar_token()` usa
# options={"verify_exp": False} — vulnerabilidade de segurança.
# Corrija `src/auth/auth_service.py` removendo essa opção para passar aqui.
# ---------------------------------------------------------------------------


def test_token_expirado_deve_ser_rejeitado():
    """
    Segurança: tokens com mais de 8h devem ser rejeitados.
    Ref: TICKET-003 — usuários com tokens antigos ainda acessando o sistema.
    """
    token_expirado = _criar_token_expirado("USER-004", "admin")

    with pytest.raises(pyjwt.ExpiredSignatureError):
        validar_token(token_expirado)


def test_token_expirado_nao_pode_obter_perfil():
    """
    Segurança: obter_perfil_usuario também deve rejeitar tokens expirados.
    """
    token_expirado = _criar_token_expirado("USER-004", "admin")

    with pytest.raises(pyjwt.ExpiredSignatureError):
        obter_perfil_usuario(token_expirado)


# ---------------------------------------------------------------------------
# Testes de perfil de usuário — devem PASSAR
# ---------------------------------------------------------------------------


def test_obter_perfil_admin():
    token = gerar_token("USER-001", "admin")
    assert obter_perfil_usuario(token) == "admin"


def test_obter_perfil_suporte():
    token = gerar_token("USER-002", "suporte")
    assert obter_perfil_usuario(token) == "suporte"


def test_obter_perfil_dev():
    token = gerar_token("USER-003", "dev")
    assert obter_perfil_usuario(token) == "dev"
