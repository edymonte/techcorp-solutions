"""
TechCorp Solutions — API de Pedidos
Responsável por receber, validar e encaminhar pedidos para processamento.
"""

import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class PedidoInvalidoError(Exception):
    pass


def validar_pedido(pedido: dict) -> bool:
    """
    Valida os campos obrigatórios de um pedido antes do processamento.

    Args:
        pedido: dicionário com os dados do pedido

    Returns:
        True se o pedido for válido

    Raises:
        PedidoInvalidoError: se algum campo obrigatório estiver ausente ou inválido
    """
    campos_obrigatorios = ["cliente_id", "produto_id", "quantidade"]

    for campo in campos_obrigatorios:
        if campo not in pedido:
            raise PedidoInvalidoError(f"Campo obrigatório ausente: {campo}")

    # BUG INTENCIONAL: não trata None no campo quantidade
    # Se quantidade for None, a comparação abaixo lança TypeError
    if pedido["quantidade"] <= 0:
        raise PedidoInvalidoError("Quantidade deve ser maior que zero")

    return True


def registrar_pedido(pedido: dict) -> dict:
    """
    Registra um novo pedido no sistema.

    Args:
        pedido: dicionário com os dados do pedido

    Returns:
        dicionário com o pedido registrado e o id gerado
    """
    validar_pedido(pedido)

    pedido_registrado = {
        **pedido,
        "id": _gerar_id_pedido(),
        "status": "pendente",
        "criado_em": datetime.utcnow().isoformat(),
    }

    logger.info(f"Pedido registrado: {pedido_registrado['id']}")
    return pedido_registrado


def listar_pedidos_pendentes(pedidos: list) -> list:
    """Retorna apenas os pedidos com status 'pendente'."""
    return [p for p in pedidos if p.get("status") == "pendente"]


def _gerar_id_pedido() -> str:
    """Gera um ID único para o pedido baseado no timestamp."""
    return f"PED-{int(datetime.utcnow().timestamp())}"
