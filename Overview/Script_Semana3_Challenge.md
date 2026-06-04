# Script — Semana 3: CHALLENGE
## "Tudo caiu ao mesmo tempo"
**Duração total:** 2h | **Formato:** Apresentação (40min) + Desafio em duplas (1h20)

---

> 💬 **LEGENDA**
> - 🎙️ = O que você fala
> - 🖥️ = O que você faz na tela
> - ⏱️ = Tempo estimado
> - 💡 = Dica para o instrutor

---

## BLOCO 1 — Abertura: o cenário de crise
⏱️ *8 minutos*

---

🎙️ **FALA:**
> "Semana 1: vocês foram suporte, usaram o Copilot para entender e corrigir código. Semana 2: foram devs, trouxeram um pipeline de volta ao verde, conectaram o Copilot ao GitHub via MCP. Hoje é diferente."

🖥️ **AÇÃO:** Mostrar slide com texto: *"São 17h de uma sexta-feira."*

---

🎙️ **FALA:**
> "São 17h de uma sexta-feira. Três chamados abertos ao mesmo tempo. O sistema de autenticação caiu — nenhum usuário consegue logar. O pipeline de produção está bloqueado. E o cliente VIP da TechCorp, a maior farmácia da rede, está sem acesso há 40 minutos. Isso é um incidente crítico."

🖥️ **AÇÃO:** Abrir o AnythingLLM. Mostrar 3 notificações fictícias chegando ao mesmo tempo — pode ser o `ticket-003.md` com os 3 chamados listados.

---

🎙️ **FALA:**
> "Hoje vocês não são só suporte e não são só devs. Vocês são os dois ao mesmo tempo. E as ferramentas que vocês vão usar hoje são as mais avançadas da trilha: Agent Mode, agentes personalizados, skills e MCP com banco de dados. Vamos começar."

---

## BLOCO 2 — MCP SQLite: consultando os chamados em tempo real
⏱️ *8 minutos*

---

🎙️ **FALA:**
> "Primeira ação em qualquer incidente: entender o que está aberto. Na TechCorp, os chamados ficam num banco SQLite. Com o MCP de banco de dados configurado, o Copilot consegue consultar esse banco direto do chat — sem abrir nenhuma ferramenta separada."

🖥️ **AÇÃO:** Abrir o Copilot Chat no VS Code. Digitar:
```
Use o MCP do SQLite para listar todos os chamados abertos no banco techcorp.db, ordenados por prioridade.
```

---

🖥️ **AÇÃO:** Aguardar. Mostrar os 3 chamados aparecendo no chat com prioridade, status e descrição.

---

🎙️ **FALA:**
> "Três chamados. Autenticação, pipeline e cliente VIP. O Copilot leu o banco de dados e trouxe aqui — sem eu abrir o DB Browser, sem escrever SQL, sem trocar de janela. Esse é o poder do MCP: o Copilot se conecta ao mundo real."

---

🎙️ **FALA:**
> "Agora vou triagem com o N1 para saber por onde começar."

🖥️ **AÇÃO:** Abrir o AnythingLLM. Digitar:
```
Temos 3 chamados abertos simultaneamente: autenticação caiu, pipeline bloqueado e cliente VIP sem acesso. Qual a ordem de prioridade de acordo com o SLA da TechCorp e qual runbook devo seguir primeiro?
```

---

🖥️ **AÇÃO:** O N1 deve retornar a prioridade baseada no `docs/suporte/sla.md` e indicar o `runbook/auth-reset.md` como primeiro passo.

---

## BLOCO 3 — Agent Mode: implementando o fix com IA autônoma
⏱️ *15 minutos*

---

🎙️ **FALA:**
> "O N1 definiu a prioridade: autenticação primeiro. Vou abrir o código e usar o Agent Mode. Isso é diferente de tudo que fizemos até agora."

🖥️ **AÇÃO:** Abrir o Copilot Chat. Trocar para o modo **Agent** (ícone de agente no chat). Mostrar ao vivo a mudança de modo.

---

🎙️ **FALA:**
> "No modo normal, eu peço uma coisa por vez. No Agent Mode, eu descrevo um objetivo — e o Copilot planeja, edita múltiplos arquivos, executa ações e me reporta o que fez. Mas atenção: eu aprovo cada passo. Não aceito nada cegamente."

🖥️ **AÇÃO:** No Agent Mode, digitar:
```
#file:docs/arquitetura/visao-geral.md #file:docs/runbooks/auth-reset.md

O módulo de autenticação JWT em src/auth/auth_service.py não está validando a expiração do token. Tokens expirados estão sendo aceitos como válidos. 

Faça o seguinte:
1. Identifique o problema no código
2. Corrija a validação de expiração
3. Gere testes cobrindo token válido, token expirado e token inválido
4. Documente a função corrigida
```

---

🖥️ **AÇÃO:** Aguardar o Agent planejar. **PARAR antes de aceitar.** Mostrar o plano gerado.

---

🎙️ **FALA:**
> "Olhem — antes de executar, o Agent me mostrou o plano. Quatro etapas. Eu preciso revisar cada uma antes de aprovar. Isso não é diferente de revisar um PR de um colega. O Agent propõe, eu decido."

🖥️ **AÇÃO:** Aceitar etapa por etapa. Mostrar cada arquivo sendo modificado em tempo real. Destacar o diff de cada mudança.

---

🎙️ **FALA:**
> "Etapa 3 — os testes. Vou aprovar. Etapa 4 — a documentação. Vou aprovar. Agora vou rodar os testes para confirmar."

🖥️ **AÇÃO:** Rodar no terminal:
```bash
python -m pytest src/tests/test_auth.py -v
```

---

🖥️ **AÇÃO:** Mostrar todos os testes passando.

---

🎙️ **FALA:**
> "O Agent implementou, testou e documentou. Levou 4 minutos. Um dev experiente levaria 20. E eu não escrevi uma linha — eu tomei decisões. Essa é a virada: de dev que escreve para dev que decide."

---

## BLOCO 4 — Criando o agente de incidentes
⏱️ *10 minutos*

---

🎙️ **FALA:**
> "O fix está feito. Mas quero garantir que o próximo incidente seja resolvido mais rápido ainda. Vou criar um agente personalizado para a TechCorp — um agente de resposta a incidentes que qualquer dev do time pode usar."

🖥️ **AÇÃO:** Abrir `.github/agents/incident-responder.agent.md` no VS Code. Arquivo pode estar vazio ou com template.

---

🎙️ **FALA:**
> "Um agente personalizado é um arquivo markdown que define: qual é o papel do agente, quais são as regras que ele segue, quais ferramentas ele pode usar e como ele deve se comunicar. É literalmente um dev virtual que segue os padrões da TechCorp."

🖥️ **AÇÃO:** No Copilot Chat, digitar:
```
#file:docs/suporte/sla.md #file:docs/suporte/escalation-policy.md

Crie o conteúdo do arquivo .github/agents/incident-responder.agent.md para um agente de resposta a incidentes da TechCorp Solutions. O agente deve: seguir o SLA da empresa, consultar runbooks antes de agir, priorizar por impacto ao cliente, e sempre documentar as ações tomadas.
```

---

🖥️ **AÇÃO:** Aceitar e salvar o arquivo. Mostrar o conteúdo gerado.

---

🎙️ **FALA:**
> "Agora este agente existe no repositório. Qualquer dev que clonar o projeto tem acesso a ele. É um ativo do time — não um prompt que some quando você fecha o chat."

---

## BLOCO 5 — Fechando os chamados via MCP
⏱️ *5 minutos*

---

🎙️ **FALA:**
> "Fix feito, agente criado. Agora preciso fechar os chamados e abrir o PR. Tudo via MCP — sem sair do VS Code."

🖥️ **AÇÃO:** No Copilot Chat, digitar:
```
Use o MCP do SQLite para atualizar o status do chamado ID 1 para "resolvido" com a nota: "Bug de validação JWT corrigido. Tokens expirados agora são rejeitados corretamente. Testes adicionados."
```

---

🖥️ **AÇÃO:** Confirmar a atualização no banco. Em seguida:
```
Use o MCP do GitHub para abrir um PR com o título "fix: validação de expiração JWT" e descrever as mudanças feitas, referenciando os chamados 001, 002 e 003.
```

---

🖥️ **AÇÃO:** Mostrar o PR aparecendo no GitHub.

---

🎙️ **FALA:**
> "Chamados fechados no banco. PR aberto no GitHub. Issues referenciadas. Tudo a partir do chat — sem trocar de contexto, sem perder o fio do raciocínio. Isso é o que o MCP muda: o Copilot age no mundo real."

---

## BLOCO 6 — Passagem para o desafio em duplas
⏱️ *5 minutos*

---

🎙️ **FALA:**
> "Agora é com vocês. O cenário é o mesmo — incidente crítico, 3 chamados abertos, sexta às 17h. Vocês têm 1h20 para resolver tudo."

🖥️ **AÇÃO:** Projetar o checklist do desafio:
```
✅ Consultar chamados via MCP SQLite
✅ Triagem com o N1 (AnythingLLM)
✅ Corrigir auth_service.py via Agent Mode (revisar cada diff!)
✅ Testes passando no terminal
✅ .github/agents/incident-responder.agent.md criado
✅ Chamados fechados via MCP SQLite
✅ PR aberto via MCP GitHub
```

---

🎙️ **FALA:**
> "Uma regra absoluta no Challenge: nenhum diff do Agent é aceito sem leitura. Se eu ver alguém clicando em 'Accept All' sem ler, a dupla perde os pontos bônus. O Agent propõe — vocês decidem. Sempre."

💡 *Distribuir os cenários conforme o público:*
- *🟢 Padrão: Agent Mode + fix do auth, sem MCP SQLite*
- *🟡 Avançado: tudo com MCP GitHub + SQLite*
- *🔴 Expert: fluxo completo + `.agent.md` + `.skill.md` + fechar tudo via MCP*

---

## BLOCO 7 — Acompanhamento durante o desafio
⏱️ *1h20 minutos*

---

💡 **Durante o desafio — o que observar:**

| Momento | O que fazer |
|---|---|
| 10min | Verificar se o MCP SQLite está respondendo para todos |
| 20min | Checkpoint: quem já consultou os chamados? Quem está no Agent Mode? |
| 40min | Checkpoint: quem aprovou os diffs sem ler? Chamar atenção educadamente |
| 60min | Verificar se alguém criou o `.agent.md` — pedir para mostrar ao vivo |
| 75min | Aviso: 20 minutos. Priorizar fechar os chamados via MCP |

---

💡 **Perguntas para fazer durante a circulação:**
- *"O que o Agent planejou antes de você aceitar?"*
- *"Você leu o diff antes de aceitar? O que ele mudou?"*
- *"O que o seu agente de incidente sabe fazer que o Copilot padrão não sabe?"*
- *"Os 3 chamados estão fechados no banco? Mostra."*

---

## BLOCO 8 — Encerramento e retrospectiva final
⏱️ *5 minutos*

---

🎙️ **FALA:**
> "Vamos fechar o workshop. Não só a sessão de hoje — o workshop inteiro."

🖥️ **AÇÃO:** Mostrar o slide de retrospectiva com as 3 semanas.

---

🎙️ **FALA:**
> "Semana 1: vocês descobriram que o Copilot enxerga o código, não é um chatbot genérico. Semana 2: vocês aprenderam que contexto é tudo — @workspace, #file, copilot-instructions transformam o Copilot em um membro do time. Semana 3: vocês viram o Copilot agir no mundo real — Agent Mode, MCP, agentes personalizados."

---

🎙️ **FALA:**
> "O que muda a partir de agora? Vocês não vão mais usar o Copilot só para completar linha de código. Vocês vão usá-lo para dirigir — definir objetivos, revisar planos, tomar decisões. O Copilot executa. Vocês decidem. Essa é a nova divisão de trabalho."

---

🎙️ **FALA:**
> "A TechCorp Solutions vai continuar no repositório. Os documentos, os runbooks, os agentes — tudo que vocês criaram ficou lá. Usem como referência. Adaptem para os projetos reais de vocês. Obrigado pela participação."

---

🎙️ **FALA:**
> "Perguntas finais?"

💡 *Reservar 5 minutos. Coletar feedback informal: o que foi mais útil? O que faltou? Usar para próximas edições.*

---

## Checklist pré-sessão

- [ ] Ollama rodando: `ollama serve`
- [ ] AnythingLLM aberto com workspace TechCorp configurado
- [ ] MCP SQLite configurado e apontando para `db/techcorp.db`
- [ ] Banco com 3 chamados pré-inseridos (status: "aberto")
- [ ] MCP GitHub configurado com token válido
- [ ] Agent Mode disponível no Copilot Chat (verificar plano/licença)
- [ ] `ticket-003.md` aberto no VS Code
- [ ] `src/auth/auth_service.py` com bug intencional (não corrigir antes!)
- [ ] Terminal aberto e pytest instalado
- [ ] `.github/agents/incident-responder.agent.md` — arquivo vazio aguardando criação ao vivo
- [ ] PR aberto no GitHub aguardando (para demo de fechamento via MCP)

---

## Resumo das 3 semanas — tabela rápida

| | Semana 1 | Semana 2 | Semana 3 |
|---|---|---|---|
| **Papel** | Suporte N2 | Dev de plataforma | Dev + Suporte |
| **Problema** | Bug no código | Pipeline quebrado | Incidente crítico |
| **Copilot** | /explain /fix /tests /doc | @workspace #file instructions.md | Agent Mode + agents + skills |
| **MCP** | ❌ | GitHub | GitHub + SQLite |
| **Pipeline** | ❌ | ✅ real no fork | ✅ real no fork |
| **Entrega** | Ticket fechado + bug corrigido | Pipeline verde + PR comentado | Incidente resolvido + agente criado |
