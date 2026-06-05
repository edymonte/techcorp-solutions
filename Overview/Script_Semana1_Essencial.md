# Script — Semana 1: ESSENCIAL
## "O chamado chegou"
**Duração total:** 2h | **Formato:** Apresentação (40min) + Desafio em duplas (1h20)

---

> 💬 **LEGENDA**
> - 🎙️ = O que você fala
> - 🖥️ = O que você faz na tela
> - ⏱️ = Tempo estimado
> - 💡 = Dica para o instrutor

---

## BLOCO 1 — Abertura e Contexto
⏱️ *10 minutos*

---

🎙️ **FALA:**
> "Bom dia, pessoal. Bem-vindos à primeira semana do GitHub Copilot Workshop. Antes de abrir qualquer ferramenta, quero que vocês entendam o cenário em que vão trabalhar hoje."

🖥️ **AÇÃO:** Abrir o slide da TechCorp Solutions — logo e apresentação da empresa.

---

🎙️ **FALA:**
> "A TechCorp Solutions é uma empresa que vende um sistema de gestão para clínicas e farmácias. Ela tem um time de suporte, um time de devs, e — diferente de qualquer empresa que vocês já viram — ela tem uma IA interna chamada N1 que faz a triagem de chamados antes de chegar em vocês."

🖥️ **AÇÃO:** Mostrar o diagrama: Cliente → Chamado → N1 (IA) → N2 (vocês) → Solução.

---

🎙️ **FALA:**
> "Hoje vocês são o N2. O N1 já recebeu o chamado, fez a triagem, consultou os documentos internos e deixou uma nota para vocês. O seu trabalho começa daqui."

💡 *Pausa dramática. Deixa a ideia absorver.*

---

🎙️ **FALA:**
> "O cliente é a Farmácia Boa Saúde. Às 14h de hoje, o sistema parou de processar pedidos. Nenhum pedido está sendo confirmado. Nenhum estoque está sendo baixado. O cliente está travado."

🖥️ **AÇÃO:** Abrir o arquivo `tickets/ticket-001.md` no VS Code. Projetar na tela.

---

🎙️ **FALA:**
> "Esse é o ticket. Leiam comigo."

🖥️ **AÇÃO:** Ler em voz alta o conteúdo do ticket, incluindo a nota do N1.

---

## BLOCO 2 — Apresentando o N1 (AnythingLLM)
⏱️ *10 minutos*

---

🎙️ **FALA:**
> "Antes de colocar a mão no código, eu preciso apresentar para vocês o N1. Ele é o primeiro ponto de contato com qualquer problema na TechCorp. Ele não inventa — ele responde com base nos documentos internos da empresa."

🖥️ **AÇÃO:** Abrir o AnythingLLM no navegador (`localhost:3001`). Mostrar o workspace `TechCorp Knowledge Base` já configurado.

---

🎙️ **FALA:**
> "Olha o que eu tenho aqui. Todos os runbooks, políticas de SLA, arquitetura do sistema — tudo indexado. Quando eu pergunto algo para o N1, ele busca a resposta nesses documentos. Vou demonstrar."

🖥️ **AÇÃO:** Digitar no chat do AnythingLLM:
```
O sistema de pedidos está falhando desde as 14h. Nenhum pedido está sendo confirmado. O que pode estar causando isso?
```

---

🖥️ **AÇÃO:** Aguardar a resposta. O N1 deve citar o `runbook/pedidos-falha.md` e indicar os passos de diagnóstico.

---

🎙️ **FALA:**
> "Vejam — ele não inventou nada. Ele citou exatamente o runbook interno da TechCorp. Essa é a diferença entre uma IA com RAG e um chatbot genérico. O N1 sabe o que a TechCorp sabe."

💡 *Se a resposta não citar o runbook, abra o AnythingLLM e mostre o documento indexado manualmente. Explique que a qualidade da resposta depende da qualidade dos documentos.*

---

## BLOCO 3 — Demo ao vivo com o Copilot
⏱️ *20 minutos*

---

🎙️ **FALA:**
> "Agora o N1 me deu o caminho. Ele disse que o problema provavelmente está na validação do pedido antes de salvar. Vou abrir o código e usar o Copilot para entender o que está acontecendo."

🖥️ **AÇÃO:** Abrir `src/api/pedidos.py` no VS Code.

---

🎙️ **FALA:**
> "Primeiro passo: entender. Não vou presumir que sei o que esse código faz. Vou selecionar a função inteira e pedir para o Copilot explicar."

🖥️ **AÇÃO:** Selecionar a função `processar_pedido`. Abrir Copilot Chat. Digitar:
```
/explain
```

---

🖥️ **AÇÃO:** Aguardar a explicação do Copilot. Ler em voz alta os pontos principais.

---

🎙️ **FALA:**
> "O Copilot me mostrou exatamente o que essa função faz. E olhem — ele já está me dizendo que existe um problema com o campo `quantidade`. Vamos confirmar."

🖥️ **AÇÃO:** No Copilot Chat, digitar:
```
/fix

Existe um problema quando o campo 'quantidade' vem como None. A função lança uma exceção não tratada. Corrija isso.
```

---

🖥️ **AÇÃO:** Aceitar a sugestão do Copilot. Mostrar o diff antes/depois lado a lado.

---

🎙️ **FALA:**
> "Perfeito. O Copilot identificou e corrigiu. Mas não vou confiar cegamente — vou pedir para ele gerar testes que cubram exatamente esse cenário."

🖥️ **AÇÃO:** Selecionar a função corrigida. No Copilot Chat, digitar:
```
/tests

Gere testes para cobrir os seguintes cenários:
- Pedido válido com quantidade preenchida
- Pedido com quantidade None
- Pedido com quantidade zero
```

---

🖥️ **AÇÃO:** Mostrar os testes gerados. Rodar os testes no terminal:
```bash
python -m pytest src/tests/ -v
```

---

🎙️ **FALA:**
> "Todos passando. Agora vou documentar a função para o próximo dev que pegar nesse código não ter o mesmo problema."

🖥️ **AÇÃO:** Selecionar a função. No Copilot Chat, digitar:
```
/doc

Inclua exemplos de uso e descreva os casos de erro possíveis.
```

---

🎙️ **FALA:**
> "Isso é o ciclo completo: entender → corrigir → testar → documentar. Quatro comandos. Menos de 10 minutos. E olhem — eu não escrevi uma linha de código manualmente. Eu dirigi. O Copilot executou."

---

🎙️ **FALA:**
> "Última coisa antes de passar para vocês: preciso fechar o ticket com a solução documentada."

🖥️ **AÇÃO:** Abrir `tickets/ticket-001.md`. Mostrar a seção de resolução. Preencher ao vivo com o resumo do fix.

---

## BLOCO 4 — Passagem para o desafio em duplas
⏱️ *5 minutos*

---

🎙️ **FALA:**
> "Agora é com vocês. Formem as duplas. Cada dupla vai trabalhar no próprio fork do repositório."

🖥️ **AÇÃO:** Mostrar o link do repositório no GitHub. Projetar o README com as instruções do desafio.

---

🎙️ **FALA:**
> "Vocês têm 1 hora e 20 minutos. O objetivo é simples: resolver o ticket-001, corrigir o bug, garantir que os testes passam e fechar o ticket com a solução documentada. Usem o N1 antes de abrir o código. Usem o Copilot para tudo — não quero ver ninguém digitando função na mão."

💡 *Distribuir os cenários conforme o público:*
- *🟢 Iniciantes: só `/explain` + `/fix`*
- *🟡 Padrão: fluxo completo*
- *🔴 Avançados: fix + refatorar o módulo inteiro*

---

🎙️ **FALA:**
> "Uma regra: se eu perguntar qual prompt você usou para gerar aquilo, você precisa saber responder. Se não sabe o prompt, você não aprendeu — o Copilot aprendeu por você."

---

## BLOCO 5 — Acompanhamento durante o desafio
⏱️ *1h20 minutos*

---

💡 **Durante o desafio — o que observar:**

| Momento | O que fazer |
|---|---|
| Primeiros 10min | Circular e verificar se todos conseguiram clonar/fazer fork |
| 20min | Checkpoint: quem já consultou o N1? Quem já abriu o código? |
| 40min | Checkpoint: quem já corrigiu o bug? Mostrar ao vivo 1 solução parcial |
| 60min | Aviso: 20 minutos restantes |
| 75min | Pedir para pararem e mostrarem o que têm |

---

💡 **Perguntas para fazer durante a circulação:**
- *"Qual prompt você usou no /explain?"*
- *"O que o N1 te disse antes de abrir o código?"*
- *"Por que o Copilot sugeriu essa correção específica?"*
- *"Seus testes cobrem o caso do `None`?"*

---

## BLOCO 6 — Encerramento e retrospectiva
⏱️ *5 minutos*

---

🎙️ **FALA:**
> "Vamos fechar. Alguém quer mostrar a solução que chegou?"

🖥️ **AÇÃO:** Pedir para uma dupla compartilhar a tela. Mostrar o diff e o ticket fechado.

---

🎙️ **FALA:**
> "O que aprendemos hoje: o Copilot não substitui o raciocínio — ele amplifica. O N1 deu o caminho, vocês dirigiram o Copilot, o Copilot executou. Essa é a divisão de trabalho da TechCorp. Na semana que vem, o problema vai ser mais fundo: o pipeline vai quebrar, e vocês vão precisar ir além do código."

---

🎙️ **FALA:**
> "Dúvidas antes de encerrar?"

💡 *Reservar 5 minutos para perguntas. Anotar dúvidas recorrentes para ajustar a próxima sessão.*

---

## Checklist pré-sessão (fazer antes da aula)

- [ ] Ollama rodando: `ollama serve`
- [ ] Modelo carregado: `ollama run llama3.2`
- [ ] AnythingLLM aberto em `localhost:3001` com workspace TechCorp configurado
- [ ] Pasta `/docs` indexada no AnythingLLM
- [ ] Repositório clonado e aberto no VS Code
- [ ] `ticket-001.md` aberto em aba separada
- [ ] Terminal aberto na raiz do projeto
- [ ] GitHub Copilot ativo (verificar ícone no VS Code)
- [ ] Pytest instalado: `pip install pytest`
