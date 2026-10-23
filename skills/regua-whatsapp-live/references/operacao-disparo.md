# Operação na ferramenta de disparo: passo a passo testado

Escrito a partir da operação real numa ferramenta de automação de grupos de WhatsApp (DevZap), pelo navegador do usuário com a extensão Claude in Chrome. O navegador embutido do app não tem a sessão da ferramenta.

## Acesso

- Pode haver mais de um perfil do Chrome conectado. Se cair na tela de login, troque de perfil (`list_connected_browsers` → `select_browser`) antes de pedir ajuda.
- Ao entrar aparecem pop-ups ("Cadastre seu telefone", "Autenticação de dois fatores"): escolha "Fazer mais tarde" / "Agora não". Não aceite nem configure nada neles.
- Guarde em `config.md` as URLs diretas da campanha (mensagens, nova mensagem, disparos, agendamentos, novo agendamento). Se não abrirem, entre pelo card da campanha.

## Cadastrar mensagem

1. Abra "Nova mensagem". Espere ~6 s e tire um screenshot: **a primeira digitação logo após carregar costuma se perder.**
2. Clique no campo do título e digite. Clique no campo da mensagem e digite com `type` (as quebras de linha funcionam).
3. Confirme por JS antes de salvar:
   ```js
   const t=document.querySelector('textarea'); [document.querySelector('input').value, t.value.length, t.value.slice(0,40), t.value.slice(-45)]
   ```
   Se vier vazio, clique de novo nos campos e redigite (sem recarregar).
4. Não ligue "Mencionar todos", "Fixar mensagem" nem recursos de IA da ferramenta.
5. Salvar → no modal de sucesso escolha **Fazer depois** (não "Enviar agora" nem "Agendar" por ali).
6. Confira na lista que existe exatamente uma de cada (sem duplicatas).

## Enviar teste (só grupo de teste)

1. Ícone de enviar na linha da mensagem → "Selecione os grupos" → busque o grupo de teste → marque.
2. **Confirme o chip "1 de N selecionados" antes de "Enviar".** A altura do diálogo muda conforme o tamanho da mensagem, então as coordenadas mudam: screenshot a cada mensagem em vez de reaproveitar posições.
3. Repita em ordem M1 → M6. No histórico de disparos: N envios, todos entregues, **1 destino**.

## Agendar para os grupos da comunidade

Para cada mensagem M1–M5, uma por vez, recarregando "Novo agendamento" entre elas:

1. Espere ~6 s; marque o rádio de envio de mensagem ao grupo.
2. Use `find` para pegar as refs do item da mensagem, campos de data e horário, busca de grupos e botão Agendar.
3. Data: clique no **segmento do dia** e digite `DDMMAAAA`. Horário: clique no segmento da hora e digite `HHMM`. Confirme por JS:
   ```js
   [...document.querySelectorAll('input[type=date],input[type=time]')].map(i=>i.value)
   ```
4. Grupos: busque pelo prefixo e marque **"Selecione todos" clicando por coordenada** no checkbox visível. Clicar pela ref do input escondido **não marca nada**.
5. Limpe a busca e verifique a lista inteira:
   ```js
   const r=[...document.querySelectorAll('input[type=checkbox]')].map(c=>{let el=c;for(let i=0;i<6&&el;i++){el=el.parentElement;const t=el&&el.textContent.trim();if(t&&t.length<60)return[t,c.checked];}return['?',c.checked];});
   [r.filter(x=>x[1]).length, r.filter(x=>x[1]&&!x[0].includes(PREFIXO))]
   ```
   Esperado: contagem = nº de grupos da comunidade; segunda lista vazia.
6. Zoom na área para conferência visual e **Agendar**. Confira na lista de agendamentos (outra aba) antes de seguir. Nunca clique em "Agendar" duas vezes sem conferir.

## Conferência final

Lista de agendamentos filtrada por envio de mensagem: 5 itens programados com as datas certas. Cada um tem "Cancelar" e "Ver detalhes" para correção.
