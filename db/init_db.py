"""
TechCorp Solutions — Script de inicialização do banco de dados
Execute uma vez durante o setup: python db/init_db.py
"""

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "techcorp.db")


def criar_banco():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS chamados (
            id TEXT PRIMARY KEY,
            titulo TEXT NOT NULL,
            cliente_id TEXT NOT NULL,
            cliente_nome TEXT NOT NULL,
            prioridade TEXT NOT NULL,
            status TEXT NOT NULL,
            descricao TEXT,
            responsavel TEXT,
            aberto_em TEXT NOT NULL,
            fechado_em TEXT,
            resolucao TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            id TEXT PRIMARY KEY,
            nome TEXT NOT NULL,
            plano TEXT NOT NULL,
            contato TEXT,
            email TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id TEXT PRIMARY KEY,
            nome TEXT NOT NULL,
            perfil TEXT NOT NULL,
            email TEXT NOT NULL,
            ativo INTEGER DEFAULT 1,
            force_reset INTEGER DEFAULT 0
        )
    """)

    cur.executemany("INSERT OR REPLACE INTO clientes VALUES (?,?,?,?,?)", [
        ("CLI-001", "Farmácia Boa Saúde", "Premium", "Maria Silva", "maria@boasaude.com.br"),
        ("CLI-007", "Drogaria Central", "Premium", "João Alves", "joao@drogariacentral.com.br"),
        ("CLI-012", "Rede Saúde+", "Premium", "Carlos Melo", "carlos@redesaude.com.br"),
        ("CLI-020", "Farmácia Popular", "Standard", "Ana Costa", "ana@farmaciapopular.com.br"),
    ])

    cur.executemany("INSERT OR REPLACE INTO chamados VALUES (?,?,?,?,?,?,?,?,?,?,?)", [
        (
            "TICKET-001",
            "Falha no Processamento de Pedidos",
            "CLI-001", "Farmácia Boa Saúde",
            "P1", "aberto",
            "Desde as 14h o sistema não processa pedidos. Tela de erro ao finalizar compra.",
            None, "2026-06-03T14:12:00", None, None,
        ),
        (
            "TICKET-002",
            "Pipeline de Produção Bloqueado",
            "INTERNO", "Time de Desenvolvimento",
            "P2", "aberto",
            "GitHub Actions falhando com ModuleNotFoundError: No module named 'techcorp_core'",
            None, "2026-06-10T09:47:00", None, None,
        ),
        (
            "TICKET-003",
            "Incidente Crítico: Múltiplas Falhas Simultâneas",
            "CLI-012", "Rede Saúde+",
            "P1", "aberto",
            "Autenticação fora do ar + pipeline bloqueado + cliente VIP sem acesso simultâneos.",
            None, "2026-06-20T17:03:00", None, None,
        ),
    ])

    cur.executemany("INSERT OR REPLACE INTO usuarios VALUES (?,?,?,?,?,?)", [
        ("USER-001", "Admin TechCorp", "admin", "admin@techcorp.com.br", 1, 0),
        ("USER-002", "Ana Suporte", "suporte", "ana@techcorp.com.br", 1, 0),
        ("USER-003", "Carlos Dev", "dev", "carlos@techcorp.com.br", 1, 0),
        ("USER-004", "João Gerente", "admin", "joao.gerente@boasaude.com.br", 1, 0),
    ])

    conn.commit()
    conn.close()

    print(f"Banco criado em: {DB_PATH}")
    print("\nChamados inseridos:")

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT id, titulo, prioridade, status FROM chamados ORDER BY id")
    for row in cur.fetchall():
        print(f"  {row[0]} | {row[1]} | {row[2]} | {row[3]}")
    conn.close()


if __name__ == "__main__":
    criar_banco()
