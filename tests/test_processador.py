"""
Testes unitários — Processador de Pedidos
Módulo de referência — todos os testes devem PASSAR sem alterações.
"""

import pytest
from src.pedidos.processador import cancelar_pedido, processar_pedido, resumo_pedidos


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def pedido_pendente():
    return {
        "id": "PED-001",
        "cliente_id": "CLI-001",
        "produto_id": "PROD-042",
        "quantidade": 3,
        "preco_unitario": 29.90,
        "status": "pendente",
    }


@pytest.fixture
def pedido_processado():
    return {
        "id": "PED-002",
        "cliente_id": "CLI-001",
        "produto_id": "PROD-010",
        "quantidade": 2,
        "preco_unitario": 15.50,
        "status": "processado",
        "valor_total": 31.00,
        "processado_em": "2026-06-03T14:00:00",
    }


# ---------------------------------------------------------------------------
# Testes de processamento — devem PASSAR
# ---------------------------------------------------------------------------


def test_processar_pedido_calcula_valor_total(pedido_pendente):
    resultado = processar_pedido(pedido_pendente)
    assert resultado["valor_total"] == 89.70  # 3 * 29.90


def test_processar_pedido_atualiza_status(pedido_pendente):
    resultado = processar_pedido(pedido_pendente)
    assert resultado["status"] == "processado"


def test_processar_pedido_preserva_campos_originais(pedido_pendente):
    resultado = processar_pedido(pedido_pendente)
    assert resultado["cliente_id"] == "CLI-001"
    assert resultado["produto_id"] == "PROD-042"
    assert resultado["quantidade"] == 3


def test_processar_pedido_adiciona_processado_em(pedido_pendente):
    resultado = processar_pedido(pedido_pendente)
    assert "processado_em" in resultado


def test_processar_pedido_valor_arredondado():
    pedido = {
        "id": "PED-003",
        "quantidade": 3,
        "preco_unitario": 10.005,  # arredondamento
        "status": "pendente",
    }
    resultado = processar_pedido(pedido)
    assert resultado["valor_total"] == round(3 * 10.005, 2)


# ---------------------------------------------------------------------------
# Testes de casos de borda no processamento
# ---------------------------------------------------------------------------


def test_processar_pedido_quantidade_none_levanta_erro():
    pedido = {"id": "PED-X", "quantidade": None, "preco_unitario": 10.0, "status": "pendente"}
    with pytest.raises(ValueError, match="nulo"):
        processar_pedido(pedido)


def test_processar_pedido_quantidade_zero_levanta_erro():
    pedido = {"id": "PED-X", "quantidade": 0, "preco_unitario": 10.0, "status": "pendente"}
    with pytest.raises(ValueError):
        processar_pedido(pedido)


def test_processar_pedido_quantidade_negativa_levanta_erro():
    pedido = {"id": "PED-X", "quantidade": -1, "preco_unitario": 10.0, "status": "pendente"}
    with pytest.raises(ValueError):
        processar_pedido(pedido)


# ---------------------------------------------------------------------------
# Testes de cancelamento
# ---------------------------------------------------------------------------


def test_cancelar_pedido_atualiza_status(pedido_pendente):
    resultado = cancelar_pedido(pedido_pendente, "Produto fora de estoque")
    assert resultado["status"] == "cancelado"


def test_cancelar_pedido_registra_motivo(pedido_pendente):
    motivo = "Produto fora de estoque"
    resultado = cancelar_pedido(pedido_pendente, motivo)
    assert resultado["motivo_cancelamento"] == motivo


def test_cancelar_pedido_ja_processado_levanta_erro(pedido_processado):
    with pytest.raises(ValueError, match="processados"):
        cancelar_pedido(pedido_processado, "Desistência")


def test_cancelar_pedido_adiciona_cancelado_em(pedido_pendente):
    resultado = cancelar_pedido(pedido_pendente, "Teste")
    assert "cancelado_em" in resultado


# ---------------------------------------------------------------------------
# Testes de resumo
# ---------------------------------------------------------------------------


def test_resumo_pedidos_conta_por_status():
    pedidos = [
        {"status": "pendente"},
        {"status": "processado"},
        {"status": "processado"},
        {"status": "cancelado"},
        {"status": "pendente"},
    ]
    resumo = resumo_pedidos(pedidos)
    assert resumo["pendente"] == 2
    assert resumo["processado"] == 2
    assert resumo["cancelado"] == 1


def test_resumo_pedidos_lista_vazia():
    resumo = resumo_pedidos([])
    assert resumo == {"pendente": 0, "processado": 0, "cancelado": 0}


def test_resumo_pedidos_ignora_status_desconhecido():
    pedidos = [{"status": "erro"}, {"status": "pendente"}]
    resumo = resumo_pedidos(pedidos)
    assert resumo["pendente"] == 1
    assert resumo["processado"] == 0
    assert resumo["cancelado"] == 0
