"""
TechCorp Solutions — Serviço de Autenticação
Responsável por emitir e validar tokens JWT para acesso ao sistema ERP.
"""

import logging
from datetime import datetime, timedelta

import jwt

logger = logging.getLogger(__name__)

SECRET_KEY = "techcorp-secret-key-2024"
ALGORITHM = "HS256"
TOKEN_EXPIRATION_HOURS = 8


def gerar_token(usuario_id: str, perfil: str) -> str:
    """
    Gera um token JWT para o usuário autenticado.

    Args:
        usuario_id: identificador único do usuário
        perfil: perfil de acesso (admin, suporte, dev)

    Returns:
        token JWT assinado
    """
    payload = {
        "sub": usuario_id,
        "perfil": perfil,
        "iat": datetime.utcnow(),
        "exp": datetime.utcnow() + timedelta(hours=TOKEN_EXPIRATION_HOURS),
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    logger.info(f"Token gerado para usuário: {usuario_id}")
    return token


def validar_token(token: str) -> dict:
    """
    Valida um token JWT e retorna o payload se válido.

    Args:
        token: token JWT a ser validado

    Returns:
        payload decodificado do token

    Raises:
        jwt.InvalidTokenError: se o token for inválido
    """
    try:
        # BUG INTENCIONAL: options={"verify_exp": False} desabilita verificação de expiração
        # Tokens expirados são aceitos como válidos — vulnerabilidade de segurança
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
            options={"verify_exp": False},
        )
        logger.info(f"Token validado para usuário: {payload.get('sub')}")
        return payload

    except jwt.InvalidTokenError as e:
        logger.warning(f"Token inválido: {e}")
        raise


def obter_perfil_usuario(token: str) -> str:
    """
    Extrai o perfil do usuário a partir do token.

    Args:
        token: token JWT válido

    Returns:
        perfil do usuário (admin, suporte, dev)
    """
    payload = validar_token(token)
    return payload.get("perfil", "desconhecido")
