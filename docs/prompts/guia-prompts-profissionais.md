# Guia de Prompts Profissionais — TechCorp Workshop

> O GitHub Copilot é tão bom quanto o prompt que você escreve.  
> Este guia mostra como passar de respostas genéricas para respostas que você pode usar direto.

---

## Por que seu prompt atual provavelmente está fraco

A maioria das pessoas usa o Copilot como um buscador:

> *"o que faz essa função?"*  
> *"tem bug aqui?"*  
> *"como faço para corrigir isso?"*

Essas perguntas funcionam — mas geram respostas genéricas que exigem que **você** faça todo o trabalho de adaptação. Um prompt profissional transfere esse trabalho para o Copilot.

---

## A Anatomia de um Prompt Profissional

Todo prompt eficaz tem até cinco elementos. Não é obrigatório usar todos — mas quanto mais relevantes você incluir, melhor a resposta.

```
[PAPEL]     Quem o Copilot deve ser nesta resposta
[CONTEXTO]  O que ele precisa saber sobre o sistema/empresa
[TAREFA]    O que você quer que ele faça (uma coisa só)
[RESTRIÇÕES] O que ele não pode fazer ou deve respeitar
[FORMATO]   Como a resposta deve ser estruturada
```

---

## Comparações lado a lado — cenários reais da TechCorp

### Cenário 1 — Investigar o bug do Ticket-001 (Semana 2)

**Prompt fraco:**
```
tem bug na função validar_pedido?
```

**O que você recebe:** uma explicação genérica de como a função funciona.

---

**Prompt profissional:**
```
Você é um desenvolvedor Python sênior revisando o código da TechCorp Solutions,
um ERP de pedidos para farmácias.

Analise a função `validar_pedido()` em `src/api/pedidos.py`.

O Ticket-001 relata que pedidos com `quantidade = None` travam o sistema com
um TypeError, mas a função deveria lançar `PedidoInvalidoError`.

Identifique:
1. A linha exata onde o TypeError ocorre e por quê
2. A correção mínima que resolve o problema sem alterar o comportamento atual
3. Um teste pytest para o caso `quantidade = None`

Restrições:
- Não altere a assinatura da função
- Siga o padrão do arquivo `.github/copilot-instructions.md`
- O teste deve ficar em `tests/test_pedidos.py`
```

**O que você recebe:** diagnóstico preciso + código pronto para revisar e usar.

---

### Cenário 2 — Investigar falha no pipeline (Semana 3)

**Prompt fraco:**
```
o pipeline tá quebrando, o que pode ser?
```

---

**Prompt profissional:**
```
Você é um engenheiro de plataforma da TechCorp Solutions.

O GitHub Actions falhou no step "Install dependencies" com este erro:
  ERROR: No matching distribution found for techcorp_core

O padrão da empresa (documentado em `docs/pipelines/padrao-ci.md`) proíbe
importar módulos internos como pacotes externos.

Faça:
1. Identifique qual arquivo e qual linha contém o import problemático
2. Mostre o import correto usando caminho relativo
3. Verifique se há outros imports que violam o mesmo padrão em `src/`

Formato: liste cada problema encontrado como `arquivo:linha → correção`.
```

---

### Cenário 3 — Corrigir vulnerabilidade de autenticação (Semana 4)

**Prompt fraco:**
```
como funciona o JWT aqui?
```

---

**Prompt profissional:**
```
Você é um especialista em segurança revisando o serviço de autenticação
da TechCorp Solutions (`src/auth/auth_service.py`).

O Ticket-003 relata que tokens expirados ainda são aceitos pelo sistema,
causando acesso indevido a clientes VIP.

Analise a função `validar_token()` e responda:
1. Qual opção está desabilitando a verificação de expiração?
2. Qual é o risco de segurança exato (OWASP categoria)?
3. Mostre a correção com diff — apenas as linhas que mudam
4. Que teste deve ser adicionado para garantir que tokens expirados
   sejam rejeitados a partir de agora?

Não explique como JWT funciona — assuma que já sei.
Seja direto: diagnóstico → fix → teste.
```

---

## Os 5 erros mais comuns

| Erro | Exemplo ruim | Como corrigir |
|------|-------------|---------------|
| **Sem contexto** | "tem bug aqui?" | Informe o sistema, o módulo, o sintoma |
| **Tarefa vaga** | "melhore isso" | Uma tarefa específica por prompt |
| **Sem restrições** | (sem mencionar nada) | Diga o que ele NÃO deve mudar |
| **Sem formato** | (sem pedir formato) | Peça diff, lista numerada, bloco de código |
| **Pergunta aberta demais** | "como funciona autenticação?" | Foque no problema específico que você quer resolver |

---

## Progressão de ferramentas do Copilot

Use a ferramenta certa para cada situação:

| Situação | Ferramenta | Exemplo |
|----------|-----------|---------|
| Corrigir uma linha de código | **Inline** (`Ctrl+I`) | "adiciona verificação de None antes da comparação" |
| Investigar um bug | **Chat** (`Ctrl+Shift+I`) | Prompt completo com contexto e tarefa |
| Explorar todo o repositório | **@workspace** | "quais funções não validam None antes de comparar?" |
| Tarefa recorrente (ex: fechar ticket) | **Prompt salvo** (`.github/prompts/`) | Reutilize sem reescrever |
| Incidente com múltiplos arquivos | **Agent Mode** | Deixe o agente investigar, editar e testar |

---

## Checklist rápido antes de enviar um prompt

```
[ ] Defini o papel do Copilot?
[ ] Dei o contexto mínimo necessário (sistema, módulo, sintoma)?
[ ] A tarefa é específica e única?
[ ] Listei o que ele não deve mudar?
[ ] Pedi o formato que quero (diff, lista, código, explicação)?
[ ] Removi o que é óbvio / o que ele já sabe pelo contexto do arquivo?
```

Se você marcou 4 ou mais, o prompt está bom. Se marcou menos de 3, reescreva.

---

## Exercício prático — Escreva antes de rodar

Antes de enviar um prompt para o Copilot, escreva à mão:

1. **Qual é o papel?**
2. **O que o Copilot precisa saber que ele não vê na tela?**
3. **O que exatamente você quer como saída?**

Depois compare a resposta que você imaginou com a que o Copilot deu.  
Se forem muito diferentes — o problema está no prompt, não no Copilot.

---

## Referência rápida — Template

Copie e adapte conforme a situação:

```
Você é [papel] na TechCorp Solutions.

Contexto: [descrição do sistema/situação em 1-3 frases]

Tarefa: [o que você quer — uma coisa só]

Restrições:
- [o que não pode mudar]
- [padrão que deve seguir]

Formato esperado: [diff / lista numerada / bloco pytest / explicação em 3 parágrafos]
```
