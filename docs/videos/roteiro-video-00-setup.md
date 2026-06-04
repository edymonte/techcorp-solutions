# Roteiro — Vídeo 0: Setup do Ambiente
**Duração estimada:** 3–4 minutos  
**Objetivo:** Mostrar o clone do repositório, execução do setup e validação do ambiente  
**Janelas abertas antes de gravar:** Explorer do Windows, terminal

---

## CENA 1 — Introdução (0:00–0:20)

**[TELA: fundo neutro ou logo TechCorp]**

**NARRAÇÃO:**
> "Antes de começar o workshop, você vai preparar o seu ambiente em menos de 3 minutos.
> Você vai precisar de: Python 3.11 ou superior, Node.js LTS, Git e o VS Code com o GitHub Copilot ativo.
> Se você ainda não tem essas ferramentas, consulte o README do projeto — tem o link de cada uma.
> Vamos lá."

---

## CENA 2 — Clone do repositório (0:20–0:50)

**[TELA: terminal aberto na pasta de trabalho]**

**AÇÃO:** Digitar ao vivo:
```bash
git clone https://github.com/edymonte/techcorp-solutions.git
cd techcorp-solutions
```

**NARRAÇÃO:**
> "Clone o repositório com o Git. Você vai trabalhar dentro da pasta techcorp-solutions durante todo o workshop.
> Depois de clonar, abra o VS Code nessa pasta."

**AÇÃO:** Digitar:
```bash
code .
```

**NARRAÇÃO:**
> "O VS Code vai abrir e provavelmente vai pedir para você instalar as extensões recomendadas.
> Aceite — elas já estão configuradas para o workshop."

---

## CENA 3 — Executando o setup (0:50–1:40)

**[TELA: VS Code aberto, Explorer lateral mostrando a estrutura do projeto]**

**NARRAÇÃO:**
> "Agora localize o arquivo setup.bat na raiz do projeto e dê um duplo clique nele.
> Ele vai instalar as dependências Python, criar o banco de dados e verificar o ambiente — tudo automaticamente."

**AÇÃO:** Mostrar o setup.bat sendo executado. Mostrar a saída no terminal.

**NARRAÇÃO:**
> "Aguarde. O processo leva menos de um minuto na maioria das máquinas."

**[TELA: saída do terminal com as verificações aparecendo]**

**NARRAÇÃO:**
> "Você vai ver cada verificação aparecendo em sequência — Python, dependências, banco de dados, Node.js."

---

## CENA 4 — Validando o resultado (1:40–2:40)

**[TELA: saída final do verificar_ambiente.py]**

**NARRAÇÃO:**
> "No final, o verificador mostra o resumo. Você precisa ver: 9 verificações com ✔, zero erros.
> Os 3 avisos com ⚠ são esperados — são os bugs intencionais do desafio. Eles estão lá de propósito."

**AÇÃO:** Destacar na tela:
```
✔ 9 ok   ✘ 0 erro(s)   ⚠ 3 aviso(s)
Ambiente pronto para o workshop!
```

**NARRAÇÃO:**
> "Se aparecer qualquer ✘ vermelho — não avance. Chame o facilitador ou consulte o arquivo setup/SETUP.md.
> Se tudo está verde, você está pronto."

---

## CENA 5 — Estrutura do projeto (2:40–3:20)

**[TELA: VS Code, Explorer mostrando as pastas]**

**NARRAÇÃO:**
> "Antes de começar o desafio, conheça os três arquivos que você vai usar em todas as etapas.
> Primeiro: a pasta tickets — aqui estão os chamados que você vai resolver.
> Segundo: a pasta .github/prompts — aqui estão os templates de prompt que você vai usar como base.
> Terceiro: o guia do participante em docs/participante — esse é o seu mapa para não se perder."

**AÇÃO:** Abrir cada pasta no Explorer e mostrar brevemente os arquivos.

---

## CENA 6 — Encerramento (3:20–3:40)

**[TELA: VS Code com o README aberto]**

**NARRAÇÃO:**
> "Ambiente pronto. No próximo vídeo, começa o desafio real — você vai receber um chamado P1 de um cliente VIP
> e terá que usar o GitHub Copilot para diagnosticar e corrigir o problema antes que o SLA expire.
> Boa sorte."

---

## Checklist de gravação

```
[ ] Resolução: 1920x1080
[ ] Fonte do VS Code: tamanho 16 ou maior (Ctrl+= para aumentar)
[ ] Tema escuro ativado (ex: GitHub Dark)
[ ] Terminal com fonte monoespaçada visível
[ ] Notificações do Windows desativadas
[ ] GitHub Copilot ativo (ícone no canto inferior direito do VS Code)
[ ] Janelas desnecessárias fechadas
[ ] Gravação começa ANTES de digitar o primeiro comando
```
