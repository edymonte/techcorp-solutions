"""
Testes unitários — API de Pedidos
Semana 2: encontre e corrija o bug que faz test_quantidade_none falhar.
"""

import pytest
from src.api.pedidos import (
    PedidoInvalidoError,
    listar_pedidos_pendentes,
    registrar_pedido,
    validar_pedido,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def pedido_valido():
    return {
        "cliente_id": "CLI-001",
        "produto_id": "PROD-042",
        "quantidade": 3,
        "preco_unitario": 29.90,
    }


# ---------------------------------------------------------------------------
# Testes de validação — casos que DEVEM passar
# ---------------------------------------------------------------------------


def test_pedido_valido_retorna_true(pedido_valido):
    assert validar_pedido(pedido_valido) is True


def test_pedido_quantidade_um_e_valido():
    pedido = {"cliente_id": "CLI-001", "produto_id": "P1", "quantidade": 1}
    assert validar_pedido(pedido) is True


def test_pedido_quantidade_grande_e_valido():
    pedido = {"cliente_id": "CLI-001", "produto_id": "P1", "quantidade": 9999}
    assert validar_pedido(pedido) is True


# ---------------------------------------------------------------------------
# Testes de validação — casos de borda que DEVEM levantar exceção
# ---------------------------------------------------------------------------


def test_pedido_sem_cliente_id_levanta_erro():
    pedido = {"produto_id": "P1", "quantidade": 2}
    with pytest.raises(PedidoInvalidoError, match="cliente_id"):
        validar_pedido(pedido)


def test_pedido_sem_produto_id_levanta_erro():
    pedido = {"cliente_id": "CLI-001", "quantidade": 2}
    with pytest.raises(PedidoInvalidoError, match="produto_id"):
        validar_pedido(pedido)


def test_pedido_sem_quantidade_levanta_erro():
    pedido = {"cliente_id": "CLI-001", "produto_id": "P1"}
    with pytest.raises(PedidoInvalidoError, match="quantidade"):
        validar_pedido(pedido)


def test_pedido_quantidade_zero_levanta_erro():
    pedido = {"cliente_id": "CLI-001", "produto_id": "P1", "quantidade": 0}
    with pytest.raises(PedidoInvalidoError):
        validar_pedido(pedido)


def test_pedido_quantidade_negativa_levanta_erro():
    pedido = {"cliente_id": "CLI-001", "produto_id": "P1", "quantidade": -5}
    with pytest.raises(PedidoInvalidoError):
        validar_pedido(pedido)


# ---------------------------------------------------------------------------
# ⚠️  BUG — Este teste FALHA antes da correção
#
# O campo `quantidade` pode chegar como None quando o PDV não envia o valor.
# Esperamos PedidoInvalidoError, mas o código atual lança TypeError.
# Corrija a função `validar_pedido()` em src/api/pedidos.py para passar aqui.
# ---------------------------------------------------------------------------


def test_pedido_quantidade_none_deve_levantar_pedido_invalido_error():
    """
    Regressão: sistema de PDV envia quantidade=None quando produto sem estoque.
    Deve levantar PedidoInvalidoError, não TypeError.
    Ref: TICKET-001 — Farmácia Boa Saúde.
    """
    pedido = {
        "cliente_id": "CLI-001",
        "produto_id": "PROD-042",
        "quantidade": None,
    }
    with pytest.raises(PedidoInvalidoError):
        validar_pedido(pedido)


# ---------------------------------------------------------------------------
# Testes de registro de pedido
# ---------------------------------------------------------------------------


def test_registrar_pedido_retorna_campos_esperados(pedido_valido):
    resultado = registrar_pedido(pedido_valido)

    assert resultado["status"] == "pendente"
    assert resultado["cliente_id"] == "CLI-001"
    assert resultado["produto_id"] == "PROD-042"
    assert resultado["quantidade"] == 3
    assert "id" in resultado
    assert resultado["id"].startswith("PED-")
    assert "criado_em" in resultado


def test_registrar_pedido_invalido_propaga_excecao():
    pedido_invalido = {"cliente_id": "CLI-001", "produto_id": "P1", "quantidade": 0}
    with pytest.raises(PedidoInvalidoError):
        registrar_pedido(pedido_invalido)


# ---------------------------------------------------------------------------
# Testes de listagem
# ---------------------------------------------------------------------------


def test_listar_pedidos_pendentes_filtra_corretamente():
    pedidos = [
        {"id": "PED-1", "status": "pendente"},
        {"id": "PED-2", "status": "processado"},
        {"id": "PED-3", "status": "pendente"},
        {"id": "PED-4", "status": "cancelado"},
    ]
    pendentes = listar_pedidos_pendentes(pedidos)
    assert len(pendentes) == 2
    assert all(p["status"] == "pendente" for p in pendentes)


def test_listar_pedidos_pendentes_lista_vazia():
    assert listar_pedidos_pendentes([]) == []


def test_listar_pedidos_pendentes_nenhum_pendente():
    pedidos = [{"id": "PED-1", "status": "processado"}]
    assert listar_pedidos_pendentes(pedidos) == []
