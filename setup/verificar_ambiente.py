"""
Verificação de Ambiente — TechCorp Solutions Workshop
Execute: python setup/verificar_ambiente.py
"""

import sys
import subprocess
import urllib.request
import urllib.error
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
print(f"{NEGRITO}  VERIFICAÇÃO DE AMBIENTE — TechCorp Workshop{RESET}")
print(f"{NEGRITO}{'═' * 50}{RESET}")

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

pacotes = {
    "pytest": "pytest==8.2.0 (requirements-dev.txt)",
    "jwt": "pyjwt==2.8.0 (requirements.txt)",
    "flask": "flask==3.0.3 (requirements.txt)",
}

for modulo, origem in pacotes.items():
    try:
        __import__(modulo)
        ok(f"{modulo} instalado")
    except ImportError:
        erro(f"{modulo} não encontrado", f"Execute: pip install -r requirements-dev.txt  [{origem}]")

# ─────────────────────────────────────────────
titulo("3. Testes da aplicação")

raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
resultado = subprocess.run(
    [sys.executable, "-m", "pytest", "tests/", "-v", "--tb=no", "-q"],
    capture_output=True,
    text=True,
    cwd=raiz,
)
linhas = resultado.stdout.strip().splitlines()
for linha in linhas:
    if "passed" in linha or "failed" in linha or "error" in linha:
        if "failed" in linha or "error" in linha:
            erro(f"pytest: {linha.strip()}", "Revise os erros acima — alguns são intencionais (bugs do workshop)")
        else:
            ok(f"pytest: {linha.strip()}")
        break
else:
    if resultado.returncode == 0:
        ok("pytest: todos os testes passaram")
    else:
        erro("pytest retornou erro", "Execute: pytest tests/ -v  para detalhes")

# ─────────────────────────────────────────────
titulo("4. Banco de dados SQLite")

db_path = os.path.join(raiz, "db", "techcorp.db")
if os.path.exists(db_path):
    ok(f"db/techcorp.db encontrado")
else:
    erro("db/techcorp.db não existe", "Execute: python db/init_db.py")

# ─────────────────────────────────────────────
titulo("5. Node.js / npx")

for cmd in ["node", "npx"]:
    try:
        res = subprocess.run([cmd, "--version"], capture_output=True, text=True)
        if res.returncode == 0:
            ok(f"{cmd} {res.stdout.strip()}")
        else:
            erro(f"{cmd} não respondeu", "Reinstale Node.js LTS: https://nodejs.org")
    except FileNotFoundError:
        erro(f"{cmd} não encontrado", "Instale Node.js LTS: https://nodejs.org e reabra o terminal")

# ─────────────────────────────────────────────
titulo("6. Ollama (LLM local)")

if not checar_http("http://localhost:11434", "Ollama"):
    erro("Ollama não está rodando", "Abra o Ollama pelo menu Iniciar ou execute: ollama serve")
else:
    # Verificar se llama3.2 está instalado
    try:
        res = subprocess.run(["ollama", "list"], capture_output=True, text=True)
        if "llama3.2" in res.stdout:
            ok("Modelo llama3.2 disponível")
        else:
            aviso("Modelo llama3.2 não encontrado", "Execute: ollama pull llama3.2  (~2GB de download)")
    except FileNotFoundError:
        aviso("Não foi possível verificar modelos do Ollama")

# ─────────────────────────────────────────────
titulo("7. AnythingLLM (interface RAG)")

if not checar_http("http://localhost:3001", "AnythingLLM"):
    aviso(
        "AnythingLLM não está rodando",
        "Abra o aplicativo AnythingLLM pelo menu Iniciar",
    )

# ─────────────────────────────────────────────
titulo("8. MCP — configuração")

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
