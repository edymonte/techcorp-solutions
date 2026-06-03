"""
TechCorp Solutions — Processador de Pedidos
Módulo limpo de referência — responsável por processar pedidos validados.
"""

import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class PedidoNaoEncontradoError(Exception):
    pass


def processar_pedido(pedido: dict) -> dict:
    """
    Processa um pedido validado, calculando o valor total e atualizando o status.

    Args:
        pedido: dicionário com os dados do pedido já validado

    Returns:
        pedido com status atualizado e valor total calculado
    """
    quantidade = pedido.get("quantidade")
    preco_unitario = pedido.get("preco_unitario", 0.0)

    if quantidade is None:
        raise ValueError("Campo 'quantidade' não pode ser nulo")

    if quantidade <= 0:
        raise ValueError("Quantidade deve ser maior que zero")

    valor_total = round(quantidade * preco_unitario, 2)

    pedido_processado = {
        **pedido,
        "valor_total": valor_total,
        "status": "processado",
        "processado_em": datetime.utcnow().isoformat(),
    }

    logger.info(
        f"Pedido {pedido.get('id')} processado — total: R$ {valor_total}"
    )
    return pedido_processado


def cancelar_pedido(pedido: dict, motivo: str) -> dict:
    """
    Cancela um pedido com o motivo informado.

    Args:
        pedido: dicionário com os dados do pedido
        motivo: descrição do motivo do cancelamento

    Returns:
        pedido com status 'cancelado' e motivo registrado
    """
    if pedido.get("status") == "processado":
        raise ValueError("Pedidos já processados não podem ser cancelados")

    return {
        **pedido,
        "status": "cancelado",
        "motivo_cancelamento": motivo,
        "cancelado_em": datetime.utcnow().isoformat(),
    }


def resumo_pedidos(pedidos: list) -> dict:
    """
    Gera um resumo estatístico de uma lista de pedidos.

    Args:
        pedidos: lista de dicionários de pedidos

    Returns:
        dicionário com totais por status
    """
    resumo = {"pendente": 0, "processado": 0, "cancelado": 0}

    for pedido in pedidos:
        status = pedido.get("status", "desconhecido")
        if status in resumo:
            resumo[status] += 1

    return resumo
