# Roteiro — Vídeo 1: Etapa 1 — "O chamado chegou"
**Duração estimada:** 8–10 minutos  
**Objetivo:** Mostrar como ler um ticket, construir um prompt profissional e corrigir o bug com testes  
**Janelas abertas antes de gravar:** VS Code com o projeto aberto, terminal integrado

---

## CENA 1 — Introdução e contexto (0:00–0:40)

**[TELA: VS Code, nenhum arquivo aberto ainda]**

**NARRAÇÃO:**
> "Etapa 1. Você acaba de assumir o plantão N2 da TechCorp Solutions.
> São 14h15. A Farmácia Boa Saúde — um cliente VIP — está com o sistema de pedidos travado há 15 minutos.
> Nenhum pedido está sendo confirmado. O SLA é de 2 horas.
> O N1 já fez a triagem. Sua missão começa agora."

---

## CENA 2 — Lendo o ticket (0:40–1:30)

**[TELA: abrir tickets/ticket-001.md no VS Code]**

**AÇÃO:** Abrir o arquivo e rolar lentamente pela tela.

**NARRAÇÃO:**
> "Sempre comece lendo o ticket completo. Não pule direto para o código.
> Veja o relato da Maria Silva — supervisora da farmácia.
> Agora desça até a seção de triagem do N1. O bot de suporte já consultou os runbooks internos
> e deixou uma nota com a causa mais provável e as ações recomendadas para você."

**AÇÃO:** Destacar (selecionar) a seção "Triagem N1" na tela.

**NARRAÇÃO:**
> "O N1 indica que o problema está na função validar_pedido() em src/api/pedidos.py.
> Ele suspeita que o campo quantidade está chegando como None — e a função não trata esse caso.
> Mas não vamos abrir o arquivo ainda. Vamos deixar o Copilot nos mostrar onde está o problema."

---

## CENA 3 — Abrindo o template de prompt (1:30–2:10)

**[TELA: abrir .github/prompts/investigar-bug-ticket.prompt.md]**

**NARRAÇÃO:**
> "A TechCorp tem templates de prompt prontos para cada tipo de situação.
> Abra o arquivo investigar-bug-ticket.prompt.md. Esse é o ponto de partida — não invente do zero.
> Veja a estrutura: papel, tarefa, restrições e formato de resposta. Cada elemento tem um propósito."

**AÇÃO:** Rolar pelo arquivo lentamente mostrando a estrutura.

---

## CENA 4 — Prompt FRACO: demonstração (2:10–3:00)

**[TELA: Copilot Chat aberto à direita, VS Code à esquerda]**

**NARRAÇÃO:**
> "Antes de mostrar o prompt certo, vou te mostrar o que NÃO fazer.
> Esse é o prompt que a maioria das pessoas tenta primeiro."

**AÇÃO:** Digitar no Copilot Chat:
```
tem bug no pedidos.py?
```

**NARRAÇÃO:**
> "Olha a resposta. Genérica. Sem linha específica. Sem diff. Sem teste.
> O Copilot não errou — ele fez o que pôde com o que você deu.
> O problema está no prompt. Faltou papel, contexto e restrições."

---

## CENA 5 — Prompt PROFISSIONAL: construção ao vivo (3:00–4:30)

**[TELA: Copilot Chat, novo chat aberto]**

**NARRAÇÃO:**
> "Agora o prompt profissional. Vamos construir juntos, elemento por elemento."

**AÇÃO:** Digitar o prompt pausadamente, comentando cada parte:

```
Você é um desenvolvedor N2 da TechCorp Solutions, responsável por
resolver o TICKET-001.

Sintoma reportado: pedidos com quantidade=None travam o sistema com
TypeError. O N1 indicou que o problema está em validar_pedido() em
src/api/pedidos.py.

O que preciso:
1. Identifique a linha exata do TypeError e explique por quê ocorre
2. Mostre o fix mínimo em formato diff
3. Escreva um teste pytest para o caso quantidade=None em tests/test_pedidos.py

Restrições:
- Não altere a assinatura da função validar_pedido()
- Fix mínimo — não refatore o código ao redor
- Siga os padrões de .github/copilot-instructions.md
```

**NARRAÇÃO:**
> "Note o que mudou: dei um papel — N2 da TechCorp. Dei contexto — o ticket e o sintoma.
> Pedi tarefas específicas — linha exata, diff, teste. E coloquei restrições — fix mínimo, sem refatoração.
> Agora vou enviar."

---

## CENA 6 — Analisando a resposta (4:30–5:30)

**[TELA: resposta do Copilot no chat]**

**NARRAÇÃO:**
> "Veja a diferença. O Copilot identificou a linha exata, explicou por que o TypeError ocorre,
> mostrou o diff e escreveu o teste. Isso é utilizável direto.
> Antes de aceitar qualquer coisa — leia. Entenda o que está mudando."

**AÇÃO:** Ler a resposta em voz alta, pausar em cada ponto importante.

---

## CENA 7 — Aplicando o fix (5:30–6:30)

**[TELA: abrir src/api/pedidos.py]**

**NARRAÇÃO:**
> "Agora sim abrimos o arquivo. Aplique exatamente o que o diff sugere — nada a mais."

**AÇÃO:** Fazer a edição no arquivo mostrando a mudança claramente.

**NARRAÇÃO:**
> "Veja o antes e o depois. A mudança é mínima — exatamente o necessário para o bug ser corrigido.
> Fix mínimo não é preguiça — é disciplina."

---

## CENA 8 — Rodando os testes (6:30–7:30)

**[TELA: terminal integrado]**

**AÇÃO:** Digitar:
```bash
pytest tests/test_pedidos.py -v
```

**NARRAÇÃO:**
> "Antes de considerar o ticket resolvido, rode os testes. O teste é a prova — não a leitura do código.
> Aguarde..."

**AÇÃO:** Mostrar a saída com 14 passed.

**NARRAÇÃO:**
> "14 passed. O teste que estava falhando agora passa — incluindo o caso quantidade=None.
> Nenhum outro teste quebrou. O fix funcionou."

---

## CENA 9 — Preenchendo o ticket e gerando evidência (7:30–8:30)

**[TELA: tickets/ticket-001.md aberto]**

**NARRAÇÃO:**
> "Última etapa — documente o que foi feito. Peça ao Copilot para preencher a seção Ações do N2 no ticket."

**AÇÃO:** Abrir o Copilot Chat e digitar:
```
Gere o texto para preencher a seção "Ações do N2" do TICKET-001
com base no diagnóstico e fix que aplicamos. Siga o formato do ticket.
```

**[TELA: terminal]**

**AÇÃO:** Digitar:
```bash
python setup/gerar_evidencia.py --semana 1 --nome "Participante" --parceiro "Parceiro"
```

**NARRAÇÃO:**
> "O script gera um HTML com o resumo da etapa. Esse é o comprovante de que você completou o desafio.
> Etapa 1 concluída. No próximo vídeo — o pipeline de produção vai quebrar."

---

## Checklist de gravação

```
[ ] Copilot Chat visível ao lado do editor (layout dividido ou painel lateral)
[ ] ticket-001.md fechado antes de começar — abrir ao vivo
[ ] Prompt fraco digitado devagar o suficiente para ser lido
[ ] Pausa de 2–3 segundos antes de enviar cada prompt (dá tempo para o espectador ler)
[ ] Resposta do Copilot lida em voz alta antes de aplicar o fix
[ ] Terminal mostra pytest passando em tela cheia antes de cortar
```
