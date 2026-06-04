# Roteiro do Facilitador — GitHub Copilot Workshop
## TechCorp Solutions ERP

> **Para uso exclusivo do facilitador.**  
> Este documento orienta a condução de cada semana do workshop, com blocos de tempo, falas sugeridas, perguntas de debrief e sinais de progresso para monitorar durante os exercícios.

---

## Visão Geral do Workshop

| Etapa | Nível | Tema | Papel dos participantes | Duração |
|-------|-------|------|------------------------|---------||
| 1 | 🟢 ESSENCIAL | "O chamado chegou" — debugging com Copilot | Analista N2 | ~1h30 |
| 2 | 🟡 INTERMEDIÁRIO | "O pipeline quebrou" — CI com Copilot | Dev de Plataforma | ~1h30 |
| 3 | 🔴 CHALLENGE | "Tudo caiu ao mesmo tempo" — Agent Mode | Dev + Suporte | ~1h30 |

**Formato:** duplas. Um escreve o prompt, o outro revisa antes de enviar.  
**Entrega:** evidência gerada por `python setup/gerar_evidencia.py` ao final de cada semana.

---

## Antes de cada semana — Checklist do facilitador

```
[ ] Ambiente validado: setup.bat rodou sem erros críticos
[ ] VS Code com GitHub Copilot ativo nas máquinas das duplas
[ ] Projetor exibindo o repositório (aba README ou o ticket da semana)
[ ] Cronômetro visível para os participantes
[ ] Copilot-instructions.md revisado (não altere durante o workshop)
```

---

---

# ETAPA 1 — ESSENCIAL — "O chamado chegou"
## Tema: Debugging com GitHub Copilot Chat
## Duração total: ~1h30

---

### ⏱ 00:00 – 00:10 | Abertura e Contextualização

**O que fazer:** Apresente o cenário com energia. Projete o `tickets/ticket-001.md`.

**Fala sugerida:**
> "Vocês acabaram de assumir o plantão N2 da TechCorp Solutions.
> São 14h15 de uma segunda-feira. A Farmácia Boa Saúde — cliente VIP — 
> está ligando com pedidos travando há 15 minutos. O N1 já fez a triagem 
> pelo Bot de Suporte TechCorp e jogou na mesa de vocês.
> O SLA é de 2 horas. O relógio está correndo."

**Mostre no projetor:**
- O ticket aberto (`tickets/ticket-001.md`)
- O diagnóstico do N1 (seção Bot de Suporte TechCorp do ticket)
- A estrutura do projeto no VS Code (`src/api/pedidos.py` ainda fechado)

**O que NÃO fazer:** Não abra o arquivo `pedidos.py` ainda. Deixe a descoberta para as duplas.

---

### ⏱ 00:10 – 00:20 | Apresentação do Guia de Prompts (mini-aula)

**O que fazer:** Projete `docs/prompts/guia-prompts-profissionais.md`. Fique nos 3 primeiros blocos.

**Pontos obrigatórios para cobrir:**

1. **A anatomia de um prompt** — mostre os 5 elementos (Papel, Contexto, Tarefa, Restrições, Formato)

2. **Demonstração ao vivo — prompt fraco vs. profissional:**

   Abra o Copilot Chat e digite ao vivo, mostrando na tela:

   ```
   FRACO:
   "tem bug aqui?"
   ```
   Mostre a resposta genérica que vem.

   Depois:
   ```
   PROFISSIONAL:
   "Você é um dev N2 da TechCorp. Analise validar_pedido() em 
   src/api/pedidos.py. O ticket-001 diz que quantidade=None causa TypeError. 
   Mostre a linha exata e o fix mínimo em formato diff."
   ```
   Mostre a diferença de qualidade na resposta.

3. **Regra de ouro:** diga em voz alta:
   > "Se o Copilot te deu uma resposta genérica, o problema está no prompt — não no Copilot."

---

### ⏱ 00:20 – 00:55 | Exercício Hands-on (35 minutos)

**O que fazer:** Libere as duplas para trabalhar. Circule pela sala.

**Instrução para as duplas:**

> "Usem o prompt em `.github/prompts/investigar-bug-ticket.prompt.md` como base.
> Preencham os campos `[TICKET-XXX]` com o conteúdo do ticket-001.
> Objetivo: fazer o teste `test_pedido_quantidade_none_deve_levantar_pedido_invalido_error` passar.
> Ao final, preencham a seção 'Ações do N2' no ticket."

**O que monitorar durante o exercício:**

| Sinal | O que fazer |
|-------|-------------|
| Dupla copiou só o erro e perguntou "o que é isso?" | Pergunte: "Qual é o papel que vocês deram para o Copilot?" |
| Dupla recebeu resposta correta mas não sabe se confiar | Diga: "Rodem o pytest antes de aceitar. O teste é a prova." |
| Dupla já corrigiu e ficou parada | Incentive: "Adicionem o teste pytest que o ticket pede." |
| Dupla está tentando refatorar o código todo | Intervenha: "Fix mínimo — a restrição no prompt é importante." |
| Dupla não sabe usar o Copilot Chat | Mostre: `Ctrl+Shift+I` abre o chat; `@workspace` dá contexto do projeto |

**Perguntas que o facilitador pode fazer circulando:**
- "Qual papel vocês deram para o Copilot nesse prompt?"
- "Como vocês saberiam que o fix está certo sem rodar o teste?"
- "O que mudou na resposta quando vocês adicionaram as restrições?"

---

### ⏱ 00:55 – 01:10 | Debrief Guiado (15 minutos)

**O que fazer:** Reúna todos. Projete o código original e correto lado a lado.

**Perguntas de debrief — conduza uma discussão:**

1. **"Quantas iterações de prompt vocês precisaram antes de chegar no fix?"**
   - Resposta esperada: 2 a 4 iterações
   - Se alguém diz 1: "O que vocês colocaram no primeiro prompt que foi tão preciso?"
   - Se alguém diz 8+: "O que estava faltando nos seus prompts?"

2. **"Alguém tentou um prompt genérico primeiro? O que aconteceu?"**
   - Objetivo: confirmar que viram a diferença na prática

3. **"O que as restrições (`não altere a assinatura`) fizeram pela resposta?"**
   - Resposta esperada: evitaram que o Copilot reescrevesse a função inteira

4. **"Se fosse um incidente real, vocês conseguiriam fechar em 2h?"**
   - Discussão livre — é reflexão, não julgamento

**Mostre a correção completa:**
```python
# Antes (bug):
if pedido.get("quantidade") <= 0:

# Depois (fix mínimo):
quantidade = pedido.get("quantidade")
if quantidade is None or quantidade <= 0:
    raise PedidoInvalidoError("quantidade inválida")
```

---

### ⏱ 01:10 – 01:25 | Geração da Evidência + Encerramento

**O que fazer:** Cada dupla roda o script de evidência em sua máquina.

**Comando — projete na tela:**
```bash
python setup/gerar_evidencia.py --semana 1 --nome "Nome1" --parceiro "Nome2"
```

**Enquanto as duplas rodam:**
- Circule confirmando que a tela abriu no navegador
- Se alguma dupla ainda não passou nos testes, oriente-os a corrigir antes de gerar
- Bata um print da tela de quem conseguiu como momento de celebração

**Fala de encerramento:**
> "Na semana que vem, vocês vão sair do papel de quem conserta bugs e entrar no papel 
> de quem garante que os bugs não chegam em produção. A pipeline vai quebrar — 
> e vocês vão usar o Copilot para entender por quê antes de mexer em qualquer código."

---

---

# ETAPA 2 — INTERMEDIÁRIO — "O pipeline quebrou"
## Tema: Diagnóstico de CI com Copilot + MCP GitHub
## Duração total: ~1h30

---

### ⏱ 00:00 – 00:10 | Abertura e Contextualização

**O que fazer:** Projete o `tickets/ticket-002.md`. Mostre o log de erro do Actions.

**Fala sugerida:**
> "O PR #14 foi aprovado e mergeado. O pipeline disparou sozinho — e está vermelho.
> Ninguém consegue fazer deploy. O time todo está bloqueado.
> Vocês são Dev de Plataforma. A missão: entender o que causou, corrigir e 
> comentar no PR explicando o diagnóstico. Sem chute — evidência técnica."

**Mostre no projetor:**
- O erro do Actions (está no próprio ticket-002):
  ```
  ERROR: No matching distribution found for techcorp_core
  ```
- O PR hipotético que causou a falha: "feat: adicionar validação de estoque no processador"
- O padrão CI da empresa: `docs/pipelines/padrao-ci.md`

---

### ⏱ 00:10 – 00:20 | Mini-aula — @workspace e ferramentas certas

**O que fazer:** Demonstre ao vivo as ferramentas de nível 2.

**Ponto 1 — @workspace:**
> "Quando o problema pode estar em qualquer arquivo do projeto, usem @workspace.
> O Copilot passa a ver todo o repositório — não só o arquivo aberto."

Demonstre ao vivo:
```
@workspace quais arquivos em src/ fazem import de módulos que não estão 
em requirements.txt?
```

**Ponto 2 — MCP GitHub (se disponível):**
> "Quem tem o MCP GitHub configurado pode fazer o Copilot comentar no PR 
> diretamente, sem abrir o GitHub. Vamos ver isso em ação."

Mostre o prompt do arquivo `.github/prompts/corrigir-pipeline.prompt.md`.

**Ponto 3 — Ferramenta certa para cada situação:**

Projete a tabela do guia de prompts:
| Situação | Ferramenta |
|----------|-----------|
| Arquivo específico | Inline ou Chat com arquivo aberto |
| Problema em qualquer lugar | `@workspace` |
| Ação no GitHub | MCP GitHub |

---

### ⏱ 00:20 – 00:55 | Exercício Hands-on (35 minutos)

**Instrução para as duplas:**

> "Usem o prompt em `.github/prompts/corrigir-pipeline.prompt.md`.
> Preencham com o log do ticket-002.
> Objetivos:
> 1. Identificar o arquivo e a linha com o import indevido
> 2. Corrigir usando caminho relativo
> 3. Verificar que nenhum outro arquivo em src/ viola o mesmo padrão
> 4. Rodar pytest para confirmar que nada quebrou
> 5. Gerar o comentário para o PR (campo no prompt)"

**O que monitorar:**

| Sinal | O que fazer |
|-------|-------------|
| Dupla encontrou o arquivo mas não sabe a correção | Diga: "Pergunte ao Copilot qual é o padrão de import para módulos internos em Python." |
| Dupla corrigiu mas não verificou outros arquivos | Diga: "O prompt pede para verificar efeitos colaterais — o @workspace pode ajudar." |
| Dupla gerou o comentário de PR mas está informal | Diga: "Copiem o formato exato do prompt — o facilitador vai avaliar o comentário também." |
| Dupla terminou cedo | Challenge extra: "Adicionem uma regra no copilot-instructions.md para que isso nunca aconteça de novo." |

---

### ⏱ 00:55 – 01:10 | Debrief Guiado (15 minutos)

**Perguntas de debrief:**

1. **"Como vocês localizaram o import problemático — por leitura manual ou com o Copilot?"**
   - Objetivo: reforçar que @workspace é mais rápido que grep manual

2. **"O que o @workspace faz que o Chat normal não faz?"**
   - Resposta esperada: analisa o projeto inteiro, não só o arquivo aberto

3. **"Leiam para a sala o comentário de PR que vocês geraram."**
   - Compare 2 ou 3 duplas. Discuta: qual é mais útil para o revisor? Por quê?

4. **"Se esse erro voltasse amanhã com outro import, como vocês evitariam?"**
   - Resposta esperada: regra no copilot-instructions.md ou verificação no CI

**Mostre a solução:**
```python
# Errado (causou a falha):
import techcorp_core

# Correto (import relativo interno):
from src.pedidos import processador
```

---

### ⏱ 01:10 – 01:25 | Evidência + Encerramento

**Comando:**
```bash
python setup/gerar_evidencia.py --semana 2 --nome "Nome1" --parceiro "Nome2"
```

**Fala de encerramento:**
> "Vocês foram de analistas de bug para engenheiros de plataforma. 
> Na próxima etapa vai ser diferente: não vai ser um problema, vão ser três 
> ao mesmo tempo, numa sexta à tarde, com VIPs afetados.
> Vamos usar o Agent Mode — e deixar o Copilot investigar enquanto vocês tomam as decisões."

---

---

# ETAPA 3 — CHALLENGE — "Tudo caiu ao mesmo tempo"
## Tema: Incidente múltiplo — Agent Mode + Segurança
## Duração total: ~1h30

---

### ⏱ 00:00 – 00:10 | Abertura e Contextualização

**O que fazer:** Projete `tickets/ticket-003.md`. Mostre os 3 sub-incidentes.

**Fala sugerida — crie urgência:**
> "São 17h03 de uma sexta-feira. Três chamados chegaram ao mesmo tempo.
> Dois clientes VIP sem acesso. Pipeline bloqueado de novo.
> O faturamento parado.
> Vocês são o dev de plantão. Não dá para investigar um de cada vez.
> É aqui que o Agent Mode entra — deixem o Copilot abrir arquivos, rodar buscas,
> enquanto vocês tomam as decisões que importam."

**Mostre os 3 sub-incidentes:**
- **A:** Autenticação fora do ar — tokens rejeitados (CLI-012, VIP)
- **B:** Pipeline vermelho — `ModuleNotFoundError: No module named 'jwt'`
- **C:** Cliente VIP sem acesso (CLI-001) — token de 10h sendo aceito/rejeitado randomicamente

**Destaque o SLA:** 2 horas para clientes VIP — é real, é agora.

---

### ⏱ 00:10 – 00:20 | Mini-aula — Agent Mode e tomada de decisão

**O que fazer:** Demonstre o Agent Mode no VS Code.

**Ponto 1 — O que é Agent Mode:**
> "No Chat normal, você escreve um prompt, lê a resposta, age.
> No Agent Mode, você define o objetivo — e o Copilot age:
> abre arquivos, lê código, propõe mudanças, executa buscas.
> Vocês ficam no papel de aprovador: aceitar ou rejeitar cada ação."

**Ponto 2 — Demonstração rápida:**
Abra o Agent Mode (`Ctrl+Shift+I` → selecione "Agent") e mostre:
```
Você é o engenheiro de plantão da TechCorp Solutions.
Analise src/auth/auth_service.py e identifique 
por que tokens expirados estão sendo aceitos.
Mostre apenas o problema — não corrija ainda.
```

Deixe o agente investigar ao vivo. Mostre como ele abre o arquivo e retorna o diagnóstico.

**Ponto 3 — Regra de ouro do Agent Mode:**
> "No Agent Mode, NUNCA aceitem uma ação sem ler o que o Copilot vai mudar.
> Ele pode estar certo — mas a responsabilidade é de vocês."

---

### ⏱ 00:20 – 00:55 | Exercício Hands-on (35 minutos)

**Instrução para as duplas:**

> "Usem o prompt em `.github/prompts/resposta-incidente-multiplo.prompt.md`.
> Preencham os 3 sub-incidentes com o conteúdo do ticket-003.
> A sequência importa:
> 1. Façam a triagem — qual sub-incidente resolver primeiro?
> 2. Corrijam na ordem definida (dica: segurança antes de pipeline)
> 3. Verifiquem que os testes passam depois de cada fix
> 4. Usem o MCP SQLite para atualizar o status dos chamados no banco
> 5. Respondam: o que adicionar ao copilot-instructions.md para evitar recorrência?"

**Dica para explicar a ordem correta:**
- Sub-incidente A (auth) = raiz de tudo → corrigir primeiro
- Sub-incidente C (VIP sem acesso) = consequência do A → resolve junto
- Sub-incidente B (pipeline) = independente → resolver por último

**O que monitorar:**

| Sinal | O que fazer |
|-------|-------------|
| Dupla quer corrigir os 3 ao mesmo tempo | Diga: "Qual é o risco de corrigir auth e pipeline em paralelo?" |
| Dupla não entende o bug do JWT | Diga: "Peçam ao Copilot para explicar o que `verify_exp: False` faz — sem corrigir ainda." |
| Dupla corrigiu mas não rodou os testes | Diga: "O incidente só está fechado quando o teste passa. Qual teste cobre esse cenário?" |
| Dupla quer rotacionar a SECRET_KEY | INTERVENHA: "O prompt tem uma restrição específica sobre isso — leiam antes de prosseguir." |
| Dupla não sabe usar MCP SQLite | Oriente: mostre o comando no `.vscode/mcp.json` e a query básica de UPDATE |

---

### ⏱ 00:55 – 01:10 | Debrief Guiado (15 minutos)

**Perguntas de debrief:**

1. **"Qual sub-incidente vocês priorizaram e por quê?"**
   - Resposta esperada: A (auth) — é a causa raiz dos outros dois
   - Se alguém priorizou B: "O pipeline bloqueado impacta o cliente VIP ou o time interno?"

2. **"O que `verify_exp: False` faz exatamente — e qual é o risco em produção?"**
   - Resposta esperada: desabilita verificação de expiração → tokens velhos são aceitos indefinidamente → OWASP A07 (Falhas de Autenticação)
   - Reforce: "Isso é uma vulnerabilidade real. Esse tipo de configuração aparece em código de desenvolvimento que vazou para produção."

3. **"Alguém tentou rotacionar a SECRET_KEY? O que aconteceria se fizessem?"**
   - Resposta esperada: todos os usuários seriam deslogados simultaneamente
   - Diga: "O prompt tem uma restrição explícita por isso. Restrições em prompts não são sugestões — são guardrails."

4. **"O Agent Mode ajudou ou atrapalhou? Em que momento?"**
   - Discussão livre — é reflexão honesta sobre limites da ferramenta

5. **"O que vocês colocaram no copilot-instructions.md para evitar que isso volte?"**
   - Peça para 2 duplas lerem o que escreveram. Compare as abordagens.

**Mostre o fix da vulnerabilidade:**
```python
# Antes (vulnerável):
payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM],
                     options={"verify_exp": False})

# Depois (correto):
payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
```

---

### ⏱ 01:10 – 01:25 | Evidência + Encerramento Final do Workshop

**Comando:**
```bash
python setup/gerar_evidencia.py --semana 3 --nome "Nome1" --parceiro "Nome2"
```

**Fala de encerramento do Workshop completo:**
> "Em três etapas, vocês passaram de 'tem bug aqui?' para prompts que identificam 
> causa raiz, geram diffs revisáveis, constroem testes e documentam o incidente.
> Isso é a diferença entre usar o Copilot como buscador e usá-lo como parceiro técnico.
>
> O que vocês escreveram hoje vai direto para a avaliação da competição.
> O código foi o pretexto. O prompt foi o produto."

---

---

## Apêndice A — Respostas para perguntas frequentes

| Pergunta | Resposta sugerida |
|----------|------------------|
| "O Copilot pode estar errado?" | "Sim — e é por isso que temos testes. Roda o pytest antes de aceitar qualquer fix." |
| "Posso usar o Copilot para entender o código inteiro?" | "Pode — mas prompts focados dão respostas melhores que 'explica esse projeto todo'." |
| "O Agent Mode vai substituir o dev?" | "O Agent Mode é tão bom quanto quem escreve o prompt e revisa as ações. Sem contexto e sem decisão humana, ele erra feio." |
| "Por que não posso simplesmente pedir 'corrija o bug'?" | "Peça e veja o que acontece. Depois compare com um prompt estruturado. A resposta é a demonstração." |
| "O MCP GitHub precisa de token?" | "Sim — o token deve estar configurado em `.vscode/mcp.json`. Se não estiver, as etapas 2 e 3 funcionam sem o MCP também." |

---

## Apêndice B — Critérios de aprovação por etapa (referência rápida)

| Etapa | Critério 1 | Critério 2 | Critério 3 |
|-------|-----------|-----------|-----------|
| 1 | `test_quantidade_none` passa | `test_quantidade_zero` passa | — |
| 2 | `requirements.txt` sem `techcorp_core` | Nenhum import indevido em `src/` | `test_processador.py` passa |
| 3 | `test_token_expirado_deve_ser_rejeitado` passa | `test_token_expirado_nao_pode_obter_perfil` passa | `verify_exp: False` removido do código |

---

## Apêndice C — Sinais de que a dupla está no caminho errado

- Passaram mais de 10 min lendo o código sem abrir o Copilot → peça para escrever um prompt
- Aceitaram o fix do Copilot sem rodar os testes → intervenha com "como vocês sabem que funciona?"
- Estão refatorando código além do escopo → leia a restrição do prompt em voz alta
- Geraram a evidência com critérios falhando → oriente a corrigir antes de tirar screenshot

---

*Documento de uso interno — Workshop GitHub Copilot — TechCorp Solutions ERP*
