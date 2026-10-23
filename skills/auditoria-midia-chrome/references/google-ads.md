# Google Ads: navegação e auditoria

## URLs
Ao entrar numa conta, a URL traz `ocid`, `euid`, `__u`, `uscid`, `__c` e `authuser`. Reaproveite esses parâmetros para ir direto às páginas (troque só o caminho):

| Página | Caminho |
|---|---|
| Seletor de contas | `/nav/selectaccount?authuser=N` |
| Contas do MCC (performance) | `/aw/accounts?...` |
| Campanhas | `/aw/campaigns?...` |
| Configurações de uma campanha | `/aw/settings/campaign/search?campaignId=ID&...` |
| Resumo de metas | `/aw/conversions?...` |
| Todas as ações de conversão | `/aw/conversions/all?...` |
| Detalhe de uma ação | `/aw/conversions/detail?ctId=ID&...` |
| Páginas de destino | `/aw/landingpages?...` |
| Termos de pesquisa | `/aw/keywords/searchterms?...` |

O `campaignId` sai de `location.href.match(/campaignId=\d+/)` depois de abrir a campanha pela busca do topo ("Pesquisar").

## Leitura
- `get_page_text` costuma devolver só o banner de segurança. Use JS: `document.body.innerText`.
- Linhas da tabela: `[...document.querySelectorAll('[role="row"], tr')].map(r=>r.innerText.replace(/\n+/g,' ; '))`.
- Ordem das colunas: leia os cabeçalhos com `[role="columnheader"]` antes de interpretar números.
- Moeda: o MCC pode converter para a moeda dele. Confira a moeda da subconta.
- Fuso da conta aparece no rodapé ("Fuso horário de todas as datas").

## O que conferir em cada ação de conversão
- **Status**: "Conversões pendentes" = nunca recebeu ou parou; "Configuração incorreta" = nunca recebeu dados; "Requer atenção" = recebe com problema (ex.: conversões otimizadas sem dados do usuário).
- **Última conversão registrada** (no detalhe). Uma ação principal parada há meses distorce relatórios e metas.
- **Rótulo e ID**: no detalhe, "Fontes de dados › Gerenciar › Usar o Google Tag Manager" mostra o rótulo e o ID para comparar com o GTM.
- **Categoria e metas**: ações da mesma categoria (ex.: "Enviar formulários de lead") somam juntas na meta padrão da conta. Para separar país ou produto, crie uma **meta personalizada** e aplique por campanha.

## Diagnósticos que já apareceram
- Conversão de um país contada na ação de outro, porque o acionador do GTM não filtra hostname. Detecte segmentando campanhas por ação de conversão e cruzando com páginas de destino.
- Tag com ID de uma conta e rótulo de outra: a conversão nunca registra. Use `scripts/decode_label.py`.
- Campanha em **Maximizar cliques** com meta de conversão: a meta só afeta o relatório, não o lance. Diga isso antes de recomendar trocar a meta.
- Termo de marca em campanha não-marca com CPC alto: recomende negativar a marca nas não-marca.
- Campanha de marca com CTR baixo e CPC alto: investigue o leilão e a estratégia.

## Mudanças (só com aprovação)
- Meta personalizada: Metas › Resumo › Metas personalizadas › Adicionar meta personalizada.
- Meta por campanha: Campanha › Configurações › Metas de conversão › "Específicas da campanha". Pode ser bloqueado pela política do agente; nesse caso, passe o caminho ao usuário.
- Antes de remover um filtro da tabela, lembre que ele é estado de visualização do usuário; avise.
