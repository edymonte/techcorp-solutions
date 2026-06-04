"""
Setup e Verificação de Ambiente — TechCorp Solutions Workshop
Execute: python setup/verificar_ambiente.py
     ou: clique duas vezes em setup.bat
"""

import sys
import subprocess
import importlib
import os

VERDE = "\033[92m"
VERMELHO = "\033[91m"
AMARELO = "\033[93m"
RESET = "\033[0m"
NEGRITO = "\033[1m"

resultados = []


def ok(msg):
    print(f"  {VERDE}✔{RESET}  {msg}")
    resultados.append(("ok", msg))


def erro(msg, dica=""):
    texto = f"  {VERMELHO}✘{RESET}  {msg}"
    if dica:
        texto += f"\n     {AMARELO}→ {dica}{RESET}"
    print(texto)
    resultados.append(("erro", msg))


def aviso(msg, dica=""):
    texto = f"  {AMARELO}⚠{RESET}  {msg}"
    if dica:
        texto += f"\n     {AMARELO}→ {dica}{RESET}"
    print(texto)
    resultados.append(("aviso", msg))


def titulo(msg):
    print(f"\n{NEGRITO}{msg}{RESET}")
    print("─" * 50)


def checar_http(url, nome):
    try:
        with urllib.request.urlopen(url, timeout=3) as resp:
            if resp.status == 200:
                ok(f"{nome} está rodando ({url})")
                return True
    except Exception:
        pass
    return False


# ─────────────────────────────────────────────
print(f"\n{NEGRITO}{'═' * 50}{RESET}")
print(f"{NEGRITO}  TechCorp Workshop — Preparando seu ambiente{RESET}")
print(f"{NEGRITO}{'═' * 50}{RESET}")

raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ─────────────────────────────────────────────
titulo("1. Python")

major, minor = sys.version_info.major, sys.version_info.minor
versao = f"{major}.{minor}.{sys.version_info.micro}"
if major == 3 and minor >= 11:
    ok(f"Python {versao}")
elif major == 3 and minor >= 9:
    aviso(f"Python {versao} (recomendado: 3.11+)", "Pode funcionar, mas prefira 3.11")
else:
    erro(f"Python {versao} incompatível", "Instale Python 3.11: https://python.org/downloads")

# ─────────────────────────────────────────────
titulo("2. Dependências Python")

print(f"     instalando pacotes...")
req_files = []
for req in ["requirements.txt", "requirements-dev.txt"]:
    path = os.path.join(raiz, req)
    if os.path.exists(path):
        req_files += ["-r", path]

res_pip = subprocess.run(
    [sys.executable, "-m", "pip", "install", "--quiet"] + req_files,
    capture_output=True,
    text=True,
    cwd=raiz,
)
if res_pip.returncode != 0:
    erro("Falha ao instalar pacotes", "Verifique sua conexão e tente novamente")
else:
    importlib.invalidate_caches()
    pacotes = {
        "pytest": "pytest (requirements-dev.txt)",
        "jwt": "pyjwt (requirements.txt)",
        "flask": "flask (requirements.txt)",
    }
    for modulo, origem in pacotes.items():
        try:
            __import__(modulo)
            ok(f"{modulo} instalado")
        except ImportError:
            erro(f"{modulo} não encontrado", f"[{origem}]")

# ─────────────────────────────────────────────
titulo("3. Banco de dados SQLite")

db_path = os.path.join(raiz, "db", "techcorp.db")
if os.path.exists(db_path):
    ok("db/techcorp.db encontrado")
else:
    print(f"     criando banco de dados...")
    res_db = subprocess.run(
        [sys.executable, "db/init_db.py"],
        capture_output=True,
        text=True,
        cwd=raiz,
    )
    if res_db.returncode == 0:
        ok("db/techcorp.db criado com sucesso")
    else:
        erro("Falha ao criar db/techcorp.db", "Execute: python db/init_db.py")

# ─────────────────────────────────────────────
titulo("4. Testes da aplicação")

BUGS_INTENCIONAIS = {
    "test_pedido_quantidade_none_deve_levantar_pedido_invalido_error":
        "Bug intencional Semana 2 (TICKET-001) — use o Copilot para investigar",
    "test_token_expirado_deve_ser_rejeitado":
        "Bug intencional Semana 4 (TICKET-003) — use o Copilot para investigar",
    "test_token_expirado_nao_pode_obter_perfil":
        "Bug intencional Semana 4 (TICKET-003) — use o Copilot para investigar",
}

resultado = subprocess.run(
    [sys.executable, "-m", "pytest", "tests/", "-v", "--tb=no"],
    capture_output=True,
    text=True,
    cwd=raiz,
)

# Classifica cada linha de resultado FAILED
falhas_inesperadas = []
falhas_intencionais = []
for linha in resultado.stdout.splitlines():
    if " FAILED " in linha:
        nome_teste = linha.split("::")[-1].split(" ")[0]
        if nome_teste in BUGS_INTENCIONAIS:
            falhas_intencionais.append((nome_teste, BUGS_INTENCIONAIS[nome_teste]))
        else:
            falhas_inesperadas.append(linha.strip())

# Contagem geral
sumario = next(
    (l for l in resultado.stdout.splitlines() if "passed" in l or "failed" in l),
    None,
)

if falhas_inesperadas:
    dica = "Execute: pytest tests/ -v  para detalhes"
    erro(f"pytest: falhas inesperadas encontradas", dica)
    for f in falhas_inesperadas:
        print(f"     {VERMELHO}↳ {f}{RESET}")
elif sumario:
    # Extrai só a contagem (ex: "3 failed, 36 passed")
    partes = [p.strip() for p in sumario.split("=") if p.strip() and "in" in p]
    resumo = partes[0] if partes else sumario.strip()
    ok(f"pytest: {resumo}")
else:
    ok("pytest: concluído")

for nome, descricao in falhas_intencionais:
    aviso(f"pytest (esperado): {nome}", descricao)

# ─────────────────────────────────────────────
titulo("5. Node.js / npx")

for cmd in ["node", "npx"]:
    try:
        res = subprocess.run(
            [cmd, "--version"],
            capture_output=True,
            text=True,
            shell=(sys.platform == "win32"),
        )
        if res.returncode == 0:
            ok(f"{cmd} {res.stdout.strip()}")
        else:
            erro(f"{cmd} não respondeu", "Reinstale Node.js LTS: https://nodejs.org")
    except FileNotFoundError:
        erro(f"{cmd} não encontrado", "Instale Node.js LTS: https://nodejs.org e reabra o terminal")

# ─────────────────────────────────────────────
titulo("6. MCP — configuração")

mcp_path = os.path.join(raiz, ".vscode", "mcp.json")
if os.path.exists(mcp_path):
    ok(".vscode/mcp.json presente")
else:
    erro(".vscode/mcp.json ausente", "O arquivo deve estar na raiz do repositório clonado")

# ─────────────────────────────────────────────
print(f"\n{NEGRITO}{'═' * 50}{RESET}")

total_ok = sum(1 for r in resultados if r[0] == "ok")
total_erro = sum(1 for r in resultados if r[0] == "erro")
total_aviso = sum(1 for r in resultados if r[0] == "aviso")

print(f"  {VERDE}✔ {total_ok} ok{RESET}   {VERMELHO}✘ {total_erro} erro(s){RESET}   {AMARELO}⚠ {total_aviso} aviso(s){RESET}")

if total_erro == 0:
    print(f"\n  {VERDE}{NEGRITO}Ambiente pronto para o workshop!{RESET}")
else:
    print(f"\n  {VERMELHO}{NEGRITO}Corrija os erros acima antes do workshop.{RESET}")

print()
