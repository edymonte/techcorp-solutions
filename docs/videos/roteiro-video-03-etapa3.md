# Roteiro — Vídeo 3: Etapa 3 — "Tudo caiu ao mesmo tempo"
**Duração estimada:** 10–12 minutos  
**Objetivo:** Mostrar o Agent Mode, MCP SQLite, triagem de múltiplos incidentes e resposta coordenada  
**Janelas abertas antes de gravar:** VS Code com Copilot Chat no modo Agent, terminal integrado

---

## CENA 1 — Introdução e cenário de crise (0:00–0:50)

**[TELA: VS Code, nenhum arquivo aberto. Relógio do sistema visível no canto.]**

**NARRAÇÃO:**
> "Etapa 3. São 17h03 de uma sexta-feira.
> Três chamados P1 abriram nos últimos 15 minutos — ao mesmo tempo.
> Sub-incidente A: autenticação fora do ar. Tokens expirados sendo aceitos como válidos.
> Sub-incidente B: pipeline de produção bloqueado de novo. Erro diferente dessa vez.
> Sub-incidente C: a Farmácia Boa Saúde e a Rede Saúde+ — dois clientes VIP — sem acesso ao painel.
> Impacto financeiro estimado: R$ 12.000 por hora.
> Você tem 2 horas de SLA. E não pode errar na ordem."

---

## CENA 2 — Ativando o Agent Mode (0:50–1:30)

**[TELA: Copilot Chat, mostrando o seletor de modo]**

**NARRAÇÃO:**
> "Essa etapa usa o Agent Mode — o modo mais avançado do GitHub Copilot.
> No modo normal, você pede uma coisa por vez. No Agent Mode, você descreve um objetivo
> e o Copilot planeja, lê arquivos, executa ações e reporta o que fez.
> Mas atenção: você revisa e aprova cada passo. Nunca aceite cegamente."

**AÇÃO:** Mostrar a ativação do Agent Mode no seletor de modo do Copilot Chat.

---

## CENA 3 — Consultando o banco via MCP SQLite (1:30–2:30)

**[TELA: Copilot Chat no modo Agent]**

**NARRAÇÃO:**
> "Primeira ação: entender o estado atual dos chamados. Na TechCorp, os tickets ficam no banco SQLite.
> Com o MCP configurado, o Copilot se conecta direto ao banco — sem abrir nenhuma ferramenta separada."

**AÇÃO:** Digitar no Agent Chat:
```
Use o MCP do SQLite para listar todos os chamados abertos em db/techcorp.db,
ordenados por prioridade. Mostre: ID, título, prioridade e status.
```

**[TELA: resposta do Copilot mostrando os 3 chamados]**

**NARRAÇÃO:**
> "Três chamados. O banco respondeu direto no chat — sem SQL manual, sem trocar de janela.
> Esse é o MCP: o Copilot conectado a ferramentas reais."

---

## CENA 4 — Montando o prompt de incidente múltiplo (2:30–4:00)

**[TELA: abrir .github/prompts/resposta-incidente-multiplo.prompt.md]**

**NARRAÇÃO:**
> "A TechCorp tem um template específico para incidentes múltiplos.
> Ele já exige triagem, priorização e restrições de segurança — tudo definido antes do Copilot agir."

**AÇÃO:** Mostrar a estrutura do template brevemente.

**[TELA: Copilot Chat, novo prompt]**

**NARRAÇÃO:**
> "Agora monto o prompt com os três sub-incidentes e as restrições críticas."

**AÇÃO:** Digitar o prompt ao vivo:
```
#file:docs/runbooks/auth-reset.md
#file:src/auth/auth_service.py
#file:requirements.txt

Sub-incidente A: autenticação JWT — tokens expirados aceitos como válidos
Sub-incidente B: pipeline bloqueado — ModuleNotFoundError: No module named 'jwt'
Sub-incidente C: cliente VIP CLI-001 sem acesso ao painel

Faça a triagem dos 3 sub-incidentes em ordem de prioridade.
Para cada um: causa raiz, arquivo, linha, fix mínimo em diff, teste de validação.

Restrições:
- Fixes de segurança têm prioridade absoluta
- NÃO rotacione SECRET_KEY sem avisar explicitamente
- Não feche um sub-incidente sem teste que previne regressão
- Clientes CLI-001 e CLI-012 têm SLA de 2h — sinalize se estiver em risco
```

**NARRAÇÃO:**
> "Duas restrições críticas aqui. Primeira: segurança tem prioridade absoluta.
> Segunda: não rotacionar a SECRET_KEY sem aviso — isso deslogaria todos os usuários simultaneamente."

---

## CENA 5 — Analisando a triagem do Copilot (4:00–5:00)

**[TELA: resposta do Copilot com a tabela de triagem]**

**NARRAÇÃO:**
> "Veja a tabela de triagem. O Copilot propôs a ordem correta: auth primeiro, pipeline segundo, acesso terceiro.
> E sinalizou que o SLA do CLI-001 está em risco — exatamente o que pedimos nas restrições.
> Sempre verifique se a ordem de prioridade faz sentido antes de avançar.
> Nesse caso faz — vulnerabilidade de segurança antes de qualquer outra coisa."

---

## CENA 6 — Sub-incidente A: corrigindo o auth (5:00–7:00)

**[TELA: src/auth/auth_service.py aberto]**

**NARRAÇÃO:**
> "Sub-incidente A. O Copilot identificou a linha exata: options com verify_exp igual a False.
> Isso desabilita a verificação de expiração do JWT — tokens de ontem, de semana passada,
> de qualquer data são aceitos como válidos. É uma vulnerabilidade de segurança crítica."

**AÇÃO:** Mostrar o código com o bug destacado:
```python
options={"verify_exp": False}
```

**NARRAÇÃO:**
> "O fix é simples: remover essa opção. Sem ela, o PyJWT valida a expiração automaticamente."

**AÇÃO:** Aplicar o fix mostrando o antes e depois.

**[TELA: terminal]**

**AÇÃO:** Digitar:
```bash
pytest tests/test_auth.py -v
```

**NARRAÇÃO:**
> "Rodamos os testes de autenticação. Os dois que estavam falhando — token expirado deve ser rejeitado
> e token expirado não pode obter perfil — agora passam. Sub-incidente A e C: resolvidos."

---

## CENA 7 — Sub-incidente B: corrigindo o requirements (7:00–7:50)

**[TELA: requirements.txt aberto]**

**NARRAÇÃO:**
> "Sub-incidente B. O pipeline está falhando porque pyjwt não está declarado no requirements.txt.
> O auth_service.py importa jwt, mas nunca foi commitado no arquivo de dependências."

**AÇÃO:** Mostrar o requirements.txt e confirmar que `pyjwt==2.8.0` já está presente.

**NARRAÇÃO:**
> "Neste caso o arquivo já contém a dependência — a falha era no ci.yml do incidente anterior.
> O sub-incidente B é resolvido como parte da correção do pipeline da Etapa 2.
> Se ainda não estivesse no arquivo, seria apenas adicionar uma linha."

---

## CENA 8 — Atualizando o banco via MCP (7:50–8:40)

**[TELA: Copilot Chat no modo Agent]**

**NARRAÇÃO:**
> "Com os três sub-incidentes resolvidos, atualizamos o banco de chamados."

**AÇÃO:** Digitar:
```
Use o MCP do SQLite para atualizar o status dos 3 chamados
em db/techcorp.db para 'resolvido'.
Mostre o SQL que vai executar antes de aplicar.
```

**NARRAÇÃO:**
> "Note que pedi para mostrar o SQL antes de executar. Sempre revise o que o Agent Mode
> vai fazer antes de confirmar. Aqui está o SELECT de verificação antes do UPDATE."

**AÇÃO:** Mostrar a resposta com o SQL e confirmar a execução.

---

## CENA 9 — Atualizando o copilot-instructions (8:40–9:30)

**[TELA: Copilot Chat]**

**NARRAÇÃO:**
> "Parte do processo de pós-incidente é atualizar as instruções do Copilot para prevenir recorrência.
> Pedimos ao Agent para sugerir as regras."

**AÇÃO:** Digitar:
```
Com base nos 3 problemas que resolvemos hoje, sugira uma regra para adicionar
em .github/copilot-instructions.md que previna regressão de cada um.
```

**NARRAÇÃO:**
> "O Copilot sugere três regras: nunca usar verify_exp False em JWT, nunca instalar módulos internos via pip,
> e sempre declarar dependências no requirements.txt antes de importar.
> Revisar e aplicar essas regras fecha o ciclo do incidente."

---

## CENA 10 — Validação final e evidência (9:30–10:30)

**[TELA: terminal]**

**AÇÃO:** Digitar:
```bash
pytest tests/ -v
python setup/verificar_ambiente.py
```

**NARRAÇÃO:**
> "Validação final completa. 39 testes passando. Zero erros. 9 verificações verdes.
> As 3 falhas intencionais do início do workshop agora passam — o desafio está completo."

**AÇÃO:** Mostrar o resultado:
```
39 passed
✔ 9 ok   ✘ 0 erro(s)   ⚠ 0 aviso(s)
```

**AÇÃO:** Digitar:
```bash
python setup/gerar_evidencia.py --semana 3 --nome "Participante" --parceiro "Parceiro"
```

**NARRAÇÃO:**
> "Evidência gerada. As três etapas do workshop concluídas.
> Você usou Copilot Chat, @workspace, #file, Agent Mode e MCP — as ferramentas mais avançadas disponíveis.
> E o mais importante: você aprendeu que a qualidade do resultado depende da qualidade do prompt."

---

## CENA 11 — Encerramento (10:30–11:00)

**[TELA: fundo neutro ou logo TechCorp]**

**NARRAÇÃO:**
> "O GitHub Copilot não é um oráculo. Ele é um par de programação.
> Como qualquer par, ele precisa de contexto para dar boas respostas.
> Papel, contexto, tarefa, restrições e formato — esses são os cinco elementos que fazem a diferença.
> Bom workshop."

---

## Checklist de gravação

```
[ ] Agent Mode ativado e visível ANTES de começar a gravar a Cena 2
[ ] MCP SQLite configurado e testado — confirmar antes de gravar
[ ] Mostrar explicitamente o seletor de modo ao mudar para Agent Mode
[ ] Pausa de 4–5 segundos quando o Agent Mode processar — deixar a ação aparecer
[ ] Mostrar o SQL ANTES de confirmar a execução do MCP (momento pedagógico importante)
[ ] pytest rodando em tela cheia com resultado visível — não cortar antes do "passed"
[ ] Encerramento gravado por último — com a calma de quem já terminou
```
