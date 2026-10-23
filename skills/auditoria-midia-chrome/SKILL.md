---
name: auditoria-midia-chrome
description: Audita e otimiza contas de mídia paga (Google Ads, Google Tag Manager, GA4, Meta Ads/Events Manager) operando direto no Google Chrome do usuário pela extensão Claude in Chrome. Use SEMPRE que o usuário pedir para "entrar", "olhar", "auditar", "otimizar", "mexer" ou "conferir conversões" em campanhas de um cliente pelo navegador, quando mencionar tag manager, GTM, conversões que não batem, pixel, CAPI, Events Manager, contas de anúncio de clientes, ou quando pedir para aplicar ajustes em campanhas, tags ou metas de conversão diretamente nas plataformas, mesmo que não diga "Chrome".
---

# Gestão de mídia via Chrome

Esta skill opera as interfaces web das plataformas de anúncio no Chrome real do usuário, com as sessões dele já logadas. O trabalho tem duas fases, sempre nesta ordem:

1. **Auditoria só de leitura**: mapear contas, campanhas, conversões e tags, e cruzar tudo.
2. **Mudanças com aprovação**: relatório do que será feito, OK explícito do usuário, aplicação e relatório final com o status de cada item.

O motivo da ordem: mudanças em tags e campanhas mexem em dinheiro e dados de cliente, e um erro de tag passa dias sem ninguém notar. Ler primeiro custa pouco, e o relatório deixa o usuário decidir com os números na mão.

## 1. Conectar ao navegador certo

O usuário pode ter mais de um Chrome ou perfil aberto (ex.: um perfil da empresa e um pessoal, onde ficam as contas de clientes). Errar o navegador faz a busca pelas contas falhar e irrita o usuário.

1. Carregue as ferramentas do Chrome numa única ToolSearch: `tabs_context_mcp, navigate, computer, read_page, find, get_page_text, javascript_tool, tabs_create_mcp, tabs_close_mcp, browser_batch, list_connected_browsers, select_browser, switch_browser`.
2. Rode `list_connected_browsers`. Se houver mais de um, pergunte qual usar, ou escolha pelo que o usuário disse. Se só houver um e as contas não aparecerem nele, explique como conectar o outro: instalar a extensão Claude naquele perfil, logar com **a mesma conta Claude deste app** (pergunte qual é; não presuma pelo e-mail da sessão) e clicar em Connect. Depois chame `switch_browser`.
3. Crie a própria aba (`tabs_context_mcp` com `createIfEmpty`) e não mexa nas abas do usuário.
4. **Contas Google ficam em `authuser=N`.** Varra `authuser=0` até cerca de 8 em `https://ads.google.com/nav/selectaccount?authuser=N` e `https://tagmanager.google.com/?authuser=N#/home`. Um URL que o usuário colar (ou um print dele) já revela o índice certo. Consulte `references/contas.md` antes de varrer: o índice pode já estar registrado.

## 2. Técnicas de leitura que funcionam

- **`get_page_text` falha no Google Ads** (pega só o banner). Use `javascript_tool` com `document.body.innerText`, fatiado a partir de um marcador (`t.indexOf('Campanha\n')`).
- **A saída do javascript_tool trunca em cerca de 1.000 caracteres.** Guarde o resultado em `window.__T` e leia em fatias (`__T.slice(0,950)`, `__T.slice(950,1900)`...).
- **Tabelas do Ads são virtualizadas.** Leia linhas com `document.querySelectorAll('[role="row"], tr')`, ordene a coluna Custo para trazer o que gastou ao topo e aumente "Mostrar linhas" para 100.
- **Respostas com cookies ou query strings são bloqueadas** pelo filtro da ferramenta (ex.: ler `location.href` cheio, ou código de tag HTML com cookies). Extraia só o necessário com regex (`location.href.match(/ctId=\d+/)`) ou use screenshot.
- **Painéis do GTM empilham.** Se a URL de uma tag/acionador não abrir, recarregue com um parâmetro novo (`?authuser=6&r=7#/container/...`).
- Prefira `browser_batch` para sequências previsíveis (navegar → esperar → extrair).
- Os detalhes de URL e navegação por plataforma estão nas referências:
  - Google Ads: `references/google-ads.md`
  - Google Tag Manager e site: `references/gtm.md`
  - Meta Ads / Events Manager: `references/meta-ads.md`

## 3. Checklist de auditoria

Rode na ordem. Cada item tem o porquê e o como na referência da plataforma.

1. **Mapa de contas**: MCC, subcontas, gasto nos últimos 30 dias. Identifique a conta ativa de verdade; nomes enganam (pode haver uma conta antiga parada com nome quase igual ao da conta ativa sob o MCC).
2. **Campanhas**: status, orçamento, estratégia de lance, cliques, conversões, CPA, IS perdida por orçamento e por classificação. Remova filtros de visualização só para ler, e avise que mexeu na visualização.
3. **Ações de conversão**: status (pendente, incorreta, requer atenção), **data da última conversão** (abra cada ação), principal ou secundária, contagem, janela e se entram nas metas da conta.
4. **Segmentar campanhas por "Ação de conversão"** e cruzar com o relatório de **páginas de destino**. Isso revela conversões de um país ou domínio caindo na ação de outro.
5. **GTM**: liste tags, acionadores e variáveis. Abra cada tag de conversão e anote ID, rótulo, acionador e variável de dados do usuário.
6. **Decodifique os rótulos** com `python3 scripts/decode_label.py <rotulo> <id_da_tag>`. O rótulo carrega o código do tipo de conversão (ctId) e a conta AW de origem. Um ID diferente do embutido no rótulo significa que a conversão não registra.
7. **Site/landing**: abra a URL final dos anúncios e liste os contêineres e IDs carregados (`Object.keys(google_tag_manager)`), os formulários (plataforma e nomes dos campos), os links de WhatsApp, o consent mode (`dataLayer` com `consent`) e os pixels Meta.
8. **Termos de pesquisa**: marca em campanha não-marca, concorrentes e termos irrelevantes.

## 4. Relatório antes de mudar

Publique o relatório como Artifact (carregue a skill `artifact-design` antes). Estrutura:

- **Resumo** com KPIs: custo, cliques, conversões, CPA reportado e CPA limpo, sem a contaminação encontrada.
- **Tabela de campanhas**.
- **Diagnóstico** com severidade: Crítico, Atenção ou Observação. Cada achado diz o que está errado, a evidência (IDs, rótulos, datas) e o impacto.
- **O que será aplicado agora**: passos numerados, correções pontuais e reversíveis.
- **Recomendado, aguardando decisão**: o que envolve outra conta, outra equipe, mudança no site, orçamento ou estratégia.
- **Como validar**: modo Visualizar do GTM e o que conferir no Ads em 24 a 48 horas.

Depois de aplicar, acrescente uma tabela **Status da execução** (Publicado / Parcial / Pendente, manual) e republique no mesmo arquivo.

## 5. Regras para aplicar mudanças

### Plano fechado antes, execução de uma vez (regra do operador)

- **Toda alteração passa por um plano fechado antes**, para qualquer conta ou cliente: negativas, palavras-chave, anúncios, tags, metas, lances, ajustes de dispositivo, orçamentos e configurações.
- **Termine toda a análise e as verificações antes de propor.** Por exemplo: ler a landing para saber o que o cliente vende, abrir o simulador de orçamento do Google e conferir a tag. Decisões no meio da execução são o que esta regra quer evitar. Num caso real, só durante a execução se descobriu o que o cliente de fato vendia e que o CPL marginal de uma campanha era quase o dobro do médio, e o plano mudou pela metade.
- **O plano lista cada item com valor exato**: campanha, ID, valor atual → novo valor, e os termos exatos. Inclua a evidência de cada item e o que fica de fora.
- **Depois do OK, execute tudo numa única passada, sem voltar para perguntar.** Isso economiza tokens e contexto. No fim, entregue só a tabela **Status da execução**.
- **Se algo novo aparecer durante a execução**, siga com o restante do plano aprovado. O item novo vai para o relatório final como recomendação para o próximo plano; não decida isso no meio.
- Um OK não vale para itens fora do plano aprovado.
- **Lances e orçamentos estão liberados pelo usuário** (ajuste de dispositivo, orçamento, estratégia e CPA desejado), desde que estejam no plano aprovado.
- **Se a política de permissões do agente bloquear uma ação mesmo assim**, não repita a ação, porque a repetição é tratada como tentativa de contorno. Cancele sem salvar, termine o resto e informe no relatório o caminho de cliques para o usuário aplicar.
- **Correção pontual**: crie acionadores novos (ex.: `form_submit - BR - hostname`) em vez de editar um acionador compartilhado por tags de outras contas. Não apague tags; pause ou troque o acionador.
- **GTM**: salve tudo no workspace, confira a lista de "Alterações pendentes" (só as suas devem estar lá; se houver alterações de outra pessoa, pare e pergunte) e publique **uma** versão com nome no estilo Conventional Commits e descrição listando cada mudança.
- Confira os valores digitados por JS (`[...document.querySelectorAll('input')].map(i=>i.value)`). O GTM recolhe painéis ao carregar e o texto pode cair no campo errado.
- **Não toque** em tags ou contas fora do escopo combinado, nem em edições recentes de outra pessoa ("há X minutos"). Reporte em vez de corrigir.
- **Algumas ações podem ser bloqueadas pela política de permissões do agente**, por exemplo criar variável de "Dados fornecidos pelo usuário" (coleta de PII). Quando isso acontecer, não tente contornar: cancele o painel sem salvar, siga com o resto e deixe no relatório o caminho exato de cliques para o usuário fazer.
- **Lance de celular no Google Ads**: abra Campanha › Insights e relatórios › Quando e onde os anúncios foram veiculados › Dispositivos. Passe o mouse na célula "Ajuste de lance" da linha Smartphones e clique no lápis. Escolha "Diminuir", digite a %, e salve. O aviso de saldo no topo desloca a tela, então tire um screenshot antes de clicar por coordenada. Esse ajuste só vale em Maximizar cliques e CPC manual; em Maximizar conversões ou CPA desejado, só -100% tem efeito.
- **Orçamento**: abra Campanha › Configurações › Orçamento (seção expansível), mude o valor e salve. Já aconteceu de o classificador de permissões bloquear na 1ª tentativa e liberar quando o usuário autorizou no chat aquela mudança específica (campanha e valor). Por isso o plano aprovado deve citar valor e campanha explicitamente. O clique em "Orçamento" pelo `ref` do find abre um diálogo oculto; clique na linha visível da seção, por coordenada depois de um screenshot, e confira depois de recarregar a página. Antes de propor aumento, leia os exemplos do simulador que aparecem ali (conversões extras por semana e custo extra) e calcule o CPL marginal.
- **Aplicação automática de recomendações** (Recomendações › Configurações de aplicação automática): ao desmarcar uma regra, a mudança só é gravada pelo diálogo "Salvar mudanças…?", que aparece ao trocar de aba. Recarregue a página para conferir.
- Não envie formulários de teste nos sites sem pedir; isso gera lead falso no CRM do cliente.
- Ao terminar, feche as abas que você abriu.

## 6. Depois de cada conta

Atualize `references/contas.md` com o `authuser`, os IDs (MCC, contas, AW, GTM, pixels), a landing atual e as pendências. A próxima sessão começa daí, sem varrer tudo de novo.
