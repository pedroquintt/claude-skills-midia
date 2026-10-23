# Google Tag Manager e site

## URLs
- Home (lista de contas e contêineres): `https://tagmanager.google.com/?authuser=N#/home`. Os links dos contêineres trazem `accounts/<id>/containers/<id>`.
- Workspace: `#/container/accounts/A/containers/C/workspaces/W`. Abrir `.../workspaces` redireciona para o workspace padrão e revela o W.
- Listas: `.../workspaces/W/tags`, `/triggers`, `/variables`.
- Tag específica: `.../tags/<id>`. Os IDs saem de `[...document.querySelectorAll('a')].filter(a=>a.href.includes('/tags/'))`.
- Acionadores não têm href; abra pelo `find` e clique no link com o nome.
- Versões: `#/versions/accounts/A/containers/C`.
- Se o hash não abrir o painel, recarregue com um parâmetro novo: `?authuser=N&r=2#/...`.

## Ler a configuração de uma tag
```js
const t=document.body.innerText; const k='Configuração da tag'; const i=t.lastIndexOf(k);
t.slice(i+k.length).replace(/\n+/g,' | ').slice(0,900)
```
Para acionador, use `'Configuração do acionador'`. O código de tags HTML personalizadas costuma ser bloqueado pelo filtro de cookies; nesse caso, tire screenshot do editor.

## Checklist do contêiner
- **Filtro de hostname**: o mesmo contêiner roda em vários domínios (ex.: .com.br, .com.mx, .com)? Acionadores de conversão sem `Page Hostname` contaminam contas.
- **Tags de outras contas disparando no site errado** (ex.: tag Google da conta de outro país disparando em All Pages).
- **ID × rótulo** em cada tag de conversão do Ads: rode `scripts/decode_label.py`.
- **Dados fornecidos pelo usuário**: a variável combina com o formulário real? (ex.: variável montada para o formulário de uma plataforma aplicada ao formulário de outra, cujo campo de e-mail tem outro nome).
- **Acionadores que nunca disparam**: links de WhatsApp que a página não tem mais, URLs de página de agradecimento antigas, URLs com parâmetros de sessão fixos (ex.: `page view - profile` igual a uma URL com `sessionid`).
- **Duplicidade**: duas tags Google com o mesmo ID; tag de conversão disparada por dois acionadores para o mesmo evento.
- **Edições recentes de outra pessoa** ("há X minutos"): alguém pode estar trabalhando no contêiner. Não publique por cima sem perguntar.

## Inspeção do site (só leitura)
```js
JSON.stringify({
  ids: Object.keys(window.google_tag_manager||{}).filter(k=>/^(GTM|AW|G)-/.test(k)),
  forms: [...document.forms].map(f=>f.className.slice(0,30)+':'+[...f.elements].map(e=>e.name).filter(Boolean).slice(0,10).join(',')),
  wa: [...document.querySelectorAll('a')].filter(a=>/whatsapp|wa\.me/.test(a.href)).length,
  consent: (window.dataLayer||[]).filter(e=>e&&e[0]==='consent').length
})
```
Espere 6 a 8 segundos após navegar para o GTM carregar. Repare em contêineres legados (dois GTM na mesma página), Universal Analytics (desativado), vários pixels Meta e várias propriedades GA4.

## Fluxo de mudança
1. Crie acionadores novos em vez de editar os compartilhados.
   - Evento personalizado › nome do evento › "Alguns eventos personalizados" › `{{Page Hostname}}` contém `dominio`.
   - O campo de variável é um autocomplete: digite "Page Hostname" e clique na sugestão `{{Page Hostname}}`. Confira com zoom, porque ele já escolheu a variável errada uma vez.
2. Na tag: seção Acionamento › ícone de remover no acionador antigo › "+" › clique na linha do novo acionador.
3. Tag nova de conversão do Ads: Nova › Google Ads › Acompanhamento de conversões do Google Ads › Código de conversão + Rótulo. O painel recolhe ao validar o ID; reabra e confira o rótulo via JS.
4. Confira em "Visão geral" a lista de alterações pendentes.
5. Enviar › Publicar e criar versão › nome no estilo Conventional Commits › descrição com cada item › Publicar.
6. Anote o número e o horário da versão no relatório.
