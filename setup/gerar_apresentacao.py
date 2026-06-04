"""
Gera o PowerPoint oficial do workshop GitHub Copilot — TechCorp Solutions.
Uso: python setup/gerar_apresentacao.py
Saída: docs/apresentacao-workshop.pptx
"""

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt
import os
import random

# ── Paleta de cores ────────────────────────────────────────────────────────────
AZUL_ESCURO   = RGBColor(0x0D, 0x1B, 0x2A)   # fundo principal
AZUL_MEDIO    = RGBColor(0x1B, 0x3A, 0x5C)   # fundo secundário
AZUL_ACENTO   = RGBColor(0x00, 0x78, 0xD4)   # destaque Microsoft blue
VERDE         = RGBColor(0x10, 0x7C, 0x10)   # aprovado / critérios
AMARELO       = RGBColor(0xFF, 0xB9, 0x00)   # atenção
BRANCO        = RGBColor(0xFF, 0xFF, 0xFF)
CINZA_CLARO   = RGBColor(0xD0, 0xD8, 0xE4)

# Cores dos níveis — Copilot Challenge
COR_ESSENCIAL     = RGBColor(0x18, 0x7A, 0x2E)   # verde    — Etapa 1 Essencial
COR_INTERMEDIARIO = RGBColor(0x96, 0x78, 0x00)   # âmbar    — Etapa 2 Intermediário
COR_CHALLENGE     = RGBColor(0xAA, 0x22, 0x22)   # vermelho — Etapa 3 Challenge

# ── Dimensões (Widescreen 16:9) ────────────────────────────────────────────────
W = Inches(13.33)
H = Inches(7.5)

prs = Presentation()
prs.slide_width  = W
prs.slide_height = H

BLANK = prs.slide_layouts[6]  # layout completamente em branco


# ── Helpers ────────────────────────────────────────────────────────────────────

def add_rect(slide, l, t, w, h, fill_rgb, alpha=None):
    shape = slide.shapes.add_shape(1, l, t, w, h)  # MSO_SHAPE_TYPE.RECTANGLE
    shape.line.fill.background()
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill_rgb
    return shape


def add_text(slide, text, l, t, w, h,
             font_size=24, bold=False, color=BRANCO,
             align=PP_ALIGN.LEFT, italic=False, wrap=True):
    txb = slide.shapes.add_textbox(l, t, w, h)
    txb.word_wrap = wrap
    tf = txb.text_frame
    tf.word_wrap = wrap
    para = tf.paragraphs[0]
    para.alignment = align
    run = para.add_run()
    run.text = text
    run.font.size = Pt(font_size)
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = color
    return txb


def add_bullet_box(slide, items, l, t, w, h,
                   font_size=20, color=BRANCO, bullet="▸ ", indent=0):
    txb = slide.shapes.add_textbox(l, t, w, h)
    txb.word_wrap = True
    tf = txb.text_frame
    tf.word_wrap = True
    first = True
    for item in items:
        if first:
            para = tf.paragraphs[0]
            first = False
        else:
            para = tf.add_paragraph()
        para.alignment = PP_ALIGN.LEFT
        para.space_before = Pt(4)
        run = para.add_run()
        run.text = (" " * indent) + bullet + item
        run.font.size = Pt(font_size)
        run.font.color.rgb = color
    return txb


def slide_header(slide, title, subtitle=None, accent=AZUL_ACENTO):
    """Barra superior com título."""
    add_rect(slide, 0, 0, W, Inches(1.3), AZUL_ESCURO)
    add_rect(slide, 0, Inches(1.3), Inches(0.08), H - Inches(1.3), accent)
    add_text(slide, title,
             Inches(0.4), Inches(0.15), W - Inches(0.8), Inches(0.85),
             font_size=34, bold=True, color=BRANCO, align=PP_ALIGN.LEFT)
    if subtitle:
        add_text(slide, subtitle,
                 Inches(0.4), Inches(0.85), W - Inches(0.8), Inches(0.5),
                 font_size=18, color=CINZA_CLARO, align=PP_ALIGN.LEFT)


def full_bg(slide, color=AZUL_ESCURO):
    add_rect(slide, 0, 0, W, H, color)


# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 1 — Capa
# ══════════════════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
full_bg(s)
add_rect(s, 0, Inches(2.8), W, Inches(2.4), AZUL_MEDIO)
add_rect(s, 0, Inches(2.8), Inches(0.12), Inches(2.4), AZUL_ACENTO)

add_text(s, "TechCorp Solutions",
         Inches(0.5), Inches(0.4), W - Inches(1), Inches(0.8),
         font_size=22, color=AZUL_ACENTO, align=PP_ALIGN.CENTER)

add_text(s, "GitHub Copilot Workshop",
         Inches(0.5), Inches(1.1), W - Inches(1), Inches(1.4),
         font_size=54, bold=True, color=BRANCO, align=PP_ALIGN.CENTER)

# Badges das 3 etapas
niveis_capa = [
    ("● ESSENCIAL",     COR_ESSENCIAL),
    ("● INTERMEDIÁRIO", COR_INTERMEDIARIO),
    ("● CHALLENGE",     COR_CHALLENGE),
]
for i, (nome, cor) in enumerate(niveis_capa):
    bx = Inches(0.9) + i * Inches(3.9)
    add_rect(s, bx, Inches(2.9), Inches(3.6), Inches(0.62), cor)
    add_text(s, nome, bx + Inches(0.1), Inches(2.93), Inches(3.4), Inches(0.55),
             font_size=18, bold=True, color=BRANCO, align=PP_ALIGN.CENTER)

add_text(s, "Do prompt genérico ao diagnóstico profissional",
         Inches(0.5), Inches(3.72), W - Inches(1), Inches(0.6),
         font_size=20, italic=True, color=CINZA_CLARO, align=PP_ALIGN.CENTER)

add_text(s, "1h30 por etapa  ·  Trabalho em duplas  ·  GitHub Copilot obrigatório",
         Inches(0.5), Inches(6.6), W - Inches(1), Inches(0.5),
         font_size=16, color=CINZA_CLARO, align=PP_ALIGN.CENTER)


# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 2 — Como funciona
# ══════════════════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
full_bg(s)
slide_header(s, "Como funciona o workshop")

boxes = [
    ("ETAPA 1", "ESSENCIAL",     '"O chamado chegou"',         "Debugging com Copilot Chat",     COR_ESSENCIAL),
    ("ETAPA 2", "INTERMEDIÁRIO", '"O pipeline quebrou"',       "CI com @workspace + MCP GitHub",  COR_INTERMEDIARIO),
    ("ETAPA 3", "CHALLENGE",     '"Tudo caiu ao mesmo tempo"', "Agent Mode + MCP SQLite",         COR_CHALLENGE),
]
for i, (etapa, nivel, tema, desc, cor) in enumerate(boxes):
    bx = Inches(0.4) + i * Inches(4.25)
    add_rect(s, bx, Inches(1.7), Inches(4.0), Inches(3.4), AZUL_MEDIO)
    add_rect(s, bx, Inches(1.7), Inches(4.0), Inches(0.25), cor)
    add_text(s, etapa, bx + Inches(0.15), Inches(1.82), Inches(3.7), Inches(0.4),
             font_size=13, color=cor, bold=True)
    add_text(s, nivel, bx + Inches(0.15), Inches(2.18), Inches(3.7), Inches(0.35),
             font_size=12, color=CINZA_CLARO)
    add_text(s, tema,  bx + Inches(0.15), Inches(2.5),  Inches(3.7), Inches(0.75),
             font_size=18, bold=True, color=BRANCO)
    add_text(s, desc,  bx + Inches(0.15), Inches(3.2),  Inches(3.7), Inches(0.6),
             font_size=15, color=CINZA_CLARO)

add_bullet_box(s, [
    "Trabalho em duplas — um escreve o prompt, o outro revisa antes de enviar",
    "Ao final de cada etapa: gerar evidência HTML com os critérios cumpridos",
    "Ferramenta usada: GitHub Copilot (Chat · Inline · Agent Mode)",
], Inches(0.4), Inches(5.35), W - Inches(0.8), Inches(1.8),
   font_size=18, color=CINZA_CLARO)


# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 3 — Linha do Tempo
# ══════════════════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
full_bg(s)
slide_header(s, "Linha do Tempo — 1h30 por etapa")

marcos = [
    ("00:00", "10 min", "Briefing",          "Instrutor apresenta o desafio, entrega os tickets e responde dúvidas de setup",   AZUL_ACENTO),
    ("00:10", "15 min", "Setup do ambiente", "Dupla instala dependências e configura o workspace com ajuda do Copilot",       AZUL_ACENTO),
    ("00:25", "50 min", "Desenvolvimento",   "Dupla usa o Copilot para resolver o ticket — instrutor circula e observa",        COR_ESSENCIAL),
    ("01:15", "10 min", "Validação",         "Instrutor testa o output de cada dupla com pytest e os critérios definidos",      AMARELO),
    ("01:25", " 5 min", "Pontuação e recap", "Critérios verificados, bônus anunciados, preview da próxima etapa",             AZUL_ACENTO),
]

for i, (hora, duracao, nome, desc, cor) in enumerate(marcos):
    ty = Inches(1.5) + i * Inches(1.1)
    if i < len(marcos) - 1:
        add_rect(s, Inches(1.57), ty + Inches(0.5), Inches(0.06), Inches(1.1), CINZA_CLARO)
    add_rect(s, Inches(1.2), ty + Inches(0.05), Inches(0.72), Inches(0.44), cor)
    add_text(s, hora, Inches(1.2), ty + Inches(0.07), Inches(0.72), Inches(0.38),
             font_size=12, bold=True, color=BRANCO, align=PP_ALIGN.CENTER)
    add_text(s, duracao, Inches(2.1), ty + Inches(0.08), Inches(1.1), Inches(0.35),
             font_size=13, color=cor, bold=True)
    add_text(s, nome, Inches(3.4), ty + Inches(0.04), Inches(3.0), Inches(0.42),
             font_size=19, bold=True, color=BRANCO)
    add_text(s, desc, Inches(6.65), ty + Inches(0.05), Inches(6.35), Inches(0.52),
             font_size=14, color=CINZA_CLARO, italic=True)


# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 4 — Configuração do ambiente
# ══════════════════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
full_bg(s)
slide_header(s, "Configuração do ambiente",
             "Pré-requisitos e passos para começar")

# Pré-requisitos (tabela visual)
requisitos = [
    ("Python 3.11+",  "python.org/downloads"),
    ("VS Code",       "code.visualstudio.com  —  extensão GitHub Copilot ativa"),
    ("Node.js LTS",   "nodejs.org  (necessário para o MCP GitHub)"),
    ("Git",           "git-scm.com/download/win"),
]
for i, (req, detalhe) in enumerate(requisitos):
    ty = Inches(1.55) + i * Inches(0.9)
    even = i % 2 == 0
    bg = AZUL_MEDIO if even else RGBColor(0x12, 0x28, 0x42)
    add_rect(s, Inches(0.3), ty, Inches(12.7), Inches(0.82), bg)
    add_rect(s, Inches(0.3), ty, Inches(0.06), Inches(0.82), AZUL_ACENTO)
    add_text(s, req,    Inches(0.55), ty + Inches(0.08), Inches(3.5), Inches(0.4),
             font_size=17, bold=True, color=AMARELO)
    add_text(s, detalhe, Inches(4.2), ty + Inches(0.12), Inches(8.7), Inches(0.55),
             font_size=16, color=CINZA_CLARO)

# Passos de setup
add_rect(s, Inches(0.3), Inches(5.25), Inches(12.7), Inches(1.7), RGBColor(0x06, 0x1A, 0x35))
add_rect(s, Inches(0.3), Inches(5.25), Inches(0.06), Inches(1.7), VERDE)
add_text(s, "1. Clone o repositório:",
         Inches(0.55), Inches(5.32), Inches(12.0), Inches(0.4),
         font_size=16, color=CINZA_CLARO)
add_text(s, "git clone https://github.com/edymonte/techcorp-solutions.git",
         Inches(0.55), Inches(5.68), Inches(12.0), Inches(0.45),
         font_size=18, bold=True, color=AMARELO)
add_text(s, "2. Abra a pasta no VS Code  →  clique duas vezes em  setup.bat  → aguarde (~30 seg)",
         Inches(0.55), Inches(6.13), Inches(12.0), Inches(0.45),
         font_size=16, color=BRANCO)

add_text(s, "💡  VS Code instala o GitHub Copilot automaticamente ao abrir a pasta — sem Docker necessário",
         Inches(0.3), Inches(7.0), W - Inches(0.6), Inches(0.4),
         font_size=15, color=CINZA_CLARO, align=PP_ALIGN.CENTER)


# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 4 — Anatomia do prompt profissional (renumerado — era slide 3)
# ══════════════════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
full_bg(s)
slide_header(s, "Anatomia de um prompt profissional",
             "5 elementos que fazem a diferença")

elementos = [
    ("1  Papel",      "Quem é o Copilot nesse contexto?",          '"Você é um dev N2 da TechCorp..."'),
    ("2  Contexto",   "Onde está o problema?",                      '"Em src/api/pedidos.py, função validar_pedido..."'),
    ("3  Tarefa",     "O que exatamente você quer?",                '"Identifique a linha que causa o TypeError"'),
    ("4  Restrições", "O que NÃO pode ser feito?",                  '"Não altere a assinatura da função"'),
    ("5  Formato",    "Como quer receber a resposta?",              '"Mostre em formato diff"'),
]

for i, (titulo, pergunta, exemplo) in enumerate(elementos):
    ty = Inches(1.55) + i * Inches(1.05)
    add_rect(s, Inches(0.3), ty, Inches(2.5), Inches(0.9), AZUL_MEDIO)
    add_text(s, titulo, Inches(0.4), ty + Inches(0.08), Inches(2.3), Inches(0.45),
             font_size=17, bold=True, color=AMARELO)
    add_text(s, pergunta, Inches(0.4), ty + Inches(0.45), Inches(2.3), Inches(0.4),
             font_size=13, color=CINZA_CLARO)
    add_text(s, exemplo, Inches(3.0), ty + Inches(0.15), Inches(9.9), Inches(0.65),
             font_size=15, color=BRANCO, italic=True)

add_rect(s, Inches(2.8), Inches(1.5), Inches(0.06), Inches(5.3), AZUL_ACENTO)

add_text(s, "💡  Se o Copilot te deu uma resposta genérica, o problema está no prompt — não no Copilot.",
         Inches(0.3), Inches(6.8), W - Inches(0.6), Inches(0.55),
         font_size=16, bold=True, color=AMARELO, align=PP_ALIGN.CENTER)


# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 5 — Prompt fraco vs. profissional
# ══════════════════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
full_bg(s)
slide_header(s, "Prompt fraco vs. Prompt profissional")

# Coluna esquerda — fraco
add_rect(s, Inches(0.3), Inches(1.5), Inches(6.1), Inches(4.8), RGBColor(0x3A, 0x10, 0x10))
add_rect(s, Inches(0.3), Inches(1.5), Inches(6.1), Inches(0.5), RGBColor(0x8B, 0x00, 0x00))
add_text(s, "✗  FRACO", Inches(0.5), Inches(1.52), Inches(5.7), Inches(0.45),
         font_size=18, bold=True, color=BRANCO)
add_text(s, '"tem bug aqui?"',
         Inches(0.5), Inches(2.1), Inches(5.7), Inches(0.7),
         font_size=22, italic=True, color=CINZA_CLARO)
add_bullet_box(s, [
    "Sem papel definido",
    "Sem arquivo ou função indicados",
    "Sem contexto do ticket",
    "Sem restrições",
    "Sem formato de saída",
], Inches(0.5), Inches(2.9), Inches(5.7), Inches(2.8), font_size=17,
   color=CINZA_CLARO, bullet="✗ ")

# Coluna direita — profissional
add_rect(s, Inches(6.9), Inches(1.5), Inches(6.1), Inches(4.8), RGBColor(0x06, 0x2A, 0x10))
add_rect(s, Inches(6.9), Inches(1.5), Inches(6.1), Inches(0.5), VERDE)
add_text(s, "✓  PROFISSIONAL", Inches(7.1), Inches(1.52), Inches(5.7), Inches(0.45),
         font_size=18, bold=True, color=BRANCO)
add_text(s,
         '"Você é dev N2 da TechCorp.\nAnalise validar_pedido() em\nsrc/api/pedidos.py.\nTicket-001: quantidade=None causa\nTypeError. Mostre linha exata\ne fix mínimo em diff."',
         Inches(7.1), Inches(2.05), Inches(5.7), Inches(2.1),
         font_size=15, italic=True, color=CINZA_CLARO)
add_bullet_box(s, [
    "Papel: dev N2 da TechCorp",
    "Contexto: arquivo + função + ticket",
    "Tarefa: mostrar linha exata",
    "Restrição: fix mínimo",
    "Formato: diff",
], Inches(7.1), Inches(4.15), Inches(5.7), Inches(2.0), font_size=17,
   color=CINZA_CLARO, bullet="✓ ")

add_rect(s, Inches(6.4), Inches(1.5), Inches(0.06), Inches(4.8), AZUL_ACENTO)
add_text(s, "VS", Inches(6.1), Inches(3.5), Inches(0.8), Inches(0.7),
         font_size=24, bold=True, color=AMARELO, align=PP_ALIGN.CENTER)

add_text(s, "Use o arquivo  .github/prompts/  como base — ele já tem a estrutura certa.",
         Inches(0.3), Inches(6.6), W - Inches(0.6), Inches(0.55),
         font_size=16, color=CINZA_CLARO, align=PP_ALIGN.CENTER)


# ══════════════════════════════════════════════════════════════════════════════
# FUNÇÃO Matrix gate — slide de portão antes de cada etapa
# ══════════════════════════════════════════════════════════════════════════════
def slide_matrix_gate(numero, nivel, cor):
    """Slide estilo Matrix: fundo preto + chuva katakana verde + badge da etapa."""
    PRETO        = RGBColor(0x00, 0x00, 0x00)
    VERDE_MATRIX = RGBColor(0x00, 0xFF, 0x41)   # verde clássico do Matrix
    VERDE_MED    = RGBColor(0x00, 0xBB, 0x2C)
    VERDE_DIM    = RGBColor(0x00, 0x77, 0x1A)
    VERDE_DARK   = RGBColor(0x00, 0x33, 0x0A)

    s = prs.slides.add_slide(BLANK)

    # Fundo totalmente preto
    bg = s.shapes.add_shape(1, 0, 0, W, H)
    bg.fill.solid()
    bg.fill.fore_color.rgb = PRETO
    bg.line.fill.background()

    # Chuva Matrix — colunas de caracteres katakana/dígitos
    CHARS = list("ﾊﾐﾋｰｳｼﾅﾓﾆｻﾜﾂｵﾘｱﾎﾃﾏｹﾒｴｶｷﾑﾕﾗｾﾈｪｩｨ01アイウエオカキクケコサシスセソタチツテト▓▒░")
    rng = random.Random(numero * 7 + 13)   # seed por etapa → padrão diferente em cada portão
    col_count = 26
    for ci in range(col_count):
        col_chars = [rng.choice(CHARS) for _ in range(rng.randint(10, 24))]
        col_text  = "\n".join(col_chars)
        cx = Inches(ci * (13.33 / col_count))
        cy = Inches(rng.uniform(-1.0, 1.0))
        brightness = rng.choice([0x1A, 0x33, 0x55, 0x77, 0x99, 0xBB])
        txb = s.shapes.add_textbox(cx, cy, Inches(0.55), Inches(8.5))
        tf  = txb.text_frame
        tf.word_wrap = False
        tf.text = col_text
        for para in tf.paragraphs:
            para.alignment = PP_ALIGN.CENTER
            for run in para.runs:
                run.font.name  = "Courier New"
                run.font.size  = Pt(rng.choice([10, 11, 13]))
                run.font.color.rgb = RGBColor(0x00, brightness, 0x00)

    # Caixa central opaca com borda verde
    BOX_W = Inches(8.5)
    BOX_H = Inches(3.8)
    BOX_X = (W - BOX_W) / 2
    BOX_Y = Inches(1.85)
    frame = s.shapes.add_shape(1, BOX_X, BOX_Y, BOX_W, BOX_H)
    frame.fill.solid()
    frame.fill.fore_color.rgb = RGBColor(0x00, 0x08, 0x02)
    frame.line.color.rgb = VERDE_MATRIX
    frame.line.width = Pt(1.5)

    # Linha topo: "■ ACESSO RESTRITO ■"
    add_text(s, "■  ACESSO RESTRITO — AGUARDANDO LIBERAÇÃO  ■",
             BOX_X, BOX_Y + Inches(0.12), BOX_W, Inches(0.4),
             font_size=10, color=VERDE_DIM, align=PP_ALIGN.CENTER)

    # Número da etapa em destaque
    add_text(s, f"ETAPA  {numero}",
             BOX_X, BOX_Y + Inches(0.55), BOX_W, Inches(1.15),
             font_size=64, bold=True, color=VERDE_MATRIX, align=PP_ALIGN.CENTER)

    # Badge de nível
    add_text(s, f"[  {nivel}  ]",
             BOX_X, BOX_Y + Inches(1.75), BOX_W, Inches(0.75),
             font_size=26, bold=True, color=cor, align=PP_ALIGN.CENTER)

    # Separador
    sep = s.shapes.add_shape(1, BOX_X + Inches(1.0), BOX_Y + Inches(2.6),
                              BOX_W - Inches(2.0), Pt(1))
    sep.fill.solid()
    sep.fill.fore_color.rgb = VERDE_DIM
    sep.line.fill.background()

    # Status inferior
    add_text(s, "▌DESCRIPTOGRAFANDO MISSÃO...",
             BOX_X, BOX_Y + Inches(2.75), BOX_W, Inches(0.5),
             font_size=13, color=VERDE_MED, align=PP_ALIGN.CENTER)

    return s


# ══════════════════════════════════════════════════════════════════════════════
# FUNÇÃO para slides de semana
# ══════════════════════════════════════════════════════════════════════════════
def slide_etapa_capa(numero, nivel, titulo, papel, hora, cor=AZUL_ACENTO):
    s = prs.slides.add_slide(BLANK)
    full_bg(s, AZUL_ESCURO)
    add_rect(s, 0, 0, W, H, AZUL_ESCURO)
    add_rect(s, 0, Inches(2.2), W, Inches(3.1), AZUL_MEDIO)
    add_rect(s, 0, Inches(2.2), Inches(0.15), Inches(3.1), cor)

    # Badge de nível no topo
    add_rect(s, Inches(4.0), Inches(0.25), Inches(5.3), Inches(0.6), cor)
    add_text(s, f"● ETAPA {numero}  ·  {nivel}",
             Inches(4.0), Inches(0.28), Inches(5.3), Inches(0.55),
             font_size=18, bold=True, color=BRANCO, align=PP_ALIGN.CENTER)

    add_text(s, f'"{titulo}"',
             Inches(0.5), Inches(1.05), W - Inches(1), Inches(1.25),
             font_size=44, bold=True, color=BRANCO, align=PP_ALIGN.CENTER)

    add_text(s, f"Papel: {papel}",
             Inches(0.5), Inches(2.4), W - Inches(1), Inches(0.6),
             font_size=22, color=AMARELO, align=PP_ALIGN.CENTER)
    add_text(s, f"Duração: {hora}   ·   Trabalho em duplas",
             Inches(0.5), Inches(2.95), W - Inches(1), Inches(0.5),
             font_size=18, color=CINZA_CLARO, align=PP_ALIGN.CENTER)
    return s


def slide_cenario(etapa_n, ticket, situacao, itens, cor=AZUL_ACENTO):
    s = prs.slides.add_slide(BLANK)
    full_bg(s)
    slide_header(s, f"Etapa {etapa_n} — Cenário", ticket, accent=cor)
    add_text(s, situacao,
             Inches(0.4), Inches(1.45), W - Inches(0.8), Inches(0.8),
             font_size=20, italic=True, color=AMARELO)
    add_bullet_box(s, itens,
                   Inches(0.4), Inches(2.3), W - Inches(0.8), Inches(4.5),
                   font_size=19, color=BRANCO)
    return s


def slide_objetivo(etapa_n, objetivos, ferramenta, prompt_arquivo, cor=AZUL_ACENTO):
    s = prs.slides.add_slide(BLANK)
    full_bg(s)
    slide_header(s, f"Etapa {etapa_n} — Seu objetivo", accent=cor)
    add_bullet_box(s, objetivos,
                   Inches(0.4), Inches(1.5), Inches(8.5), Inches(4.5),
                   font_size=19, color=BRANCO)
    add_rect(s, Inches(9.2), Inches(1.5), Inches(3.8), Inches(3.2), AZUL_MEDIO)
    add_text(s, "Ferramenta principal", Inches(9.4), Inches(1.6), Inches(3.4), Inches(0.5),
             font_size=14, color=CINZA_CLARO)
    add_text(s, ferramenta, Inches(9.4), Inches(2.05), Inches(3.4), Inches(0.7),
             font_size=19, bold=True, color=AMARELO)
    add_text(s, "Prompt base", Inches(9.4), Inches(2.9), Inches(3.4), Inches(0.4),
             font_size=14, color=CINZA_CLARO)
    add_text(s, prompt_arquivo, Inches(9.4), Inches(3.3), Inches(3.4), Inches(1.1),
             font_size=13, italic=True, color=AZUL_ACENTO)
    return s


def slide_criterios(etapa_n, criterios, cor=AZUL_ACENTO):
    s = prs.slides.add_slide(BLANK)
    full_bg(s)
    slide_header(s, f"Etapa {etapa_n} — Critérios de aprovação", accent=cor)
    for i, (crit, detalhe) in enumerate(criterios):
        ty = Inches(1.6) + i * Inches(1.35)
        add_rect(s, Inches(0.3), ty, Inches(12.7), Inches(1.15), AZUL_MEDIO)
        add_rect(s, Inches(0.3), ty, Inches(0.08), Inches(1.15), VERDE)
        add_text(s, f"✓  {crit}", Inches(0.55), ty + Inches(0.07), Inches(12.0), Inches(0.5),
                 font_size=19, bold=True, color=BRANCO)
        add_text(s, detalhe, Inches(0.55), ty + Inches(0.55), Inches(12.0), Inches(0.5),
                 font_size=15, color=CINZA_CLARO)
    add_text(s, "Rode  pytest tests/ -v  antes de gerar a evidência para confirmar.",
             Inches(0.3), Inches(6.75), W - Inches(0.6), Inches(0.5),
             font_size=16, color=AMARELO, align=PP_ALIGN.CENTER)
    return s


# ══════════════════════════════════════════════════════════════════════════════
# ETAPA 1 — ESSENCIAL
# ══════════════════════════════════════════════════════════════════════════════
slide_matrix_gate(1, "ESSENCIAL", COR_ESSENCIAL)
slide_etapa_capa(1, "ESSENCIAL", "O chamado chegou", "Analista N2", "~1h30", COR_ESSENCIAL)

slide_cenario("1 — Essencial", "TICKET-001 — Falha no Processamento de Pedidos (P1)",
    "São 14h15 de segunda. A Farmácia Boa Saúde — cliente VIP — está ligando há 15 min.\nO Bot de Suporte TechCorp já fez a triagem. SLA: 2 horas.",
    [
        "Pedidos da Farmácia Boa Saúde estão falhando na API",
        "O Bot de Suporte indica: TypeError em validar_pedido() quando quantidade=None",
        "Arquivo suspeito: src/api/pedidos.py",
        "Você precisa identificar a linha exata, corrigir e provar com teste",
    ], COR_ESSENCIAL)

slide_objetivo("1 — Essencial",
    [
        "Abrir o ticket-001.md e ler o diagnóstico do Bot de Suporte",
        "Usar o Copilot Chat para identificar a linha que causa o TypeError",
        "Aplicar o fix mínimo — sem alterar a assinatura da função",
        "Confirmar que test_pedido_quantidade_none_deve_levantar_pedido_invalido_error passa",
        "Preencher a seção 'Ações do N2' no ticket",
    ],
    "Copilot Chat (Inline)",
    ".github/prompts/\ninvestigar-bug-ticket\n.prompt.md",
    COR_ESSENCIAL)

slide_criterios("1 — Essencial", [
    ("test_pedido_quantidade_none passa",
     "pytest tests/test_pedidos.py::test_pedido_quantidade_none_deve_levantar_pedido_invalido_error -v"),
    ("test_pedido_quantidade_zero passa",
     "pytest tests/test_pedidos.py::test_pedido_quantidade_zero_deve_levantar_pedido_invalido_error -v"),
], COR_ESSENCIAL)


# ══════════════════════════════════════════════════════════════════════════════
# ETAPA 2 — INTERMEDIÁRIO
# ══════════════════════════════════════════════════════════════════════════════
slide_matrix_gate(2, "INTERMEDIÁRIO", COR_INTERMEDIARIO)
slide_etapa_capa(2, "INTERMEDIÁRIO", "O pipeline quebrou", "Dev de Plataforma", "~1h30", COR_INTERMEDIARIO)

slide_cenario("2 — Intermediário", "TICKET-002 — Pipeline de Produção Bloqueado (P2)",
    "O PR #14 foi mergeado. O pipeline disparou — e está vermelho. Ninguém faz deploy.",
    [
        "Erro no GitHub Actions: ERROR: No matching distribution found for techcorp_core",
        "O time todo está bloqueado — nenhum deploy passa",
        "Suspeita: import indevido introduzido no PR #14",
        "Você precisa identificar, corrigir e documentar para o PR",
    ], COR_INTERMEDIARIO)

slide_objetivo("2 — Intermediário",
    [
        "Usar @workspace para localizar o import problemático em src/",
        "Corrigir usando caminho relativo correto (módulo interno)",
        "Verificar que nenhum outro arquivo em src/ viola o mesmo padrão",
        "Rodar pytest para confirmar que nada quebrou",
        "Gerar o comentário técnico para o PR (campo no prompt)",
    ],
    "Copilot @workspace\n+ MCP GitHub",
    ".github/prompts/\ncorrigir-pipeline\n.prompt.md",
    COR_INTERMEDIARIO)

slide_criterios("2 — Intermediário", [
    ("requirements.txt sem techcorp_core",
     "O pacote fictício foi removido — nenhum import externo indevido"),
    ("Nenhum import indevido em src/",
     "@workspace confirmou que todos os imports usam caminhos relativos internos"),
    ("test_processador.py passa",
     "pytest tests/test_processador.py -v — todos os testes verdes"),
], COR_INTERMEDIARIO)


# ══════════════════════════════════════════════════════════════════════════════
# ETAPA 3 — CHALLENGE
# ══════════════════════════════════════════════════════════════════════════════
slide_matrix_gate(3, "CHALLENGE", COR_CHALLENGE)
slide_etapa_capa(3, "CHALLENGE", "Tudo caiu ao mesmo tempo", "Dev + Suporte", "~1h30", COR_CHALLENGE)

slide_cenario("3 — Challenge", "TICKET-003 — Incidente Crítico: Múltiplas Falhas Simultâneas (P1)",
    "17h03 de sexta. Três chamados ao mesmo tempo. Dois VIPs sem acesso. SLA correndo.",
    [
        "Sub-incidente A: Autenticação fora do ar — tokens expirados sendo rejeitados (CLI-012, VIP)",
        "Sub-incidente B: Pipeline vermelho — ModuleNotFoundError: No module named 'jwt'",
        "Sub-incidente C: Cliente VIP (CLI-001) com token de 10h sendo aceito randomicamente",
        "Causa raiz suspeita: verify_exp: False em src/auth/auth_service.py",
        "⚠  Restrição crítica: NÃO rotacionar a SECRET_KEY sem aprovação do CTO",
    ], COR_CHALLENGE)

slide_objetivo("3 — Challenge",
    [
        "Usar Agent Mode para investigar os 3 sub-incidentes em paralelo",
        "Priorizar: A (auth) → C (VIP) → B (pipeline)",
        "Remover verify_exp: False — corrigir sem rotacionar a SECRET_KEY",
        "Atualizar status dos chamados no banco via MCP SQLite",
        "Adicionar regra no copilot-instructions.md para evitar recorrência",
    ],
    "Copilot Agent Mode\n+ MCP SQLite",
    ".github/prompts/\nresposta-incidente\n-multiplo.prompt.md",
    COR_CHALLENGE)

slide_criterios("3 — Challenge", [
    ("test_token_expirado_deve_ser_rejeitado passa",
     "pytest tests/test_auth.py::test_token_expirado_deve_ser_rejeitado -v"),
    ("test_token_expirado_nao_pode_obter_perfil passa",
     "pytest tests/test_auth.py::test_token_expirado_nao_pode_obter_perfil -v"),
    ("verify_exp: False removido do código",
     "grep em src/auth/auth_service.py não deve encontrar verify_exp: False"),
], COR_CHALLENGE)


# ══════════════════════════════════════════════════════════════════════════════
# SLIDE — Gerar evidência
# ══════════════════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
full_bg(s)
slide_header(s, "Gerar a evidência ao final de cada etapa")

add_rect(s, Inches(0.5), Inches(1.6), Inches(12.3), Inches(1.5), AZUL_MEDIO)
add_rect(s, Inches(0.5), Inches(1.6), Inches(0.08), Inches(1.5), AZUL_ACENTO)
add_text(s, "python setup/gerar_evidencia.py --semana 2 --nome \"João Silva\" --parceiro \"Ana Lima\"",
         Inches(0.8), Inches(1.75), Inches(12.0), Inches(1.1),
         font_size=20, bold=True, color=AMARELO)

add_bullet_box(s, [
    "Substitua o número: --semana 1, --semana 2 ou --semana 3 (Etapa 1, 2 e 3 respectivamente)",
    "Use os nomes da dupla exatamente como quiser que apareçam na evidência",
    "O script valida automaticamente os critérios antes de gerar",
    "Uma página HTML é aberta no navegador — tire o screenshot para envio",
    "Arquivo salvo em: evidencias/semana-X-NomeParceiro.html",
], Inches(0.5), Inches(3.3), W - Inches(1), Inches(3.0), font_size=18, color=BRANCO)

add_text(s, "⚠  Gere a evidência ANTES de sair da aula — ela valida o estado atual do código.",
         Inches(0.3), Inches(6.7), W - Inches(0.6), Inches(0.55),
         font_size=16, bold=True, color=AMARELO, align=PP_ALIGN.CENTER)


# ══════════════════════════════════════════════════════════════════════════════
# SLIDE — Regras de ouro
# ══════════════════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
full_bg(s)
slide_header(s, "Regras de ouro do workshop")

regras = [
    ("Um escreve, o outro revisa",
     "Antes de enviar qualquer prompt, o parceiro lê e aprova. Comunicação é parte do exercício."),
    ("Teste antes de aceitar",
     "O Copilot pode estar errado. Rode pytest antes de considerar qualquer fix concluído."),
    ("Prompt ruim → resposta ruim",
     "Se a resposta foi genérica, refine o prompt. Não culpe a ferramenta."),
    ("Fix mínimo, escopo fechado",
     "Corrija apenas o que o ticket pede. Refatoração não solicitada gera risco."),
    ("No Agent Mode: você é o aprovador",
     "Nunca aceite uma ação do agente sem ler o que vai mudar. A responsabilidade é sua."),
]

for i, (titulo, detalhe) in enumerate(regras):
    ty = Inches(1.5) + i * Inches(1.1)
    add_rect(s, Inches(0.3), ty, Inches(12.7), Inches(0.95), AZUL_MEDIO)
    add_rect(s, Inches(0.3), ty, Inches(0.08), Inches(0.95), AMARELO)
    add_text(s, titulo, Inches(0.55), ty + Inches(0.05), Inches(4.5), Inches(0.4),
             font_size=17, bold=True, color=AMARELO)
    add_text(s, detalhe, Inches(5.1), ty + Inches(0.1), Inches(7.9), Inches(0.75),
             font_size=15, color=CINZA_CLARO)


# ══════════════════════════════════════════════════════════════════════════════
# SLIDE FINAL — Encerramento
# ══════════════════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
full_bg(s, AZUL_ESCURO)
add_rect(s, 0, Inches(2.5), W, Inches(2.5), AZUL_MEDIO)
add_rect(s, 0, Inches(2.5), Inches(0.12), Inches(2.5), AZUL_ACENTO)

add_text(s, "O código foi o pretexto.",
         Inches(0.5), Inches(0.6), W - Inches(1), Inches(0.9),
         font_size=38, bold=True, color=BRANCO, align=PP_ALIGN.CENTER)
add_text(s, "O prompt foi o produto.",
         Inches(0.5), Inches(1.45), W - Inches(1), Inches(0.9),
         font_size=38, bold=True, color=AMARELO, align=PP_ALIGN.CENTER)

add_text(s, "Em três etapas, você passou de 'tem bug aqui?'\npara diagnósticos que identificam causa raiz,\ngeram diffs revisáveis e documentam o incidente.",
         Inches(0.8), Inches(2.65), W - Inches(1.6), Inches(2.1),
         font_size=20, color=CINZA_CLARO, align=PP_ALIGN.CENTER, italic=True)

add_text(s, "TechCorp Solutions  ·  GitHub Copilot Workshop",
         Inches(0.5), Inches(6.7), W - Inches(1), Inches(0.5),
         font_size=16, color=AZUL_ACENTO, align=PP_ALIGN.CENTER)


# ── Salvar ─────────────────────────────────────────────────────────────────────
out_dir = os.path.join(os.path.dirname(__file__), "..", "docs")
os.makedirs(out_dir, exist_ok=True)
out_path = os.path.join(out_dir, "apresentacao-workshop.pptx")
prs.save(out_path)
print(f"Apresentação gerada: {os.path.abspath(out_path)}")
print(f"Slides: {len(prs.slides)}")
