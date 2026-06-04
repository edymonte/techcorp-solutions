# Script — Semana 2: ESPECIALISTA
## "O pipeline quebrou"
**Duração total:** 2h | **Formato:** Apresentação (40min) + Desafio em duplas (1h20)

---

> 💬 **LEGENDA**
> - 🎙️ = O que você fala
> - 🖥️ = O que você faz na tela
> - ⏱️ = Tempo estimado
> - 💡 = Dica para o instrutor

---

## BLOCO 1 — Recap e elevação do nível
⏱️ *10 minutos*

---

🎙️ **FALA:**
> "Na semana passada, vocês atuaram como N2 de suporte. Consultaram o N1, usaram /explain, /fix, /tests, /doc e fecharam um chamado. Isso é o Copilot no modo assistente — você pede, ele entrega."

🖥️ **AÇÃO:** Mostrar o slide de recap da Semana 1 — diagrama do fluxo N1 → N2 → solução.

---

🎙️ **FALA:**
> "Hoje o nível sobe. Vocês deixam de ser suporte e entram no time de devs da TechCorp. E o problema não está no código — está no pipeline. Um PR foi aprovado, o código foi para o repositório, e o GitHub Actions explodiu."

🖥️ **AÇÃO:** Abrir o GitHub no repositório da TechCorp. Navegar até a aba Actions e mostrar o pipeline falhando com erro vermelho.

---

🎙️ **FALA:**
> "Esse erro vermelho está bloqueando o deploy de produção. Enquanto esse pipeline não voltar ao verde, nenhuma entrega sai. Vamos resolver isso — e vamos usar ferramentas que vocês ainda não viram: @workspace, #file, copilot-instructions.md e o MCP do GitHub."

---

## BLOCO 2 — Lendo o ticket e consultando o N1
⏱️ *8 minutos*

---

🎙️ **FALA:**
> "Antes de qualquer coisa — regra da TechCorp — consulte o N1. Sempre."

🖥️ **AÇÃO:** Abrir `tickets/ticket-002.md` no VS Code. Ler o conteúdo em voz alta.

---

🖥️ **AÇÃO:** Abrir o AnythingLLM. Digitar:
```
O pipeline de CI falhou com o erro: ModuleNotFoundError: No module named 'techcorp_core'. O que pode estar causando isso no nosso ambiente?
```

---

🖥️ **AÇÃO:** Aguardar a resposta. O N1 deve citar `docs/pipelines/pipeline-troubleshooting.md` e indicar que o pacote pode estar faltando no `requirements.txt`.

---

🎙️ **FALA:**
> "O N1 já apontou o caminho: o pacote `techcorp_core` provavelmente não está declarado no requirements.txt. Mas antes de ir direto corrigir — eu quero usar o @workspace para entender o impacto disso no projeto inteiro."

---

## BLOCO 3 — Usando @workspace e #file
⏱️ *15 minutos*

---

🎙️ **FALA:**
> "O @workspace é um dos recursos mais poderosos do Copilot Chat. Em vez de perguntar sobre um arquivo, você pergunta sobre o projeto inteiro. O Copilot lê tudo e responde com contexto completo."

🖥️ **AÇÃO:** Abrir o Copilot Chat no VS Code. Digitar:
```
@workspace Onde o pacote techcorp_core é importado no projeto? Liste todos os arquivos e linhas.
```

---

🖥️ **AÇÃO:** Aguardar. Mostrar a lista de arquivos que importam o pacote.

---

🎙️ **FALA:**
> "Olha — ele mapeou todos os lugares onde esse pacote é usado. Em vez de eu ficar fazendo Ctrl+F em cada arquivo, o Copilot fez isso por mim em segundos. Agora vou usar o #file para ser mais preciso na correção."

🖥️ **AÇÃO:** No Copilot Chat, digitar:
```
#file:requirements.txt #file:.github/workflows/ci.yml

O pacote techcorp_core está sendo importado no código mas não está declarado no requirements.txt. O ci.yml também está referenciando esse pacote incorretamente. Sugira as correções necessárias em ambos os arquivos.
```

---

🖥️ **AÇÃO:** Mostrar as sugestões do Copilot para os dois arquivos. Aplicar as correções.

---

🎙️ **FALA:**
> "Notem a diferença. Com #file eu trouxe exatamente os dois arquivos relevantes para o contexto. O Copilot não teve que adivinhar — ele tinha as informações certas para dar a resposta certa. Contexto rico, resposta precisa."

---

## BLOCO 4 — MCP GitHub: interagindo com o repositório via chat
⏱️ *15 minutos*

---

🎙️ **FALA:**
> "Agora vem a parte que muda o jogo. O MCP — Model Context Protocol — conecta o Copilot diretamente ao GitHub. Eu não preciso sair do VS Code para abrir uma issue, comentar num PR ou criar uma branch. Faço tudo via chat."

🖥️ **AÇÃO:** Mostrar o arquivo `.vscode/mcp.json` aberto no VS Code. Explicar brevemente a configuração.

---

🎙️ **FALA:**
> "Vou demonstrar. Vou pedir para o Copilot comentar no PR com o diagnóstico do problema — tudo sem sair do editor."

🖥️ **AÇÃO:** No Copilot Chat, com o MCP GitHub ativo, digitar:
```
Use o MCP do GitHub para comentar no PR #2 com o seguinte diagnóstico: "Bug identificado: pacote techcorp_core ausente no requirements.txt. Correção aplicada nas linhas 12 e 34. Pipeline deve voltar ao verde após este merge."
```

---

🖥️ **AÇÃO:** Ir ao GitHub no navegador e mostrar o comentário aparecendo no PR em tempo real.

---

🎙️ **FALA:**
> "Sem sair do VS Code. Sem trocar de aba. O Copilot agiu no GitHub por mim. Isso é o MCP — o Copilot deixa de ser um assistente de código e vira um agente conectado ao seu ambiente de trabalho."

---

🖥️ **AÇÃO:** No Copilot Chat, digitar:
```
Use o MCP do GitHub para criar uma issue no repositório techcorp-solutions com o título "Dívida técnica: declarar dependências internas no requirements.txt" e descrever o problema encontrado hoje.
```

---

🖥️ **AÇÃO:** Mostrar a issue criada no GitHub.

---

## BLOCO 5 — Criando o copilot-instructions.md
⏱️ *10 minutos*

---

🎙️ **FALA:**
> "Resolvemos o problema de hoje. Mas o que garante que o próximo dev não vai cometer o mesmo erro? Precisamos configurar o Copilot para conhecer os padrões da TechCorp — para que toda sugestão que ele faça já esteja alinhada com o que o time usa."

🖥️ **AÇÃO:** Abrir `.github/copilot-instructions.md` no VS Code.

---

🎙️ **FALA:**
> "Esse arquivo é lido pelo Copilot automaticamente em todo o projeto. É como contratar o Copilot como dev sênior da TechCorp — você explica os padrões uma vez e ele segue para sempre."

🖥️ **AÇÃO:** No Copilot Chat, digitar:
```
#file:docs/pipelines/padrao-ci.md

Com base nos padrões de pipeline da TechCorp descritos neste documento, gere o conteúdo do arquivo .github/copilot-instructions.md incluindo: padrões de import, estrutura de requirements.txt e boas práticas de CI/CD que o time deve seguir.
```

---

🖥️ **AÇÃO:** Aceitar e salvar o arquivo gerado. Mostrar o conteúdo ao vivo.

---

🎙️ **FALA:**
> "A partir de agora, qualquer sugestão do Copilot neste projeto vai considerar esses padrões. É a diferença entre usar o Copilot como ferramenta e configurá-lo como membro do time."

---

## BLOCO 6 — Passagem para o desafio em duplas
⏱️ *5 minutos*

---

🎙️ **FALA:**
> "Agora é com vocês. O desafio da semana está no `ticket-002.md` do fork de vocês. O pipeline está quebrado — vocês precisam trazer ele de volta ao verde. Mas mais do que isso: precisam deixar o projeto melhor do que encontraram."

🖥️ **AÇÃO:** Projetar o checklist do desafio:
```
✅ Pipeline voltando ao verde no GitHub Actions
✅ PR comentado via MCP GitHub com o diagnóstico
✅ .github/copilot-instructions.md criado com padrões do time
✅ ticket-002.md fechado com solução documentada
```

---

🎙️ **FALA:**
> "Lembrem: usem o N1 antes de abrir o código. Usem @workspace para mapear o impacto. Usem #file para contexto preciso. E usem o MCP para interagir com o GitHub sem sair do VS Code."

💡 *Distribuir os cenários conforme o público:*
- *🟢 Padrão: corrigir `requirements.txt` + `ci.yml` e ver o pipeline verde*
- *🟡 Avançado: corrigir + criar `copilot-instructions.md` + comentar no PR via MCP*
- *🔴 Expert: tudo acima + criar `.prompt.md` de troubleshooting reutilizável*

---

## BLOCO 7 — Acompanhamento durante o desafio
⏱️ *1h20 minutos*

---

💡 **Durante o desafio — o que observar:**

| Momento | O que fazer |
|---|---|
| 10min | Verificar se todos conseguiram ver o pipeline falhando no fork |
| 25min | Checkpoint: quem já usou @workspace? Mostrar a diferença vs prompt simples |
| 45min | Checkpoint: quem já viu o pipeline ficando verde? Pedir para mostrar |
| 60min | Verificar uso do MCP — quem já comentou no PR via chat? |
| 75min | Aviso: 20 minutos restantes |

---

💡 **Perguntas para fazer durante a circulação:**
- *"Qual contexto você passou com o #file?"*
- *"Você usou @workspace antes ou foi direto ao arquivo?"*
- *"O pipeline está verde agora? Mostra o Actions."*
- *"O que você colocou no copilot-instructions que mudou as sugestões?"*

---

## BLOCO 8 — Encerramento
⏱️ *2 minutos*

---

🎙️ **FALA:**
> "O que aprendemos hoje: contexto é poder. @workspace dá ao Copilot visão do projeto inteiro. #file dá precisão cirúrgica. O copilot-instructions.md transforma o Copilot em um membro do time. E o MCP conecta o Copilot ao mundo fora do editor. Na semana que vem, tudo isso junto — mais o Agent Mode. O desafio vai ser um incidente real. Sejam rápidos."

---

## Checklist pré-sessão

- [ ] Ollama rodando: `ollama serve`
- [ ] AnythingLLM aberto com workspace TechCorp configurado
- [ ] Pipeline falhando visível no GitHub (não corrigir antes!)
- [ ] MCP GitHub configurado no `.vscode/mcp.json` com token válido
- [ ] Token do GitHub com permissões: `repo`, `issues`, `pull_requests`
- [ ] `ticket-002.md` aberto no VS Code
- [ ] GitHub aberto no navegador na aba Actions — mostrando o erro
- [ ] PR #2 aberto e aguardando comentário (para a demo do MCP)
