# Roteiro — Vídeo 2: Etapa 2 — "O pipeline quebrou"
**Duração estimada:** 8–10 minutos  
**Objetivo:** Mostrar como diagnosticar uma falha de CI usando @workspace, #file e o template de pipeline  
**Janelas abertas antes de gravar:** VS Code com o projeto aberto, terminal integrado

---

## CENA 1 — Introdução e contexto (0:00–0:40)

**[TELA: VS Code, nenhum arquivo aberto]**

**NARRAÇÃO:**
> "Etapa 2. Você deixou o papel de suporte e entrou no time de desenvolvimento da TechCorp.
> São 9h47 de uma segunda-feira. Um PR foi aprovado e mergeado na main há sete minutos.
> O GitHub Actions disparou automaticamente — e está vermelho.
> Ninguém consegue fazer deploy. O time inteiro está bloqueado."

---

## CENA 2 — Lendo o ticket (0:40–1:30)

**[TELA: abrir tickets/ticket-002.md]**

**AÇÃO:** Abrir o arquivo e rolar pela tela.

**NARRAÇÃO:**
> "Regra da TechCorp: antes de abrir qualquer arquivo, leia o ticket.
> Veja o log do Actions — o erro está claro: 'No matching distribution found for techcorp_core'.
> O PR suspeito é o número 14, do dev-carlos: 'feat: adicionar validação de estoque no processador'.
> O N1 já consultou o runbook de pipeline e aponta que o problema está no requirements.txt ou no workflow."

**AÇÃO:** Destacar o trecho do log de erro e a seção do N1.

---

## CENA 3 — Usando @workspace para mapear o impacto (1:30–2:30)

**[TELA: Copilot Chat aberto]**

**NARRAÇÃO:**
> "Antes de mexer em qualquer arquivo, precisamos entender o escopo do problema.
> O @workspace é um recurso do Copilot que analisa o projeto inteiro — não só o arquivo aberto.
> Vou usar ele para mapear onde esse pacote problemático aparece."

**AÇÃO:** Digitar no Copilot Chat:
```
@workspace Onde o pacote techcorp_core é referenciado no projeto?
Liste todos os arquivos e linhas.
```

**NARRAÇÃO:**
> "Aguarde. O Copilot está lendo o projeto inteiro."

**[TELA: resposta do Copilot listando os arquivos]**

**NARRAÇÃO:**
> "Em segundos ele mapeou onde o problema aparece — sem eu precisar fazer Ctrl+F em cada arquivo.
> Agora sabemos exatamente onde olhar."

---

## CENA 4 — Abrindo o template de prompt de pipeline (2:30–3:10)

**[TELA: abrir .github/prompts/corrigir-pipeline.prompt.md]**

**NARRAÇÃO:**
> "A TechCorp tem um template específico para problemas de pipeline.
> Abra o arquivo corrigir-pipeline.prompt.md. Veja que ele já pede o log do Actions,
> o PR suspeito, e exige conformidade com o padrão de CI documentado."

**AÇÃO:** Rolar pelo arquivo mostrando a estrutura.

---

## CENA 5 — Montando o prompt com #file (3:10–4:30)

**[TELA: Copilot Chat, novo chat]**

**NARRAÇÃO:**
> "Agora o #file. Diferente do @workspace que lê tudo, o #file direciona o Copilot
> para arquivos específicos. Vou usar os dois arquivos mais relevantes."

**AÇÃO:** Digitar o prompt ao vivo:
```
#file:.github/workflows/ci.yml #file:docs/pipelines/padrao-ci.md

Log de erro do Actions:
ERROR: Could not find a version that satisfies the requirement techcorp_core
ERROR: No matching distribution found for techcorp_core
[exit code 1]

PR suspeito: #14 — "feat: adicionar validação de estoque no processador"
Autor: dev-carlos

1. Identifique o step com falha e a causa raiz em uma frase
2. Localize o problema no arquivo ci.yml com a linha exata
3. Mostre o fix em formato diff
4. Verifique conformidade com docs/pipelines/padrao-ci.md
5. Gere o comentário de diagnóstico para o PR no formato do template
```

**NARRAÇÃO:**
> "Note que colei o log de erro diretamente no prompt — o Copilot precisa do contexto real,
> não de uma descrição vaga do problema."

---

## CENA 6 — Analisando a resposta (4:30–5:30)

**[TELA: resposta do Copilot]**

**NARRAÇÃO:**
> "Veja o que o Copilot entregou: identificou a linha exata no ci.yml, explicou a causa raiz,
> mostrou o diff e verificou se o fix está alinhado com o padrão de CI da empresa.
> Também gerou o comentário para o PR — que vou usar a seguir."

**AÇÃO:** Rolar pela resposta lentamente, destacando cada ponto.

**NARRAÇÃO:**
> "Um ponto importante: o problema NÃO está no requirements.txt — está no ci.yml.
> Alguém adicionou um comando pip install direto no workflow para um pacote interno que não existe externamente.
> Isso viola o padrão documentado em docs/pipelines/padrao-ci.md."

---

## CENA 7 — Aplicando o fix no ci.yml (5:30–6:30)

**[TELA: abrir .github/workflows/ci.yml]**

**NARRAÇÃO:**
> "Abra o ci.yml e aplique o diff. Veja o que está sendo removido."

**AÇÃO:** Mostrar a linha problemática antes de remover.

```yaml
# BUG INTENCIONAL
pip install techcorp_core
```

**NARRAÇÃO:**
> "Essa linha não deveria estar aqui. Módulos internos do projeto não se instalam via pip —
> eles são importados pelo caminho relativo dentro do código.
> Remover essa linha é o fix completo."

**AÇÃO:** Fazer a edição e salvar o arquivo.

---

## CENA 8 — Validando localmente (6:30–7:10)

**[TELA: terminal]**

**AÇÃO:** Digitar:
```bash
pytest tests/ --tb=no -q
```

**NARRAÇÃO:**
> "Mesmo sem ter acesso ao Actions agora, rodamos os testes localmente para garantir
> que o fix não quebrou nada. O resultado deve ser as mesmas 3 falhas intencionais — nenhuma nova."

**AÇÃO:** Mostrar a saída confirmando.

---

## CENA 9 — Gerando o comentário do PR e a evidência (7:10–8:30)

**[TELA: Copilot Chat]**

**NARRAÇÃO:**
> "Antes de fechar, geramos o comentário de diagnóstico para o PR — parte do processo da TechCorp."

**AÇÃO:** Mostrar o texto gerado pelo Copilot no formato:
```
## Diagnóstico — TICKET-002
**Causa:** ...
**Arquivo:** ...
**Fix:** ...
**Teste local:** ...
```

**[TELA: terminal]**

**AÇÃO:** Digitar:
```bash
python setup/gerar_evidencia.py --semana 2 --nome "Participante" --parceiro "Parceiro"
```

**NARRAÇÃO:**
> "Evidência gerada. Pipeline corrigido. PR documentado.
> No próximo vídeo — tudo cai ao mesmo tempo. Três incidentes P1 simultâneos, numa sexta à tarde."

---

## Checklist de gravação

```
[ ] Copilot Chat em painel lateral (não em janela flutuante)
[ ] @workspace digitado devagar — é um recurso novo para muitos espectadores
[ ] Mostrar o ci.yml ANTES e DEPOIS do fix lado a lado se possível
[ ] Pausa de 3 segundos após cada resposta do Copilot antes de continuar narrando
[ ] Terminal mostra zero falhas inesperadas antes de cortar
```
