#!/usr/bin/env python3
"""
TechCorp Solutions — Gerador de Evidências do Workshop GitHub Copilot

Uso:
    python setup/gerar_evidencia.py --semana 2 --nome "João Silva"
    python setup/gerar_evidencia.py --semana 3 --nome "Ana Lima"
    python setup/gerar_evidencia.py --semana 4 --nome "Carlos Mota"

Cada participante gera sua própria evidência individualmente.

A evidência gerada é salva em evidencias/ e aberta no navegador.
"""

import argparse
import glob
import hashlib
import os
import re
import subprocess
import sys
import webbrowser
from datetime import datetime

# ─────────────────────────────────────────────────────────────────────────────
# Garantir que o script roda sempre da raiz do projeto
# ─────────────────────────────────────────────────────────────────────────────

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

# ─────────────────────────────────────────────────────────────────────────────
# Definição dos objetivos e critérios de aprovação por semana
# ─────────────────────────────────────────────────────────────────────────────

SEMANAS = {
    2: {
        "titulo": "Debugging com GitHub Copilot",
        "objetivo": (
            "Identificar e corrigir o bug de validação de pedidos (Ticket-001) "
            "usando prompts profissionais no GitHub Copilot. "
            "O sistema aceitava 'quantidade = None' causando TypeError em produção — "
            "a correção garante que PedidoInvalidoError seja lançado corretamente."
        ),
        "papel": "Analista N2",
        "ferramenta": "GitHub Copilot Chat + @workspace",
        "ticket": "TICKET-001",
        "criterios": [
            {
                "tipo": "pytest",
                "descricao": "pedido com quantidade=None deve lançar PedidoInvalidoError",
                "test_id": "tests/test_pedidos.py::test_pedido_quantidade_none_deve_levantar_pedido_invalido_error",
            },
            {
                "tipo": "pytest",
                "descricao": "pedido com quantidade=0 deve lançar PedidoInvalidoError",
                "test_id": "tests/test_pedidos.py::test_pedido_quantidade_zero_levanta_erro",
            },
        ],
    },
    3: {
        "titulo": "Corrigindo Pipeline CI com Copilot",
        "objetivo": (
            "Diagnosticar e corrigir a falha no pipeline GitHub Actions (Ticket-002). "
            "O PR #14 introduziu 'techcorp_core' como dependência externa inexistente — "
            "módulos internos devem ser importados por caminho relativo, "
            "nunca como pacotes externos."
        ),
        "papel": "Dev de Plataforma",
        "ferramenta": "GitHub Copilot + MCP GitHub",
        "ticket": "TICKET-002",
        "criterios": [
            {
                "tipo": "ausencia_texto",
                "descricao": "requirements.txt não contém 'techcorp_core'",
                "arquivo": "requirements.txt",
                "pattern": r"techcorp[_-]core",
            },
            {
                "tipo": "ausencia_texto_glob",
                "descricao": "nenhum arquivo em src/ importa 'techcorp_core'",
                "glob": "src/**/*.py",
                "pattern": r"import\s+techcorp[_-]core|from\s+techcorp[_-]core",
            },
            {
                "tipo": "pytest",
                "descricao": "módulo processador passa em todos os testes",
                "test_id": "tests/test_processador.py",
            },
        ],
    },
    4: {
        "titulo": "Segurança e Agent Mode",
        "objetivo": (
            "Identificar e corrigir a vulnerabilidade JWT (Ticket-003 — P1 Crítico). "
            "A opção 'verify_exp: False' desabilitava a verificação de expiração, "
            "permitindo acesso indevido com tokens vencidos. "
            "Categoria OWASP: A07 — Falhas de Identificação e Autenticação."
        ),
        "papel": "Dev + Suporte",
        "ferramenta": "GitHub Copilot Agent Mode + MCP SQLite",
        "ticket": "TICKET-003",
        "criterios": [
            {
                "tipo": "pytest",
                "descricao": "token expirado deve ser rejeitado por validar_token()",
                "test_id": "tests/test_auth.py::test_token_expirado_deve_ser_rejeitado",
            },
            {
                "tipo": "pytest",
                "descricao": "token expirado não pode acessar obter_perfil_usuario()",
                "test_id": "tests/test_auth.py::test_token_expirado_nao_pode_obter_perfil",
            },
            {
                "tipo": "ausencia_texto",
                "descricao": "verify_exp não está desabilitado em auth_service.py",
                "arquivo": "src/auth/auth_service.py",
                "pattern": r"[\"']verify_exp[\"']\s*:\s*False",
            },
        ],
    },
}

# ─────────────────────────────────────────────────────────────────────────────
# Executores de critério
# ─────────────────────────────────────────────────────────────────────────────


def _rodar_pytest(test_id: str) -> tuple[bool, str]:
    """Executa um teste ou módulo pytest e retorna (passou, mensagem_curta)."""
    result = subprocess.run(
        [sys.executable, "-m", "pytest", test_id, "-v", "--tb=short", "--no-header", "-q"],
        capture_output=True,
        text=True,
        cwd=ROOT,
    )
    passou = result.returncode == 0
    # Extrair resumo da última linha (ex: "1 passed", "1 failed")
    output = (result.stdout + result.stderr).strip()
    linhas = [l for l in output.splitlines() if l.strip()]
    resumo = linhas[-1] if linhas else "sem saída"
    return passou, resumo


def _verificar_ausencia_texto(arquivo: str, pattern: str) -> tuple[bool, str]:
    """Retorna True (ok) se o padrão NÃO for encontrado no arquivo."""
    caminho = os.path.join(ROOT, arquivo)
    if not os.path.exists(caminho):
        return False, f"{arquivo} não encontrado"
    with open(caminho, encoding="utf-8") as f:
        conteudo = f.read()
    if re.search(pattern, conteudo, re.IGNORECASE):
        return False, f"padrão '{pattern}' encontrado em {arquivo}"
    return True, f"padrão não encontrado em {arquivo}"


def _verificar_ausencia_glob(pattern_glob: str, pattern_re: str) -> tuple[bool, str]:
    """Retorna True (ok) se o padrão NÃO for encontrado em nenhum arquivo do glob."""
    arquivos = glob.glob(os.path.join(ROOT, pattern_glob), recursive=True)
    violadores = []
    for caminho in arquivos:
        with open(caminho, encoding="utf-8") as f:
            conteudo = f.read()
        if re.search(pattern_re, conteudo, re.IGNORECASE):
            violadores.append(os.path.relpath(caminho, ROOT))
    if violadores:
        return False, "encontrado em: " + ", ".join(violadores)
    return True, f"{len(arquivos)} arquivo(s) verificado(s) — nenhuma violação"


def executar_criterio(criterio: dict) -> dict:
    """Executa um critério e retorna resultado enriquecido."""
    tipo = criterio["tipo"]
    resultado = {"descricao": criterio["descricao"], "passou": False, "detalhe": ""}

    if tipo == "pytest":
        passou, detalhe = _rodar_pytest(criterio["test_id"])
        resultado["passou"] = passou
        resultado["detalhe"] = detalhe

    elif tipo == "ausencia_texto":
        passou, detalhe = _verificar_ausencia_texto(criterio["arquivo"], criterio["pattern"])
        resultado["passou"] = passou
        resultado["detalhe"] = detalhe

    elif tipo == "ausencia_texto_glob":
        passou, detalhe = _verificar_ausencia_glob(criterio["glob"], criterio["pattern"])
        resultado["passou"] = passou
        resultado["detalhe"] = detalhe

    return resultado


# ─────────────────────────────────────────────────────────────────────────────
# Geração do HTML de evidência
# ─────────────────────────────────────────────────────────────────────────────


def _gerar_codigo_unico(nome: str, semana: int, timestamp: str) -> str:
    raw = f"{nome}|{semana}|{timestamp}"
    return "TC-" + hashlib.sha256(raw.encode()).hexdigest()[:8].upper()


def gerar_html(nome: str, semana: int, info: dict, resultados: list[dict], aprovado: bool, timestamp: str) -> str:
    codigo = _gerar_codigo_unico(nome, semana, timestamp)
    status_class = "aprovado" if aprovado else "pendente"
    status_label = "OBJETIVO ALCANÇADO" if aprovado else "PENDENTE — critérios não atendidos"
    status_icon = "✓" if aprovado else "✗"
    ts_display = datetime.strptime(timestamp, "%Y%m%d_%H%M%S").strftime("%d/%m/%Y %H:%M:%S")

    linhas_criterios = ""
    for r in resultados:
        icon = "✔" if r["passou"] else "✘"
        cls = "ok" if r["passou"] else "fail"
        linhas_criterios += f"""
            <tr>
              <td class="ci {cls}">{icon}</td>
              <td class="cdesc">{r["descricao"]}</td>
              <td class="cres {cls}">{"PASSOU" if r["passou"] else "FALHOU"}</td>
            </tr>"""

    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Evidência · Semana {semana} · {nome}</title>
  <style>
    *{{box-sizing:border-box;margin:0;padding:0}}
    body{{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;
          background:#eef2f7;min-height:100vh;display:flex;
          align-items:center;justify-content:center;padding:2rem}}
    .card{{background:#fff;border-radius:16px;
           box-shadow:0 24px 64px rgba(0,0,0,.13);max-width:780px;width:100%;overflow:hidden}}

    /* ── HEADER ── */
    .hd{{background:linear-gradient(135deg,#0d1117 0%,#161b22 60%,#1a2332 100%);
         color:#fff;padding:2rem 2.5rem 1.75rem;position:relative}}
    .hd-top{{display:flex;align-items:center;justify-content:space-between;margin-bottom:1.1rem}}
    .brand{{font-size:.7rem;font-weight:700;letter-spacing:.18em;
            text-transform:uppercase;color:#58a6ff}}
    .wkbadge{{font-size:.65rem;border:1px solid rgba(88,166,255,.35);
              color:#58a6ff;padding:.25rem .8rem;border-radius:100px;
              letter-spacing:.09em;text-transform:uppercase}}
    .sw-label{{font-size:.8rem;color:rgba(255,255,255,.45);margin-bottom:.35rem}}
    .sw-titulo{{font-size:1.55rem;font-weight:800;line-height:1.2;margin-bottom:.3rem}}
    .sw-papel{{font-size:.82rem;color:rgba(255,255,255,.5)}}
    .sw-ticket{{position:absolute;top:2rem;right:2.5rem;
                font-family:'Courier New',monospace;font-size:.7rem;
                background:rgba(255,255,255,.07);color:rgba(255,255,255,.5);
                padding:.2rem .55rem;border-radius:4px}}

    /* ── BANNER DE STATUS ── */
    .banner{{display:flex;align-items:center;gap:1.1rem;
             padding:1.25rem 1.5rem;border-radius:10px;margin-bottom:1.75rem}}
    .banner.aprovado{{background:#f0fdf4;border:2px solid #22c55e}}
    .banner.pendente{{background:#fff7ed;border:2px solid #f97316}}
    .b-icon{{width:52px;height:52px;border-radius:50%;display:flex;
             align-items:center;justify-content:center;
             font-size:1.6rem;font-weight:900;flex-shrink:0}}
    .aprovado .b-icon{{background:#22c55e;color:#fff}}
    .pendente .b-icon{{background:#f97316;color:#fff}}
    .b-text .bl{{font-size:.65rem;font-weight:800;letter-spacing:.14em;
                 text-transform:uppercase;margin-bottom:.2rem}}
    .aprovado .bl{{color:#16a34a}}
    .pendente .bl{{color:#c2410c}}
    .b-text .bnome{{font-size:1.65rem;font-weight:900;color:#0d1117;line-height:1.1}}
    .b-text .bnome2{{font-size:1.3rem;font-weight:700;color:#374151;line-height:1.1}}
    .b-text .bsep{{font-size:.65rem;font-weight:700;letter-spacing:.1em;
                   text-transform:uppercase;color:#9ca3af;margin:.25rem 0}}

    /* ── CORPO ── */
    .body{{padding:0 2.5rem 2rem}}
    .sec{{margin-bottom:1.5rem}}
    .sec-title{{font-size:.65rem;font-weight:800;letter-spacing:.14em;
                text-transform:uppercase;color:#9ca3af;margin-bottom:.55rem}}
    .obj{{font-size:.92rem;color:#374151;line-height:1.65;
          padding:.8rem 1rem;background:#f8fafc;
          border-left:3px solid #3b82f6;border-radius:0 6px 6px 0}}

    /* ── TABELA DE CRITÉRIOS ── */
    table{{width:100%;border-collapse:collapse;font-size:.875rem}}
    th{{text-align:left;font-size:.65rem;font-weight:700;letter-spacing:.1em;
        text-transform:uppercase;color:#9ca3af;padding:.5rem .75rem;
        border-bottom:2px solid #e5e7eb}}
    td{{padding:.65rem .75rem;border-bottom:1px solid #f3f4f6;color:#374151}}
    .ci{{font-size:1.05rem;width:40px;text-align:center}}
    .cdesc{{color:#374151}}
    .cres{{font-weight:700;font-size:.8rem;white-space:nowrap}}
    .ok{{color:#16a34a}}
    .fail{{color:#dc2626}}

    /* ── FERRAMENTA ── */
    .ftag{{display:inline-flex;align-items:center;gap:.4rem;
           background:#eff6ff;color:#1d4ed8;border:1px solid #bfdbfe;
           font-size:.8rem;font-weight:600;padding:.35rem .85rem;border-radius:6px}}

    /* ── FOOTER ── */
    .ft{{padding:1.1rem 2.5rem;background:#f9fafb;
         border-top:1px solid #e5e7eb;display:flex;
         justify-content:space-between;align-items:center;gap:.5rem;flex-wrap:wrap}}
    .ft-meta{{font-size:.72rem;color:#9ca3af;line-height:1.7}}
    .ft-code{{font-family:'Courier New',monospace;font-size:.7rem;
              background:#e5e7eb;color:#374151;
              padding:.3rem .65rem;border-radius:4px;white-space:nowrap}}

    @media print{{
      body{{background:#fff;padding:0}}
      .card{{box-shadow:none;border-radius:0;max-width:100%}}
    }}
  </style>
</head>
<body>
  <div class="card">

    <div class="hd">
      <div class="hd-top">
        <span class="brand">TechCorp Solutions</span>
        <span class="wkbadge">GitHub Copilot Workshop</span>
      </div>
      <div class="sw-label">Semana {semana}</div>
      <div class="sw-titulo">{info["titulo"]}</div>
      <div class="sw-papel">{info["papel"]}</div>
      <div class="sw-ticket">{info["ticket"]}</div>
    </div>

    <div class="body">

      <div style="padding-top:2rem">
        <div class="banner {status_class}">
          <div class="b-icon">{status_icon}</div>
          <div class="b-text">
            <div class="bl">{status_label}</div>
            <div class="bnome">{nome}</div>
          </div>
        </div>
      </div>

      <div class="sec">
        <div class="sec-title">Objetivo da Semana</div>
        <div class="obj">{info["objetivo"]}</div>
      </div>

      <div class="sec">
        <div class="sec-title">Critérios de Aprovação</div>
        <table>
          <thead>
            <tr>
              <th></th>
              <th>Critério verificado</th>
              <th>Resultado</th>
            </tr>
          </thead>
          <tbody>{linhas_criterios}
          </tbody>
        </table>
      </div>

      <div class="sec">
        <div class="sec-title">Ferramenta principal utilizada</div>
        <span class="ftag">{info["ferramenta"]}</span>
      </div>

    </div>

    <div class="ft">
      <div class="ft-meta">
        Gerado em: {ts_display}<br>
        Workshop de GitHub Copilot — TechCorp Solutions ERP
      </div>
      <span class="ft-code">{codigo}</span>
    </div>

  </div>
</body>
</html>
"""


# ─────────────────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────────────────


def main():
    parser = argparse.ArgumentParser(
        description="Gera evidência de conclusão de semana do workshop."
    )
    parser.add_argument("--semana", type=int, required=True, choices=[2, 3, 4],
                        help="Número da semana (2, 3 ou 4)")
    parser.add_argument("--nome", type=str, required=True,
                        help='Nome do participante (ex: "João Silva")')
    args = parser.parse_args()

    nome = args.nome.strip()
    semana = args.semana
    info = SEMANAS[semana]

    print()
    print(f"  TechCorp Solutions — Workshop GitHub Copilot")
    print(f"  Gerando evidência · Semana {semana} · {info['titulo']}")
    print(f"  Participante: {nome}")
    print()

    resultados = []
    for criterio in info["criterios"]:
        print(f"  ... {criterio['descricao']}")
        r = executar_criterio(criterio)
        resultados.append(r)
        icone = "OK" if r["passou"] else "FALHOU"
        print(f"      -> {icone}")

    aprovado = all(r["passou"] for r in resultados)
    print()

    if aprovado:
        print("  [OK] Todos os criterios atendidos -- APROVADO")
    else:
        falhas = sum(1 for r in resultados if not r["passou"])
        print(f"  [!!] {falhas} criterio(s) nao atendido(s) -- verifique os itens acima")

    # Gerar HTML
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nome_arquivo = re.sub(r"[^\w]", "_", nome.lower())
    pasta = os.path.join(ROOT, "evidencias")
    os.makedirs(pasta, exist_ok=True)
    nome_html = f"semana{semana}_{nome_arquivo}_{timestamp}.html"
    caminho_html = os.path.join(pasta, nome_html)

    html = gerar_html(nome, semana, info, resultados, aprovado, timestamp)
    with open(caminho_html, "w", encoding="utf-8") as f:
        f.write(html)

    print()
    print(f"  Evidência salva em: evidencias/{nome_html}")
    webbrowser.open(f"file:///{caminho_html.replace(os.sep, '/')}")
    print("  Abrindo no navegador...")
    print()


if __name__ == "__main__":
    main()
